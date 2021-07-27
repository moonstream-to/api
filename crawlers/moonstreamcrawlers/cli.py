"""
Moonstream crawlers CLI.
"""
import argparse
from distutils.util import strtobool
import time

from .ethereum import crawl
from .settings import MOONSTREAM_CRAWL_WORKERS


def ethcrawler_blocks_add_handler(args: argparse.Namespace) -> None:
    """
    Add blocks to moonstream database.
    """
    try:
        blocks_start_end = args.blocks.split("-")
        top_block_number = int(blocks_start_end[1])
        bottom_block_number = int(blocks_start_end[0])
    except Exception:
        print(
            "Wrong format provided, expected {bottom_block}-{top_block}, as ex. 105-340"
        )
        return

    block_step = 1000
    blocks_numbers_list_raw = list(range(top_block_number, bottom_block_number - 1, -1))
    blocks_numbers_list_raw_len = len(blocks_numbers_list_raw)
    # Block steps used to prevent long executor tasks and data loss possibility
    # Block step 2 convert [1,2,3] -> [[1,2],[3]]
    if len(blocks_numbers_list_raw) / block_step > 1:
        blocks_numbers_lists = [
            blocks_numbers_list_raw[i : i + block_step]
            for i in range(0, blocks_numbers_list_raw_len, block_step)
        ]
    else:
        blocks_numbers_lists = [blocks_numbers_list_raw]

    startTime = time.time()
    for blocks_numbers_list in blocks_numbers_lists:
        crawl(
            blocks_numbers=blocks_numbers_list,
            with_transactions=bool(strtobool(args.transactions)),
            check=bool(strtobool(args.check)),
        )
    print(
        f"Required time: {time.time() - startTime} for: {blocks_numbers_list_raw_len} "
        f"blocks with {MOONSTREAM_CRAWL_WORKERS} workers"
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
        default="False",
        help="Add or not block transactions",
    )
    parser_ethcrawler_blocks_add.add_argument(
        "-c",
        "--check",
        choices=["True", "False"],
        default="False",
        help="If True, it will check existence of block and transaction before write to database",
    )

    parser_ethcrawler_blocks_add.set_defaults(func=ethcrawler_blocks_add_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
