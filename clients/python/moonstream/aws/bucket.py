from typing import Any, Dict

import boto3


def upload_to_aws_s3_bucket(
    data: str,
    bucket: str,
    key: str,
    metadata: Dict[str, Any] = {},
) -> str:
    """
    Push data to AWS S3 bucket and return URL to object.
    """
    s3 = boto3.client("s3")
    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=key,
        ContentType="application/json",
        Metadata=metadata,
    )

    return f"{bucket}/{key}"
