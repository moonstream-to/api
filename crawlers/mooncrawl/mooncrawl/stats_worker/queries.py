import csv
from collections import OrderedDict
import hashlib
import json
import logging
import re
from io import StringIO
from typing import Any, Dict

from moonstreamdb.db import (
    create_moonstream_engine,
    MOONSTREAM_DB_URI_READ_ONLY,
    MOONSTREAM_POOL_SIZE,
)
from sqlalchemy.orm import sessionmaker

from ..actions import push_data_to_bucket
from ..reporter import reporter

from ..settings import (
    MOONSTREAM_S3_QUERIES_BUCKET_PREFIX,
    MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS,
)

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

    if isinstance(value, (str, int, tuple, dict)):
        return value
    if isinstance(value, list):  # psycopg2 issue with list support
        return tuple(value)
    elif isinstance(value, set):
        return tuple(value)
    else:
        return str(value)


def to_csv_types(value):
    return str(value)


def data_generate(
    query_id: str,
    file_type: str,
    bucket: str,
    key: str,
    query: str,
    params: Dict[str, Any],
    params_hash: str,
):
    """
    Generate query and push it to S3
    """

    # Create session
    engine = create_moonstream_engine(
        MOONSTREAM_DB_URI_READ_ONLY,
        pool_pre_ping=True,
        pool_size=MOONSTREAM_POOL_SIZE,
        statement_timeout=MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS,
    )
    process_session = sessionmaker(bind=engine)
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
            "SELECT block_number, block_timestamp FROM polygon_labels WHERE block_number=(SELECT max(block_number) FROM polygon_labels where label='moonworm-alpha') limit 1;",
        ).one()

        if file_type == "csv":
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=";")

            result = db_session.execute(query, params).keys()

            csv_writer.writerow(result.keys())
            csv_writer.writerows(result.fetchAll())

            metadata["block_number"] = block_number
            metadata["block_timestamp"] = block_timestamp

            data = csv_buffer.getvalue().encode("utf-8")

        else:

            data = json.dumps(
                {
                    "block_number": block_number,
                    "block_timestamp": block_timestamp,
                    "data": [
                        {key: to_json_types(value) for key, value in dict(row).items()}
                        for row in db_session.execute(query, params)
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
