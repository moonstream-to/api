import logging
import time
from typing import Dict, List, Optional
from uuid import UUID

from eth_typing.evm import ChecksumAddress
from moonstreamdb.blockchain import AvailableBlockchainType
from moonstreamdb.networks import Network  # type: ignore
from moonworm.crawler.moonstream_ethereum_state_provider import (  # type: ignore
    MoonstreamEthereumStateProvider,
)
from sqlalchemy.orm.session import Session
from web3 import Web3

from .crawler import (
    EventCrawlJob,
    FunctionCallCrawlJob,
    _retry_connect_web3,
    update_entries_status_and_progress,
)
from .db import add_events_to_session, add_function_calls_to_session, commit_session
from .event_crawler import _autoscale_crawl_events, _crawl_events
from .function_call_crawler import _crawl_functions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def historical_crawler(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    web3: Optional[Web3],
    event_crawl_jobs: List[EventCrawlJob],
    function_call_crawl_jobs: List[FunctionCallCrawlJob],
    start_block: int,
    end_block: int,
    max_blocks_batch: int = 100,
    min_sleep_time: float = 0.1,
    web3_uri: Optional[str] = None,
    addresses_deployment_blocks: Optional[Dict[ChecksumAddress, int]] = None,
    max_insert_batch: int = 10000,
):
    assert max_blocks_batch > 0, "max_blocks_batch must be greater than 0"
    assert min_sleep_time > 0, "min_sleep_time must be greater than 0"
    assert start_block >= end_block, "start_block must be greater than end_block"
    assert end_block > 0, "end_block must be greater than 0"

    if web3 is None:
        web3 = _retry_connect_web3(blockchain_type, web3_uri=web3_uri)

    assert (
        web3.eth.block_number >= start_block
    ), "start_block must be less than current block"

    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        network = Network.ethereum
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        network = Network.polygon
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        network = Network.mumbai
    elif blockchain_type == AvailableBlockchainType.XDAI:
        network = Network.xdai
    elif blockchain_type == AvailableBlockchainType.WYRM:
        network = Network.wyrm
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
        network = Network.zksync_era_testnet
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
        network = Network.zksync_era
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        network = Network.arbitrum_nova
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        network = Network.arbitrum_sepolia
    elif blockchain_type == AvailableBlockchainType.XAI:
        network = Network.xai
    elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
        network = Network.xai_sepolia
    else:
        raise Exception("Unsupported blockchain type provided")

    ethereum_state_provider = MoonstreamEthereumStateProvider(
        web3,
        network,
        db_session,
    )

    logger.info(f"Starting historical event crawler start_block={start_block}")

    blocks_cache: Dict[int, int] = {}
    failed_count = 0

    original_start_block = start_block

    progess_map: Dict[ChecksumAddress, float] = {}

    while start_block >= end_block:
        try:
            time.sleep(min_sleep_time)

            batch_end_block = max(
                start_block - max_blocks_batch,
                end_block,
            )

            logger.info(f"Crawling events from {start_block} to {batch_end_block}")

            if function_call_crawl_jobs:
                all_events = _crawl_events(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    web3=web3,
                    jobs=event_crawl_jobs,
                    from_block=batch_end_block,
                    to_block=start_block,
                    blocks_cache=blocks_cache,
                    db_block_query_batch=max_blocks_batch,
                )

            else:
                all_events, max_blocks_batch = _autoscale_crawl_events(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    web3=web3,
                    jobs=event_crawl_jobs,
                    from_block=batch_end_block,
                    to_block=start_block,
                    blocks_cache=blocks_cache,
                    db_block_query_batch=max_blocks_batch,
                )
            logger.info(
                f"Crawled {len(all_events)} events from {start_block} to {batch_end_block}."
            )

            if len(all_events) > max_insert_batch:

                for i in range(0, len(all_events), max_insert_batch):
                    add_events_to_session(
                        db_session,
                        all_events[i : i + max_insert_batch],
                        blockchain_type,
                    )

            else:

                add_events_to_session(db_session, all_events, blockchain_type)

            if function_call_crawl_jobs:
                logger.info(
                    f"Crawling function calls from {start_block} to {batch_end_block}"
                )
                all_function_calls = _crawl_functions(
                    blockchain_type,
                    ethereum_state_provider,
                    function_call_crawl_jobs,
                    batch_end_block,
                    start_block,
                )
                logger.info(
                    f"Crawled {len(all_function_calls)} function calls from {start_block} to {batch_end_block}."
                )

                if len(all_function_calls) > max_insert_batch:

                    for i in range(0, len(all_function_calls), max_insert_batch):
                        add_function_calls_to_session(
                            db_session,
                            all_function_calls[i : i + max_insert_batch],
                            blockchain_type,
                        )
                else:

                    add_function_calls_to_session(
                        db_session, all_function_calls, blockchain_type
                    )

            if addresses_deployment_blocks:
                for address, deployment_block in addresses_deployment_blocks.items():
                    current_position = batch_end_block

                    progess = (original_start_block - current_position) / (
                        original_start_block - deployment_block
                    )
                    progess_map[address] = progess

                if len(function_call_crawl_jobs) > 0:
                    function_call_crawl_jobs = update_entries_status_and_progress(  # type: ignore
                        events=function_call_crawl_jobs,
                        progess_map=progess_map,
                    )

                if len(event_crawl_jobs) > 0:
                    event_crawl_jobs = update_entries_status_and_progress(  # type: ignore
                        events=event_crawl_jobs,
                        progess_map=progess_map,
                    )

            # Commiting to db
            commit_session(db_session)

            start_block = batch_end_block - 1
            failed_count = 0
        except Exception as e:
            db_session.rollback()
            logger.error(f"Internal error: {e}")
            logger.exception(e)
            failed_count += 1
            if failed_count > 10:
                logger.error("Too many failures, exiting")
                raise e
            try:
                web3 = _retry_connect_web3(blockchain_type, web3_uri=web3_uri)
            except Exception as err:
                logger.error(f"Failed to reconnect: {err}")
                logger.exception(err)
                raise err
