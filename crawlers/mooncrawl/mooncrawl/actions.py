import hashlib
import json
import logging
import time
import uuid
from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict, Optional, Union, List

import boto3  # type: ignore
import requests  # type: ignore
from bugout.data import BugoutResources, BugoutSearchResult
from bugout.exceptions import BugoutResponseException
from moonstream.client import (  # type: ignore
    ENDPOINT_QUERIES,
    Moonstream,
    MoonstreamQueryResultUrl,
)
from sqlalchemy import text, TextClause
from moonstreamtypes.blockchain import (
    AvailableBlockchainType,
    get_block_model,
    get_label_model,
    get_transaction_model,
)

from .data import QueryDataUpdate
from .middleware import MoonstreamHTTPException
from .settings import (
    bugout_client as bc,
    MOONSTREAM_DB_V3_CONTROLLER_API,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EntityCollectionNotFoundException(Exception):
    """
    Raised when entity collection is not found
    """


class QueryTextClauseException(Exception):
    """
    Raised when query can't be transformed to TextClause
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
    customer_params: Optional[Dict[str, Any]] = {},
) -> Any:
    """
    Await the query to be update data on S3 with if_modified_since and return new the data.
    """

    keep_going = True

    repeat = 0

    if_modified_since_datetime = datetime.utcnow()
    if_modified_since = if_modified_since_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")

    time.sleep(2)
    if custom_body or customer_params:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        json = custom_body

        response = requests.post(
            url=f"{client.api.endpoints[ENDPOINT_QUERIES]}/{query_name}/update_data",
            headers=headers,
            params=customer_params,
            json=json,
            timeout=5,
        )
        print(response.json())
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


def get_all_entries_from_search(
    journal_id: str, search_query: str, limit: int, token: str, content: bool = False
) -> List[BugoutSearchResult]:
    """
    Get all required entries from journal using search interface
    """
    offset = 0
    results: List[BugoutSearchResult] = []
    existing_methods = bc.search(
        token=token,
        journal_id=journal_id,
        query=search_query,
        content=content,
        timeout=10.0,
        limit=limit,
        offset=offset,
    )
    results.extend(existing_methods.results)  # type: ignore
    if len(results) != existing_methods.total_results:
        for offset in range(limit, existing_methods.total_results, limit):
            existing_methods = bc.search(
                token=token,
                journal_id=journal_id,
                query=search_query,
                content=content,
                timeout=10.0,
                limit=limit,
                offset=offset,
            )
            results.extend(existing_methods.results)  # type: ignore

    return results


def get_customer_db_uri(
    customer_id: str,
    instance_id: str,
    user: str,
) -> str:

    try:
        response = requests.get(
            f"{MOONSTREAM_DB_V3_CONTROLLER_API}/customers/{customer_id}/instances/{instance_id}/creds/{user}/url",
            headers={"Authorization": f"Bearer {MOONSTREAM_ADMIN_ACCESS_TOKEN}"},
        )
        response.raise_for_status()
        return response.text.replace('"', "")
    except Exception as e:
        logger.error(f"Error get customer db uri: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)


def resolve_table_names(request_data: QueryDataUpdate) -> Dict[str, str]:
    """
    Determines the table names based on the blockchain and labels version.
    Returns an empty dictionary if blockchain is not provided.
    """
    if not request_data.blockchain:
        return {"labels_table": "ethereum_labels"}

    if request_data.blockchain not in [i.value for i in AvailableBlockchainType]:
        logger.error(f"Unknown blockchain {request_data.blockchain}")
        raise MoonstreamHTTPException(status_code=403, detail="Unknown blockchain")

    blockchain = AvailableBlockchainType(request_data.blockchain)
    labels_version = 2

    if request_data.customer_id is not None and request_data.instance_id is not None:
        labels_version = 3

    print(labels_version, blockchain)

    tables = {
        "labels_table": get_label_model(blockchain, labels_version).__tablename__,
    }

    if labels_version != 3:
        tables.update(
            {
                "transactions_table": get_transaction_model(blockchain).__tablename__,
                "blocks_table": get_block_model(blockchain).__tablename__,
            }
        )

    return tables


def prepare_query(
    requested_query: str, tables: Dict[str, str], query_id: str
) -> TextClause:
    """
    Prepares the SQL query by replacing placeholders with actual table names.
    """
    # Check and replace placeholders only if they exist in the query
    if "__labels_table__" in requested_query:
        requested_query = requested_query.replace(
            "__labels_table__", tables.get("labels_table", "ethereum_labels")
        )

    if "__transactions_table__" in requested_query and "transactions_table" in tables:
        requested_query = requested_query.replace(
            "__transactions_table__", tables["transactions_table"]
        )

    if "__blocks_table__" in requested_query and "blocks_table" in tables:
        requested_query = requested_query.replace(
            "__blocks_table__", tables["blocks_table"]
        )

        # Check if it can transform to TextClause
    try:
        query = text(requested_query)
    except Exception as e:
        logger.error(
            f"Can't parse query {query_id} to TextClause in drones /query_update endpoint, error: {e}"
        )
        raise QueryTextClauseException(
            f"Can't parse query {query_id} to TextClause in drones /query_update endpoint, error: {e}"
        )

    return query
