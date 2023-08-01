import json
import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, cast, Union, Tuple
from uuid import UUID

from bugout.data import BugoutSearchResult, BugoutJournalEntries
from eth_typing.evm import ChecksumAddress
from moonstreamdb.blockchain import AvailableBlockchainType
from web3.main import Web3
from moonworm.deployment import find_deployment_block  # type: ignore

from ..blockchain import connect
from ..reporter import reporter
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    bugout_client,
    HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES,
    HISTORICAL_CRAWLER_STATUSES,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubscriptionTypes(Enum):
    POLYGON_BLOCKCHAIN = "polygon_smartcontract"
    ETHEREUM_BLOCKCHAIN = "ethereum_smartcontract"
    MUMBAI_BLOCKCHAIN = "mumbai_smartcontract"
    XDAI_BLOCKCHAIN = "xdai_smartcontract"
    WYRM_BLOCKCHAIN = "wyrm_smartcontract"
    ZKSYNC_ERA_TESTNET_BLOCKCHAIN = "zksync_era_testnet_smartcontract"


def abi_input_signature(input_abi: Dict[str, Any]) -> str:
    """
    Stringifies a function ABI input object according to the ABI specification:
    https://docs.soliditylang.org/en/v0.5.3/abi-spec.html
    """
    input_type = input_abi["type"]
    if input_type.startswith("tuple"):
        component_types = [
            abi_input_signature(component) for component in input_abi["components"]
        ]
        input_type = f"({','.join(component_types)}){input_type[len('tuple'):]}"
    return input_type


def abi_function_signature(function_abi: Dict[str, Any]) -> str:
    """
    Stringifies a function ABI according to the ABI specification:
    https://docs.soliditylang.org/en/v0.5.3/abi-spec.html
    """
    function_name = function_abi["name"]
    function_arg_types = [
        abi_input_signature(input_item) for input_item in function_abi["inputs"]
    ]
    function_signature = f"{function_name}({','.join(function_arg_types)})"
    return function_signature


def encode_function_signature(function_abi: Dict[str, Any]) -> Optional[str]:
    """
    Encodes the given function (from ABI) with arguments arg_1, ..., arg_n into its 4 byte signature
    by calculating:
    keccak256("<function_name>(<arg_1_type>,...,<arg_n_type>")

    If function_abi is not actually a function ABI (detected by checking if function_abi["type"] == "function),
    returns None.
    """
    if function_abi["type"] != "function":
        return None
    function_signature = abi_function_signature(function_abi)
    encoded_signature = Web3.keccak(text=function_signature)[:4]
    return encoded_signature.hex()


def _generate_reporter_callback(
    crawler_type: str, blockchain_type: AvailableBlockchainType
) -> Callable[[Exception], None]:
    def reporter_callback(error: Exception) -> None:
        reporter.error_report(
            error,
            [
                "moonworm",
                "crawler",
                "decode_error",
                crawler_type,
                blockchain_type.value,
            ],
        )

    return reporter_callback


def _retry_connect_web3(
    blockchain_type: AvailableBlockchainType,
    retry_count: int = 10,
    sleep_time: float = 5,
    access_id: Optional[UUID] = None,
) -> Web3:
    """
    Retry connecting to the blockchain.
    """
    while retry_count > 0:
        retry_count -= 1
        try:
            web3 = connect(blockchain_type, access_id=access_id)
            web3.eth.block_number
            logger.info(f"Connected to {blockchain_type}")
            return web3
        except Exception as e:
            if retry_count == 0:
                error = e
                break
            logger.error(f"Failed to connect to {blockchain_type} blockchain: {e}")
            logger.info(f"Retrying in {sleep_time} seconds")
            time.sleep(sleep_time)
    raise Exception(
        f"Failed to connect to {blockchain_type} blockchain after {retry_count} retries: {error}"
    )


def blockchain_type_to_subscription_type(
    blockchain_type: AvailableBlockchainType,
) -> SubscriptionTypes:
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        return SubscriptionTypes.ETHEREUM_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        return SubscriptionTypes.POLYGON_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        return SubscriptionTypes.MUMBAI_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.XDAI:
        return SubscriptionTypes.XDAI_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.WYRM:
        return SubscriptionTypes.WYRM_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
        return SubscriptionTypes.ZKSYNC_ERA_TESTNET_BLOCKCHAIN
    else:
        raise ValueError(f"Unknown blockchain type: {blockchain_type}")


@dataclass
class EventCrawlJob:
    event_abi_hash: str
    event_abi: Dict[str, Any]
    contracts: List[ChecksumAddress]
    address_entries: Dict[ChecksumAddress, Dict[UUID, List[str]]]
    created_at: int


@dataclass
class FunctionCallCrawlJob:
    contract_abi: List[Dict[str, Any]]
    contract_address: ChecksumAddress
    entries_tags: Dict[UUID, List[str]]
    created_at: int


def get_crawl_job_entries(
    subscription_type: SubscriptionTypes,
    crawler_type: str,
    journal_id: str = MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    created_at_filter: Optional[int] = None,
    limit: int = 200,
    extend_tags: Optional[List[str]] = None,
) -> List[BugoutSearchResult]:
    """
    Get all event ABIs from bugout journal
    where tags are:
    - #crawler_type:crawler_type (either event or function)
    - #status:active
    - #subscription_type:subscription_type (either polygon_blockchain or ethereum_blockchain)

    """
    query = f"#status:active #type:{crawler_type} #subscription_type:{subscription_type.value}"

    if extend_tags is not None:
        for tag in extend_tags:
            query += f" {tag.rstrip()}"

    if created_at_filter is not None:
        # Filtering by created_at
        # Filtering not by strictly greater than
        # because theoretically we can miss some jobs
        #       (in the last query bugout didn't return all of by last created_at)
        # On the other hand, we may have multiple same jobs that will be filtered out
        #
        query += f" created_at:>={created_at_filter}"

    current_offset = 0
    entries: List[BugoutSearchResult] = []
    while True:
        search_result = bugout_client.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=journal_id,
            query=query,
            offset=current_offset,
            limit=limit,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        search_results = cast(List[BugoutSearchResult], search_result.results)
        entries.extend(search_results)

        # if len(entries) >= search_result.total_results:
        if len(search_results) == 0:
            break
        current_offset += limit
    return entries


def find_all_deployed_blocks(
    web3: Web3, addresses_set: List[ChecksumAddress]
) -> Dict[ChecksumAddress, int]:
    """
    find all deployed blocks for given addresses
    """

    all_deployed_blocks = {}
    for address in addresses_set:
        try:
            code = web3.eth.getCode(address)
            if code != "0x":
                block = find_deployment_block(
                    web3_client=web3,
                    contract_address=address,
                    web3_interval=0.5,
                )
                if block is not None:
                    all_deployed_blocks[address] = block
                if block is None:
                    logger.error(f"Failed to get deployment block for {address}")
        except Exception as e:
            logger.error(f"Failed to get code for {address}: {e}")
    return all_deployed_blocks


def _get_tag(entry: BugoutSearchResult, tag: str) -> str:
    for entry_tag in entry.tags:
        if entry_tag.startswith(tag):
            return entry_tag.split(":")[1]
    raise ValueError(f"Tag {tag} not found in {entry}")


def make_event_crawl_jobs(entries: List[BugoutSearchResult]) -> List[EventCrawlJob]:
    """
    Create EventCrawlJob objects from bugout entries.
    """

    crawl_job_by_hash: Dict[str, EventCrawlJob] = {}

    for entry in entries:
        abi_hash = _get_tag(entry, "abi_method_hash")
        contract_address = Web3().toChecksumAddress(_get_tag(entry, "address"))

        entry_id = UUID(entry.entry_url.split("/")[-1])  # crying emoji

        existing_crawl_job = crawl_job_by_hash.get(abi_hash)
        if existing_crawl_job is not None:
            if contract_address not in existing_crawl_job.contracts:
                existing_crawl_job.contracts.append(contract_address)
                existing_crawl_job.address_entries[contract_address] = {
                    entry_id: entry.tags
                }

        else:
            abi = cast(str, entry.content)
            new_crawl_job = EventCrawlJob(
                event_abi_hash=abi_hash,
                event_abi=json.loads(abi),
                contracts=[contract_address],
                address_entries={contract_address: {entry_id: entry.tags}},
                created_at=int(datetime.fromisoformat(entry.created_at).timestamp()),
            )
            crawl_job_by_hash[abi_hash] = new_crawl_job

    return [crawl_job for crawl_job in crawl_job_by_hash.values()]


def make_function_call_crawl_jobs(
    entries: List[BugoutSearchResult],
) -> List[FunctionCallCrawlJob]:
    """
    Create FunctionCallCrawlJob objects from bugout entries.
    """

    crawl_job_by_address: Dict[str, FunctionCallCrawlJob] = {}
    method_signature_by_address: Dict[str, List[str]] = {}

    for entry in entries:
        entry_id = UUID(entry.entry_url.split("/")[-1])  # crying emoji
        contract_address = Web3().toChecksumAddress(_get_tag(entry, "address"))
        abi = json.loads(cast(str, entry.content))
        method_signature = encode_function_signature(abi)
        if method_signature is None:
            raise ValueError(f"{abi} is not a function ABI")

        if contract_address not in crawl_job_by_address:
            crawl_job_by_address[contract_address] = FunctionCallCrawlJob(
                contract_abi=[abi],
                contract_address=contract_address,
                entries_tags={entry_id: entry.tags},
                created_at=int(datetime.fromisoformat(entry.created_at).timestamp()),
            )
            method_signature_by_address[contract_address] = [method_signature]

        else:
            if method_signature not in method_signature_by_address[contract_address]:
                crawl_job_by_address[contract_address].contract_abi.append(abi)
                method_signature_by_address[contract_address].append(method_signature)
                crawl_job_by_address[contract_address].entries_tags[
                    entry_id
                ] = entry.tags

    return [crawl_job for crawl_job in crawl_job_by_address.values()]


def merge_event_crawl_jobs(
    old_crawl_jobs: List[EventCrawlJob], new_event_crawl_jobs: List[EventCrawlJob]
) -> List[EventCrawlJob]:
    """
    Merge new event crawl jobs with old ones.
    If there is a new event crawl job with the same event_abi_hash
    then we will merge the contracts to one job.
    Othervise new job will be created

    Important:
        old_crawl_jobs will be modified
    Returns:
        Merged list of event crawl jobs
    """
    for new_crawl_job in new_event_crawl_jobs:
        for old_crawl_job in old_crawl_jobs:
            if new_crawl_job.event_abi_hash == old_crawl_job.event_abi_hash:
                old_crawl_job.contracts.extend(
                    [
                        contract
                        for contract in new_crawl_job.contracts
                        if contract not in old_crawl_job.contracts
                    ]
                )

                for contract_address, entries in new_crawl_job.address_entries.items():
                    if contract_address in old_crawl_job.address_entries:
                        old_crawl_job.address_entries[contract_address].update(entries)
                    else:
                        old_crawl_job.address_entries[contract_address] = entries
                break
        else:
            old_crawl_jobs.append(new_crawl_job)
    return old_crawl_jobs


def merge_function_call_crawl_jobs(
    old_crawl_jobs: List[FunctionCallCrawlJob],
    new_function_call_crawl_jobs: List[FunctionCallCrawlJob],
) -> List[FunctionCallCrawlJob]:
    """
    Merge new function call crawl jobs with old ones.
    If there is a new function call crawl job with the same contract_address
    then we will merge the contracts to one job.
    Othervise new job will be created

    Important:
        old_crawl_jobs will be modified
    Returns:
        Merged list of function call crawl jobs

    """
    for new_crawl_job in new_function_call_crawl_jobs:
        for old_crawl_job in old_crawl_jobs:
            if new_crawl_job.contract_address == old_crawl_job.contract_address:
                old_selectors = [
                    encode_function_signature(function_abi)
                    for function_abi in old_crawl_job.contract_abi
                ]
                old_crawl_job.contract_abi.extend(
                    [
                        function_abi
                        for function_abi in new_crawl_job.contract_abi
                        if encode_function_signature(function_abi) not in old_selectors
                    ]
                )
                break
        else:
            old_crawl_jobs.append(new_crawl_job)
    return old_crawl_jobs


def _get_heartbeat_entry_id(
    crawler_type: str, blockchain_type: AvailableBlockchainType
) -> str:
    entries = bugout_client.search(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        query=f"#{crawler_type} #heartbeat #{blockchain_type.value} !#dead",
        limit=1,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    search_results = cast(List[BugoutSearchResult], entries.results)
    if search_results:
        return search_results[0].entry_url.split("/")[-1]
    else:
        logger.info(f"No {crawler_type} heartbeat entry found, creating one")
        entry = bugout_client.create_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
            title=f"{crawler_type} Heartbeat - {blockchain_type.value}",
            tags=[crawler_type, "heartbeat", blockchain_type.value],
            content="",
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        return str(entry.id)


def heartbeat(
    crawler_type: str,
    blockchain_type: AvailableBlockchainType,
    crawler_status: Dict[str, Any],
    is_dead: bool = False,
) -> None:
    """
    Periodically crawler will update the status in bugout entry:
    - Started at timestamp
    - Started at block number
    - Status: Running/Dead
    - Last crawled block number
    - Number of current jobs
    - Time taken to crawl last crawl_step and speed per block

    and other information later will be added.
    """
    heartbeat_entry_id = _get_heartbeat_entry_id(crawler_type, blockchain_type)
    bugout_client.update_entry_content(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        entry_id=heartbeat_entry_id,
        title=f"{crawler_type} Heartbeat - {blockchain_type.value}. Status: {crawler_status['status']} - {crawler_status['current_time']}",
        content=f"{json.dumps(crawler_status, indent=2)}",
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    if is_dead:
        bugout_client.update_tags(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
            entry_id=heartbeat_entry_id,
            tags=[crawler_type, "heartbeat", blockchain_type.value, "dead"],
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )


def bugout_state_update(
    entries_tags_add: List[Dict[str, Any]],
    entries_tags_delete: List[Dict[str, Any]],
) -> BugoutJournalEntries:
    """
    Run update of entries tags in bugout
    First add tags to entries
    Second delete tags from entries
    With condition that if first step failed, second step will not be executed
    """

    new_entreis_state = BugoutJournalEntries(entries=[])

    if len(entries_tags_add) > 0:
        try:
            new_entreis_state = bugout_client.create_entries_tags(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
                entries_tags=entries_tags_add,
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
        except Exception as e:
            logger.error(f"Failed to add tags to entries: {e}")

    if len(entries_tags_delete) > 0 and (
        len(entries_tags_add) < 0 or len(new_entreis_state.entries) > 0
    ):
        try:
            new_entreis_state = bugout_client.delete_entries_tags(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
                entries_tags=entries_tags_delete,
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
        except Exception as e:
            logger.error(f"Failed to delete tags from entries: {e}")

    return new_entreis_state


def moonworm_crawler_update_job_as_pickedup(
    event_crawl_jobs: List[EventCrawlJob],
    function_call_crawl_jobs: List[FunctionCallCrawlJob],
) -> Tuple[List[EventCrawlJob], List[FunctionCallCrawlJob]]:
    """
    Apply jobs of moonworm as taked to process
    """

    if len(event_crawl_jobs) > 0:
        event_crawl_jobs = update_job_state_with_filters(  # type: ignore
            events=event_crawl_jobs,
            address_filter=[],
            required_tags=[
                f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['historical_crawl_status']}:{HISTORICAL_CRAWLER_STATUSES['pending']}",
                f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['moonworm_status']}:False",
            ],
            tags_to_add=["moonworm_task_pickedup:True"],
            tags_to_delete=["moonworm_task_pickedup:False"],
        )

    if len(function_call_crawl_jobs) > 0:
        function_call_crawl_jobs = update_job_state_with_filters(  # type: ignore
            events=function_call_crawl_jobs,
            address_filter=[],
            required_tags=[
                f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['historical_crawl_status']}:{HISTORICAL_CRAWLER_STATUSES['pending']}",
                f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['moonworm_status']}:False",
            ],
            tags_to_add=[
                f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['moonworm_status']}:True"
            ],
            tags_to_delete=[
                f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['moonworm_status']}:False"
            ],
        )

    return event_crawl_jobs, function_call_crawl_jobs


def update_job_tags(
    events: Union[List[EventCrawlJob], List[FunctionCallCrawlJob]],
    new_entreis_state: BugoutJournalEntries,
):
    """
    Update tags of the jobs in job object
    """
    entry_tags_by_id = {entry.id: entry.tags for entry in new_entreis_state.entries}

    for event in events:
        if isinstance(event, EventCrawlJob):
            for contract_address, entries_ids in event.address_entries.items():
                for entry_id in entries_ids.keys():
                    if entry_id in entry_tags_by_id:
                        event.address_entries[contract_address][
                            entry_id
                        ] = entry_tags_by_id[entry_id]

        if isinstance(event, FunctionCallCrawlJob):
            for entry_id in event.entries_tags.keys():
                if entry_id in entry_tags_by_id:
                    event.entries_tags[entry_id] = entry_tags_by_id[entry_id]

    return events


def update_job_state_with_filters(
    events: Union[List[EventCrawlJob], List[FunctionCallCrawlJob]],
    address_filter: List[ChecksumAddress],
    required_tags: List[str],
    tags_to_add: List[str] = [],
    tags_to_delete: List[str] = [],
) -> Union[List[EventCrawlJob], List[FunctionCallCrawlJob]]:
    """
    Function that updates the state of the job in bugout.
    """

    entries_ids_to_update: List[UUID] = []

    ### TODO: refactor this function

    if len(tags_to_add) == 0 and len(tags_to_delete) == 0:
        return events

    for event in events:
        # events
        if isinstance(event, EventCrawlJob):
            for contract_address, entries_ids in event.address_entries.items():
                if address_filter and contract_address not in address_filter:
                    continue
                for entry_id, tags in entries_ids.items():
                    if set(required_tags).issubset(set(tags)):
                        entries_ids_to_update.append(entry_id)

        # functions
        if isinstance(event, FunctionCallCrawlJob):
            if address_filter and event.contract_address not in address_filter:
                continue
            for entry_id, tags in event.entries_tags.items():
                if set(required_tags).issubset(set(tags)):
                    entries_ids_to_update.append(entry_id)

    if len(entries_ids_to_update) == 0:
        return events

    new_entries_state = bugout_state_update(
        entries_tags_add=[
            {"entry_id": entry_id, "tags": tags_to_add}
            for entry_id in entries_ids_to_update
        ],
        entries_tags_delete=[
            {"entry_id": entry_id, "tags": tags_to_delete}
            for entry_id in entries_ids_to_update
        ],
    )

    events = update_job_tags(events, new_entries_state)

    return events


def update_entries_status_and_progress(
    events: Union[List[EventCrawlJob], List[FunctionCallCrawlJob]],
    progess_map: Dict[ChecksumAddress, float],
) -> Union[List[EventCrawlJob], List[FunctionCallCrawlJob]]:
    """
    Update entries status and progress in mooncrawl bugout journal
    """

    entries_tags_delete: List[Dict[str, Any]] = []

    entries_tags_add: List[Dict[str, Any]] = []

    for event in events:
        if isinstance(event, EventCrawlJob):
            for contract_address, entries_ids in event.address_entries.items():
                progress = round(progess_map.get(contract_address, 0), 4) * 100

                (
                    entries_tags_delete,
                    entries_tags_add,
                ) = add_progress_to_tags(
                    entries=entries_ids,
                    contract_progress=progress,
                    entries_tags_delete=entries_tags_delete,
                    entries_tags_add=entries_tags_add,
                )

        if isinstance(event, FunctionCallCrawlJob):
            progress = round(progess_map.get(event.contract_address, 0), 4) * 100

            (
                entries_tags_delete,
                entries_tags_add,
            ) = add_progress_to_tags(
                entries=event.entries_tags,
                contract_progress=progress,
                entries_tags_delete=entries_tags_delete,
                entries_tags_add=entries_tags_add,
            )

    new_entries_state = bugout_state_update(
        entries_tags_add=entries_tags_add,
        entries_tags_delete=entries_tags_delete,
    )

    events = update_job_tags(events, new_entries_state)

    return events


def add_progress_to_tags(
    entries: Dict[UUID, List[str]],
    contract_progress: float,
    entries_tags_delete: List[Dict[str, Any]],
    entries_tags_add: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Calculate progress and add finished tag if progress is 100
    """

    new_progress = f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['progress_status']}:{contract_progress}"

    for entry_id, tags in entries.items():
        # progress

        if (
            f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['historical_crawl_status']}:{HISTORICAL_CRAWLER_STATUSES['finished']}"
            in tags
        ):
            continue

        if new_progress not in tags:
            entries_tags_delete.append(
                {
                    "entry_id": entry_id,
                    "tags": [
                        tag
                        for tag in tags
                        if tag.startswith(
                            f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['progress_status']}"
                        )
                    ],
                }
            )

            entries_tags_add.append(
                {
                    "entry_id": entry_id,
                    "tags": [new_progress],
                }
            )

        if contract_progress >= 100:
            entries_tags_add.append(
                {
                    "entry_id": entry_id,
                    "tags": [
                        f"{HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES['historical_crawl_status']}:{HISTORICAL_CRAWLER_STATUSES['finished']}"
                    ],
                }
            )

    return entries_tags_delete, entries_tags_add
