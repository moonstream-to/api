"""
Generate entity subscriptions from existing brood resources subscriptions
"""
import hashlib
import logging
import json
import os
import traceback
from typing import List, Optional, Dict, Any, Union, Tuple
import uuid
import time

import boto3  # type: ignore
from bugout.data import BugoutResources, BugoutResource
from bugout.exceptions import BugoutResponseException
from entity.exceptions import EntityUnexpectedResponse  # type: ignore
from entity.data import EntityCollectionResponse, EntityResponse  # type: ignore

from ...settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
    BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
    MOONSTREAM_APPLICATION_ID,
    BUGOUT_RESOURCE_TYPE_DASHBOARD,
)
from ...settings import bugout_client as bc, entity_client as ec
from ..subscription_types import CANONICAL_SUBSCRIPTION_TYPES

logger = logging.getLogger(__name__)


### create collection for user


def create_collection_for_user(user_id: uuid.UUID) -> str:
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
    return str(collection_id)


def add_entity_subscription(
    user_id: uuid.UUID,
    subscription_type_id: str,
    collection_id: str,
    address: str,
    color: str,
    label: str,
    content: Dict[str, Any],
) -> EntityResponse:
    """
    Add subscription to collection
    """

    if subscription_type_id not in CANONICAL_SUBSCRIPTION_TYPES:
        raise ValueError(
            f"Unknown subscription type ID: {subscription_type_id}. "
            f"Known subscription type IDs: {CANONICAL_SUBSCRIPTION_TYPES.keys()}"
        )
    elif CANONICAL_SUBSCRIPTION_TYPES[subscription_type_id].blockchain is None:
        raise ValueError(
            f"Subscription type ID {subscription_type_id} is not a blockchain subscription type."
        )

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

    return entity


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


def find_user_collection(
    user_id: uuid.UUID,
    create_if_not_exists: bool = False,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Find user collection in Brood resources
    Can create new collection if not exists and create_if_not_exists = True
    """
    params = {
        "type": BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
        "user_id": str(user_id),
    }
    logger.info(f"Looking for collection for user {user_id}")
    try:
        user_entity_resources: BugoutResources = bc.list_resources(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
        )
    except BugoutResponseException as e:
        logger.error(
            f"Error listing subscriptions for user ({user_id}) Bugout error: {str(e)}"
        )
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({user_id}) error: {str(e)}"
        )

    if len(user_entity_resources.resources) > 0:
        collection_id = user_entity_resources.resources[0].resource_data[
            "collection_id"
        ]
        logger.info(
            f"Collection found for user {user_id}. collection_id: {collection_id}"
        )
        return collection_id, str(user_entity_resources.resources[0].id)
    elif create_if_not_exists:
        # Create collection new collection for user
        logger.info(f"Creating new collection")
        collection = create_collection_for_user(user_id)
        return collection, None

    return None, None


def generate_entity_subscriptions_from_brood_resources() -> None:
    """
    Parse all existing dashboards at Brood resource
    and replace key to correct one.
    Schema can use for rename first level keys
    """

    ### Get admin user id

    admin_user = bc.get_user(token=MOONSTREAM_ADMIN_ACCESS_TOKEN)

    admin_user_id = admin_user.id

    logger.info(f"admin user :{admin_user.username}")

    ### Get all subscription resources type = "subscription"

    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    logger.info(f"Admin own {len(resources.resources)} subscriptions")

    ### initial users_subscriptions, dashboards_by_user, stages is empty

    users_subscriptions: Dict[Union[str, uuid.UUID], Any] = {}

    stages: Dict[Union[str, uuid.UUID], Any] = {}

    ### Restore previous stages if exists stages.json

    if os.path.exists("stages.json"):
        with open("stages.json", "r") as f:
            stages = json.load(f)

    ### Subscriptions parsing and save to users_subscriptions

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

    logger.info(f"parsed users: {len(users_subscriptions)}")

    ### Create collections and add subscriptions

    try:
        for user_id, subscriptions in users_subscriptions.items():
            user_id = str(user_id)

            collection_id = None
            resource_id_of_user_collection = None

            ### Collection can already exist in stages.json
            if "collection_id" in stages[user_id]:
                collection_id = stages[user_id]["collection_id"]
                if "subscription_resource_id" in stages[user_id]:
                    resource_id_of_user_collection = stages[user_id][
                        "subscription_resource_id"
                    ]
            else:
                ### look for collection in brood resources
                collection_id, resource_id_of_user_collection = find_user_collection(
                    user_id, create_if_not_exists=True
                )

            if collection_id is None:
                logger.info(f"Collection not found or create for user {user_id}")
                continue

            stages[user_id]["collection_id"] = collection_id

            # Create user subscription collection resource

            if "subscription_resource_id" not in stages[user_id]:
                if resource_id_of_user_collection is not None:
                    stages[user_id]["subscription_resource_id"] = str(
                        resource_id_of_user_collection
                    )
                else:
                    resource_data = {
                        "type": BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
                        "user_id": str(user_id),
                        "collection_id": str(collection_id),
                        "version": "1.0.0",
                    }

                    ### Create resource for user collection
                    try:
                        subscription_resource: BugoutResource = bc.create_resource(
                            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                            application_id=MOONSTREAM_APPLICATION_ID,
                            resource_data=resource_data,
                        )
                        stages[user_id]["subscription_resource_id"] = str(
                            subscription_resource.id
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to create subscription brood resource: {str(e)}"
                        )

            if "processed_subscriptions" not in stages[user_id]:
                stages[user_id]["processed_subscriptions"] = {}

            ### Add subscriptions to collection

            for subscription in subscriptions:
                if (
                    str(subscription["subscription_id"])
                    in stages[user_id]["processed_subscriptions"]
                ):
                    continue

                subscription_type_id = subscription["subscription_type_id"]
                address = subscription["address"]
                color = subscription["color"]
                label = subscription["label"]

                # try to get abi from S3
                abi = None
                if subscription.get("bucket") and subscription.get("s3_path"):
                    try:
                        abi_body = get_abi_from_s3(
                            bucket=subscription["bucket"],
                            s3_path=subscription["s3_path"],
                        )
                        # abi hash
                        abi_hash = hashlib.sha256(abi_body.encode("utf-8")).hexdigest()
                        abi = True
                        logger.info(
                            f"Got abi from S3 from path {subscription['s3_path']}"
                        )
                    except Exception as e:
                        logger.error(f"Failed to get abi from S3: {str(e)}")
                        abi = None

                # Add subscription to collection

                logger.info(f"Add subscription to collection: {collection_id}")

                entity = add_entity_subscription(
                    user_id=user_id,
                    collection_id=collection_id,
                    subscription_type_id=subscription_type_id,
                    address=address,
                    color=color,
                    label=label,
                    content={"abi": abi_body, "abi_hash": abi_hash} if abi else {},
                )
                stages[user_id]["processed_subscriptions"][
                    str(subscription["subscription_id"])
                ] = {"entity_id": str(entity.entity_id), "dashboard_ids": []}

            # Add permissions to user

            if user_id != admin_user_id:
                # Add permissions to user

                if "permissions_granted" not in stages[user_id]:
                    try:
                        bc.update_journal_scopes(
                            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                            journal_id=collection_id,
                            holder_type="user",
                            holder_id=user_id,
                            permission_list=[
                                "journals.read",
                                "journals.update",
                                "journals.entries.read",
                                "journals.entries.create",
                                "journals.entries.update",
                                "journals.entries.delete",
                            ],
                        )

                        stages[user_id]["permissions_granted"] = True
                    except Exception as e:
                        logger.error(f"Failed to add permissions to user: {str(e)}")
                        continue
            else:
                logger.warn(
                    f"User {user_id} == {admin_user_id} permissions not changed. Unexpected behaivior!"
                )

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Failed to proccess user subscriptions: {str(e)}")
    finally:
        try:
            with open("stages.json", "w") as f:
                json.dump(stages, f)
        except Exception as e:
            logger.error(f"Failed to save stages: {str(e)}")
            # write as text
            with open("stages-json-failed.txt", "w") as f:
                f.write(str(stages))


def update_dashboards_connection():
    """
    Look up all dashboards and update their connection to the user subscription
    """

    dashboards_by_user: Dict[Union[str, uuid.UUID], Any] = {}

    stages: Dict[Union[str, uuid.UUID], Any] = {}

    ### Restore previous stages if exists stages.json

    if os.path.exists("stages.json"):
        with open("stages.json", "r") as f:
            stages = json.load(f)

    ### Dashboards parsing and save to dashboards_by_user

    dashboard_resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_DASHBOARD},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    for dashboard in dashboard_resources.resources:
        if "user_id" not in dashboard.resource_data:
            continue

        user_id = dashboard.resource_data["user_id"]

        if user_id not in dashboards_by_user:
            dashboards_by_user[user_id] = []

        dashboards_by_user[user_id].append(dashboard)

    try:
        for user in dashboards_by_user:
            logger.info(f"dashboards: {len(dashboards_by_user[user])}")

            if user not in stages:
                continue

            for dashboard in dashboards_by_user[user]:
                dashboard_data = dashboard.resource_data

                dashboard_subscription_settings = dashboard_data.get(
                    "subscription_settings"
                )

                if dashboard_subscription_settings is None:
                    continue

                if len(dashboard_subscription_settings) == 0:
                    continue

                logger.info(f"dashboard {dashboard.id}")

                for setting_index, subscription_setting in enumerate(
                    dashboard_subscription_settings
                ):
                    logger.info(
                        f"Find subscripton: {subscription_setting['subscription_id']}"
                    )

                    old_subscription_id = str(subscription_setting["subscription_id"])

                    if old_subscription_id in stages[user]["processed_subscriptions"]:
                        logger.info(
                            f"subscription found: {subscription_setting['subscription_id']}"
                        )

                        subscription_stages_metadata = stages[user][
                            "processed_subscriptions"
                        ][subscription_setting["subscription_id"]]

                        if (
                            str(dashboard.id)
                            in subscription_stages_metadata["dashboard_ids"]
                        ):
                            continue

                        # change original dashboard subscription settings

                        dashboard_data["subscription_settings"][setting_index][
                            "subscription_id"
                        ] = subscription_stages_metadata["entity_id"]

                        # Update brood resource in bugout client

                        stages[user]["processed_subscriptions"][old_subscription_id][
                            "dashboard_ids"
                        ].append(str(dashboard.id))

                try:
                    logger.info(f"Update dashboard: {dashboard.id} for user {user}")

                    bc.update_resource(
                        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                        resource_id=dashboard.id,
                        resource_data={
                            "update": {
                                "subscription_settings": dashboard_data[
                                    "subscription_settings"
                                ]
                            }
                        },
                    )

                except Exception as e:
                    traceback.print_exc()
                    logger.error(
                        f"**Failed to update dashboard: {str(e)} for user {user}**"
                    )
                    continue
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Failed to proccess dashboards: {str(e)}")

    finally:
        try:
            with open("stages.json", "w") as f:
                json.dump(stages, f)
        except Exception as e:
            logger.error(f"Failed to save stages: {str(e)}")
            # write as text
            with open("stages-json-failed.txt", "w") as f:
                f.write(str(stages))


def delete_generated_entity_subscriptions_from_brood_resources():
    """
    Delete all generated entity subscriptions previously created by the script
    Also delete all generated entity subscriptions from the brood resources
    """

    ### stages file example

    admin_user = bc.get_user(token=MOONSTREAM_ADMIN_ACCESS_TOKEN)

    logger.info(f"admin user :{admin_user.username}")

    # Get all subscriptions

    ### Get all subscription resources type = "subscription"

    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    logger.info(f"Admin own {len(resources.resources)} subscriptions")

    ### initial users_subscriptions, dashboards_by_user, stages is empty

    users_subscriptions: Dict[Union[str, uuid.UUID], Any] = {}

    stages: Dict[Union[str, uuid.UUID], Any] = {}

    ### Restore previous stages if exists stages.json

    if os.path.exists("stages.json"):
        with open("stages.json", "r") as f:
            stages = json.load(f)

    ### Subscriptions parsing and save to users_subscriptions

    for resource in resources.resources:
        resource_data = resource.resource_data

        resource_data["subscription_id"] = resource.id

        if "user_id" not in resource_data:
            continue

        user_id = resource_data["user_id"]

        if user_id not in users_subscriptions:
            users_subscriptions[user_id] = []

        users_subscriptions[user_id].append(resource_data)

    logger.info(f"parsed users: {len(users_subscriptions)}")

    ### Create collections and add subscriptions

    try:
        for user_id, _ in users_subscriptions.items():
            user_id = str(user_id)

            collection_id = None
            resource_id_of_user_collection = None

            ### Collection can already exist in stages.json
            if "collection_id" in stages[user_id]:
                collection_id = stages[user_id]["collection_id"]

                if "subscription_resource_id" in stages[user_id]:
                    resource_id_of_user_collection = stages[user_id][
                        "subscription_resource_id"
                    ]

            else:
                ### look for collection in brood resources
                collection_id, resource_id_of_user_collection = find_user_collection(
                    user_id, create_if_not_exists=False
                )

            if collection_id is None:
                logger.info(f"Collection not found or create for user {user_id}")
                continue

            ### Delete collection

            try:
                ec.delete_collection(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN, collection_id=collection_id
                )
                logger.info(f"Collection deleted {collection_id}")

            except Exception as e:
                logger.error(f"Failed to delete collection: {str(e)}")

            ### Delete collection resource

            try:
                logger.info(f"Collection resource id {resource_id_of_user_collection}")
                bc.delete_resource(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    resource_id=resource_id_of_user_collection,
                )
                logger.info(
                    f"Collection resource deleted {resource_id_of_user_collection}"
                )

                # clear stages

                stages[user_id] = {}

            except Exception as e:
                logger.error(f"Failed to delete collection resource: {str(e)}")
                continue

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Failed to proccess user subscriptions: {str(e)}")


def restore_dashboard_state():
    ### initial users_subscriptions, dashboards_by_user, stages is empty

    dashboards_by_user: Dict[Union[str, uuid.UUID], Any] = {}

    stages: Dict[Union[str, uuid.UUID], Any] = {}

    ### Restore previous stages if exists stages.json

    if os.path.exists("stages.json"):
        with open("stages.json", "r") as f:
            stages = json.load(f)

    ### Subscriptions parsing and save to users_subscriptions

    ### Dashboards parsing and save to dashboards_by_user

    dashboards: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_DASHBOARD},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    for dashboard in dashboards.resources:
        if "user_id" not in dashboard.resource_data:
            continue

        user_id = dashboard.resource_data["user_id"]

        if user_id not in dashboards_by_user:
            dashboards_by_user[user_id] = []

        dashboards_by_user[user_id].append(dashboard)

    ### Retunr all dashboards to old state

    logger.info(f"Amount of users: {len(dashboards_by_user)}")

    # print(dashboards_by_user)

    for user_id in dashboards_by_user:
        logger.info(
            f"Amount of dashboards: {len(dashboards_by_user[user_id])} of user {user_id}"
        )

        user_entity_subscriptions = {
            subscription["entity_id"]: key
            for key, subscription in stages[user_id]["processed_subscriptions"].items()
        }

        for dashboard in dashboards_by_user[user_id]:
            try:
                dashboard_data = dashboard.resource_data

                if "subscription_settings" not in dashboard_data:
                    print("no subscription_settings")
                    continue

                if len(dashboard_data["subscription_settings"]) == 0:
                    print("no subscription_settings")
                    continue

                dashboard_metadata = dashboard_data["subscription_settings"]

                for index, settings in enumerate(dashboard_metadata):
                    if "subscription_id" not in settings:
                        print("no subscription_id")
                        continue

                    subscription_id = settings["subscription_id"]

                    if subscription_id not in user_entity_subscriptions:
                        continue

                    logger.info(
                        f"Update dashboard {dashboard.id} with subscription {subscription_id} to old state"
                    )

                    dashboard_metadata[index][
                        "subscription_id"
                    ] = user_entity_subscriptions[subscription_id]

                bc.update_resource(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    resource_id=dashboard.id,
                    resource_data={
                        "update": {"subscription_settings": dashboard_metadata}
                    },
                )
            except Exception as e:
                traceback.print_exc()
                logger.error(f"Failed to update dashboard: {str(e)}")
                continue
