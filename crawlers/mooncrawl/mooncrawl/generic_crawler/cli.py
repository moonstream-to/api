import argparse
import json
import logging
from typing import Optional
from uuid import UUID

from moonstreamdb.blockchain import AvailableBlockchainType
from web3 import Web3
from web3.middleware import geth_poa_middleware

from ..blockchain import connect
from ..db import yield_db_session_ctx
from ..settings import NB_CONTROLLER_ACCESS_ID
from .base import crawl, get_checkpoint, populate_with_events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_nft_crawler(args: argparse.Namespace) -> None:
    logger.info(f"Starting NFT crawler")

    with open("mooncrawl/generic_crawler/abis/erc721.json") as f:
        abi = json.load(f)

    label = args.label_name
    from_block = args.start_block
    to_block = args.end_block

    # january_2021_block = 9013700  # for polygon
    # to_block = 24975113  # for polygon, 15 february 2022

    blockchain_type = AvailableBlockchainType(args.blockchain_type)

    logger.info(f"Blockchain type: {blockchain_type.value}")
    with yield_db_session_ctx() as db_session:
        web3: Optional[Web3] = None
        if args.web3 is None:
            logger.info(
                "No web3 provider URL provided, using default (blockchan.py: connect())"
            )
            web3 = connect(blockchain_type, access_id=args.access_id)
        else:
            logger.info(f"Using web3 provider URL: {args.web3}")
            web3 = Web3(
                Web3.HTTPProvider(args.web3),
            )
            if args.poa:
                logger.info("Using PoA middleware")
                web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        last_crawled_block = get_checkpoint(
            db_session, blockchain_type, from_block, to_block, label
        )

        logger.info(f"Starting from block: {last_crawled_block}")
        crawl(
            db_session,
            web3,
            blockchain_type,
            label,
            abi,
            [],
            from_block=last_crawled_block,
            to_block=to_block,
            batch_size=args.max_blocks_batch,
        )


def populate_with_erc20_transfers(args: argparse.Namespace) -> None:
    logger.info(f"Starting erc20 transfer crawler")

    label = args.label_name
    from_block = args.start_block
    to_block = args.end_block

    with open(args.abi) as f:
        erc20_abi = json.load(f)
        # Taking only transfer event from erc20_abi
        erc20_abi = [
            event
            for event in erc20_abi
            if event["type"] == "event" and event["name"] == "Transfer"
        ]

    blockchain_type = AvailableBlockchainType(args.blockchain_type)

    logger.info(f"Blockchain type: {blockchain_type.value}")
    with yield_db_session_ctx() as db_session:
        web3: Optional[Web3] = None
        if args.web3 is None:
            logger.info(
                "No web3 provider URL provided, using default (blockchan.py: connect())"
            )
            web3 = connect(blockchain_type, access_id=args.access_id)
        else:
            logger.info(f"Using web3 provider URL: {args.web3}")
            web3 = Web3(
                Web3.HTTPProvider(args.web3),
            )
            if args.poa:
                logger.info("Using PoA middleware")
                web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        last_crawled_block = get_checkpoint(
            db_session, blockchain_type, from_block, to_block, label
        )

        logger.info(f"Starting from block: {last_crawled_block}")
        populate_with_events(
            db_session,
            web3,
            blockchain_type,
            label,
            args.label_to_populate,
            erc20_abi,
            last_crawled_block,
            to_block,
            batch_size=args.max_blocks_batch,
        )


def handle_crawl(args: argparse.Namespace) -> None:
    logger.info(f"Starting generic crawler")

    label = args.label_name
    from_block = args.start_block
    to_block = args.end_block

    with open(args.abi) as f:
        abi = json.load(f)

    blockchain_type = AvailableBlockchainType(args.blockchain_type)

    logger.info(f"Blockchain type: {blockchain_type.value}")
    with yield_db_session_ctx() as db_session:
        web3: Optional[Web3] = None
        if args.web3 is None:
            logger.info(
                "No web3 provider URL provided, using default (blockchan.py: connect())"
            )
            web3 = connect(blockchain_type, access_id=args.access_id)
        else:
            logger.info(f"Using web3 provider URL: {args.web3}")
            web3 = Web3(
                Web3.HTTPProvider(args.web3),
            )
            if args.poa:
                logger.info("Using PoA middleware")
                web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        last_crawled_block = get_checkpoint(
            db_session, blockchain_type, from_block, to_block, label
        )

        logger.info(f"Starting from block: {last_crawled_block}")
        crawl_transaction = not args.disable_transactions
        crawl(
            db_session,
            web3,
            blockchain_type,
            label,
            abi,
            secondary_abi=[],
            from_block=last_crawled_block,
            to_block=to_block,
            crawl_transactions=crawl_transaction,
            batch_size=args.max_blocks_batch,
        )


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser.add_argument(
        "--access-id",
        default=NB_CONTROLLER_ACCESS_ID,
        type=UUID,
        help="User access ID",
    )

    crawl_parser = subparsers.add_parser("crawl", help="Crawl with abi")
    crawl_parser.add_argument(
        "--blockchain_type",
        type=str,
        required=True,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    crawl_parser.add_argument(
        "--abi",
        type=str,
        default=None,
        help="Abi of the contract",
    )
    crawl_parser.add_argument(
        "--disable_transactions",
        action="store_true",
        help="Disable transactions crawling",
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
        "--start_block",
        type=int,
        default=None,
    )
    crawl_parser.add_argument(
        "--end_block",
        type=int,
        default=None,
    )

    crawl_parser.add_argument(
        "--max_blocks_batch",
        type=int,
        default=500,
        help="Maximum number of blocks to crawl in a single crawl step",
    )

    crawl_parser.add_argument(
        "--label_name",
        type=str,
        default="erc721",
        help="Label name",
    )

    crawl_parser.set_defaults(func=handle_crawl)

    nft_crawler_parser = subparsers.add_parser(
        "nft",
        help="Run the NFT crawler",
    )

    nft_crawler_parser.add_argument(
        "--blockchain_type",
        type=str,
        required=True,
        choices=[member.value for member in AvailableBlockchainType],
    )
    nft_crawler_parser.add_argument(
        "--web3",
        type=str,
        default=None,
        help="Web3 provider URL",
    )

    nft_crawler_parser.add_argument(
        "--poa",
        action="store_true",
        default=False,
        help="Use PoA middleware",
    )

    nft_crawler_parser.add_argument(
        "--start_block",
        type=int,
        default=None,
    )
    nft_crawler_parser.add_argument(
        "--end_block",
        type=int,
        default=None,
    )

    nft_crawler_parser.add_argument(
        "--max_blocks_batch",
        type=int,
        default=500,
        help="Maximum number of blocks to crawl in a single crawl step",
    )

    nft_crawler_parser.add_argument(
        "--label_name",
        type=str,
        default="erc721",
        help="Label name",
    )

    nft_crawler_parser.set_defaults(func=handle_nft_crawler)

    erc20_populate_parser = subparsers.add_parser(
        "erc20_populate",
        help="Populate erc20 labels",
    )

    erc20_populate_parser.add_argument(
        "--blockchain_type",
        type=str,
        required=True,
        choices=[member.value for member in AvailableBlockchainType],
    )
    erc20_populate_parser.add_argument(
        "--web3",
        type=str,
        default=None,
        help="Web3 provider URL",
    )

    erc20_populate_parser.add_argument(
        "--poa",
        action="store_true",
        default=False,
        help="Use PoA middleware",
    )

    erc20_populate_parser.add_argument(
        "--start_block",
        type=int,
        default=None,
    )
    erc20_populate_parser.add_argument(
        "--end_block",
        type=int,
        default=None,
    )

    erc20_populate_parser.add_argument(
        "--max_blocks_batch",
        type=int,
        default=500,
        help="Maximum number of blocks to crawl in a single crawl step",
    )

    erc20_populate_parser.add_argument(
        "--label_name",
        type=str,
        required=True,
        help="Label name",
    )

    erc20_populate_parser.add_argument(
        "--label_to_populate",
        type=str,
        required=True,
        help="Label name to populate",
    )

    erc20_populate_parser.add_argument(
        "--abi",
        type=str,
        default=None,
        help="Abi of the erc20 contract",
    )

    erc20_populate_parser.set_defaults(func=populate_with_erc20_transfers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
