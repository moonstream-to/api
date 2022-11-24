import logging
from typing import Any, Dict

import boto3  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def push_data_to_bucket(
    data: Any, key: str, bucket: str, metadata: Dict[str, Any] = {}
) -> None:
    s3 = boto3.client("s3")
    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=key,
        ContentType="application/json",
        Metadata=metadata,
    )

    logger.info(f"Data pushed to bucket: s3://{bucket}/{key}")
