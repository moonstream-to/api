import json
import logging
from typing import List, Dict, Union, Any
from uuid import UUID

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources, BugoutSearchResult
from bugout.exceptions import BugoutResponseException
from moonstreamdbv3.db import MoonstreamDBEngine
from moonstreamdbv3.models_indexes import AbiJobs
from web3 import Web3


from ..actions import apply_moonworm_tasks, get_all_entries_from_search
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
)
from ..settings import bugout_client as bc
from .subscription_types import CANONICAL_SUBSCRIPTION_TYPES

logger = logging.getLogger(__name__)


def get_list_of_addresses():
    """
    Return list of addresses of tasks
    """

    entries = get_all_entries_from_search(
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        search_query=f"?tag:type:event ?tag:type:function",
        limit=100,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
    )

    addresses = set()

    for entry in entries:
        addresses.add(entry.title)

    print(addresses)


def add_subscription(id: str):
    """
    Return list of tags depends on query and tag
    """

    try:
        subscription_resource: BugoutResource = bc.get_resource(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            resource_id=id,
        )

    except BugoutResponseException as e:
        logging.error(f"Bugout error: {str(e)}")
    except Exception as e:
        logger.error(f"Error get resource: {str(e)}")

    s3_client = boto3.client("s3")

    if subscription_resource.resource_data["abi"] is not None:
        bucket = subscription_resource.resource_data["bucket"]
        key = subscription_resource.resource_data["s3_path"]

        if bucket is None or key is None:
            logger.error(f"Error subscription not have s3 path to abi")

        s3_path = f"s3://{bucket}/{key}"

        try:
            response = s3_client.get_object(
                Bucket=bucket,
                Key=key,
            )

        except s3_client.exceptions.NoSuchKey as e:
            logger.error(
                f"Error getting Abi for subscription {str(id)} S3 {s3_path} does not exist : {str(e)}"
            )

        abi = json.loads(response["Body"].read())

        apply_moonworm_tasks(
            subscription_type=subscription_resource.resource_data[
                "subscription_type_id"
            ],
            abi=abi,
            address=subscription_resource.resource_data["address"],
        )
    else:
        logging.info("For apply to moonworm tasks subscriptions must have an abi.")


def migrate_v3_tasks(user_id: UUID, customer_id: UUID) -> None:
    """
    Migrate moonworm tasks

    """

    ### get user subscription entity journal id

    subscription_resources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,  # type: ignore
        params={
            "user_id": user_id,
            "type": "entity_subscription",
        },
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    logger.info(
        "Found users collection resources: %s", len(subscription_resources.resources)
    )

    if len(subscription_resources.resources) == 0:
        raise Exception("User has no subscriptions")

    collection_id = subscription_resources.resources[0].resource_data["collection_id"]

    subscriptions: List[BugoutSearchResult] = get_all_entries_from_search(
        journal_id=collection_id,
        search_query=f"tag:type:subscription",
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
    )

    logger.info("Found users subscriptions: %s", len(subscriptions))

    if len(subscriptions) == 0:
        raise Exception("User has no subscriptions")

    for subscription in subscriptions:

        abi = None
        address = None
        subscription_type_id = None

        if subscription.content is None:
            continue

        subscription_data = json.loads(subscription.content)

        if "abi" in subscription_data:
            abi = subscription_data["abi"]

        for tag in subscription.tags:
            if tag.startswith("subscription_type_id:"):
                subscription_type_id = tag.split(":")[1]
            if tag.startswith("address:"):
                address = tag.split(":")[1]

        if subscription_type_id is None:
            continue

        ### reformat abi to separate abi tasks

        if abi is None:
            continue

        chain = CANONICAL_SUBSCRIPTION_TYPES[subscription_type_id]["blockchain"]

        with MoonstreamDBEngine.yield_db_session_ctx() as session:
            for abi_task in abi:

                if abi_task["type"] not in ("event", "function"):
                    continue

                abi_selector = Web3.keccak(
                    text=abi_task["name"]
                    + "("
                    + ",".join(map(lambda x: x["type"], abi_task["inputs"]))
                    + ")"
                )[:4].hex()

                try:

                    subscription = AbiJobs(
                        address=address,
                        user_id=user_id,
                        customer_id=customer_id,
                        abi_selector=abi_selector,
                        chain=chain,
                        abi_name=abi_task["name"],
                        status="active",
                        historical_crawl_status="pending",
                        progress=0,
                        moonworm_task_pickedup=False,
                        abi=abi_task,
                    )

                    session.add(subscription)

                except Exception as e:
                    logger.error(
                        f"Error creating subscription for subscription {subscription.id}: {str(e)}"
                    )
                    session.rollback()
                    continue

            session.commit()

    return None
