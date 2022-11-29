import csv
import json
import logging
import re
from io import StringIO
from typing import Any, Dict, Optional

import boto3  # type: ignore
from moonstreamdb.db import (
    create_moonstream_engine,
    MOONSTREAM_DB_URI_READ_ONLY,
    MOONSTREAM_POOL_SIZE,
)
from sqlalchemy.orm import sessionmaker
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


def push_statistics(s3: Any, data: Any, key: str, bucket: str) -> None:

    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=key,
        ContentType="application/json",
        Metadata={"drone_query": "data"},
    )

    logger.info(f"Statistics push to bucket: s3://{bucket}/{key}")


def query_validation(query: str) -> str:
    """
    Sanitize provided query.
    """
    if QUERY_REGEX.search(query) != None:
        raise QueryNotValid("Query contains restricted symbols")

    return query


def to_json_types(value):

    if isinstance(value, (str, int, tuple, list, dict)):
        return value
    elif isinstance(value, set):
        return list(value)
    else:
        return str(value)

def from_json_types(value):

    if isinstance(value, (str, int, tuple, dict)):
        return value
    elif isinstance(value, list): # psycopg2 issue with list support
        return tuple(value)
    else:
        return str(value)


def data_generate(
    bucket: str,
    query_id: str,
    file_type: str,
    query: str,
    params: Optional[Dict[str, Any]],
):
    """
    Generate query and push it to S3
    """
    s3 = boto3.client("s3")

    # Create session
    engine = create_moonstream_engine(
        MOONSTREAM_DB_URI_READ_ONLY,
        pool_pre_ping=True,
        pool_size=MOONSTREAM_POOL_SIZE,
        statement_timeout=MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS,
    )
    process_session = sessionmaker(bind=engine)
    db_session = process_session()

    try:
        if file_type == "csv":
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=";")

            # engine.execution_options(stream_results=True)
            result = db_session.execute(query, params).keys()

            csv_writer.writerow(result.keys())
            csv_writer.writerows(result.fetchAll())

            push_statistics(
                s3=s3,
                data=csv_buffer.getvalue().encode("utf-8"),
                key=f"queries/{query_id}/data.{file_type}",
                bucket=bucket,
            )
        else:
            block_number, block_timestamp = db_session.execute(
                "SELECT block_number, block_timestamp FROM polygon_labels WHERE block_number=(SELECT max(block_number) FROM polygon_labels where label='moonworm-alpha') limit 1;",
            ).one()

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
            push_statistics(
                s3=s3,
                data=data,
                key=f"{MOONSTREAM_S3_QUERIES_BUCKET_PREFIX}/queries/{query_id}/data.{file_type}",
                bucket=bucket,
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
