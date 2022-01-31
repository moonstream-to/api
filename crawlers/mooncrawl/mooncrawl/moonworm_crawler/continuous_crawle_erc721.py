import argparse
import hashlib
import logging
import json
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from moonworm.crawler.moonstream_ethereum_state_provider import (  # type: ignore
    MoonstreamEthereumStateProvider,
)
from moonworm.crawler.networks import Network  # type: ignore
from sqlalchemy.orm.session import Session
from web3 import Web3


from ..blockchain import connect
from ..data import AvailableBlockchainType
from .crawler import (
    EventCrawlJob,
    heartbeat,
    get_crawler_point,
    update_crawl_point,
)
from .db import add_events_to_session, commit_session
from .event_crawler import _crawl_events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _date_to_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")


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
    abi: List[Dict[str, Any]],
    start_block: int,
    end_block: int,
    max_blocks_batch: int = 100,
    min_blocks_batch: int = 10,
    confirmations: int = 60,
    min_sleep_time: float = 0.1,
    heartbeat_interval: float = 60,
    new_jobs_refetch_interval: float = 120,
    use_traker: bool = True,
):
    crawler_type = "ERC721_crawler"
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

    # Create tables if not exists works good for sqlite

    from db.moonstreamdb.models import PolygonLabel
    from db.moonstreamdb.db import engine
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    Base.metadata.create_all(engine)
    db_session.commit()

    crawl_start_time = datetime.utcnow()

    jobs_refetchet_time = crawl_start_time
    if web3 is None:
        web3 = _retry_connect_web3(blockchain_type)

    if use_traker:

        start_block, end_block, entry_id = get_crawler_point(
            crawler_type=crawler_type,
            blockchain_type=blockchain_type,
            abi_hash=hashlib.md5(json.dumps(abi).encode("utf-8")).hexdigest(),
            start_block=start_block,
            end_block=end_block,
        )

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

    # Create events jobs

    events = [event for event in abi if event["type"]]

    event_crawl_jobs = []

    for event in events:
        event_crawl_jobs.append(
            EventCrawlJob(
                event_abi_hash="", event_abi=event, contracts=[], created_at=0
            )
        )

    heartbeat_template = {
        "status": "crawling",
        "start_block": start_block,
        "last_block": start_block,
        "crawl_start_time": _date_to_str(crawl_start_time),
        "current_time": _date_to_str(crawl_start_time),
        "current_event_jobs_length": len(event_crawl_jobs),
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

    failed_count = 0
    try:
        while True:
            try:
                # query db  with limit 1, to avoid session closing
                db_session.execute("SELECT 1")
                time.sleep(min_sleep_time)

                update_crawl_point(
                    crawler_type=crawler_type,
                    blockchain_type=blockchain_type,
                    entry_id=entry_id,
                    start_block=start_block,
                    end_block=end_block,
                )

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

                add_events_to_session(db_session, all_events, blockchain_type)

                logger.info(
                    f"Crawling function calls from {start_block} to {end_block}"
                )

                current_time = datetime.utcnow()

                if current_time - jobs_refetchet_time > timedelta(
                    seconds=new_jobs_refetch_interval
                ):
                    logger.info(
                        f"Refetching new jobs from bugout journal since {jobs_refetchet_time}"
                    )
                    # event_crawl_jobs, function_call_crawl_jobs = _refetch_new_jobs(
                    #     event_crawl_jobs, function_call_crawl_jobs, blockchain_type
                    # )
                    jobs_refetchet_time = current_time

                if current_time - last_heartbeat_time > timedelta(
                    seconds=heartbeat_interval
                ):
                    # Commiting to db
                    commit_session(db_session)

                    # Update heartbeat
                    heartbeat_template["last_block"] = end_block
                    heartbeat_template["current_time"] = _date_to_str(current_time)
                    heartbeat_template["current_event_jobs_length"] = len(
                        event_crawl_jobs
                    )
                    heartbeat_template["jobs_last_refetched_at"] = _date_to_str(
                        jobs_refetchet_time
                    )
                    # heartbeat_template["current_function_call_jobs_length"] = len(
                    #     function_call_crawl_jobs
                    # )
                    heartbeat_template[
                        "function_call metrics"
                    ] = ethereum_state_provider.metrics
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
                logger.error(f"Internal error: {e}")
                logger.exception(e)
                failed_count += 1
                if failed_count > 10:
                    logger.error("Too many failures, exiting")
                    raise e
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
            crawler_type=crawler_type,
            blockchain_type=blockchain_type,
            crawler_status=heartbeat_template,
            is_dead=True,
        )

        logger.exception(e)
        raise e


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    crawl_parser = subparsers.add_parser("crawl")

    crawl_parser.add_argument(
        "--start",
        "-s",
        type=int,
        default=None,
    )
    crawl_parser.add_argument(
        "--blockchain-type",
        "-b",
        type=str,
        choices=[
            AvailableBlockchainType.ETHEREUM.value,
            AvailableBlockchainType.POLYGON.value,
        ],
        required=True,
    )
    crawl_parser.add_argument(
        "--web3",
        type=str,
        default=None,
        help="Web3 provider URL",
    )
    crawl_parser.add_argument(
        "--poa",
        action="store_true",
        default=False,
        help="Use PoA middleware",
    )

    crawl_parser.add_argument(
        "--max-blocks-batch",
        "-m",
        type=int,
        default=100,
        help="Maximum number of blocks to crawl in a single batch",
    )

    crawl_parser.add_argument(
        "--min-blocks-batch",
        "-n",
        type=int,
        default=10,
        help="Minimum number of blocks to crawl in a single batch",
    )

    crawl_parser.add_argument(
        "--confirmations",
        "-c",
        type=int,
        default=175,
        help="Number of confirmations to wait for",
    )

    crawl_parser.add_argument(
        "--min-sleep-time",
        "-t",
        type=float,
        default=0.01,
        help="Minimum time to sleep between crawl step",
    )

    crawl_parser.add_argument(
        "--heartbeat-interval",
        "-i",
        type=float,
        default=60,
        help="Heartbeat interval in seconds",
    )

    crawl_parser.add_argument(
        "--new-jobs-refetch-interval",
        "-r",
        type=float,
        default=120,
        help="Time to wait before refetching new jobs",
    )

    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force start from the start block",
    )

    crawl_parser.set_defaults(func=handle_crawl)

    args = parser.parse_args()
    args.func(args)
