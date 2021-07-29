"""
Moonstream crawlers CLI.
"""
import argparse
from distutils.util import strtobool
import json
import sys
import time
from typing import List

from .ethereum import crawl, check_missing_blocks, process_contract_deployments
from .settings import MOONSTREAM_CRAWL_WORKERS


def get_blocks_numbers_lists(
    bottom_block_number: int, top_block_number: int
) -> List[List[int]]:
    """
    Generate list of blocks.
    """
    block_step = 1000
    blocks_numbers_list_raw = list(range(top_block_number, bottom_block_number - 1, -1))
    blocks_numbers_list_raw_len = len(blocks_numbers_list_raw)
    # Block steps used to prevent long executor tasks and data loss possibility
    # Block step 2 convert [1,2,3] -> [[1,2],[3]]
    if blocks_numbers_list_raw_len / block_step > 1:
        blocks_numbers_lists = [
            blocks_numbers_list_raw[i : i + block_step]
            for i in range(0, blocks_numbers_list_raw_len, block_step)
        ]
    else:
        blocks_numbers_lists = [blocks_numbers_list_raw]

    return blocks_numbers_lists, blocks_numbers_list_raw_len


def ethcrawler_blocks_add_handler(args: argparse.Namespace) -> None:
    """
    Add blocks to moonstream database.
    """
    try:
        blocks_start_end = args.blocks.split("-")
        bottom_block_number = int(blocks_start_end[0])
        top_block_number = int(blocks_start_end[1])
    except Exception:
        print(
            "Wrong format provided, expected {bottom_block}-{top_block}, as ex. 105-340"
        )
        return

    blocks_numbers_lists, blocks_numbers_list_raw_len = get_blocks_numbers_lists(
        bottom_block_number, top_block_number
    )

    startTime = time.time()
    for blocks_numbers_list in blocks_numbers_lists:
        crawl(
            block_numbers_list=blocks_numbers_list,
            with_transactions=bool(strtobool(args.transactions)),
        )
    print(
        f"Required time: {time.time() - startTime} for: {blocks_numbers_list_raw_len} "
        f"blocks with {MOONSTREAM_CRAWL_WORKERS} workers"
    )


def ethcrawler_blocks_missing_handler(args: argparse.Namespace) -> None:
    try:
        blocks_start_end = args.blocks.split("-")
        bottom_block_number = int(blocks_start_end[0])
        top_block_number = int(blocks_start_end[1])
    except Exception:
        print(
            "Wrong format provided, expected {bottom_block}-{top_block}, as ex. 105-340"
        )
        return

    blocks_numbers_lists, blocks_numbers_list_raw_len = get_blocks_numbers_lists(
        bottom_block_number, top_block_number
    )
    startTime = time.time()
    missing_blocks_numbers_total = []
    for blocks_numbers_list in blocks_numbers_lists:
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
        crawl(
            missing_blocks_numbers_total,
            with_transactions=bool(strtobool(args.transactions)),
        )
    print(
        f"Required time: {time.time() - startTime} for: {blocks_numbers_list_raw_len} "
        f"blocks with {MOONSTREAM_CRAWL_WORKERS} workers"
        f" with {len(missing_blocks_numbers_total)} missing blocks"
    )


def ethcrawler_contracts_update_handler(args: argparse.Namespace) -> None:
    results = process_contract_deployments()
    with args.outfile:
        json.dump(results, args.outfile)


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
        default="False",
        help="Add or not block transactions",
    )
    parser_ethcrawler_blocks_missing.set_defaults(
        func=ethcrawler_blocks_missing_handler
    )

    parser_ethcrawler_contracts = subcommands_ethcrawler.add_parser(
        "contracts", description="Ethereum smart contract related crawlers"
    )
    parser_ethcrawler_contracts.set_defaults(
        func=lambda _: parser_ethcrawler_contracts.print_help()
    )
    subcommands_ethcrawler_contracts = parser_ethcrawler_contracts.add_subparsers(
        description="Ethereum contracts commands"
    )

    parser_ethcrawler_contracts_update = subcommands_ethcrawler_contracts.add_parser(
        "update",
        description="Update smart contract registry to include newly deployed smart contracts",
    )
    parser_ethcrawler_contracts_update.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="(Optional) File to write new (transaction_hash, contract_address) pairs to",
    )
    parser_ethcrawler_contracts_update.set_defaults(
        func=ethcrawler_contracts_update_handler
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
