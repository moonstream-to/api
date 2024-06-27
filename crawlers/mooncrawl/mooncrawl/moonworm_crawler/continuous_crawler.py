import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


from moonstreamtypes.blockchain import AvailableBlockchainType
from moonstreamtypes.subscriptions import blockchain_type_to_subscription_type
from moonstreamtypes.networks import blockchain_type_to_network_type
from moonworm.crawler.moonstream_ethereum_state_provider import (  # type: ignore
    MoonstreamEthereumStateProvider,
)
from moonworm.crawler.ethereum_state_provider import Web3StateProvider
from sqlalchemy.orm.session import Session
from web3 import Web3

from .crawler import (
    EventCrawlJob,
    FunctionCallCrawlJob,
    _retry_connect_web3,
    get_crawl_job_entries,
    heartbeat,
    make_event_crawl_jobs,
    make_function_call_crawl_jobs,
    merge_event_crawl_jobs,
    merge_function_call_crawl_jobs,
    moonworm_crawler_update_job_as_pickedup,
    get_event_crawl_job_records,
    get_function_call_crawl_job_records,
)
from .db import add_events_to_session, add_function_calls_to_session, commit_session
from .event_crawler import _crawl_events
from .function_call_crawler import _crawl_functions
from ..settings import CRAWLER_LABEL, SEER_CRAWLER_LABEL

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
    max_created_at_event_job: Optional[int] = None
    max_created_at_function_call_job: Optional[int] = None
    if len(old_event_jobs) != 0:
        max_created_at_event_job = max(job.created_at for job in old_event_jobs)
    if len(old_function_call_jobs) != 0:
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


def continuous_crawler(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    web3: Optional[Web3],
    event_crawl_jobs: List[EventCrawlJob],
    function_call_crawl_jobs: List[FunctionCallCrawlJob],
    start_block: int,
    max_blocks_batch: int = 100,
    min_blocks_batch: int = 40,
    confirmations: int = 60,
    min_sleep_time: float = 0.1,
    heartbeat_interval: float = 60,
    new_jobs_refetch_interval: float = 120,
    web3_uri: Optional[str] = None,
    max_insert_batch: int = 10000,
    version: int = 2,
    index_db_session: Optional[Session] = None,
    customer_id: Optional[str] = None,
):
    crawler_type = "continuous"
    if version == 3:
        crawler_type = "continuous_v3"

    label_name = CRAWLER_LABEL
    if version == 3:
        label_name = SEER_CRAWLER_LABEL
    assert (
        min_blocks_batch < max_blocks_batch
    ), "min_blocks_batch must be less than max_blocks_batch"
    assert min_blocks_batch > 0, "min_blocks_batch must be greater than 0"
    assert max_blocks_batch > 0, "max_blocks_batch must be greater than 0"
    assert min_sleep_time > 0, "min_sleep_time must be greater than 0"
    assert heartbeat_interval > 0, "heartbeat_interval must be greater than 0"
    assert (
        new_jobs_refetch_interval > 0
    ), "new_jobs_refetch_interval must be greater than 0"

    crawl_start_time = datetime.utcnow()

    jobs_refetchet_time = crawl_start_time
    if web3 is None:
        web3 = _retry_connect_web3(blockchain_type, web3_uri=web3_uri)

    try:
        network = blockchain_type_to_network_type(blockchain_type=blockchain_type)
    except Exception as e:
        raise Exception(e)

    evm_state_provider = Web3StateProvider(web3)

    if version == 2:
        evm_state_provider = MoonstreamEthereumStateProvider(
            web3,
            network,  # type: ignore
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
        crawler_type=crawler_type,
        blockchain_type=blockchain_type,
        crawler_status=heartbeat_template,
    )
    last_heartbeat_time = datetime.utcnow()
    blocks_cache: Dict[int, int] = {}
    current_sleep_time = min_sleep_time
    failed_count = 0
    try:
        while True:
            try:
                time.sleep(current_sleep_time)

                end_block = min(
                    web3.eth.blockNumber - confirmations,
                    start_block + max_blocks_batch,
                )

                if start_block + min_blocks_batch > end_block:
                    current_sleep_time += 0.1
                    logger.info(
                        f"Sleeping for {current_sleep_time} seconds because of low block count"
                    )
                    continue
                current_sleep_time = max(min_sleep_time, current_sleep_time - 0.1)

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
                    version=version,
                )
                logger.info(
                    f"Crawled {len(all_events)} events from {start_block} to {end_block}."
                )

                if len(all_events) > max_insert_batch:

                    for i in range(0, len(all_events), max_insert_batch):
                        add_events_to_session(
                            db_session,
                            all_events[i : i + max_insert_batch],
                            blockchain_type,
                            version,
                            label_name,
                        )
                else:
                    add_events_to_session(
                        db_session, all_events, blockchain_type, version, label_name
                    )

                logger.info(
                    f"Crawling function calls from {start_block} to {end_block}"
                )
                all_function_calls = _crawl_functions(
                    blockchain_type,
                    evm_state_provider,
                    function_call_crawl_jobs,
                    start_block,
                    end_block,
                )
                logger.info(
                    f"Crawled {len(all_function_calls)} function calls from {start_block} to {end_block}."
                )

                if len(all_function_calls) > max_insert_batch:

                    for i in range(0, len(all_function_calls), max_insert_batch):
                        add_function_calls_to_session(
                            db_session,
                            all_function_calls[i : i + max_insert_batch],
                            blockchain_type,
                            db_version=version,
                            label_name=label_name,
                        )
                else:
                    add_function_calls_to_session(
                        db_session,
                        all_function_calls,
                        blockchain_type,
                        db_version=version,
                        label_name=label_name,
                    )

                current_time = datetime.utcnow()

                if current_time - jobs_refetchet_time > timedelta(
                    seconds=new_jobs_refetch_interval
                ):
                    if version == 2:
                        ## Refetch new jobs from bugout journal
                        logger.info(
                            f"Refetching new jobs from bugout journal since {jobs_refetchet_time}"
                        )
                        event_crawl_jobs, function_call_crawl_jobs = _refetch_new_jobs(
                            event_crawl_jobs, function_call_crawl_jobs, blockchain_type
                        )

                        (
                            event_crawl_jobs,
                            function_call_crawl_jobs,
                        ) = moonworm_crawler_update_job_as_pickedup(
                            event_crawl_jobs=event_crawl_jobs,
                            function_call_crawl_jobs=function_call_crawl_jobs,
                        )
                    elif version == 3 and index_db_session is not None:
                        ## Refetch new jobs from index db

                        updated_event_crawl_jobs = get_event_crawl_job_records(
                            index_db_session,
                            blockchain_type,
                            [],
                            {event.event_abi_hash: event for event in event_crawl_jobs},
                            customer_id=customer_id,
                        )

                        event_crawl_jobs = [
                            event for event in updated_event_crawl_jobs.values()
                        ]

                        updated_function_call_crawl_jobs = (
                            get_function_call_crawl_job_records(
                                index_db_session,
                                blockchain_type,
                                [],
                                {
                                    function_call.contract_address: function_call
                                    for function_call in function_call_crawl_jobs
                                },
                                customer_id=customer_id,
                            )
                        )

                        function_call_crawl_jobs = [
                            function_call
                            for function_call in updated_function_call_crawl_jobs.values()
                        ]
                    else:
                        raise ValueError("Invalid version")

                    jobs_refetchet_time = current_time

                commit_session(db_session)

                if current_time - last_heartbeat_time > timedelta(
                    seconds=heartbeat_interval
                ):
                    # Update heartbeat
                    heartbeat_template["last_block"] = end_block
                    heartbeat_template["current_time"] = _date_to_str(current_time)
                    heartbeat_template["current_event_jobs_length"] = len(
                        event_crawl_jobs
                    )
                    heartbeat_template["jobs_last_refetched_at"] = _date_to_str(
                        jobs_refetchet_time
                    )
                    heartbeat_template["current_function_call_jobs_length"] = len(
                        function_call_crawl_jobs
                    )
                    heartbeat_template["function_call metrics"] = (
                        evm_state_provider.metrics
                    )
                    heartbeat(
                        crawler_type=crawler_type,
                        blockchain_type=blockchain_type,
                        crawler_status=heartbeat_template,
                    )
                    logger.info("Sending heartbeat.", heartbeat_template)
                    last_heartbeat_time = datetime.utcnow()

                start_block = end_block + 1
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
        heartbeat_template["die_reason"] = (
            f"{e.__class__.__name__}: {e}\n error_summary: {error_summary}\n error_traceback: {error_traceback}"
        )
        heartbeat_template["last_block"] = end_block
        heartbeat(
            crawler_type=crawler_type,
            blockchain_type=blockchain_type,
            crawler_status=heartbeat_template,
            is_dead=True,
        )

        logger.exception(e)
        raise e
