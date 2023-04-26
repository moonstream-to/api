from collections import OrderedDict
import hashlib
import json
import logging
from typing import Any, Dict, Optional, Union
import uuid

from bugout.data import (
    BugoutResources,
)
from bugout.exceptions import BugoutResponseException
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
) -> Optional[str]:
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
