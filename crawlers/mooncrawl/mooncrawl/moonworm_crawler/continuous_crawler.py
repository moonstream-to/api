import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from moonworm.crawler.moonstream_ethereum_state_provider import (
    MoonstreamEthereumStateProvider,
)
from moonworm.crawler.networks import Network
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_
from web3 import Web3
from ..blockchain import connect
from ..data import AvailableBlockchainType
from .crawler import (
    EventCrawlJob,
    FunctionCallCrawlJob,
    blockchain_type_to_subscription_type,
    get_crawl_job_entries,
    heartbeat,
    make_event_crawl_jobs,
    make_function_call_crawl_jobs,
    merge_event_crawl_jobs,
    merge_function_call_crawl_jobs,
)

from .event_crawler import _crawl_events
from .function_call_crawler import _crawl_functions
from .db import save_events, save_function_calls

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _date_to_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")


def _refetch_new_jobs(
    old_event_jobs: List[EventCrawlJob],
    old_function_call_jobs: List[FunctionCallCrawlJob],
    blockchain_type: AvailableBlockchainType,
) -> Tuple[List[EventCrawlJob], List[FunctionCallCrawlJob]]:
    """
    Refetches new jobs from bugout journal, merges, and returns new jobs.
    """

    max_created_at_event_job = max(job.created_at for job in old_event_jobs)
    max_created_at_function_call_job = max(
        job.created_at for job in old_function_call_jobs
    )

    logger.info("Looking for new event crawl jobs.")
    old_event_jobs_length = len(old_event_jobs)
    new_event_entries = get_crawl_job_entries(
        subscription_type=blockchain_type_to_subscription_type(blockchain_type),
        crawler_type="event",
        created_at_filter=max_created_at_event_job,
    )
    new_event_jobs = make_event_crawl_jobs(new_event_entries)
    event_crawl_jobs = merge_event_crawl_jobs(old_event_jobs, new_event_jobs)
    logger.info(
        f"Found {len(event_crawl_jobs) - old_event_jobs_length} new event crawl jobs. "
    )

    logger.info("Looking for new function call crawl jobs.")
    old_function_call_jobs_length = len(old_function_call_jobs)
    new_function_entries = get_crawl_job_entries(
        subscription_type=blockchain_type_to_subscription_type(blockchain_type),
        crawler_type="function",
        created_at_filter=max_created_at_function_call_job,
    )
    new_function_call_jobs = make_function_call_crawl_jobs(new_function_entries)
    function_call_crawl_jobs = merge_function_call_crawl_jobs(
        old_function_call_jobs, new_function_call_jobs
    )
    logger.info(
        f"Found {len(function_call_crawl_jobs) - old_function_call_jobs_length} new function call crawl jobs. "
    )

    return event_crawl_jobs, function_call_crawl_jobs


def _retry_connect_web3(
    blockchain_type: AvailableBlockchainType,
    retry_count: int = 10,
    sleep_time: float = 5,
) -> Web3:
    """
    Retry connecting to the blockchain.
    """
    while retry_count > 0:
        retry_count -= 1
        try:
            web3 = connect(blockchain_type)
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


def continuous_crawler(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    web3: Optional[Web3],
    event_crawl_jobs: List[EventCrawlJob],
    function_call_crawl_jobs: List[FunctionCallCrawlJob],
    start_block: int,
    max_blocks_batch: int = 100,
    min_blocks_batch: int = 10,
    confirmations: int = 60,
    min_sleep_time: float = 0.1,
    heartbeat_interval: float = 60,
    new_jobs_refetch_interval: float = 120,
):

    assert (
        min_blocks_batch < max_blocks_batch
    ), "min_blocks_batch must be less than max_blocks_batch"
    assert min_blocks_batch > 0, "min_blocks_batch must be greater than 0"
    assert max_blocks_batch > 0, "max_blocks_batch must be greater than 0"
    assert confirmations > 0, "confirmations must be greater than 0"
    assert min_sleep_time > 0, "min_sleep_time must be greater than 0"
    assert heartbeat_interval > 0, "heartbeat_interval must be greater than 0"
    assert (
        new_jobs_refetch_interval > 0
    ), "new_jobs_refetch_interval must be greater than 0"

    crawl_start_time = datetime.utcnow()

    jobs_refetchet_time = crawl_start_time
    if web3 is None:
        web3 = _retry_connect_web3(blockchain_type)

    network = (
        Network.ethereum
        if blockchain_type == AvailableBlockchainType.ETHEREUM
        else Network.polygon
    )
    ethereum_state_provider = MoonstreamEthereumStateProvider(
        web3,
        network,
        db_session,
    )

    heartbeat_template = {
        "status": "crawling",
        "start_block": start_block,
        "last_block": start_block,
        "crawl_start_time": _date_to_str(crawl_start_time),
        "current_time": _date_to_str(crawl_start_time),
        "current_event_jobs_length": len(event_crawl_jobs),
        "current_function_call_jobs_length": len(function_call_crawl_jobs),
        "jobs_last_refetched_at": _date_to_str(jobs_refetchet_time),
    }

    logger.info(f"Starting continuous event crawler start_block={start_block}")
    logger.info("Sending initial heartbeat")
    heartbeat(
        crawler_type="event",
        blockchain_type=blockchain_type,
        crawler_status=heartbeat_template,
    )
    last_heartbeat_time = datetime.utcnow()
    blocks_cache: Dict[int, int] = {}

    try:
        while True:
            try:
                # query db  with limit 1, to avoid session closing
                db_session.execute("SELECT 1")
                time.sleep(min_sleep_time)

                end_block = min(
                    web3.eth.blockNumber - confirmations,
                    start_block + max_blocks_batch,
                )

                if start_block + min_blocks_batch > end_block:
                    min_sleep_time *= 2
                    logger.info(
                        f"Sleeping for {min_sleep_time} seconds because of low block count"
                    )
                    continue
                min_sleep_time = max(min_sleep_time, min_sleep_time / 2)

                logger.info(f"Crawling events from {start_block} to {end_block}")
                all_events = _crawl_events(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    web3=web3,
                    jobs=event_crawl_jobs,
                    from_block=start_block,
                    to_block=end_block,
                    blocks_cache=blocks_cache,
                    db_block_query_batch=min_blocks_batch * 2,
                )
                logger.info(
                    f"Crawled {len(all_events)} events from {start_block} to {end_block}."
                )

                save_events(db_session, all_events, blockchain_type)

                logger.info(
                    f"Crawling function calls from {start_block} to {end_block}"
                )
                all_function_calls = _crawl_functions(
                    blockchain_type,
                    ethereum_state_provider,
                    function_call_crawl_jobs,
                    start_block,
                    end_block,
                )
                logger.info(
                    f"Crawled {len(all_function_calls)} function calls from {start_block} to {end_block}."
                )

                save_function_calls(db_session, all_function_calls, blockchain_type)

                current_time = datetime.utcnow()

                if current_time - jobs_refetchet_time > timedelta(
                    seconds=new_jobs_refetch_interval
                ):
                    logger.info(
                        f"Refetching new jobs from bugout journal since {jobs_refetchet_time}"
                    )
                    event_crawl_jobs, function_call_crawl_jobs = _refetch_new_jobs(
                        event_crawl_jobs, function_call_crawl_jobs, blockchain_type
                    )
                    jobs_refetchet_time = current_time

                if current_time - last_heartbeat_time > timedelta(
                    seconds=heartbeat_interval
                ):
                    # Update heartbeat and send to humbug
                    heartbeat_template["last_block"] = end_block
                    heartbeat_template["current_time"] = current_time
                    heartbeat_template["current_event_jobs_length"] = len(
                        event_crawl_jobs
                    )
                    heartbeat_template["jobs_last_refetched_at"] = jobs_refetchet_time
                    heartbeat(
                        crawler_type="event",
                        blockchain_type=blockchain_type,
                        crawler_status=heartbeat_template,
                    )
                    logger.info("Sending heartbeat to humbug.", heartbeat_template)
                    last_heartbeat_time = datetime.utcnow()

                start_block = end_block + 1
            except Exception as e:
                logger.error(f"Internal error: {e}")
                logger.exception(e)
                try:
                    web3 = _retry_connect_web3(blockchain_type)
                except Exception as err:
                    logger.error(f"Failed to reconnect: {err}")
                    logger.exception(err)
                    raise err

    except BaseException as e:
        logger.error(f"!!!!Crawler Died!!!!")
        heartbeat_template["status"] = "dead"
        heartbeat_template["current_time"] = _date_to_str(datetime.utcnow())
        heartbeat_template["current_event_jobs_length"] = len(event_crawl_jobs)
        heartbeat_template["jobs_last_refetched_at"] = _date_to_str(jobs_refetchet_time)
        error_summary = (repr(e),)
        error_traceback = (
            "".join(
                traceback.format_exception(
                    etype=type(e),
                    value=e,
                    tb=e.__traceback__,
                )
            ),
        )
        heartbeat_template[
            "die_reason"
        ] = f"{e.__class__.__name__}: {e}\n error_summary: {error_summary}\n error_traceback: {error_traceback}"
        heartbeat_template["last_block"] = end_block
        heartbeat(
            crawler_type="event",
            blockchain_type=blockchain_type,
            crawler_status=heartbeat_template,
        )

        logger.exception(e)
