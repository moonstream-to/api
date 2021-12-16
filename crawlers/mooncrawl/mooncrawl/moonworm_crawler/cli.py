import logging
import argparse

from web3 import Web3
from moonstreamdb.db import yield_db_session_ctx
from web3.middleware import geth_poa_middleware

from ..settings import MOONSTREAM_MOONWORM_TASKS_JOURNAL, bugout_client
from .crawler import (
    make_event_crawl_jobs,
    make_function_call_crawl_jobs,
    get_crawl_job_entries,
    SubscriptionTypes,
)
from ..blockchain import AvailableBlockchainType
from .continuous_crawler import continuous_crawler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_crawl(args: argparse.Namespace) -> None:

    initial_event_jobs = make_event_crawl_jobs(
        get_crawl_job_entries(
            SubscriptionTypes.POLYGON_BLOCKCHAIN,
            "event",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    logger.info(f"Initial event crawl jobs count: {len(initial_event_jobs)}")

    initial_function_call_jobs = make_function_call_crawl_jobs(
        get_crawl_job_entries(
            SubscriptionTypes.POLYGON_BLOCKCHAIN,
            "function",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    logger.info(
        f"Initial function call crawl jobs count: {len(initial_function_call_jobs)}"
    )
    print(initial_function_call_jobs)

    with yield_db_session_ctx() as db_session:
        web3 = None
        if args.web3 is not None:
            web3 = Web3(
                Web3.HTTPProvider(
                    args.web3,
                )
            )
            if args.poa:
                web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        start_block = args.start_block
        continuous_crawler(
            db_session,
            args.blockchain_type,
            web3,
            initial_event_jobs,
            initial_function_call_jobs,
            start_block,
            args.max_blocks_batch,
            args.min_blocks_batch,
            args.confirmations,
            args.min_sleep_time,
            args.heartbeat_interval,
            args.new_jobs_refetch_interval,
        )


def generate_parser() -> argparse.ArgumentParser:
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
        default=100,
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

    crawl_parser.set_defaults(func=handle_crawl)
    return parser
