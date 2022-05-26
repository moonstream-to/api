import argparse
import contextlib
from enum import Enum
import logging
import os
import sqlite3
from shutil import copyfile
from typing import Optional, Union

from mooncrawl.data import AvailableBlockchainType
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumLabel, PolygonLabel

from .data import BlockBounds
from .datastore import setup_database, get_last_saved_block
from .derive import (
    current_owners,
    current_market_values,
    current_values_distribution,
    transfer_statistics_by_address,
    quantile_generating,
    mint_holding_times,
    ownership_transitions,
    transfer_holding_times,
    transfers_mints_connection_table,
)
from .materialize import crawl_erc721_labels


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


derive_functions = {
    "current_owners": current_owners,
    "current_market_values": current_market_values,
    "current_values_distribution": current_values_distribution,
    "mint_holding_times": mint_holding_times,
    "ownership_transitions": ownership_transitions,
    "quantile_generating": quantile_generating,
    "transfer_holding_times": transfer_holding_times,
    "transfers_mints_connection_table": transfers_mints_connection_table,
    "transfer_statistics_by_address": transfer_statistics_by_address,
}


class Blockchain(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"


def handle_initdb(args: argparse.Namespace) -> None:
    with contextlib.closing(sqlite3.connect(args.datastore)) as conn:
        setup_database(conn)


def _get_label_model(
    blockchain: AvailableBlockchainType,
) -> Union[EthereumLabel, PolygonLabel]:
    if blockchain == AvailableBlockchainType.ETHEREUM:
        return EthereumLabel
    elif blockchain == AvailableBlockchainType.POLYGON:
        return PolygonLabel
    else:
        raise ValueError(f"Unknown blockchain: {blockchain}")


def handle_materialize(args: argparse.Namespace) -> None:

    if args.start is None or args.end is None:
        raise ValueError("Set --end  --start")

    bounds: Optional[BlockBounds] = None
    if args.start is not None:
        bounds = BlockBounds(starting_block=args.start, ending_block=args.end)

    logger.info(f"Materializing NFT events to datastore: {args.datastore}")
    logger.info(f"Block bounds: {bounds}")

    blockchain_type = AvailableBlockchainType(args.blockchain)
    label_model = _get_label_model(blockchain_type)

    with yield_db_session_ctx() as db_session, contextlib.closing(
        sqlite3.connect(args.datastore)
    ) as moonstream_datastore:
        last_saved_block = get_last_saved_block(moonstream_datastore, args.blockchain)
        logger.info(f"Last saved block: {last_saved_block}")
        if last_saved_block and last_saved_block >= bounds.starting_block:
            logger.info(
                f"Skipping blocks {bounds.starting_block}-{last_saved_block}, starting from {last_saved_block + 1}"
            )
            bounds.starting_block = last_saved_block + 1

        crawl_erc721_labels(
            db_session,
            moonstream_datastore,
            label_model,
            start_block=bounds.starting_block,
            end_block=bounds.ending_block,
            batch_size=args.batch_size,
        )


def handle_derive(args: argparse.Namespace) -> None:
    with contextlib.closing(sqlite3.connect(args.datastore)) as moonstream_datastore:
        calling_functions = []
        if not args.derive_functions:
            calling_functions.extend(derive_functions.keys())
        else:
            calling_functions.extend(args.derive_functions)

        for function_name in calling_functions:
            if function_name in calling_functions:
                derive_functions[function_name](moonstream_datastore)
    logger.info("Done!")


def main() -> None:
    """
    "nfts" command handler.

    When reading this code, to find the definition of any of the "nfts" subcommands, grep for comments
    of the form:
    # Command: nfts <subcommand>
    """
    default_web3_provider = os.environ.get("MOONSTREAM_WEB3_PROVIDER")
    if default_web3_provider is not None and not default_web3_provider.startswith(
        "http"
    ):
        raise ValueError(
            f"Please either unset MOONSTREAM_WEB3_PROVIDER environment variable or set it to an HTTP/HTTPS URL. Current value: {default_web3_provider}"
        )

    parser = argparse.ArgumentParser(
        description="Tools to work with the Moonstream NFTs dataset"
    )
    subcommands = parser.add_subparsers(title="Subcommands")

    # Command: nfts initdb
    parser_initdb = subcommands.add_parser(
        "initdb",
        description="Initialize an SQLite datastore for the Moonstream NFTs dataset",
    )
    parser_initdb.add_argument("datastore")
    parser_initdb.set_defaults(func=handle_initdb)

    # Command: nfts materialize
    parser_materialize = subcommands.add_parser(
        "materialize", description="Create/update the NFTs dataset"
    )
    parser_materialize.add_argument(
        "-d",
        "--datastore",
        required=True,
        help="Path to SQLite database representing the dataset",
    )

    parser_materialize.add_argument(
        "--start", type=int, default=None, help="Starting block number"
    )
    parser_materialize.add_argument(
        "--end", type=int, default=None, help="Ending block number"
    )
    parser_materialize.add_argument(
        "-n",
        "--batch-size",
        type=int,
        default=1000,
        help="Number of events to process per batch",
    )

    parser_materialize.add_argument(
        "--blockchain",
        type=str,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )

    parser_materialize.set_defaults(func=handle_materialize)

    parser_derive = subcommands.add_parser(
        "derive", description="Create/updated derived data in the dataset"
    )
    parser_derive.add_argument(
        "-d",
        "--datastore",
        required=True,
        help="Path to SQLite database representing the dataset",
    )
    parser_derive.add_argument(
        "-f",
        "--derive-functions",
        required=False,
        nargs="+",
        help=f"Functions wich will call from derive module availabel {list(derive_functions.keys())}",
    )
    parser_derive.set_defaults(func=handle_derive)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
