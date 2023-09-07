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
        search_query="type:subscription !#version:2.0",
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    entries_tags = []

    ## batch tasks

    for task_batch in [
        moonworm_tasks[i : i + batch_size]
        for i in range(0, len(moonworm_tasks), batch_size)
    ]:
        for task in task_batch:
            tags = ["#version:2.0"]

            ## get abi
            try:
                abi = json.loads(task.content)
            except Exception as e:
                logger.warn(f"Unable to parse abi from task: {task.id}")
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

            entries_tags.append(
                {
                    "entry_id": task.entry_url.split("/")[-1],  ## 😭
                    "tags": tags,
                }
            )

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
