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


def generate_s3_access_links(
    method_name: str,
    bucket: str,
    key: str,
    http_method: str,
    expiration: int = 300,  # 12 hours
) -> str:
    s3 = boto3.client("s3")
    stats_presigned_url = s3.generate_presigned_url(
        method_name,
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expiration,
        HttpMethod=http_method,
    )

    return stats_presigned_url