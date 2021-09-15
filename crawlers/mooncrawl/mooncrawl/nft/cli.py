"""
A command line tool to crawl information about NFTs from various sources.
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
import sys
import time
from typing import Any, Dict, cast

import dateutil.parser
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumBlock
from sqlalchemy.orm.session import Session
from web3 import Web3

from ..ethereum import connect
from .ethereum import summary as ethereum_summary, add_labels
from ..publish import publish_json
from ..settings import MOONSTREAM_IPC_PATH
from ..version import MOONCRAWL_VERSION


def web3_client_from_cli_or_env(args: argparse.Namespace) -> Web3:
    """
    Returns a web3 client either by parsing "--web3" argument on the given arguments or by looking up
    the MOONSTREAM_IPC_PATH environment variable.
    """
    web3_connection_string = MOONSTREAM_IPC_PATH
    args_web3 = vars(args).get("web3")
    if args_web3 is not None:
        web3_connection_string = cast(str, args_web3)
    if web3_connection_string is None:
        raise ValueError(
            "Could not find Web3 connection information in arguments or in MOONSTREAM_IPC_PATH environment variable"
        )
    return connect(web3_connection_string)


def get_latest_block_from_db(db_session: Session):
    return (
        db_session.query(EthereumBlock)
        .order_by(EthereumBlock.timestamp.desc())
        .limit(1)
        .one()
    )


def ethereum_sync_handler(args: argparse.Namespace) -> None:
    web3_client = web3_client_from_cli_or_env(args)
    humbug_token = os.environ.get("MOONSTREAM_HUMBUG_TOKEN")
    if humbug_token is None:
        raise ValueError("MOONSTREAM_HUMBUG_TOKEN env variable is not set")

    with yield_db_session_ctx() as db_session:
        start = args.start
        if start is None:
            time_now = datetime.now(timezone.utc)
            week_ago = time_now - timedelta(weeks=1)
            start = (
                db_session.query(EthereumBlock)
                .filter(EthereumBlock.timestamp >= week_ago.timestamp())
                .order_by(EthereumBlock.timestamp.asc())
                .limit(1)
                .one()
            ).block_number

        latest_block = get_latest_block_from_db(db_session)
        end = latest_block.block_number
        assert (
            start <= end
        ), f"Start block {start} is greater than latest_block {end} in db"

        while True:
            print(f"Labeling blocks {start}-{end}")
            add_labels(web3_client, db_session, start, end)

            end_time = datetime.fromtimestamp(latest_block.timestamp, timezone.utc)
            print(f"Creating summary with endtime={end_time}")
            result = ethereum_summary(db_session, end_time)
            push_summary(result, end, humbug_token)

            sleep_time = 60 * 60
            print(f"Going to sleep for:{sleep_time}s")
            time.sleep(sleep_time)

            start = end + 1
            latest_block = get_latest_block_from_db(db_session)
            end = latest_block.block_number


def ethereum_label_handler(args: argparse.Namespace) -> None:
    web3_client = web3_client_from_cli_or_env(args)
    with yield_db_session_ctx() as db_session:
        add_labels(web3_client, db_session, args.start, args.end, args.address)


def push_summary(result: Dict[str, Any], end_block_no: int, humbug_token: str):

    title = f"NFT activity on the Ethereum blockchain: end time: {result['crawled_at'] } (block {end_block_no})"
    publish_json(
        "nft_ethereum",
        humbug_token,
        title,
        result,
        tags=[f"crawler_version:{MOONCRAWL_VERSION}", f"end_block:{end_block_no}"],
        wait=False,
    )


def ethereum_summary_handler(args: argparse.Namespace) -> None:
    with yield_db_session_ctx() as db_session:
        result = ethereum_summary(db_session, args.end)

    # humbug_token = args.humbug
    # if humbug_token is None:
    #     humbug_token = os.environ.get("MOONSTREAM_HUMBUG_TOKEN")
    # if humbug_token:
    #     title = f"NFT activity on the Ethereum blockchain: {start_time} (block {start_block}) to {end_time} (block {end_block})"
    #     publish_json(
    #         "nft_ethereum",
    #         humbug_token,
    #         title,
    #         result,
    #         tags=[f"crawler_version:{MOONCRAWL_VERSION}"],
    #         wait=False,
    #     )
    with args.outfile as ofp:
        json.dump(result, ofp)


def main() -> None:
    time_now = datetime.now(timezone.utc)

    parser = argparse.ArgumentParser(description="Moonstream NFT crawlers")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Subcommands")

    parser_ethereum = subcommands.add_parser(
        "ethereum",
        description="Collect information about NFTs from Ethereum blockchains",
    )
    parser_ethereum.set_defaults(func=lambda _: parser_ethereum.print_help())
    subparsers_ethereum = parser_ethereum.add_subparsers()

    parser_ethereum_label = subparsers_ethereum.add_parser(
        "label",
        description="Label addresses and transactions in databse using crawled NFT transfer information",
    )
    parser_ethereum_label.add_argument(
        "-s",
        "--start",
        type=int,
        default=None,
        help="Starting block number (inclusive if block available)",
    )
    parser_ethereum_label.add_argument(
        "-e",
        "--end",
        type=int,
        default=None,
        help="Ending block number (inclusive if block available)",
    )
    parser_ethereum_label.add_argument(
        "-a",
        "--address",
        type=str,
        default=None,
        help="(Optional) NFT contract address that you want to limit the crawl to, e.g. 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d for CryptoKitties.",
    )
    parser_ethereum_label.add_argument(
        "--web3",
        type=str,
        default=None,
        help="(Optional) Web3 connection string. If not provided, uses the value specified by MOONSTREAM_IPC_PATH environment variable.",
    )
    parser_ethereum_label.set_defaults(func=ethereum_label_handler)

    parser_ethereum_summary = subparsers_ethereum.add_parser(
        "summary", description="Generate Ethereum NFT summary"
    )
    parser_ethereum_summary.add_argument(
        "-e",
        "--end",
        type=dateutil.parser.parse,
        default=time_now.isoformat(),
        help=f"End time for window to calculate NFT statistics (default: {time_now.isoformat()})",
    )
    parser_ethereum_summary.add_argument(
        "--humbug",
        default=None,
        help=(
            "If you would like to write this data to a Moonstream journal, please provide a Humbug "
            "token for that here. (This argument overrides any value set in the "
            "MOONSTREAM_HUMBUG_TOKEN environment variable)"
        ),
    )
    parser_ethereum_summary.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Optional file to write output to. By default, prints to stdout.",
    )
    parser_ethereum_summary.set_defaults(func=ethereum_summary_handler)

    parser_ethereum_sync = subparsers_ethereum.add_parser(
        "sync",
        description="Label addresses and transactions in databse using crawled NFT transfer information, sync mode",
    )
    parser_ethereum_sync.add_argument(
        "-s",
        "--start",
        type=int,
        required=False,
        help="Starting block number (inclusive if block available)",
    )
    parser_ethereum_sync.set_defaults(func=ethereum_sync_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
