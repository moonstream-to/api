from typing import Optional, Dict, Any, Union, List
from datetime import datetime
import logging
import time
import uuid
import requests  # type: ignore

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


def collect_billing_information(
    month: str,
    token: Optional[str] = None,
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

    if token is None and user_id is None:
        raise Exception("Either token or user_id must be provided")

    # Get user_id

    if user_id is None and token is not None:
        bugout_user = bc.get_user(
            token=token,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

        user_id = str(bugout_user.id)

        token = token

    elif user_id is not None and token is None:
        # Get user's subscriptions resources

        token = MOONSTREAM_ADMIN_ACCESS_TOKEN

    subscription_resources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
        params={
            "user_id": user_id,
            "type": "entity_subscription",
        },
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    if len(subscription_resources.resources) == 0:
        subscription_amount = 0
    else:
        collection_id = subscription_resources.resources[0].resource_data[
            "collection_id"
        ]

        ### search in subscriptions collection

        subscription_collection = bc.search(
            token=token,  # type: ignore
            journal_id=collection_id,
            content=False,
            query="",
            limit=1000,
        )

        subscription_amount = subscription_collection.total_results

    ### Get user's queries resources

    query_resources = bc.list_resources(
        token=token,  # type: ignore
        params={"user_id": user_id, "type": BUGOUT_RESOURCE_QUERY_RESOLVER},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    query_amount = len(query_resources.resources)

    ### Get user's leaderboards resources

    leaderboards = requests.get(
        "https://engineapi.moonstream.to/leaderboard/leaderboards",
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    # Get user leaderboards

    ### contracts events

    contract_data = {}

    if contracts is not None:
        client = Moonstream()

        ### run query

        for blockchain, addresses in contracts.items():
            contracts_events = recive_S3_data_from_query(
                client=client,
                token=token,  # type: ignore
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

    return {
        "subscriptions": subscription_amount,
        "queries": query_amount,
        "leaderboards": leaderboards,
        "leaderboards_amount": len(leaderboards),
        "contracts": contract_data,
    }
