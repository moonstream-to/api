import csv
import hashlib
import json
import logging
import re
from collections import OrderedDict
from io import StringIO
from typing import Any, Dict, Optional

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import TextClause

from ..actions import push_data_to_bucket, get_customer_db_uri
from ..db import (
    RO_pre_ping_query_engine,
    MOONSTREAM_DB_URI_READ_ONLY,
    MoonstreamCustomDBEngine,
)
from ..reporter import reporter
from ..settings import (
    CRAWLER_LABEL,
    SEER_CRAWLER_LABEL,
    MOONSTREAM_DB_V3_SCHEMA_NAME,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUERY_REGEX = re.compile(r"[\[\]@#$%^&?;`]|/\*|\*/")


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
    customer_id: Optional[str] = None,
    instance_id: Optional[str] = None,
    blockchain_table: Optional[str] = None,
):
    """
    Generate query and push it to S3
    """
    label = CRAWLER_LABEL
    db_uri = MOONSTREAM_DB_URI_READ_ONLY
    if customer_id is not None and instance_id is not None:
        db_uri = get_customer_db_uri(customer_id, instance_id, "customer")
        label = SEER_CRAWLER_LABEL

        engine = MoonstreamCustomDBEngine(
            url=db_uri, schema=MOONSTREAM_DB_V3_SCHEMA_NAME
        )
    else:
        engine = RO_pre_ping_query_engine

    process_session = sessionmaker(bind=engine)
    db_session = process_session()

    metadata = {
        "source": "drone-query-generation",
        "query_id": query_id,
        "file_type": file_type,
        "params_hash": params_hash,
        "params": json.dumps(params),
    }

    block_number = None
    block_timestamp = None

    try:
        ### If blockchain is provided, we need to get the latest block number and timestamp
        if blockchain_table is not None:
            block_number, block_timestamp = db_session.execute(
                text(
                    f"SELECT block_number, block_timestamp FROM {blockchain_table} WHERE label='{label}' ORDER BY block_number DESC LIMIT 1"
                ),
            ).one()
        if file_type == "csv":
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=";")

            query_instance = db_session.execute(query, params)  # type: ignore

            csv_writer.writerow(query_instance.keys())
            csv_writer.writerows(query_instance.fetchall())

            metadata["block_number"] = block_number  # type: ignore
            metadata["block_timestamp"] = block_timestamp  # type: ignore

            data = csv_buffer.getvalue().encode("utf-8")

        else:

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
