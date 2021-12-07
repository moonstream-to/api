import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import logging

from moonworm.crawler.log_scanner import _fetch_events_chunk
from sqlalchemy.orm.session import Session
from web3 import Web3
from eth_typing.evm import ChecksumAddress

from ..settings import CRAWLER_LABEL

from db.moonstreamdb.models import Base

from ..blockchain import (
    get_block_model,
    get_label_model,
    connect,
)

from ..data import AvailableBlockchainType
from .crawler import save_labels

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EventCrawlJob:
    event_abi_hash: str
    event_abi: Dict[str, Any]
    contracts: List[ChecksumAddress]
    created_at: int


@dataclass
class Event:
    event_name: str
    args: Dict[str, Any]
    address: str
    block_number: int
    block_timestamp: int
    transaction_hash: str
    log_index: int


def _event_to_label(blockchain_type: AvailableBlockchainType, event: Event) -> Base:
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)
    label = label_model(
        label=CRAWLER_LABEL,
        label_data={
            "type": "event",
            "name": event.event_name,
            "args": event.args,
        },
        address=event.address,
        block_number=event.block_number,
        block_timestamp=event.block_timestamp,
        transaction_hash=event.transaction_hash,
        log_index=event.log_index,
    )
    return label


def _get_block_timestamp_from_web3(web3: Web3, block_number: int) -> int:
    """
    Gets the timestamp of a block from the blockchain.
    will raise an exception if the block is not found.
    """
    return web3.eth.getBlock(block_number).timestamp


# I am using blocks_cache as the argument, to reuse this function in tx_call crawler
# and support one cashe for both tx_call and event_crawler
def get_block_timestamp(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    block_number: int,
    blocks_cache: Dict[int, int],
    max_blocks_batch: int = 30,
) -> int:
    """
    Get the timestamp of a block.
    First tries to get the block from the cache,
    then tries to get the block from the db,
    then tries to get it from the blockchain.

    After the call cache is updated.
    If the cache grows too large, it is cleared.

    :param block_number: The block number.
    :param max_blocks_batch: The maximum number of blocks to fetch in a single batch from db query.
    :param blocks_cache: The cache of blocks.
    :return: The timestamp of the block.
    """
    assert max_blocks_batch > 0

    if block_number in blocks_cache:
        return blocks_cache[block_number]

    block_model = get_block_model(blockchain_type)

    blocks = (
        db_session.query(block_model)
        .filter_by(block_model.block_number >= block_number)
        .filter_by(block_model.block_number <= block_number + max_blocks_batch - 1)
        .order_by(block_model.block_number.asc())
        .all()
    )

    target_block_timestamp: Optional[int] = None
    if blocks and blocks[0].block_number == block_number:
        target_block_timestamp = blocks[0].timestamp

    if target_block_timestamp is None:
        target_block_timestamp = _get_block_timestamp_from_web3(
            connect(blockchain_type), block_number
        )

    if len(blocks_cache) > max_blocks_batch * 2:
        blocks_cache.clear()

    blocks_cache[block_number] = target_block_timestamp
    for block in blocks:
        blocks_cache[block.block_number] = block.timestamp

    return target_block_timestamp


def _crawl_events(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    web3: Web3,
    jobs: List[EventCrawlJob],
    from_block: int,
    to_block: int,
    blocks_cache: Dict[int, int] = {},
    db_block_query_batch=10,
) -> List[Event]:
    all_events = []
    for job in jobs:
        raw_events = _fetch_events_chunk(
            web3,
            job.event_abi,
            from_block,
            to_block,
            job.contracts,
            on_decode_error=lambda e: print(
                f"Error decoding event: {e}"
            ),  # TODO report via humbug
        )
        for raw_event in raw_events:
            raw_event["blockTimestamp"] = get_block_timestamp(
                db_session,
                blockchain_type,
                raw_event["blockNumber"],
                blocks_cache,
                db_block_query_batch,
            )
            event = Event(
                event_name=raw_event["event"],
                args=raw_event["args"],
                address=raw_event["address"],
                block_number=raw_event["blockNumber"],
                block_timestamp=raw_event["blockTimestamp"],
                transaction_hash=raw_event["transactionHash"],
                log_index=raw_event["logIndex"],
            )
            all_events.append(event)

    return all_events


def continious_event_crawler(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    web3: Web3,
    initial_jobs: List[EventCrawlJob],
    start_block: int,
    max_blocks_batch: int = 100,
    min_blocks_batch: int = 10,
    confirmations: int = 60,
    min_sleep_time: float = 0.1,
):

    assert min_blocks_batch < max_blocks_batch

    crawl_start_time = int(time.time())
    blocks_cache: Dict[int, int] = {}

    while True:
        # query db  with limit 1, to avoid session closing
        db_session.execute("SELECT 1")
        time.sleep(min_sleep_time)

        end_block = min(
            web3.eth.blockNumber - confirmations,
            start_block + max_blocks_batch,
        )

        if start_block + min_blocks_batch > end_block:
            min_sleep_time *= 2
            continue

        min_sleep_time /= 2

        all_events = _crawl_events(
            db_session=db_session,
            blockchain_type=blockchain_type,
            web3=web3,
            jobs=initial_jobs,
            from_block=start_block,
            to_block=end_block,
            blocks_cache=blocks_cache,
            db_block_query_batch=min_blocks_batch * 2,
        )

        # TODO ask for new jobs
