"""
A command line tool to crawl information about NFTs from various sources.
"""
import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional, cast

from bugout.app import Bugout
from bugout.journal import SearchOrder
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumBlock
from sqlalchemy.orm.session import Session
from web3 import Web3

from ..ethereum import connect
from ..publish import publish_json
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
    MOONSTREAM_IPC_PATH,
    NFT_HUMBUG_TOKEN,
)
from ..version import MOONCRAWL_VERSION
from .ethereum import (
    MINT_LABEL,
    SUMMARY_KEY_ARGS,
    SUMMARY_KEY_END_BLOCK,
    SUMMARY_KEY_ID,
    SUMMARY_KEY_NUM_BLOCKS,
    SUMMARY_KEY_START_BLOCK,
    TRANSFER_LABEL,
    add_labels,
)
from .ethereum import summary as ethereum_summary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BLOCKS_PER_SUMMARY = 40


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


def get_latest_block_from_node(web3_client: Web3):
    return web3_client.eth.block_number


def get_latest_summary_block() -> Optional[int]:
    try:

        bugout_client = Bugout()
        query = "#crawl_type:nft_ethereum"

        events = bugout_client.search(
            MOONSTREAM_ADMIN_ACCESS_TOKEN,
            MOONSTREAM_DATA_JOURNAL_ID,
            query,
            limit=1,
            timeout=30.0,
            order=SearchOrder.DESCENDING,
        )
        if not events.results:
            logger.warning("There is no summaries in Bugout")
            return None

        last_event = events.results[0]
        content = cast(str, last_event.content)
        return json.loads(content)["end_block"]
    except Exception as e:
        logger.error(f"Failed to get summary from Bugout : {e}")
        return None


# TODO(yhtiyar):
# Labeling status should be stored in new tabel, and
# latest label should be got from there
def get_latest_nft_labeled_block(db_session: Session) -> Optional[int]:
    raise NotImplementedError()


def sync_labels(db_session: Session, web3_client: Web3, start: Optional[int]) -> int:
    if start is None:
        logger.info(
            "Syncing label start block is not given, getting it from latest nft label in db"
        )
        start = get_latest_nft_labeled_block(db_session)
        if start is None:
            logger.warning(
                "Didn't find any nft labels in db, starting sync from 1st Jan 2021 before now"
            )
            start_date = datetime(2021, 1, 1, tzinfo=timezone.utc)
            start = (
                db_session.query(EthereumBlock)
                .filter(EthereumBlock.timestamp >= start_date.timestamp())
                .order_by(EthereumBlock.timestamp.asc())
                .limit(1)
                .one()
            ).block_number
    logger.info(f"Syncing labels, start block: {start}")
    end = get_latest_block_from_node(web3_client)
    if start > end:
        logger.warn(f"Start block {start} is greater than latest_block {end} in db")
        logger.warn("Maybe ethcrawler is not syncing or nft sync is up to date")
        return start - 1
    logger.info(f"Labeling blocks {start}-{end}")
    add_labels(web3_client, db_session, start, end)
    return end


def sync_summaries(
    db_session: Session,
    start: Optional[int],
    end: int,
) -> int:
    if start is None:
        logger.info(
            "Syncing summary start block is not given, getting it from latest nft summary from Bugout"
        )
        start = get_latest_summary_block()
        if start is not None:
            start += 1
        else:
            logger.info(
                "There is no entry in Bugout, starting to create summaries from 1st Jan 2021"
            )
            start_date = datetime(2021, 1, 1, tzinfo=timezone.utc)
            start = (
                db_session.query(EthereumBlock)
                .filter(EthereumBlock.timestamp >= start_date.timestamp())
                .order_by(EthereumBlock.timestamp.asc())
                .limit(1)
                .one()
            ).block_number

    logger.info(f"Syncing summaries start_block: {start}")
    batch_end = start + BLOCKS_PER_SUMMARY - 1
    if batch_end > end:
        logger.warn("Syncing summaries is not required")
    while batch_end <= end:
        summary_result = ethereum_summary(db_session, start, batch_end)
        push_summary(summary_result)
        logger.info(f"Pushed summary of blocks : {start}-{batch_end}")
        start = batch_end + 1
        batch_end += BLOCKS_PER_SUMMARY

    if start == end:
        return end
    else:
        return start - 1


def ethereum_sync_handler(args: argparse.Namespace) -> None:
    web3_client = web3_client_from_cli_or_env(args)

    with yield_db_session_ctx() as db_session:
        logger.info("Initial labeling:")
        last_labeled = sync_labels(db_session, web3_client, args.start)
        logger.info("Initial summary creation:")
        last_summary_created = sync_summaries(
            db_session,
            args.start,
            last_labeled,
        )
        while True:
            logger.info("Syncing")
            last_labeled = sync_labels(db_session, web3_client, last_labeled + 1)
            last_summary_created = sync_summaries(
                db_session,
                last_summary_created + 1,
                last_labeled,
            )
            sleep_time = 10 * 60
            logger.info(f"Going to sleep for {sleep_time}s")
            time.sleep(sleep_time)


def ethereum_label_handler(args: argparse.Namespace) -> None:
    web3_client = web3_client_from_cli_or_env(args)
    with yield_db_session_ctx() as db_session:
        add_labels(web3_client, db_session, args.start, args.end, args.address)


def push_summary(result: Dict[str, Any], humbug_token: Optional[str] = None):
    if humbug_token is None:
        humbug_token = NFT_HUMBUG_TOKEN
    title = (
        f"NFT activity on the Ethereum blockchain: crawled at: {result['crawled_at'] })"
    )

    tags = [
        f"crawler_version:{MOONCRAWL_VERSION}",
        f"summary_id:{result.get(SUMMARY_KEY_ID, '')}",
        f"start_block:{result.get(SUMMARY_KEY_START_BLOCK)}",
        f"end_block:{result.get(SUMMARY_KEY_END_BLOCK)}",
    ]

    # Add an "error:missing_blocks" tag for all summaries in which the number of blocks processed
    # is not equal to the expected number of blocks.
    args = result.get(SUMMARY_KEY_ARGS, {})
    args_start = args.get("start")
    args_end = args.get("end")
    expected_num_blocks = None
    if args_start is not None and args_end is not None:
        expected_num_blocks = cast(int, args_end) - cast(int, args_start) + 1
    num_blocks = result.get(SUMMARY_KEY_NUM_BLOCKS)
    if (
        expected_num_blocks is None
        or num_blocks is None
        or num_blocks != expected_num_blocks
    ):
        tags.append("error:missing_blocks")

    # TODO(yhtyyar, zomglings): Also add checkpoints in database for nft labelling. This way, we can
    # add an "error:stale" tag to summaries generated before nft labels were processed for the
    # block range in the summary.

    created_at = result.get("date_range", {}).get("end_time")

    publish_json(
        "nft_ethereum",
        humbug_token,
        title,
        result,
        tags=tags,
        wait=True,
        created_at=created_at,
    )


def ethereum_summary_handler(args: argparse.Namespace) -> None:

    with yield_db_session_ctx() as db_session:
        result = ethereum_summary(db_session, args.start, args.end)
    push_summary(result, args.humbug)
    with args.outfile as ofp:
        json.dump(result, ofp)


def main() -> None:
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
        "-s",
        "--start",
        type=int,
        required=True,
        help=f"Start block for window to calculate NFT statistics",
    )
    parser_ethereum_summary.add_argument(
        "-e",
        "--end",
        type=int,
        required=True,
        help=f"End block for window to calculate NFT statistics",
    )
    parser_ethereum_summary.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Optional file to write output to. By default, prints to stdout.",
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
    parser_ethereum_summary.set_defaults(func=ethereum_summary_handler)

    parser_ethereum_sync = subparsers_ethereum.add_parser(
        "synchronize",
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
