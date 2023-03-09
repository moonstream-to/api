import csv
from collections import OrderedDict
import hashlib
import json
import logging
import re
from io import StringIO
from typing import Any, Dict


from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import TextClause

from ..actions import push_data_to_bucket
from ..reporter import reporter


from ..db import RO_pre_ping_query_engine
from ..reporter import reporter
from ..settings import MOONSTREAM_S3_QUERIES_BUCKET_PREFIX

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUERY_REGEX = re.compile("[\[\]@#$%^&?;`/]")


class QueryNotValid(Exception):
    """
    Raised when query validation not passed.
    """


def query_validation(query: str) -> str:
    """
    Sanitize provided query.
    """
    if QUERY_REGEX.search(query) != None:
        raise QueryNotValid("Query contains restricted symbols")

    return query


def to_json_types(value):
    if isinstance(value, (str, int, tuple, dict, list)):
        return value
    elif isinstance(value, set):
        return list(value)
    else:
        return str(value)


def from_json_types(value):
    if isinstance(value, (str, int, tuple, dict)):
        return value
    elif isinstance(value, list):  # psycopg2 issue with list support
        return tuple(value)
    else:
        return str(value)


def data_generate(
    query_id: str,
    file_type: str,
    bucket: str,
    key: str,
    query: TextClause,
    params: Dict[str, Any],
    params_hash: str,
):
    """
    Generate query and push it to S3
    """

    process_session = sessionmaker(bind=RO_pre_ping_query_engine)
    db_session = process_session()

    metadata = {
        "source": "drone-query-generation",
        "query_id": query_id,
        "file_type": file_type,
        "params_hash": params_hash,
        "params": json.dumps(params),
    }

    try:
        # TODO:(Andrey) Need optimization that information is usefull but incomplete
        block_number, block_timestamp = db_session.execute(
            text(
                "SELECT block_number, block_timestamp FROM polygon_labels WHERE block_number=(SELECT max(block_number) FROM polygon_labels where label='moonworm-alpha') limit 1;"
            ),
        ).one()

        if file_type == "csv":
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=";")

            # engine.execution_options(stream_results=True)
            query_instance = db_session.execute(query, params)  # type: ignore

            csv_writer.writerow(query_instance.keys())
            csv_writer.writerows(query_instance.fetchall())

            metadata["block_number"] = block_number
            metadata["block_timestamp"] = block_timestamp

            data = csv_buffer.getvalue().encode("utf-8")

        else:
            block_number, block_timestamp = db_session.execute(
                text(
                    "SELECT block_number, block_timestamp FROM polygon_labels WHERE block_number=(SELECT max(block_number) FROM polygon_labels where label='moonworm-alpha') limit 1;"
                ),
            ).one()

            data = json.dumps(
                {
                    "block_number": block_number,
                    "block_timestamp": block_timestamp,
                    "data": [
                        {
                            key: to_json_types(value)
                            for key, value in row._asdict().items()
                        }
                        for row in db_session.execute(query, params).all()
                    ],
                }
            ).encode("utf-8")
        push_data_to_bucket(
            data=data,
            key=key,
            bucket=bucket,
            metadata=metadata,
        )
    except Exception as err:
        logger.error(f"Error while generating data: {err}")
        db_session.rollback()
        reporter.error_report(
            err,
            [
                "queries",
                "execution",
                f"query_id:{query_id}" f"file_type:{file_type}",
            ],
        )
    finally:
        db_session.close()
