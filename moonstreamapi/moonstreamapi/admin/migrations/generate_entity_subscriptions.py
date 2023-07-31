"""
Generate entity subscriptions from existing brood resources subscriptions
"""
import hashlib
import json
import logging
import os
import traceback
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

import boto3  # type: ignore
from bugout.data import (
    BugoutJournal,
    BugoutJournalEntity,
    BugoutResource,
    BugoutResources,
)
from bugout.exceptions import BugoutResponseException, BugoutUnexpectedResponse

from ...settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    BUGOUT_RESOURCE_TYPE_DASHBOARD,
    BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
    BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
)
from ...settings import bugout_client as bc
from ..subscription_types import CANONICAL_SUBSCRIPTION_TYPES

logger = logging.getLogger(__name__)


### Create journal for user


def create_journal_for_user(user_id: uuid.UUID) -> str:
    """
    Create journal (collection) for user if not exist
    """
    try:
        # Try to get journal
        journal: BugoutJournal = bc.create_journal(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN, name=f"subscriptions_{user_id}"
        )
        journal_id = journal.id
    except BugoutUnexpectedResponse as e:
        logger.error(f"Error create journal, error: {str(e)}")
    return str(journal_id)


def add_entity_subscription(
    user_id: uuid.UUID,
    subscription_type_id: str,
    journal_id: str,
    address: str,
    color: str,
    label: str,
    content: Dict[str, Any],
) -> BugoutJournalEntity:
    """
    Add subscription to journal (collection).
    """

    if subscription_type_id not in CANONICAL_SUBSCRIPTION_TYPES:
        raise ValueError(
            f"Unknown subscription type ID: {subscription_type_id}. "
            f"Known subscription type IDs: {CANONICAL_SUBSCRIPTION_TYPES.keys()}"
        )
    blockchain = CANONICAL_SUBSCRIPTION_TYPES[subscription_type_id].blockchain
    if blockchain is None:
        raise ValueError(
            f"Subscription type ID {subscription_type_id} is not a blockchain subscription type."
        )

    entity = bc.create_entity(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=journal_id,
        address=address,
        blockchain=blockchain,
        title=label,
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


def find_user_journal(
    user_id: uuid.UUID,
    create_if_not_exists: bool = False,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Find user journal (collection) in Brood resources
    Can create new journal (collection) if not exists and create_if_not_exists = True
    """
    params = {
        "type": BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
        "user_id": str(user_id),
    }
    logger.info(f"Looking for journal (collection) for user {user_id}")
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
        journal_id = user_entity_resources.resources[0].resource_data["collection_id"]
        logger.info(
            f"Journal (collection) found for user {user_id}. journal_id: {journal_id}"
        )
        return journal_id, str(user_entity_resources.resources[0].id)
    elif create_if_not_exists:
        # Create new journal for user
        logger.info(f"Creating new journal (collection)")
        journal_id = create_journal_for_user(user_id)
        return journal_id, None

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

    ### Create journals (collections) and add subscriptions

    try:
        for user_id, subscriptions in users_subscriptions.items():
            user_id = str(user_id)

            journal_id = None
            resource_id_of_user_collection = None

            ### Journal can already exist in stages.json
            if "collection_id" in stages[user_id]:
                journal_id = stages[user_id]["collection_id"]
                if "subscription_resource_id" in stages[user_id]:
                    resource_id_of_user_collection = stages[user_id][
                        "subscription_resource_id"
                    ]
            else:
                ### look for collection in brood resources
                journal_id, resource_id_of_user_collection = find_user_journal(
                    user_id, create_if_not_exists=True
                )

            if journal_id is None:
                logger.info(
                    f"Journal (collection) not found or create for user {user_id}"
                )
                continue

            stages[user_id]["collection_id"] = journal_id

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
                        "collection_id": str(journal_id),
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

                logger.info(f"Add subscription to journal (collection): {journal_id}")

                entity = add_entity_subscription(
                    user_id=user_id,
                    journal_id=journal_id,
                    subscription_type_id=subscription_type_id,
                    address=address,
                    color=color,
                    label=label,
                    content={"abi": abi_body, "abi_hash": abi_hash} if abi else {},
                )
                stages[user_id]["processed_subscriptions"][
                    str(subscription["subscription_id"])
                ] = {"entity_id": str(entity.id), "dashboard_ids": []}

            # Add permissions to user

            if user_id != admin_user_id:
                # Add permissions to user

                if "permissions_granted" not in stages[user_id]:
                    try:
                        bc.update_journal_scopes(
                            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                            journal_id=journal_id,
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
                    f"User {user_id} == {admin_user_id} permissions not changed. Unexpected behavior!"
                )

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Failed to process user subscriptions: {str(e)}")
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

    ### Create journals and add subscriptions

    try:
        for user_id, _ in users_subscriptions.items():
            user_id = str(user_id)

            journal_id = None
            resource_id_of_user_collection = None

            ### Collection can already exist in stages.json
            if "collection_id" in stages[user_id]:
                journal_id = stages[user_id]["collection_id"]

                if "subscription_resource_id" in stages[user_id]:
                    resource_id_of_user_collection = stages[user_id][
                        "subscription_resource_id"
                    ]

            else:
                ### look for collection in brood resources
                journal_id, resource_id_of_user_collection = find_user_journal(
                    user_id, create_if_not_exists=False
                )

            if journal_id is None:
                logger.info(f"Collection not found or create for user {user_id}")
                continue

            ### Delete collection

            try:
                bc.delete_journal(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN, journal_id=journal_id
                )
                logger.info(f"Journal (collection) deleted {journal_id}")

            except Exception as e:
                logger.error(f"Failed to delete journal (collection): {str(e)}")

            ### Delete collection resource

            try:
                logger.info(
                    f"Journal (collection) resource id {resource_id_of_user_collection}"
                )
                bc.delete_resource(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    resource_id=resource_id_of_user_collection,
                )
                logger.info(
                    f"Journal (collection) resource deleted {resource_id_of_user_collection}"
                )

                # clear stages

                stages[user_id] = {}

            except Exception as e:
                logger.error(
                    f"Failed to delete journal (collection) resource: {str(e)}"
                )
                continue

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Failed to process user subscriptions: {str(e)}")


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

    ### Return all dashboards to old state

    logger.info(f"Amount of users: {len(dashboards_by_user)}")

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
                    logger.info("no subscription_settings")
                    continue

                if len(dashboard_data["subscription_settings"]) == 0:
                    logger.info("no subscription_settings")
                    continue

                dashboard_metadata = dashboard_data["subscription_settings"]

                for index, settings in enumerate(dashboard_metadata):
                    if "subscription_id" not in settings:
                        logger.info("no subscription_id")
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


def fix_duplicates_keys_in_entity_subscription():
    """
    Migration generate_entity_subscriptions_from_brood_resources
    create duplicates keys "secondary_fields" subscriptions secondary_fields
    "secondary_fields": {
                "secondary_fields": {
        ...
        }
    }
    That function will remove internal secondary_fields and flat all keys to one level upper
    """

    # get all entities from subscriptions

    subscriptions: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    # get journal ids from that resources

    collection_id_user_id_mapping = {}

    for subscription in subscriptions.resources:
        if "collection_id" in subscription.resource_data:
            if (
                subscription.resource_data["collection_id"]
                not in collection_id_user_id_mapping
            ):
                collection_id_user_id_mapping[
                    subscription.resource_data["collection_id"]
                ] = subscription.resource_data["user_id"]
            else:
                raise Exception(
                    f"Duplicate collection_id {subscription.resource_data['collection_id']} in subscriptions"
                )
    # go through all journals and fix entities.
    # Will creating one new entity with same data but without "type:subscription" in required_fields

    for journal_id, user_id in collection_id_user_id_mapping.items():
        # get journal entities
        journal_entities = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=journal_id,
            required_field=[f"type:subscription"],
            limit=1000,
            representation="entity",
        )

        logger.info(
            f"Amount of entities in user: {user_id} journal (collection) {journal_id}: {len(journal_entities.entities)}"
        )

        for entity in journal_entities.entities:
            # get entity data

            if entity.secondary_fields is None:
                continue

            secondary_fields = entity.secondary_fields

            if "secondary_fields" not in secondary_fields:
                continue

            secondary_fields = secondary_fields["secondary_fields"]

            # get entity type
            entity_type = None

            # extract required fields
            for entity_required_field in entity.required_fields:
                if "type" in entity_required_field:
                    entity_type = entity_required_field["type"]
            if entity_type != "subscription":
                continue

            # Create new entity with same data but without "type:subscription" in required_fields

            try:
                new_required_fields = [
                    entity_field
                    for entity_field in entity.required_fields
                    if "type" not in entity_field
                ]
                new_required_fields.append(
                    {"type": "copy_of_malformed_entity_20230213"}
                )
                new_required_fields.append({"entity_id": str(entity.id)})

                new_entity = bc.create_entity(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    journal_id=journal_id,
                    blockchain=entity.blockchain,
                    address=entity.address,
                    title=entity.title,
                    required_fields=new_required_fields,
                    secondary_fields=entity.secondary_fields,
                )
                logger.info(
                    f"Entity {new_entity.id} created successfully for journal (collection) {journal_id}"
                )

            except Exception as e:
                logger.error(
                    f"Failed to create entity {entity.id} for journal (collection) {journal_id}: {str(e)}, user_id: {user_id}"
                )
                continue

            # Update old entity without secondary_fields duplicate

            try:
                bc.update_entity(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    journal_id=journal_id,
                    entity_id=entity.id,
                    blockchain=entity.blockchain,
                    address=entity.address,
                    title=entity.title,
                    required_fields=entity.required_fields,
                    secondary_fields=secondary_fields,
                )
                logger.info(
                    f"Entity {entity.id} updated successfully for journal (collection) {journal_id}"
                )

            except Exception as e:
                logger.error(
                    f"Failed to update entity {entity.id} for journal (collection) {journal_id}: {str(e)}, user_id: {user_id}"
                )
