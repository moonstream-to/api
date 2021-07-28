"""
Moonstream crawlers CLI.
"""
import argparse
from distutils.util import strtobool
import time

from .ethereum import (
    crawl_blocks_executor,
    crawl_blocks,
    check_missing_blocks,
    get_latest_blocks,
)
from .settings import MOONSTREAM_CRAWL_WORKERS


def yield_blocks_numbers_lists(blocks_range_str: str) -> None:
    """
    Generate list of blocks.
    Block steps used to prevent long executor tasks and data loss possibility.
    """
    block_step = 1000

    try:
        blocks_start_end = blocks_range_str.split("-")
        bottom_block_number = int(blocks_start_end[0])
        top_block_number = int(blocks_start_end[1])
        required_blocks_len = top_block_number - bottom_block_number + 1
    except Exception:
        print(
            "Wrong format provided, expected {bottom_block}-{top_block}, as ex. 105-340"
        )
        return

    print(f"Required {required_blocks_len} blocks to process")

    while not top_block_number < bottom_block_number:
        temp_bottom_block_number = top_block_number - block_step
        if temp_bottom_block_number < bottom_block_number:
            temp_bottom_block_number = bottom_block_number - 1
        blocks_numbers_list = list(
            range(top_block_number, temp_bottom_block_number, -1)
        )

        yield blocks_numbers_list

        top_block_number -= block_step


def ethcrawler_blocks_sync_handler(args: argparse.Namespace) -> None:
    """
    Synchronize latest Ethereum blocks with database.
    """
    while True:
        bottom_block_number, top_block_number = get_latest_blocks(
            bool(strtobool(args.transactions))
        )
        if bottom_block_number >= top_block_number:
            print(
                f"Synchronization is unnecessary for blocks {bottom_block_number}-{top_block_number}"
            )
            break
        for blocks_numbers_list in yield_blocks_numbers_lists(
            f"{bottom_block_number}-{top_block_number}"
        ):
            print(f"Adding blocks {blocks_numbers_list[0]}-{blocks_numbers_list[-1]}")
            crawl_blocks_executor(
                block_numbers_list=blocks_numbers_list,
                with_transactions=bool(strtobool(args.transactions)),
            )
        print(f"Synchronized blocks from {bottom_block_number} to {top_block_number}")
        time.sleep(10)


def ethcrawler_blocks_add_handler(args: argparse.Namespace) -> None:
    """
    Add blocks to moonstream database.
    """
    startTime = time.time()

    for blocks_numbers_list in yield_blocks_numbers_lists(args.blocks):
        print(f"Adding blocks {blocks_numbers_list[0]}-{blocks_numbers_list[-1]}")
        crawl_blocks_executor(
            block_numbers_list=blocks_numbers_list,
            with_transactions=bool(strtobool(args.transactions)),
        )

    print(f"Required {time.time() - startTime} with {MOONSTREAM_CRAWL_WORKERS} workers")


def ethcrawler_blocks_missing_handler(args: argparse.Namespace) -> None:
    startTime = time.time()
    missing_blocks_numbers_total = []
    for blocks_numbers_list in yield_blocks_numbers_lists(args.blocks):
        print(
            f"Check missing blocks from {blocks_numbers_list[0]} to {blocks_numbers_list[-1]}"
        )
        missing_blocks_numbers = check_missing_blocks(
            blocks_numbers=blocks_numbers_list,
        )
        missing_blocks_numbers_total.extend(missing_blocks_numbers)
    print(f"Found {len(missing_blocks_numbers_total)} missing blocks")

    time.sleep(5)

    if (len(missing_blocks_numbers_total)) > 0:
        if args.lazy:
            crawl_blocks(
                missing_blocks_numbers_total,
                with_transactions=bool(strtobool(args.transactions)),
            )
        else:
            crawl_blocks_executor(
                missing_blocks_numbers_total,
                with_transactions=bool(strtobool(args.transactions)),
            )
    print(
        f"Required {time.time() - startTime} with {MOONSTREAM_CRAWL_WORKERS} workers "
        f"for {len(missing_blocks_numbers_total)} missing blocks"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Moonstream crawlers CLI")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Crawlers commands")

    parser_ethcrawler = subcommands.add_parser(
        "ethcrawler", description="Ethereum crawler"
    )
    parser_ethcrawler.set_defaults(func=lambda _: parser_ethcrawler.print_help())
    subcommands_ethcrawler = parser_ethcrawler.add_subparsers(
        description="Ethereum crawler commands"
    )

    # Ethereum blocks parser
    parser_ethcrawler_blocks = subcommands_ethcrawler.add_parser(
        "blocks", description="Ethereum blocks commands"
    )
    parser_ethcrawler_blocks.set_defaults(
        func=lambda _: parser_ethcrawler_blocks.print_help()
    )
    subcommands_ethcrawler_blocks = parser_ethcrawler_blocks.add_subparsers(
        description="Ethereum blocks commands"
    )

    parser_ethcrawler_blocks_sync = subcommands_ethcrawler_blocks.add_parser(
        "synchronize", description="Synchronize to latest ethereum block commands"
    )
    parser_ethcrawler_blocks_sync.add_argument(
        "-t",
        "--transactions",
        choices=["True", "False"],
        default="True",
        help="Add or not block transactions",
    )
    parser_ethcrawler_blocks_sync.set_defaults(func=ethcrawler_blocks_sync_handler)

    parser_ethcrawler_blocks_add = subcommands_ethcrawler_blocks.add_parser(
        "add", description="Add ethereum blocks commands"
    )
    parser_ethcrawler_blocks_add.add_argument(
        "-b",
        "--blocks",
        required=True,
        help="List of blocks range in format {bottom_block}-{top_block}",
    )
    parser_ethcrawler_blocks_add.add_argument(
        "-t",
        "--transactions",
        choices=["True", "False"],
        default="True",
        help="Add or not block transactions",
    )
    parser_ethcrawler_blocks_add.set_defaults(func=ethcrawler_blocks_add_handler)

    parser_ethcrawler_blocks_missing = subcommands_ethcrawler_blocks.add_parser(
        "missing", description="Add missing ethereum blocks commands"
    )
    parser_ethcrawler_blocks_missing.add_argument(
        "-b",
        "--blocks",
        required=True,
        help="List of blocks range in format {bottom_block}-{top_block}",
    )
    parser_ethcrawler_blocks_missing.add_argument(
        "-t",
        "--transactions",
        choices=["True", "False"],
        default="True",
        help="Add or not block transactions",
    )
    parser_ethcrawler_blocks_missing.add_argument(
        "-l",
        "--lazy",
        choices=["True", "False"],
        default="False",
        help="Lazy block adding one by one",
    )
    parser_ethcrawler_blocks_missing.set_defaults(
        func=ethcrawler_blocks_missing_handler
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
