from collections import OrderedDict
from datetime import datetime
import hashlib
import json
import logging
import time
from typing import Any, Dict, Optional, Union
import uuid


from bugout.data import (
    BugoutResources,
)
from bugout.exceptions import BugoutResponseException
from moonstream.client import Moonstream, ENDPOINT_QUERIES, MoonstreamQueryResultUrl  # type: ignore
import requests  # type: ignore
from .middleware import MoonstreamHTTPException
from .settings import bugout_client as bc


import boto3  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EntityCollectionNotFoundException(Exception):
    """
    Raised when entity collection is not found
    """


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
    expiration: int = 300,
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


def query_parameter_hash(params: Dict[str, Any]) -> str:
    """
    Generate a hash of the query parameters
    """

    hash = hashlib.md5(
        json.dumps(OrderedDict(params), sort_keys=True).encode("utf-8")
    ).hexdigest()

    return hash


def get_entity_subscription_collection_id(
    resource_type: str,
    token: Union[uuid.UUID, str],
    user_id: uuid.UUID,
) -> str:
    """
    Get collection_id from brood resources. If collection not exist and create_if_not_exist is True
    """

    params = {
        "type": resource_type,
        "user_id": str(user_id),
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({user_id}) with token ({token}), error: {str(e)}"
        )
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if len(resources.resources) == 0:
        raise EntityCollectionNotFoundException("Subscription collection not found.")
    else:
        resource = resources.resources[0]
    return resource.resource_data["collection_id"]


def recive_S3_data_from_query(
    client: Moonstream,
    token: Union[str, uuid.UUID],
    query_name: str,
    params: Dict[str, Any] = {},
    time_await: int = 2,
    max_retries: int = 30,
    custom_body: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Await the query to be update data on S3 with if_modified_since and return new the data.
    """

    keep_going = True

    repeat = 0

    if_modified_since_datetime = datetime.utcnow()
    if_modified_since = if_modified_since_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")

    time.sleep(2)
    if custom_body:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        json = custom_body

        response = requests.post(
            url=f"{client.api.endpoints[ENDPOINT_QUERIES]}/{query_name}/update_data",
            headers=headers,
            json=json,
            timeout=5,
        )
        data_url = MoonstreamQueryResultUrl(url=response.json()["url"])
    else:
        data_url = client.exec_query(
            token=token,
            name=query_name,
            params=params,
        )  # S3 presign_url

    while keep_going:
        time.sleep(time_await)
        try:
            data_response = requests.get(
                data_url.url,
                headers={"If-Modified-Since": if_modified_since},
                timeout=5,
            )
        except Exception as e:
            logger.error(e)
            continue

        if data_response.status_code == 200:
            break

        repeat += 1

        if repeat > max_retries:
            logger.info("Too many retries")
            break
    return data_response.json()
