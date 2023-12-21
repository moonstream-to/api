import logging
import json
from enum import Enum
from typing import List, Optional, Literal

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException


from ..actions import get_all_entries_from_search, apply_moonworm_tasks
from ..settings import MOONSTREAM_ADMIN_ACCESS_TOKEN, MOONSTREAM_MOONWORM_TASKS_JOURNAL
from ..settings import bugout_client as bc
from .subscription_types import CANONICAL_SUBSCRIPTION_TYPES


logger = logging.getLogger(__name__)


class ActionType(Enum):
    DELETE = "delete"
    RESTART = "restart"
    MARK_AS_FINISHED = "mark_as_finished"
    VIEW = "view"


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


def restart_tasks(bc, token, journal_id, tasks):
    delete_entries_tags = []
    add_entries_tags = []
    for task in tasks:
        entry_id = task["entry_id"]
        # Find tags to delete
        tags_to_delete = [
            tag
            for tag in task["tags"]
            if tag.startswith("historical_crawl_status:") or tag.startswith("progress:")
        ]

        # Delete tags
        if tags_to_delete:
            delete_entries_tags.append({"entry_id": entry_id, "tags": tags_to_delete})

        # Add new tags
        tags_to_add = ["progress:0", "historical_crawl_status:pending"]
        add_entries_tags.append({"entry_id": entry_id, "tags": tags_to_add})

    print(delete_entries_tags)

    # Delete tags
    if delete_entries_tags:
        bc.delete_entries_tags(
            token=token, journal_id=journal_id, entries_tags=delete_entries_tags
        )

    # Add tags
    if add_entries_tags:
        bc.create_entries_tags(
            token=token, journal_id=journal_id, entries_tags=add_entries_tags
        )


def mark_tasks_as_finished(bc, token, journal_id, tasks):
    add_entries_tags = []
    for task in tasks:
        entry_id = task["entry_id"]
        # Add new tags
        tags_to_add = ["progress:100", "historical_crawl_status:finished"]
        add_entries_tags.append({"entry_id": entry_id, "tags": tags_to_add})

    # Add tags
    if add_entries_tags:
        bc.create_entries_tags(
            token=token, journal_id=journal_id, entries_tags=add_entries_tags
        )


def delete_tasks(bc, token, journal_id, tasks):
    for task in tasks:
        entry_id = task["entry_id"]
        # Delete the task
        bc.delete_entry(token, journal_id, entry_id)


def moonworm_tasks_manage_handler(args):
    print(
        f"Managing moonworm tasks with action: {args.action}, blockchain: {args.blockchain}, addresses: {args.addresses}, task type: {args.task_type}"
    )
    return manage_moonworm_tasks(
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        blockchain=args.blockchain,
        addresses=args.addresses,
        task_type=args.task_type,
        action=ActionType(args.action),
    )


def get_moonworm_tasks_by_filters(
    journal_id: str = MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    token: str = MOONSTREAM_ADMIN_ACCESS_TOKEN,
    blockchain: str = "ethereum",
    addresses: List[str] = [],
    task_type: Optional[Literal["event", "function"]] = None,
    task_names: Optional[List[str]] = None,
):
    """
    Return list of tags depends on query and tag
    """

    blockchain_to_subscription_type = {
        value.blockchain: key
        for key, value in CANONICAL_SUBSCRIPTION_TYPES.items()
        if "smartcontract" in key
    }

    if blockchain not in blockchain_to_subscription_type:
        logger.error(f"Unknown blockchain {blockchain}")
        return

    search_query = f"#subscription_type:{blockchain_to_subscription_type[blockchain]} #moonworm_task_pickedup:True"

    if addresses:
        search_query += " " + " ".join([f"#address:{address}" for address in addresses])

    if task_type:
        search_query += f" #type:{task_type}"

    if task_names:
        search_query += " " + " ".join([f"abi_name:{name}" for name in task_names])

    print(search_query)

    entries = get_all_entries_from_search(
        journal_id=journal_id,
        search_query=search_query,
        limit=100,
        token=token,
    )

    print(f"Found {len(entries)} moonworm tasks")

    tasks = []

    for entry in entries:
        historical_crawl_status = [
            tag.split(":")[-1]
            for tag in entry.tags
            if tag.startswith("historical_crawl_status:")
        ]

        address = [tag for tag in entry.tags if tag.startswith("address:")]

        progress = [tag for tag in entry.tags if tag.startswith("progress:")]

        abi_name = [tag for tag in entry.tags if tag.startswith("abi_name:")]

        moonworm_task_pickedup = [
            tag.split(":")[-1]
            for tag in entry.tags
            if tag.startswith("moonworm_task_pickedup:")
        ]

        historical_crawl_status = " ".join(historical_crawl_status)
        address = address[0].split(":")[1] if len(address) > 0 else "address not found"
        progress = (
            progress[0].split(":")[1] if len(progress) > 0 else "progress not found"
        )
        abi_name = (
            abi_name[0].split(":")[1] if len(abi_name) > 0 else "abi_name not found"
        )

        tasks.append(
            {
                "entry_id": entry.entry_url.split("/")[-1],
                "tags": entry.tags,
                "historical_crawl_status": historical_crawl_status,
                "address": address,
                "progress": progress,
                "abi_name": abi_name,
                "moonworm_task_pickedup": " ".join(moonworm_task_pickedup),
            }
        )

    return tasks


def get_moonworm_tasks_state(
    journal_id: str = MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    token: str = MOONSTREAM_ADMIN_ACCESS_TOKEN,
    blockchain: str = "ethereum",
):
    """
    Return list of tags depends on query and tag
    """

    blockchain_to_subscription_type = {
        value["blockchain"]: key
        for key, value in CANONICAL_SUBSCRIPTION_TYPES.items()
        if "smartcontract" in value
    }

    if blockchain not in blockchain_to_subscription_type:
        logger.error(f"Unknown blockchain {blockchain}")
        return

    entries = get_all_entries_from_search(
        journal_id=journal_id,
        search_query=f"#subscription_type:{blockchain_to_subscription_type[blockchain]} #moonworm_task_pickedup:True",
        limit=100,
        token=token,
    )

    print(f"Found {len(entries)} moonworm tasks")

    ### loop over tasks split by historical_crawl_status:in_progress and historical_crawl_status:finished and historical_crawl_status:pending

    tasks = {
        "in_progress": {},
        "finished": {},
        "pending": {},
    }

    for entry in entries:
        historical_crawl_status = [
            tag for tag in entry.tags if tag.startswith("historical_crawl_status:")
        ]

        address = [tag for tag in entry.tags if tag.startswith("address:")]

        progress = [tag for tag in entry.tags if tag.startswith("progress:")]

        abi_name = [tag for tag in entry.tags if tag.startswith("abi_name:")]

        if len(historical_crawl_status) == 0:
            logger.warn(
                f"Unable to find historical_crawl_status in task: {entry.entry_url.split()[-1]}"
            )
            continue

        historical_crawl_status = historical_crawl_status[0].split(":")[1]
        address = address[0].split(":")[1]
        progress = progress[0].split(":")[1]
        abi_name = abi_name[0].split(":")[1]

        if historical_crawl_status not in tasks:
            tasks[historical_crawl_status] = {}
        if address not in tasks[historical_crawl_status]:
            tasks[historical_crawl_status][address] = {}

        if abi_name not in tasks[historical_crawl_status][address]:
            tasks[historical_crawl_status][address][abi_name] = progress

    return tasks


def confirm_action(action, tasks):
    """Ask the user for confirmation before proceeding with the action."""
    print(f"You are about to {action} the following tasks:")
    tasks = sorted(tasks, key=lambda task: task["address"])
    for task in tasks:
        print(f"  {task['address']} {task['abi_name']} {task['progress']}%")

    confirmation = input(
        f"Do you want to proceed with {action} these tasks? (yes/no): "
    )
    return confirmation.lower() == "yes"


def view_tasks(tasks):
    """Display details of the tasks."""
    if not tasks:
        print("No tasks to display.")
        return

    tasks = sorted(tasks, key=lambda task: task["address"])
    for task in tasks:
        print(
            f"  {task['address']} {task['abi_name']} {task['progress']}% HC statuses:{task['historical_crawl_status']} moonworm:{task['moonworm_task_pickedup']}"
        )


def manage_moonworm_tasks(
    journal_id: str,
    token: str,
    blockchain: str,
    addresses: List[str],
    task_type: Optional[str],
    action: ActionType,
):
    """
    Manage moonworm tasks based on the provided parameters.

    :param journal_id: ID of the journal containing the tasks.
    :param token: Access token for authentication.
    :param blockchain: Type of blockchain (e.g., 'ethereum').
    :param addresses: List of contract addresses to filter tasks.
    :param task_type: Type of the task ('event' or 'function').
    :param action: Action to perform ('delete', 'restart', 'mark_as_finished').
    """

    # Get all tasks matching the provided filters
    filtered_tasks = get_moonworm_tasks_by_filters(
        journal_id=journal_id,
        token=token,
        blockchain=blockchain,
        addresses=addresses,
        task_type=task_type,
    )

    # Confirm action with the user
    if action == ActionType.VIEW:
        view_tasks(filtered_tasks)
    else:
        if confirm_action(action.value, filtered_tasks):
            if action == ActionType.DELETE:
                delete_tasks(bc, token, journal_id, filtered_tasks)
            elif action == ActionType.RESTART:
                restart_tasks(bc, token, journal_id, filtered_tasks)
            elif action == ActionType.MARK_AS_FINISHED:
                mark_tasks_as_finished(bc, token, journal_id, filtered_tasks)
            print(f"Action '{action.value}' completed on filtered tasks.")
        else:
            print("Action cancelled by the user.")

    return {
        "status": "success",
        "message": f"Action '{action.value}' was approved and executed.",
    }
