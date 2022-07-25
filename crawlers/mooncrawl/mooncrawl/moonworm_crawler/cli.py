import argparse
import logging
from typing import Optional
from uuid import UUID

from moonstreamdb.db import yield_db_session_ctx
from web3 import Web3
from web3.middleware import geth_poa_middleware

from ..blockchain import AvailableBlockchainType
from ..settings import MOONSTREAM_MOONWORM_TASKS_JOURNAL, NB_CONTROLLER_ACCESS_ID
from .continuous_crawler import _retry_connect_web3, continuous_crawler
from .crawler import (
    SubscriptionTypes,
    blockchain_type_to_subscription_type,
    get_crawl_job_entries,
    make_event_crawl_jobs,
    make_function_call_crawl_jobs,
)
from .db import get_first_labeled_block_number, get_last_labeled_block_number
from .historical_crawler import historical_crawler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_crawl(args: argparse.Namespace) -> None:

    blockchain_type = AvailableBlockchainType(args.blockchain_type)
    subscription_type = blockchain_type_to_subscription_type(blockchain_type)

    initial_event_jobs = make_event_crawl_jobs(
        get_crawl_job_entries(
            subscription_type,
            "event",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    logger.info(f"Initial event crawl jobs count: {len(initial_event_jobs)}")

    initial_function_call_jobs = make_function_call_crawl_jobs(
        get_crawl_job_entries(
            subscription_type,
            "function",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    logger.info(
        f"Initial function call crawl jobs count: {len(initial_function_call_jobs)}"
    )

    logger.info(f"Blockchain type: {blockchain_type.value}")
    with yield_db_session_ctx() as db_session:
        web3: Optional[Web3] = None
        if args.web3 is None:
            logger.info(
                "No web3 provider URL provided, using default (blockchan.py: connect())"
            )
            web3 = _retry_connect_web3(blockchain_type, access_id=args.access_id)
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

        start_block = args.start
        if start_block is None:
            logger.info("No start block provided")
            if last_labeled_block is not None:
                start_block = last_labeled_block - 1
                logger.info(f"Using last labeled block as start: {start_block}")
            else:
                logger.info(
                    "No last labeled block found, using  start block (web3.eth.blockNumber - 300)"
                )
                start_block = web3.eth.blockNumber - 10000
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
            access_id=args.access_id,
        )


def handle_historical_crawl(args: argparse.Namespace) -> None:
    blockchain_type = AvailableBlockchainType(args.blockchain_type)
    subscription_type = blockchain_type_to_subscription_type(blockchain_type)

    addresses_filter = [args.address]
    all_event_jobs = make_event_crawl_jobs(
        get_crawl_job_entries(
            subscription_type,
            "event",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    filtered_event_jobs = []
    for job in all_event_jobs:
        intersection = [
            address for address in job.contracts if address in addresses_filter
        ]
        if intersection:
            job.contracts = intersection
            filtered_event_jobs.append(job)

    logger.info(f"Filtered event crawl jobs count: {len(filtered_event_jobs)}")

    all_function_call_jobs = make_function_call_crawl_jobs(
        get_crawl_job_entries(
            subscription_type,
            "function",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    filtered_function_call_jobs = [
        job
        for job in all_function_call_jobs
        if job.contract_address in addresses_filter
    ]

    if args.only_events:
        filtered_function_call_jobs = []
        logger.info(f"Removing function call crawl jobs since --only-events is set")

    logger.info(
        f"Initial function call crawl jobs count: {len(filtered_function_call_jobs)}"
    )

    logger.info(f"Blockchain type: {blockchain_type.value}")
    with yield_db_session_ctx() as db_session:
        web3: Optional[Web3] = None
        if args.web3 is None:
            logger.info(
                "No web3 provider URL provided, using default (blockchan.py: connect())"
            )
            web3 = _retry_connect_web3(blockchain_type, access_id=args.access_id)
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

        last_labeled_block = get_first_labeled_block_number(
            db_session, blockchain_type, args.address, only_events=args.only_events
        )
        logger.info(f"Last labeled block: {last_labeled_block}")

        start_block = args.start
        if start_block is None:
            logger.info("No start block provided")
            if last_labeled_block is not None:
                start_block = last_labeled_block
                logger.info(f"Using last labeled block as start: {start_block}")
            else:
                logger.info(
                    "No last labeled block found, using  start block (web3.eth.blockNumber - 300)"
                )
                raise ValueError(
                    "No start block provided and no last labeled block found"
                )
        elif last_labeled_block is not None:
            if start_block > last_labeled_block and not args.force:
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

        if start_block < args.end:
            raise ValueError(
                f"Start block {start_block} is less than end block {args.end}. This crawler crawls in the reverse direction."
            )

        historical_crawler(
            db_session,
            blockchain_type,
            web3,
            filtered_event_jobs,
            filtered_function_call_jobs,
            start_block,
            args.end,
            args.max_blocks_batch,
            args.min_sleep_time,
            access_id=args.access_id,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda _: parser.print_help())

    parser.add_argument(
        "--access-id",
        default=NB_CONTROLLER_ACCESS_ID,
        type=UUID,
        help="User access ID",
    )

    subparsers = parser.add_subparsers()

    crawl_parser = subparsers.add_parser(
        "crawl",
        help="continuous crawling the event/function call jobs from bugout journal",
    )

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
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
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
        default=80,
        help="Maximum number of blocks to crawl in a single batch",
    )

    crawl_parser.add_argument(
        "--min-blocks-batch",
        "-n",
        type=int,
        default=20,
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
        default=0.1,
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
        default=180,
        help="Time to wait before refetching new jobs",
    )

    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force start from the start block",
    )

    crawl_parser.set_defaults(func=handle_crawl)

    historical_crawl_parser = subparsers.add_parser(
        "historical-crawl", help="Crawl historical data"
    )
    historical_crawl_parser.add_argument(
        "--address",
        "-a",
        required=True,
        type=str,
    )
    historical_crawl_parser.add_argument(
        "--start",
        "-s",
        type=int,
        default=None,
    )
    historical_crawl_parser.add_argument(
        "--end",
        "-e",
        type=int,
        required=True,
    )
    historical_crawl_parser.add_argument(
        "--blockchain-type",
        "-b",
        type=str,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    historical_crawl_parser.add_argument(
        "--web3",
        type=str,
        default=None,
        help="Web3 provider URL",
    )
    historical_crawl_parser.add_argument(
        "--poa",
        action="store_true",
        default=False,
        help="Use PoA middleware",
    )

    historical_crawl_parser.add_argument(
        "--max-blocks-batch",
        "-m",
        type=int,
        default=80,
        help="Maximum number of blocks to crawl in a single batch",
    )

    historical_crawl_parser.add_argument(
        "--min-sleep-time",
        "-t",
        type=float,
        default=0.1,
        help="Minimum time to sleep between crawl step",
    )

    historical_crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force start from the start block",
    )
    historical_crawl_parser.add_argument(
        "--only-events",
        action="store_true",
        default=False,
        help="Only crawl events",
    )
    historical_crawl_parser.set_defaults(func=handle_historical_crawl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
