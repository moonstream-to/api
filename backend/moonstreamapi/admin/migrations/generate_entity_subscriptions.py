"""
Convert all addresses in user subscriptions 
and ethereum_labels column to checksum address.
"""
import hashlib
import logging
import json
from typing import List, Optional, Dict, Any, Union
import uuid

import boto3
from bugout.data import BugoutResources, BugoutResource
from bugout.exceptions import BugoutResponseException
from entity.exceptions import EntityUnexpectedResponse
from entity.data import (
    EntityCollectionResponse,
)

from ...settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
    MOONSTREAM_APPLICATION_ID,
)
from ...settings import bugout_client as bc, entity_client as ec
from ..subscription_types import CANONICAL_SUBSCRIPTION_TYPES

logger = logging.getLogger(__name__)


# Dashboard resource type
BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"


### create collection for user


def create_collection_for_user(user_id: uuid.UUID) -> EntityCollectionResponse:
    """
    Create collection for user if not exist
    """
    try:
        # try get collection

        collection: EntityCollectionResponse = ec.add_collection(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN, name=f"subscriptions_{user_id}"
        )
        collection_id = collection.collection_id

    except EntityUnexpectedResponse as e:
        logger.error(f"Error create collection, error: {str(e)}")
    return collection_id


def add_entity_subscription(
    user_id: uuid.UUID,
    subscription_type_id: str,
    collection_id: str,
    address: str,
    color: str,
    label: str,
    content: Dict[str, Any],
) -> None:
    """
    Add subscription to collection
    """
    try:
        entity = ec.add_entity(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            collection_id=collection_id,
            address=address,
            blockchain=CANONICAL_SUBSCRIPTION_TYPES[subscription_type_id].blockchain,
            name=label,
            required_fields=[
                {"type": "subscription"},
                {"subscription_type_id": f"{subscription_type_id}"},
                {"color": f"{color}"},
                {"label": f"{label}"},
                {"user_id": f"{user_id}"},
            ],
            secondary_fields=content,
        )
    except EntityUnexpectedResponse as e:
        logger.info(f"Can't add subscription to collection: {collection_id} {str(e)}")
    except Exception as e:
        logger.error(f"Error add subscription to collection: {str(e)}")


def get_abi_from_s3(s3_path: str, bucket: str):
    """
    Get ABI from S3
    """
    try:
        s3 = boto3.resource("s3")
        obj = s3.Object(bucket, s3_path)
        abi = obj.get()["Body"].read().decode("utf-8")
        return abi
    except Exception as e:
        logger.error(f"Error get ABI from S3: {str(e)}")


def add_collection_permissions_to_user(
    user_id: uuid.UUID, collection_id: str, permissions: List[str]
) -> None:
    """
    Add permissions to user
    """
    bc.update_journal_scopes(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=collection_id,
        holder_type="user",
        holder_id=user_id,
        permission_list=permissions,
    )


def revoke_collection_permissions_from_user(
    user_id: uuid.UUID, collection_id: str, permissions: List[str]
):

    """
    Remove all permissions from user
    """
    bc.delete_journal_scopes(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=collection_id,
        holder_type="user",
        holder_id=user_id,
        permission_list=permissions,
    )


def Generate_entity_subscriptions_from_brood_resources() -> None:
    """
    Parse all existing dashboards at Brood resource
    and replace key to correct one.
    Schema can use for rename first level keys
    """
    search_by_key = BUGOUT_RESOURCE_TYPE_SUBSCRIPTION

    ### Get admin user id

    admin_user = bc.get_user(token=MOONSTREAM_ADMIN_ACCESS_TOKEN)

    admin_user_id = admin_user.id

    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": search_by_key},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    users_subscriptions: Dict[Union[str, uuid.UUID], Any] = {}
    stages: Dict[Union[str, uuid.UUID], Any] = {}

    with open("stages.json", "r") as f:
        stages = json.load(f)

    for resource in resources.resources:

        resource_data = resource.resource_data

        resource_data["subscription_id"] = resource.id

        if "user_id" not in resource_data:
            continue

        user_id = resource_data["user_id"]

        if user_id not in users_subscriptions:
            users_subscriptions[user_id] = []

            # Stages object
        if user_id not in stages:
            stages[user_id] = {}

        users_subscriptions[user_id].append(resource_data)

    # Start proccessing users subscriptions

    try:
        for user_id, subscriptions in users_subscriptions.items():

            # Create collection for user

            if "collection_id" in stages[user_id]:
                collection_id = stages[user_id]["collection_id"]
            else:
                collection_id = create_collection_for_user(user_id)
                stages[user_id]["collection_id"] = collection_id

            # Create user subscription collection resource

            resource_data = {
                "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
                "user_id": str(user_id),
                "subscription_collection": str(collection_id),
            }

            if "subscription_resource_id" in stages[user_id]:

                try:
                    subscription_resource: BugoutResource = bc.create_resource(
                        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                        application_id=MOONSTREAM_APPLICATION_ID,
                        resource_data=resource_data,
                    )
                    stages[user_id][
                        "subscription_resource_id"
                    ] = subscription_resource.id
                except Exception as e:
                    logger.error(f"Failed to create resource: {str(e)}")

            # Add subscriptions to collection

            if "proccessed_subscriptions" not in stages[user_id]:
                stages[user_id]["proccessed_subscriptions"] = []

            for subscription in subscriptions:

                """
                subscription_type_id: str,
                collection_id: str,
                address: str,
                color: str,
                label: str,
                """

                if subscription["id"] in stages[user_id]["proccessed_subscriptions"]:
                    continue

                subscription_type_id = subscription["subscription_type_id"]
                address = subscription["address"]
                color = subscription["color"]
                label = subscription["label"]

                # try to get abi from S3

                if resource_data["bucket"] and resource_data["s3_path"]:
                    try:
                        abi = get_abi_from_s3(
                            bucket=resource_data["bucket"],
                            s3_path=resource_data["s3_path"],
                        )
                        # abi hash
                        abi_hash = hashlib.sha256(abi.encode("utf-8")).hexdigest()
                    except Exception as e:
                        logger.error(f"Failed to get abi from S3: {str(e)}")
                        abi = None

                add_entity_subscription(
                    user_id=user_id,
                    collection_id=collection_id,
                    subscription_type_id=subscription_type_id,
                    address=address,
                    color=color,
                    label=label,
                    content=abi if abi else {},
                )

                stages[user_id]["proccessed_subscriptions"].append(subscription["id"])

            # Add permissions to user

            try:

                add_collection_permissions_to_user(
                    user_id=user_id,
                    collection_id=collection_id,
                    permissions=["read", "update"],
                )
                stages[user_id]["permissions_granted"] = True
            except Exception as e:
                logger.error(f"Failed to add permissions to user: {str(e)}")

            # Remove permissions from user
            try:
                revoke_collection_permissions_from_user(
                    user_id=admin_user_id,
                    collection_id=collection_id,
                    permissions=["read", "update"],
                )
                stages[user_id]["permissions_revoked"] = True
            except Exception as e:
                logger.error(f"Failed to revoke permissions from user: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to proccess user subscriptions: {str(e)}")
    finally:
        with open("stages.json", "w") as f:
            json.dump(stages, f)
