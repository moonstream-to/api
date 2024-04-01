from typing import Optional, Dict, Any, Union, List
from datetime import datetime
import json
import logging
import time
import uuid
import requests  # type: ignore

from ..actions import get_all_entries_from_search
from ..settings import bugout_client as bc
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_PUBLIC_QUERIES_TOKEN,
    MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID,
)
from ..data import BUGOUT_RESOURCE_QUERY_RESOLVER


from bugout.data import BugoutResourceHolders, ResourcePermissions, HolderType
from web3 import Web3
from moonstream.client import (
    Moonstream,
    ENDPOINT_QUERIES,
    MoonstreamQueryResultUrl,
)


logger = logging.getLogger(__name__)


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


def generate_leaderboard_owners(
    leaderboards: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Get list of all leaderboard and add owners to it.
    """

    leaderboard_owners = []

    for leaderboard in leaderboards:
        # breakpoint()
        leaderboard_id = leaderboard.resource_data["leaderboard_id"]
        resource_id = leaderboard.id

        holders: BugoutResourceHolders = bc.get_resource_holders(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            resource_id=resource_id,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

        print(holders.holders)
        try:
            owner = [
                holder.id
                for holder in holders.holders
                if holder.holder_type == HolderType.user
                and ResourcePermissions.ADMIN in holder.permissions
            ][0]
        except Exception as e:
            logger.error(e)
            breakpoint()
            continue

        leaderboard_owners.append(
            {
                "leaderboard_id": leaderboard_id,
                "owner": str(owner),
                "resource_id": str(resource_id),
                "created_at": str(leaderboard.created_at),
                "updated_at": str(leaderboard.updated_at),
            }
        )

    return leaderboard_owners


def collect_usage_information(
    month: str,
    user_id: Optional[str] = None,
    contracts: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, Any]:
    """
    Collect billing information for a user.

    By user_id or token.

    Collected info:

    Resources:
        - queries
        - subscriptions
        - leaderboards

    Contracts:
        - moonstream contracts
    """

    subscription_resources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
        params={
            "user_id": user_id,
            "type": "entity_subscription",
        },
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    print(subscription_resources.resources)

    if len(subscription_resources.resources) == 0:
        subscription_amount = 0
    else:
        collection_id = subscription_resources.resources[0].resource_data[
            "collection_id"
        ]

        ### search in subscriptions collection

        subscription_collection = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
            journal_id=collection_id,
            content=False,
            query="",
            limit=1000,
        )

        subscription_amount = subscription_collection.total_results

    ### Get user's queries resources

    query_resources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
        params={"user_id": user_id, "type": BUGOUT_RESOURCE_QUERY_RESOLVER},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    query_amount = len(query_resources.resources)

    # MOONSTREAM_ADMIN_ACCESS_TOKEN = "ad7a7364-c535-4c9f-9d2d-20d7b6ade18d"

    ### Get user's leaderboards resources
    leaderboard_resources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
        params={"type": "leaderboard"},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    leaderboards = generate_leaderboard_owners(
        leaderboards=leaderboard_resources.resources
    )

    # Get user leaderboards

    ### contracts events

    contract_data = {}

    leaderboard_configs = get_all_entries_from_search(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID,
        search_query="",
        content=True,
        limit=1000,
    )

    leaderboard_configs_mapper = {}

    for leaderboard_entry in leaderboard_configs:
        tags = leaderboard_entry.tags
        try:
            content = json.loads(leaderboard_entry.content)
        except Exception as e:
            logger.error(e)
            continue

        leaderboard_configs_mapper[content["leaderboard_id"]] = {
            "query_name": content["query_name"],
            "update_activated": True if "status:active" in tags else False,
        }

    if contracts is not None:
        client = Moonstream()

        ### run query

        for blockchain, addresses in contracts.items():
            contracts_events = recive_S3_data_from_query(
                client=client,
                token=MOONSTREAM_PUBLIC_QUERIES_TOKEN,  # type: ignore
                query_name="template_contract_events_per_month",
                params={},
                time_await=2,
                max_retries=30,
                custom_body={
                    "blockchain": blockchain,
                    "params": {
                        "block_month": month,
                        "addresses": [
                            Web3.toChecksumAddress(addresses) for addresses in addresses
                        ],
                    },
                },
            )["data"]

            contract_data[blockchain] = contracts_events

    for leaderboard in leaderboards:
        if leaderboard["leaderboard_id"] in leaderboard_configs_mapper:
            leaderboard["query_name"] = leaderboard_configs_mapper[
                leaderboard["leaderboard_id"]
            ]["query_name"]
            leaderboard["update_activated"] = leaderboard_configs_mapper[
                leaderboard["leaderboard_id"]
            ]["update_activated"]

        # get leaderboard info

        leaderboard_info = requests.get(
            f"https://engineapi.moonstream.to/leaderboard/info?leaderboard_id={leaderboard['leaderboard_id']}",
        ).json()
        try:
            leaderboard["users_count"] = leaderboard_info["users_count"]
            leaderboard["last_updated_at"] = leaderboard_info["last_updated_at"]
        except Exception as e:
            logger.error(e)
            leaderboard["users_count"] = 0
            leaderboard["last_updated_at"] = None
            continue

    return {
        "subscriptions": subscription_amount,
        "queries": query_amount,
        "leaderboards": leaderboards,
        "leaderboards_amount": len(leaderboards),
        "contracts": contract_data,
    }
