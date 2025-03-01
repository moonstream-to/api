import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


from moonstreamtypes.blockchain import (
    AvailableBlockchainType,
    get_label_model,
    get_block_model,
)
from moonworm.crawler.log_scanner import (  # type: ignore
    _crawl_events as moonworm_autoscale_crawl_events,
)
from moonworm.crawler.log_scanner import _fetch_events_chunk  # type: ignore
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_
from web3 import Web3

from .crawler import EventCrawlJob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Event:
    event_name: str
    args: Dict[str, Any]
    address: str
    block_hash: str
    block_number: int
    block_timestamp: int
    transaction_hash: str
    log_index: int
    block_hash: Optional[str] = None


def _get_block_timestamp_from_web3(
    web3: Web3,
    block_number: int,
) -> int:
    """
    Gets the timestamp of a block from the blockchain.
    will raise an exception if the block is not found.
    """
    return web3.eth.getBlock(block_number).timestamp


# I am using blocks_cache as the argument, to reuse this function in tx_call crawler
# and support one cashe for both tx_call and event_crawler
def get_block_timestamp(
    db_session: Session,
    web3: Web3,
    blockchain_type: AvailableBlockchainType,
    block_number: int,
    blocks_cache: Dict[int, int],
    max_blocks_batch: int = 30,
    version: int = 2,
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

    if version != 2:
        if block_number in blocks_cache:
            return blocks_cache[block_number]
        target_block_timestamp = _get_block_timestamp_from_web3(web3, block_number)
        blocks_cache[block_number] = target_block_timestamp
        return target_block_timestamp

    assert max_blocks_batch > 0

    if block_number in blocks_cache:
        return blocks_cache[block_number]

    block_model = get_block_model(blockchain_type)

    blocks = (
        db_session.query(
            block_model.block_number, block_model.timestamp, block_model.hash
        )
        .filter(
            and_(
                block_model.block_number >= block_number - max_blocks_batch - 1,
                block_model.block_number <= block_number + max_blocks_batch + 1,
            )
        )
        .order_by(block_model.block_number.asc())
        .all()
    )

    target_block_timestamp: Optional[int] = None
    if blocks and blocks[0].block_number == block_number:
        target_block_timestamp = blocks[0].timestamp

    if target_block_timestamp is None:
        target_block_timestamp = _get_block_timestamp_from_web3(web3, block_number)

    if len(blocks_cache) > (max_blocks_batch * 3 + 2):
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
    version: int = 2,
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
                web3,
                blockchain_type,
                raw_event["blockNumber"],
                blocks_cache,
                db_block_query_batch,
                version,
            )
            event = Event(
                event_name=raw_event["event"],
                args=raw_event["args"],
                address=raw_event["address"],
                block_hash=raw_event["blockHash"],
                block_number=raw_event["blockNumber"],
                block_timestamp=raw_event["blockTimestamp"],
                transaction_hash=raw_event["transactionHash"],
                log_index=raw_event["logIndex"],
                block_hash=raw_event.get("blockHash"),
            )
            all_events.append(event)

    return all_events


def _autoscale_crawl_events(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    web3: Web3,
    jobs: List[EventCrawlJob],
    from_block: int,
    to_block: int,
    blocks_cache: Dict[int, int] = {},
    batch_size: int = 1000,
    db_block_query_batch=10,
    version: int = 2,
) -> Tuple[List[Event], int]:
    """
    Crawl events with auto regulated batch_size.
    """
    all_events = []
    for job in jobs:
        try:
            raw_events, batch_size = moonworm_autoscale_crawl_events(
                web3=web3,
                event_abi=job.event_abi,
                from_block=from_block,
                to_block=to_block,
                batch_size=batch_size,
                contract_address=job.contracts,
                max_blocks_batch=5000,
            )
        except Exception as e:
            logger.error(f"Error while fetching events: {e}")
            raise e
        for raw_event in raw_events:
            raw_event["blockTimestamp"] = get_block_timestamp(
                db_session,
                web3,
                blockchain_type,
                raw_event["blockNumber"],
                blocks_cache,
                db_block_query_batch,
                version,
            )
            event = Event(
                event_name=raw_event["event"],
                args=raw_event["args"],
                address=raw_event["address"],
                block_hash=raw_event["blockHash"],
                block_number=raw_event["blockNumber"],
                block_timestamp=raw_event["blockTimestamp"],
                transaction_hash=raw_event["transactionHash"],
                log_index=raw_event["logIndex"],
                block_hash=raw_event.get("blockHash"),
            )
            all_events.append(event)

    return all_events, batch_size
