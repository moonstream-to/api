import json
import logging
from typing import Any

import boto3  # type: ignore
from moonstreamdb.db import yield_db_session_ctx


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def push_statistics(data: Any, key: str, bucket: str) -> None:

    result_bytes = json.dumps(data).encode("utf-8")

    s3 = boto3.client("s3")
    s3.put_object(
        Body=result_bytes,
        Bucket=bucket,
        Key=key,
        ContentType="application/json",
        Metadata={"drone_query": "data"},
    )

    logger.info(f"Statistics push to bucket: s3://{bucket}/{key}")


def data_generate(bucket: str, key: str, query: str):
    """
    Generate query and push it to S3
    """
    with yield_db_session_ctx() as db_session:
        push_statistics(data=db_session.execute(query).all(), key=key, bucket=bucket)
