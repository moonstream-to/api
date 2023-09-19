"""
Add selectors to all moonworm tasks.
"""
import logging
import json


from bugout.exceptions import BugoutResponseException
from web3 import Web3

from ...settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
)
from ...settings import bugout_client as bc
from ...actions import get_all_entries_from_search

logger = logging.getLogger(__name__)


def fill_missing_selectors_in_moonworm_tasks() -> None:
    """
    Add selectors to all moonworm tasks.
    """

    batch_size = 100

    moonworm_tasks = get_all_entries_from_search(
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        search_query="#task_type:moonworm !#version:2.0",
        limit=batch_size,
        content=True,
    )

    logger.info(f"Found {len(moonworm_tasks)} moonworm tasks versions 1.0")

    entries_tags = []

    ## batch tasks

    for task_batch in [
        moonworm_tasks[i : i + batch_size]
        for i in range(0, len(moonworm_tasks), batch_size)
    ]:
        count = 0
        for task in task_batch:
            tags = ["version:2.0"]

            ## get abi
            try:
                abi = json.loads(task.content)
            except Exception as e:
                logger.warn(
                    f"Unable to parse abi from task: {task.entry_url.split()[-1]}: {e}"
                )
                raise e
                continue

            if "name" not in abi:
                logger.warn(
                    f"Unable to find abi name in task: {task.entry_url.split()[-1]}"
                )
                continue

            if not any([tag.startswith("abi_selector:") for tag in task.tags]):
                ## generate selector

                abi_selector = Web3.keccak(
                    text=abi["name"]
                    + "("
                    + ",".join(map(lambda x: x["type"], abi["inputs"]))
                    + ")"
                )[:4].hex()

                tags.append(f"abi_selector:{abi_selector}")

                count += 1

            entries_tags.append(
                {
                    "entry_id": task.entry_url.split("/")[-1],  ## 😭
                    "tags": tags,
                }
            )

        logger.info(f"Found {count} missing selectors in batch {len(task_batch)} tasks")

        ## update entries

        try:
            bc.create_entries_tags(
                journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                entries_tags=entries_tags,
                timeout=15,
            )
        except BugoutResponseException as e:
            logger.error(f"Unable to update entries tags: {e}")
            continue


def deduplicate_moonworm_task_by_selector():
    """
    Find moonworm tasks with same selector and remove old versions
    """

    moonworm_tasks = get_all_entries_from_search(
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        search_query="#task_type:moonworm #version:2.0",
        limit=100,
        content=False,
    )

    logger.info(f"Found {len(moonworm_tasks)} moonworm tasks versions 2.0")

    ## loop over tasks

    selectors = {}

    for task in moonworm_tasks:
        tags = task.tags

        ## get selector
        selector = [tag for tag in tags if tag.startswith("abi_selector:")]

        if len(selector) == 0:
            logger.warn(
                f"Unable to find selector in task: {task.entry_url.split()[-1]}"
            )
            continue

        selector = selector[0]

        if selector not in selectors:
            selectors[selector] = {"entries": {}}

        selectors[selector]["entries"][task.entry_url.split("/")[-1]] = task.created_at

    logger.info(f"Found {len(selectors)} selectors")

    for selector, tasks_dict in selectors.items():
        if len(tasks_dict["entries"]) == 1:
            continue

        ## find latest task

        latest_task_id = max(
            tasks_dict["entries"], key=lambda key: tasks_dict["entries"][key]
        )

        ## remove all tasks except latest

        logger.info(
            f"Found {len(tasks_dict['entries'])} tasks with selector {selector}"
        )

        for task_id in tasks_dict["entries"]:
            if task_id == latest_task_id:
                continue

            try:
                bc.delete_entry(
                    journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
                    entry_id=task_id,
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                )
            except BugoutResponseException as e:
                logger.error(f"Unable to delete entry: {e}")
                continue

            logger.info(f"Deleted entry: {task_id}")
