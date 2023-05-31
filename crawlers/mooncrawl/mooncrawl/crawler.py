"""
Moonstream crawlers CLI.
"""
import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Iterator, List
from uuid import UUID

from moonstreamdb.blockchain import AvailableBlockchainType
import dateutil.parser  # type: ignore

from .blockchain import (
    DateRange,
    check_missing_blocks,
    crawl_blocks_executor,
    get_latest_blocks,
    trending,
)
from .publish import publish_json
from .settings import MOONSTREAM_CRAWL_WORKERS, NB_CONTROLLER_ACCESS_ID
from .version import MOONCRAWL_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessingOrder(Enum):
    DESCENDING = 0
    ASCENDING = 1


def yield_blocks_numbers_lists(
    blocks_range_str: str,
    order: ProcessingOrder = ProcessingOrder.DESCENDING,
    block_step: int = 1000,
) -> Iterator[List[int]]:
    """
    Generate list of blocks.
    Block steps used to prevent long executor tasks and data loss possibility.
    """
    try:
        blocks_start_end = blocks_range_str.split("-")
        input_start_block = int(blocks_start_end[0])
        input_end_block = int(blocks_start_end[1])
    except Exception:
        logger.error(
            "Wrong format provided, expected {bottom_block}-{top_block}, as ex. 105-340"
        )
        raise Exception

    starting_block = max(input_start_block, input_end_block)
    ending_block = min(input_start_block, input_end_block)

    stepsize = -1
    if order == ProcessingOrder.ASCENDING:
        starting_block = min(input_start_block, input_end_block)
        ending_block = max(input_start_block, input_end_block)
        stepsize = 1

    current_block = starting_block

    def keep_going() -> bool:
        if order == ProcessingOrder.ASCENDING:
            return current_block <= ending_block
        return current_block >= ending_block

    while keep_going():
        temp_ending_block = current_block + stepsize * block_step
        if order == ProcessingOrder.ASCENDING:
            if temp_ending_block > ending_block:
                temp_ending_block = ending_block + 1
        else:
            if temp_ending_block < ending_block:
                temp_ending_block = ending_block - 1
        blocks_numbers_list = list(range(current_block, temp_ending_block, stepsize))

        yield blocks_numbers_list

        if order == ProcessingOrder.ASCENDING:
            current_block += block_step
        else:
            current_block -= block_step


def crawler_blocks_sync_handler(args: argparse.Namespace) -> None:
    """
    Synchronize latest Blockchain blocks with database.
    """
    while True:
        latest_stored_block_number, latest_block_number = get_latest_blocks(
            AvailableBlockchainType(args.blockchain),
            args.confirmations,
            access_id=args.access_id,
        )
        if latest_stored_block_number is None:
            latest_stored_block_number = 0

        if latest_stored_block_number >= latest_block_number:
            logger.info(
                f"Synchronization is unnecessary for blocks {latest_stored_block_number}-{latest_block_number - 1}"
            )
            time.sleep(5)
            continue

        block_number_difference = latest_block_number - 1 - latest_stored_block_number
        if block_number_difference >= 70:
            logger.warning(
                f"Block difference is too large: {block_number_difference}, crawling {args.confirmations + 1} latest blocks"
            )
            bottom_block_number = latest_block_number - args.confirmations - 1
        else:
            if args.start is None:
                if block_number_difference < args.confirmations:
                    logger.info(
                        f"Synchronization is unnecessary for blocks {latest_stored_block_number}-{latest_block_number - 1}"
                    )
                    time.sleep(5)
                    continue
                else:
                    bottom_block_number = latest_stored_block_number + 1
            else:
                bottom_block_number = max(latest_stored_block_number + 1, args.start)

        for blocks_numbers_list in yield_blocks_numbers_lists(
            f"{bottom_block_number}-{latest_block_number}",
            order=args.order,
        ):
            logger.info(
                f"Adding blocks {blocks_numbers_list[-1]}-{blocks_numbers_list[0]}"
            )
            # TODO(kompotkot): Set num_processes argument based on number of blocks to synchronize.
            crawl_blocks_executor(
                blockchain_type=AvailableBlockchainType(args.blockchain),
                block_numbers_list=blocks_numbers_list,
                with_transactions=True,
                num_processes=args.jobs,
                access_id=args.access_id,
            )
        logger.info(
            f"Synchronized blocks from {latest_stored_block_number} to {latest_block_number}"
        )


def crawler_blocks_add_handler(args: argparse.Namespace) -> None:
    """
    Add blocks to moonstream database.
    """
    startTime = time.time()

    for blocks_numbers_list in yield_blocks_numbers_lists(args.blocks):
        logger.info(f"Adding blocks {blocks_numbers_list[-1]}-{blocks_numbers_list[0]}")
        crawl_blocks_executor(
            blockchain_type=AvailableBlockchainType(args.blockchain),
            block_numbers_list=blocks_numbers_list,
            with_transactions=True,
            access_id=args.access_id,
        )

    logger.info(
        f"Required {time.time() - startTime} with {MOONSTREAM_CRAWL_WORKERS} workers"
    )


def crawler_blocks_missing_handler(args: argparse.Namespace) -> None:
    """
    Check missing blocks and missing transactions in each block.
    If block range doesn't provided, get latest block from blockchain minus 50,
    and check last 2000 blocks behind.
    """
    startTime = time.time()

    missing_blocks_numbers_total = []

    block_range = args.blocks
    if block_range is None:
        confirmations = args.confirmations
        shift = args.shift
        _, latest_block_number = get_latest_blocks(
            AvailableBlockchainType(args.blockchain),
            confirmations,
            access_id=args.access_id,
        )
        start_block_number = (
            latest_block_number - shift if latest_block_number - shift >= 1 else 1
        )
        block_range = f"{start_block_number}-{latest_block_number}"

    for blocks_numbers_list in yield_blocks_numbers_lists(block_range):
        logger.info(
            f"Checking missing blocks {blocks_numbers_list[-1]}-{blocks_numbers_list[0]} "
            f"with comparing transactions: {not args.notransactions}"
        )
        missing_blocks_numbers = check_missing_blocks(
            blockchain_type=AvailableBlockchainType(args.blockchain),
            blocks_numbers=blocks_numbers_list,
            notransactions=args.notransactions,
            access_id=args.access_id,
        )
        if len(missing_blocks_numbers) > 0:
            logger.info(f"Found {len(missing_blocks_numbers)} missing blocks")
        missing_blocks_numbers_total.extend(missing_blocks_numbers)
    logger.info(
        f"Found {len(missing_blocks_numbers_total)} missing blocks total: "
        f"{missing_blocks_numbers_total if len(missing_blocks_numbers_total) <= 10 else '...'}"
    )

    if (len(missing_blocks_numbers_total)) > 0:
        time.sleep(5)
        crawl_blocks_executor(
            blockchain_type=AvailableBlockchainType(args.blockchain),
            block_numbers_list=missing_blocks_numbers_total,
            with_transactions=True,
            num_processes=1 if args.lazy else MOONSTREAM_CRAWL_WORKERS,
            access_id=args.access_id,
        )
    logger.info(
        f"Required {time.time() - startTime} with {MOONSTREAM_CRAWL_WORKERS} workers "
        f"for {len(missing_blocks_numbers_total)} missing blocks"
    )


def crawler_trending_handler(args: argparse.Namespace) -> None:
    date_range = DateRange(
        start_time=args.start,
        end_time=args.end,
        include_start=args.include_start,
        include_end=args.include_end,
    )
    results = trending(date_range)
    humbug_token = args.humbug
    if humbug_token is None:
        humbug_token = os.environ.get("MOONSTREAM_HUMBUG_TOKEN")
    if humbug_token:
        opening_bracket = "[" if args.include_start else "("
        closing_bracket = "]" if args.include_end else ")"
        title = f"Ethereum trending addresses: {opening_bracket}{args.start}, {args.end}{closing_bracket}"
        publish_json(
            "ethereum_trending",
            humbug_token,
            title,
            results,
            tags=[f"crawler_version:{MOONCRAWL_VERSION}"],
        )
    with args.outfile as ofp:
        json.dump(results, ofp)


def main() -> None:
    parser = argparse.ArgumentParser(description="Moonstream crawlers CLI")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Crawlers commands")

    time_now = datetime.now(timezone.utc)

    parser.add_argument(
        "--access-id",
        default=NB_CONTROLLER_ACCESS_ID,
        type=UUID,
        help="User access ID",
    )

    # Blockchain blocks parser
    parser_crawler_blocks = subcommands.add_parser(
        "blocks", description="Blockchain blocks commands"
    )
    parser_crawler_blocks.set_defaults(
        func=lambda _: parser_crawler_blocks.print_help()
    )
    subcommands_crawler_blocks = parser_crawler_blocks.add_subparsers(
        description="Blockchain blocks commands"
    )

    valid_processing_orders = {
        "asc": ProcessingOrder.ASCENDING,
        "desc": ProcessingOrder.DESCENDING,
    }

    def processing_order(raw_order: str) -> ProcessingOrder:
        if raw_order in valid_processing_orders:
            return valid_processing_orders[raw_order]
        raise ValueError(
            f"Invalid processing order ({raw_order}). Valid choices: {valid_processing_orders.keys()}"
        )

    parser_crawler_blocks_sync = subcommands_crawler_blocks.add_parser(
        "synchronize", description="Synchronize to latest blockchain block commands"
    )
    parser_crawler_blocks_sync.add_argument(
        "-s",
        "--start",
        type=int,
        help="(Optional) Block to start synchronization from. Default: None - current Blockchain block minus confirmations ",
    )
    parser_crawler_blocks_sync.add_argument(
        "-c",
        "--confirmations",
        type=int,
        default=0,
        help="Number of confirmations we require before storing a block in the database. (Default: 0)",
    )
    parser_crawler_blocks_sync.add_argument(
        "--order",
        type=processing_order,
        default=ProcessingOrder.ASCENDING,
        help="Order in which to process blocks (choices: desc, asc; default: asc)",
    )
    parser_crawler_blocks_sync.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=MOONSTREAM_CRAWL_WORKERS,
        help=(
            f"Number of processes to use when synchronizing (default: {MOONSTREAM_CRAWL_WORKERS})."
            " If you set to 1, the main process handles synchronization without spawning subprocesses."
        ),
    )
    parser_crawler_blocks_sync.add_argument(
        "--blockchain",
        required=True,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    parser_crawler_blocks_sync.set_defaults(func=crawler_blocks_sync_handler)

    parser_crawler_blocks_add = subcommands_crawler_blocks.add_parser(
        "add", description="Add blockchain blocks commands"
    )
    parser_crawler_blocks_add.add_argument(
        "-b",
        "--blocks",
        required=True,
        help="List of blocks range in format {bottom_block}-{top_block}",
    )
    parser_crawler_blocks_add.add_argument(
        "--blockchain",
        required=True,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    parser_crawler_blocks_add.set_defaults(func=crawler_blocks_add_handler)

    parser_crawler_blocks_missing = subcommands_crawler_blocks.add_parser(
        "missing",
        description="Add missing Blockchain blocks with transactions commands",
    )
    parser_crawler_blocks_missing.add_argument(
        "-b",
        "--blocks",
        help="List of blocks range in format {bottom_block}-{top_block}",
    )
    parser_crawler_blocks_missing.add_argument(
        "-n",
        "--notransactions",
        action="store_true",
        help="Skip crawling block transactions",
    )
    parser_crawler_blocks_missing.add_argument(
        "-l",
        "--lazy",
        action="store_true",
        help="Lazy block adding one by one",
    )
    parser_crawler_blocks_missing.add_argument(
        "--blockchain",
        required=True,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    parser_crawler_blocks_missing.add_argument(
        "--confirmations",
        type=int,
        default=150,
        help="How nuch behind the latest block to start crawling",
    )
    parser_crawler_blocks_missing.add_argument(
        "--shift",
        type=int,
        default=2000,
        help="How many blocks to shift from the latest block",
    )
    parser_crawler_blocks_missing.set_defaults(func=crawler_blocks_missing_handler)

    parser_crawler_trending = subcommands.add_parser(
        "trending", description="Trending addresses on the Blockchain blockchain"
    )
    parser_crawler_trending.add_argument(
        "-s",
        "--start",
        type=dateutil.parser.parse,
        default=(time_now - timedelta(hours=1, minutes=0)).isoformat(),
        help=f"Start time for window to calculate trending addresses in (default: {(time_now - timedelta(hours=1,minutes=0)).isoformat()})",
    )
    parser_crawler_trending.add_argument(
        "--include-start",
        action="store_true",
        help="Set this flag if range should include start time",
    )
    parser_crawler_trending.add_argument(
        "-e",
        "--end",
        type=dateutil.parser.parse,
        default=time_now.isoformat(),
        help=f"End time for window to calculate trending addresses in (default: {time_now.isoformat()})",
    )
    parser_crawler_trending.add_argument(
        "--include-end",
        action="store_true",
        help="Set this flag if range should include end time",
    )
    parser_crawler_trending.add_argument(
        "--humbug",
        default=None,
        help=(
            "If you would like to write this data to a Moonstream journal, please provide a Humbug "
            "token for that here. (This argument overrides any value set in the "
            "MOONSTREAM_HUMBUG_TOKEN environment variable)"
        ),
    )
    parser_crawler_trending.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Optional file to write output to. By default, prints to stdout.",
    )
    parser_crawler_trending.set_defaults(func=crawler_trending_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
