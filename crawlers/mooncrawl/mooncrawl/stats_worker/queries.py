import json
import logging
from typing import Any, Dict, Optional
from io import StringIO
import csv


import boto3
from moonstreamdb.db import yield_db_session_ctx


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def push_statistics(s3: Any, data: Any, key: str, bucket: str) -> None:

    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=key,
        ContentType="application/json",
        Metadata={"drone_query": "data"},
    )

    logger.info(f"Statistics push to bucket: s3://{bucket}/{key}")


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

    with yield_db_session_ctx() as db_session:

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

            data = json.dumps(
                [dict(row) for row in db_session.execute(query, params)]
            ).encode("utf-8")
            push_statistics(
                s3=s3,
                data=data,
                key=f"queries/{query_id}/data.{file_type}",
                bucket=bucket,
            )
