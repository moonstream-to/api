import argparse
import logging
from typing import Optional

from moonstreamdb.db import yield_db_session_ctx
from web3 import Web3
from web3.middleware import geth_poa_middleware

from ..blockchain import AvailableBlockchainType
from ..settings import MOONSTREAM_MOONWORM_TASKS_JOURNAL, bugout_client
from .continuous_crawler import continuous_crawler, _retry_connect_web3
from .crawler import (
    SubscriptionTypes,
    get_crawl_job_entries,
    make_event_crawl_jobs,
    make_function_call_crawl_jobs,
)
from .db import get_last_labeled_block_number

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
    blockchain_type = AvailableBlockchainType(args.blockchain_type)
    with yield_db_session_ctx() as db_session:
        web3: Optional[Web3] = None
        if args.web3 is None:
            logger.info(
                "No web3 provider URL provided, using default (blockchan.py: connect())"
            )
            web3 = _retry_connect_web3(args.blockchain_type)
        else:
            logger.info(f"Using web3 provider URL: {args.web3}")
            web3 = Web3(
                Web3.HTTPProvider(
                    args.web3,
                )
            )
            if args.poa:
                logger.info("Using PoA middleware")
                web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        last_labeled_block = get_last_labeled_block_number(db_session, blockchain_type)
        logger.info(f"Last labeled block: {last_labeled_block}")

        start_block = args.start_block
        if start_block is None:
            logger.info("No start block provided")
            if last_labeled_block is not None:
                start_block = last_labeled_block - 1
                logger.info(f"Using last labeled block as start: {start_block}")
            else:
                logger.info(
                    "No last labeled block found, using  start block (web3.eth.blockNumber - 300)"
                )
                start_block = web3.eth.blockNumber - 300
                logger.info(f"Starting from block: {start_block}")
        elif last_labeled_block is not None:
            if start_block < last_labeled_block and not args.force:
                logger.info(
                    f"Start block is less than last labeled block, using last labeled block: {last_labeled_block}"
                )
                logger.info(
                    f"Use --force to override this and start from the start block: {start_block}"
                )

                start_block = last_labeled_block
            else:
                logger.info(f"Using start block: {start_block}")
        else:
            logger.info(f"Using start block: {start_block}")

        continuous_crawler(
            db_session,
            blockchain_type,
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

    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force start from the start block",
    )

    crawl_parser.set_defaults(func=handle_crawl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
