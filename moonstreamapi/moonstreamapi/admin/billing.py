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
)
from ..data import BUGOUT_RESOURCE_QUERY_RESOLVER

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

    {
    "resources": [
        {
        "id": "ff90a1eb-6552-4bba-9d2b-f54cf2ab0103",
        "application_id": "e1b6321a-5e68-4f9d-ba0c-d87e37d9e7a9",
        "resource_data": {
            "type": "leaderboard",
            "leaderboard_id": "0b112383-c7d2-4734-818b-1600d5f096f8"
        },
        "created_at": "2023-08-09T11:49:06.992161+00:00",
        "updated_at": "2023-08-09T11:49:06.992161+00:00"
        }
    """

    leaderboard_owners = []

    for leaderboard in leaderboards:
        leaderboard_id = leaderboard["resource_data"]["leaderboard_id"]
        resource_id = leaderboard["resource_id"]

        holders = bc.get_resource_holders(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            resource_id=resource_id,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

        owner = [
            holder["id"]
            for holder in holders.holders
            if holder["holder_type"] == "user" and "admin" in holder["permissions"]
        ][0]

        leaderboard_owners.append(
            {
                "leaderboard_id": leaderboard_id,
                "owner": owner,
                "resource_id": resource_id,
                "created_at": leaderboard["created_at"],
                "updated_at": leaderboard["updated_at"],
            }
        )

    return leaderboard_owners


def collect_billing_information(
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

    # Get user_id

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

    ### Get user's leaderboards resources
    leaderboard_resources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
        params={"user_id": user_id, "type": "leaderboard"},
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
        journal_id="a75b4538-3323-4f1c-a57a-6fd858f0c424",
        search_query="",
        content=True,
        limit=1000,
    )

    """
    class BugoutSearchResult(BaseModel):
        entry_url: str
        content_url: str
        title: str
        content: Optional[str]
        tags: List[str]
        created_at: str
        updated_at: str
        score: float
        context_type: Optional[str] = None
        context_url: Optional[str] = None
        context_id: Optional[str] = None

        {
    "leaderboard_id":"258a9042-c8c5-48d2-bf33-3e516afc6c03",
    "query_name":"leaderboard_258a9042_c8c5_48d2_bf33_3e516afc6c03",
    "params":{
        "shards_common": 0,
        "shards_uncommon": 2,
        "shards_rare": 3,
        "shards_epic": 5,
        "shards_legendary": 10,
        "equipments_common": 0,
        "equipments_uncommon": 70,
        "equipments_rare": 100,
        "equipments_epic": 180,
        "equipments_legendary": 350,
        "artifacts_common": 0,
        "artifacts_uncommon": 30,
        "artifacts_rare": 40,
        "artifacts_epic": 80,
        "artifacts_legendary": 160,
        "common_upgrade_points": 0,
        "uncommon_upgrade_points": 65,
        "rare_upgrade_points": 95,
        "epic_upgrade_points": 155,
        "legendary_upgrade_points": 300,
        "gold_chest_points": 1,
        "magical_chest_points": 10,
        "legendary_chest_points": 35,
        "ultra_chest_points": 120,
        "wooden_chest_points": 0,
        "silver_chest_points": 0,
        "since_timestamp": 1698796800,
        "until_timestamp": 1701388800
    },
    "normalize_addresses": true
}


    """

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
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
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

    """
            {
            "id": "258a9042-c8c5-48d2-bf33-3e516afc6c03",
            "title": "Boomland: Hunter League - Season 3",
            "description": "U2NvcmluZzoKKiBVcGdyYWRlLCBkZXBlbmRpbmcgb24gcmFyaXR5ICh1bmNvbW1vbiB1cGdyYWRlcyB3b3J0aCA2NSBwb2ludHMsIHJhcmUgOTUsIGVwaWMgMTU1LCBsZWdlbmRhcnkgMzAwKQoqIE9wZW5pbmcgY2hlc3QKICAgICogR29sZCA9IDFwCiAgICAqIE1hZ2ljYWwgPSAxMHAKICAgICogTGVnZW5kYXJ5IFJveWFsID0gMzVwCiAgICAqIFVsdHJhIFN1cHJlbWUgPSAxMjBwCiogR2V0dGluZyBhIHNoYXJkLCAyIHBvaW50IGZvciB1bmNvbW1vbiwgMyBwb2ludCBmb3IgcmFyZSwgNSBwb2ludCBmb3IgZXBpYywgMTAgcG9pbnQgZm9yIGxlZ2VuZGFyeS4KKiBHZXR0aW5nIGVxdWlwbWVudCwgNzAgcG9pbnQgZm9yIHVuY29tbW9uLCAxMDAgcG9pbnQgZm9yIHJhcmUsIDE4MCBwb2ludCBmb3IgZXBpYywgMzUwIHBvaW50IGZvciBsZWdlbmRhcnkuCiogR2V0dGluZyBhbiBhcnRpZmFjdCwgMzAgcG9pbnQgZm9yIHVuY29tbW9uLCA0MCBwb2ludCBmb3IgcmFyZSwgODAgcG9pbnQgZm9yIGVwaWMsIDE2MCBwb2ludCBmb3IgbGVnZW5kYXJ5Lg==",
            "resource_id": "380316e7-475d-4778-bab3-55cc37d5bd31",
            "created_at": "2023-11-01T13:50:39.211766+00:00",
            "updated_at": "2023-11-01T14:25:27.953960+00:00"
        }
    """
    for leaderboard in leaderboards:
        if leaderboard["id"] in leaderboard_configs_mapper:
            leaderboard["query_name"] = leaderboard_configs_mapper[leaderboard["id"]][
                "query_name"
            ]
            leaderboard["update_activated"] = leaderboard_configs_mapper[
                leaderboard["id"]
            ]["update_activated"]

        # get leaderboard info

        leaderboard_info = requests.get(
            f"https://engineapi.moonstream.to/leaderboard/info?leaderboard_id={leaderboard['id']}",
        ).json()

        leaderboard["users_count"] = leaderboard_info["users_count"]
        leaderboard["last_updated_at"] = leaderboard_info["last_updated_at"]

    return {
        "subscriptions": subscription_amount,
        "queries": query_amount,
        "leaderboards": leaderboards,
        "leaderboards_amount": len(leaderboards),
        "contracts": contract_data,
    }
