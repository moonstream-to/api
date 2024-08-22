import json
from hexbytes import HexBytes
import logging
import os
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources, BugoutSearchResult
from bugout.exceptions import BugoutResponseException
from moonstreamdbv3.db import MoonstreamDBIndexesEngine
from moonstreamdbv3.models_indexes import AbiJobs, AbiSubscriptions
from sqlalchemy.dialects.postgresql import insert
from web3 import Web3

from ..actions import apply_moonworm_tasks, get_all_entries_from_search
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
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


def create_v3_task(
    customer_id: str,
    user_id: str,
    abi: Dict[str, Any],
    address: str,
    blockchain: str,
):
    """
    Create moonworm task for v3
    """
    abi_tasks = []

    db_engine = MoonstreamDBIndexesEngine()

    with db_engine.yield_db_session_ctx() as db_session_v3:

        for abi_task in abi:
            if abi_task["type"] != "event" and abi_task["type"] != "function":
                continue

            abi_selector = Web3.keccak(
                text=abi_task["name"]
                + "("
                + ",".join(map(lambda x: x["type"], abi_task["inputs"]))
                + ")"
            )

            if abi_task["type"] == "function":
                abi_selector = abi_selector[:4]

            abi_selector = abi_selector.hex()

            try:

                abi_tasks.append(
                    {
                        "address": bytes.fromhex(address[2:]),
                        "user_id": user_id,
                        "customer_id": customer_id,
                        "abi_selector": abi_selector,
                        "chain": blockchain,
                        "abi_name": abi_task["name"],
                        "status": "active",
                        "historical_crawl_status": "pending",
                        "progress": 0,
                        "task_pickedup": False,
                        "abi": json.dumps(abi_task),
                    }
                )

            except Exception as e:
                logger.error(
                    f"Error creating subscription for subscription for abi {abi_task['name']}: {str(e)}"
                )
                db_session_v3.rollback()
                raise e

        insert_statement = insert(AbiJobs).values(abi_tasks)

        result_stmt = insert_statement.on_conflict_do_nothing(
            index_elements=[
                AbiJobs.chain,
                AbiJobs.address,
                AbiJobs.abi_selector,
                AbiJobs.customer_id,
            ]
        )

        try:
            db_session_v3.execute(result_stmt)

            db_session_v3.commit()
        except Exception as e:
            logger.error(f"Error inserting subscriptions: {str(e)}")
            db_session_v3.rollback()
    return None


def migrate_v3_tasks(
    user_id: UUID, customer_id: UUID, blockchain: Optional[str] = None
):
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

    chain_to_subscription_type = {
        CANONICAL_SUBSCRIPTION_TYPES[key].blockchain: key
        for key in CANONICAL_SUBSCRIPTION_TYPES.keys()
        if key.endswith("smartcontract")
    }

    logger.info(
        "Found users collection resources: %s", len(subscription_resources.resources)
    )

    db_engine = MoonstreamDBIndexesEngine()

    if len(subscription_resources.resources) == 0:
        raise Exception("User has no subscriptions")

    collection_id = subscription_resources.resources[0].resource_data["collection_id"]

    query = f"tag:type:subscription"

    if blockchain is not None:
        query += f" tag:subscription_type_id:{chain_to_subscription_type[blockchain]}"

    subscriptions: List[BugoutSearchResult] = get_all_entries_from_search(
        journal_id=collection_id,
        search_query=query,
        token=os.environ.get("SPECIFIC_ACCESS_TOKEN"),
        limit=100,
        content=True,
    )

    logger.info("Found users subscriptions: %s", len(subscriptions))

    if len(subscriptions) == 0:
        raise Exception("User has no subscriptions")

    with db_engine.yield_db_session_ctx() as session:

        for index, subscription in enumerate(subscriptions):

            user_subscription_abis = []

            subscriptions_to_insert = {}

            abis = None
            address = None
            subscription_type_id = None

            subscription_id = subscription.entry_url.split("/")[-1]

            if subscription.content is None:
                continue

            subscription_data = json.loads(subscription.content)

            if "abi" in subscription_data:
                abis_container = subscription_data["abi"]

            for tag in subscription.tags:
                if tag.startswith("subscription_type_id:"):
                    subscription_type_id = tag.split(":")[1]
                if tag.startswith("address:"):
                    address = tag.split(":")[1]

            if subscription_type_id is None:
                continue

            if abis_container is not None:
                try:
                    abis = json.loads(abis_container)
                except Exception as e:
                    logger.error(
                        f"Error loading abi for subscription {subscription.id}: {str(e)}"
                    )
                    continue

            ### reformat abi to separate abi tasks

            chain = CANONICAL_SUBSCRIPTION_TYPES[subscription_type_id].blockchain

            existing_abi_jobs = (
                session.query(AbiJobs)
                .filter(AbiJobs.customer_id == customer_id)
                .filter(AbiJobs.user_id == user_id)
                .filter(AbiJobs.chain == blockchain)
            ).all()

            job_by_abi_selector = {abi.abi_selector: abi for abi in existing_abi_jobs}

            for abi_task in abis:

                if abi_task["type"] not in ("event", "function"):
                    continue

                abi_selector = Web3.keccak(
                    text=abi_task["name"]
                    + "("
                    + ",".join(map(lambda x: x["type"], abi_task["inputs"]))
                    + ")"
                )

                if abi_task["type"] == "function":
                    abi_selector = abi_selector[:4]

                abi_selector = abi_selector.hex()

                if abi_selector in job_by_abi_selector:
                    # ABI job already exists, create subscription link
                    if subscription_id:
                        subscriptions_to_insert[
                            str(job_by_abi_selector[abi_selector].id)
                        ] = subscription_id
                else:

                    try:

                        abi_job = {
                            "address": (HexBytes(address)),
                            "user_id": user_id,
                            "customer_id": customer_id,
                            "abi_selector": abi_selector,
                            "chain": chain,
                            "abi_name": abi_task["name"],
                            "status": "active",
                            "historical_crawl_status": "pending",
                            "progress": 0,
                            "task_pickedup": False,
                            "abi": json.dumps(abi_task),
                        }

                        try:
                            AbiJobs(**abi_job)
                        except Exception as e:
                            logger.error(
                                f"Error creating subscription for subscription {subscription.id}: {str(e)}"
                            )
                            continue

                        user_subscription_abis.append(abi_job)

                    except Exception as e:
                        logger.error(
                            f"Error creating subscription for subscription {subscription.id}: {str(e)}"
                        )
                        session.rollback()
                        continue
            if len(user_subscription_abis) > 0:
                insert_statement = insert(AbiJobs).values(user_subscription_abis)

                result_stmt = insert_statement.on_conflict_do_nothing().returning(
                    AbiJobs.id
                )

                try:
                    ids = session.execute(result_stmt)
                except Exception as e:
                    logger.error(f"Error inserting subscriptions: {str(e)}")
                    session.rollback()

                for id in ids:
                    subscriptions_to_insert[id[0]] = subscription_id

            if len(subscriptions_to_insert) > 0:

                insert_statement = insert(AbiSubscriptions).values(
                    [
                        {"abi_job_id": k, "subscription_id": v}
                        for k, v in subscriptions_to_insert.items()
                    ]
                )

                result_stmt = insert_statement.on_conflict_do_nothing()

                try:
                    session.execute(result_stmt)
                except Exception as e:
                    logger.error(f"Error inserting subscriptions: {str(e)}")
                    session.rollback()

            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error inserting subscriptions: {str(e)}")
                session.rollback()

            logger.info(f"Processed {index} subscriptions")

        return None
