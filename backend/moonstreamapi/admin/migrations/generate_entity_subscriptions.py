"""
Generate entity subscriptions from existing brood resources subscriptions
"""
import hashlib
import logging
import json
import os
from pprint import pprint
import traceback
from typing import List, Optional, Dict, Any, Union, Tuple
import uuid

import boto3
from bugout.data import BugoutResources, BugoutResource
from bugout.exceptions import BugoutResponseException
from entity.exceptions import EntityUnexpectedResponse
from entity.data import EntityCollectionResponse, EntityResponse

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
            "subscription_collection"
        ]
        print(f"Collection found for user {user_id}. collection_id: {collection_id}")
        return collection_id, str(user_entity_resources.resources[0].id)
    elif create_if_not_exists:
        # Create collection new collection for user
        print(f"Creating new collection")
        collection = create_collection_for_user(user_id)
        return str(collection.collection_id), None

    return None, None


def Generate_entity_subscriptions_from_brood_resources() -> None:
    """
    Parse all existing dashboards at Brood resource
    and replace key to correct one.
    Schema can use for rename first level keys
    """

    ### Get admin user id

    admin_user = bc.get_user(token=MOONSTREAM_ADMIN_ACCESS_TOKEN)

    admin_user_id = admin_user.id

    print(f"admin user :{admin_user.username}")

    ### Get all subscription resources type = "subscription"

    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    print(f"Admin own {len(resources.resources)} subscriptions")

    ### initial users_subscriptions, dashboards_by_user, stages is empty

    users_subscriptions: Dict[Union[str, uuid.UUID], Any] = {}

    dashboards_by_user: Dict[Union[str, uuid.UUID], Any] = {}

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

    print(f"parsed users: {len(users_subscriptions)}")

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

        print(f"dashboard name:{dashboard.resource_data['name']}")

        if user_id not in dashboards_by_user:
            dashboards_by_user[user_id] = []

        dashboards_by_user[user_id].append(dashboard)

    ### Create collections and add subscriptions

    try:
        for user_id, subscriptions in users_subscriptions.items():

            user_id = str(user_id)

            collection_id = None
            resource_id_of_user_collection = None

            ### Collection can already exist in stages.json
            if "collection_id" in stages[user_id]:
                collection_id = stages[user_id]["collection_id"]
            else:
                ### look for collection in brood resources
                collection_id, resource_id_of_user_collection = find_user_collection(
                    user_id, create_if_not_exists=True
                )

            if collection_id is None:
                print(f"Collection not found or create for user {user_id}")
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
                        "subscription_collection": str(collection_id),
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

            if "proccessed_subscriptions" not in stages[user_id]:
                stages[user_id]["proccessed_subscriptions"] = {}

            ### Add subscriptions to collection

            for subscription in subscriptions:

                if (
                    str(subscription["subscription_id"])
                    in stages[user_id]["proccessed_subscriptions"]
                ):
                    continue

                subscription_type_id = subscription["subscription_type_id"]
                address = subscription["address"]
                color = subscription["color"]
                label = subscription["label"]

                # try to get abi from S3
                abi = None
                if resource_data.get("bucket") and resource_data.get("s3_path"):
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

                entity = add_entity_subscription(
                    user_id=user_id,
                    collection_id=collection_id,
                    subscription_type_id=subscription_type_id,
                    address=address,
                    color=color,
                    label=label,
                    content={"abi": abi, "abi_hash": abi_hash} if abi else {},
                )
                stages[user_id]["proccessed_subscriptions"][
                    str(subscription["subscription_id"])
                ] = {"entity_id": str(entity.entity_id), "dashboard_ids": []}

            print(f"users:{len(dashboards_by_user)}")

            for user in dashboards_by_user:

                print(f"dashboards: {len(dashboards_by_user[user])}")

                for dashboard in dashboards_by_user[user]:

                    dashboard_data = dashboard.resource_data

                    dashboard_subscription_settings = dashboard_data.get(
                        "subscription_settings"
                    )

                    if dashboard_subscription_settings is None:
                        continue

                    print(f"dashboard {dashboard.id}")

                    print(f"dashboard name:{dashboard_data['name']}")

                    for setting_index, subscription_setting in enumerate(
                        dashboard_subscription_settings
                    ):

                        print(
                            f"Find subscripton: {subscription_setting['subscription_id']}"
                        )

                        if (
                            str(subscription_setting["subscription_id"])
                            in stages[user]["proccessed_subscriptions"]
                        ):

                            print(
                                f"subscription found: {subscription_setting['subscription_id']}"
                            )

                            subscription_metadata = stages[user][
                                "proccessed_subscriptions"
                            ][subscription_setting["subscription_id"]]

                            if (
                                str(dashboard.id)
                                in subscription_metadata["dashboard_ids"]
                            ):
                                continue

                            try:
                                # change original dashboard subscription settings

                                dashboard_data["subscription_settings"][setting_index][
                                    "subscription_id"
                                ] = subscription_metadata["entity_id"]

                                # Update brood resource in bugout client

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
                                stages[user_id]["proccessed_subscriptions"][
                                    str(subscription_setting["subscription_id"])
                                ]["dashboard_ids"].append(str(dashboard.id))
                            except Exception as e:
                                traceback.print_exc()
                                logger.error(f"Failed to update dashboard: {str(e)}")
                                continue

                            # print(stages[user]["proccessed_subscriptions"])

            # for subscription in subscriptions:

            #     user_dashboards = dashboards_by_user[user_id]

            #     # print(user_dashboards)

            #     for user_dashboard in user_dashboards:
            #         dashboard_subscription_settings = user_dashboard.resource_data.get(
            #             "subscription_settings"
            #         )

            #         if (
            #             str(user_dashboard.id)
            #             in stages[user_id]["proccessed_subscriptions"][
            #                 str(subscription["subscription_id"])
            #             ]["dashboard_ids"]
            #         ):
            #             print(
            #                 f"Subscription {subscription['subscription_id']} already added to dashboard {user_dashboard.id}"
            #             )
            #             continue

            #         entity_id = stages[user_id]["proccessed_subscriptions"][
            #             str(subscription["subscription_id"])
            #         ]["entity_id"]

            #         dashboard_data = user_dashboard.resource_data
            #         print(f"subscription2: {subscription['subscription_id']}")
            #         if dashboard_subscription_settings:
            #             print(f"dashboard_subscription_setting")
            #             pprint(
            #                 [
            #                     dashboard_sub_settings["subscription_id"]
            #                     for dashboard_sub_settings in dashboard_subscription_settings
            #                 ]
            #             )

            #             for index, dashboard_subscription_setting in enumerate(
            #                 dashboard_subscription_settings
            #             ):

            #                 # print(
            #                 #     f"subscription: {str(subscription['subscription_id'])}"
            #                 # )
            #                 if dashboard_subscription_setting.get(
            #                     "subscription_id"
            #                 ) == str(subscription["subscription_id"]):
            #                     try:
            #                         # change original dashboard subscription settings

            #                         dashboard_data["subscription_settings"][index][
            #                             "subscription_id"
            #                         ] = str(entity_id)

            #                         # Update brood resource in bugout client

            #                         bc.update_resource(
            #                             token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            #                             resource_id=user_dashboard.id,
            #                             resource_data={
            #                                 "update": {
            #                                     "subscription_settings": dashboard_data[
            #                                         "subscription_settings"
            #                                     ]
            #                                 }
            #                             },
            #                         )
            #                     except Exception as e:
            #                         traceback.print_exc()
            #                         logger.error(
            #                             f"Failed to update dashboard: {str(e)}"
            #                         )
            #                         continue

            #                     stages[user_id]["proccessed_subscriptions"][
            #                         str(subscription["subscription_id"])
            #                     ]["dashboard_ids"].append(str(user_dashboard.id))

            if user_id != admin_user_id:
                # Add permissions to user

                if "permissions_granted" not in stages[user_id]:
                    try:

                        add_collection_permissions_to_user(
                            user_id=user_id,
                            collection_id=collection_id,
                            permissions=[
                                "journals.read",
                                "journals.update",
                                "journals.delete",
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


def revoke_admin_permissions_from_collections(
    admin_user_id: uuid.UUID, collections: List[str]
):
    for collection in collections:
        try:
            revoke_collection_permissions_from_user(
                user_id=admin_user_id,
                collection_id=collection,
                permissions=[
                    "journals.read",
                    "journals.update",
                    "journals.delete",
                    "journals.entries.read",
                    "journals.entries.create",
                    "journals.entries.update",
                    "journals.entries.delete",
                ],
            )
        except Exception as e:
            logger.error(f"Failed to revoke permissions: {str(e)}")
            continue

    logger.info("Admin permissions revoked from collections")
