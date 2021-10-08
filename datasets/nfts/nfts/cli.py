import argparse
import contextlib
import logging
import os
import sqlite3
from shutil import copyfile
from typing import Optional

from moonstreamdb.db import yield_db_session_ctx

from .enrich import EthereumBatchloader, enrich
from .data import EventType, event_types, nft_event, BlockBounds
from .datastore import setup_database, import_data, filter_data
from .derive import (
    current_owners,
    current_market_values,
    current_values_distribution,
    transfer_statistics_by_address,
    quantile_generating,
    mint_holding_times,
    transfer_holding_times,
    transfers_mints_connection_table,
)
from .materialize import create_dataset


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


derive_functions = {
    "current_owners": current_owners,
    "current_market_values": current_market_values,
    "current_values_distribution": current_values_distribution,
    "transfer_statistics_by_address": transfer_statistics_by_address,
    "quantile_generating": quantile_generating,
    "transfers_mints_connection_table": transfers_mints_connection_table,
    "mint_holding_times": mint_holding_times,
    "transfer_holding_times": transfer_holding_times,
}


def handle_initdb(args: argparse.Namespace) -> None:
    with contextlib.closing(sqlite3.connect(args.datastore)) as conn:
        setup_database(conn)


def handle_import_data(args: argparse.Namespace) -> None:
    event_type = nft_event(args.type)
    with contextlib.closing(
        sqlite3.connect(args.target)
    ) as target_conn, contextlib.closing(sqlite3.connect(args.source)) as source_conn:
        import_data(target_conn, source_conn, event_type, args.batch_size)


def handle_filter_data(args: argparse.Namespace) -> None:

    with contextlib.closing(sqlite3.connect(args.source)) as source_conn:

        if args.target == args.source and args.source is not None:
            sqlite_path = f"{args.target}.dump"
        else:
            sqlite_path = args.target

        print(f"Creating new database:{sqlite_path}")

        copyfile(args.source, sqlite_path)

    # do connection
    with contextlib.closing(sqlite3.connect(sqlite_path)) as source_conn:
        print("Start filtering")
        filter_data(
            source_conn,
            start_time=args.start_time,
            end_time=args.end_time,
        )
        print("Filtering end.")
        for index, function_name in enumerate(derive_functions.keys()):
            print(
                f"Derive process {function_name} {index+1}/{len(derive_functions.keys())}"
            )
            derive_functions[function_name](source_conn)

        # Apply derive to new data


def handle_materialize(args: argparse.Namespace) -> None:
    event_type = nft_event(args.type)
    bounds: Optional[BlockBounds] = None
    if args.start is not None:
        bounds = BlockBounds(starting_block=args.start, ending_block=args.end)
    elif args.end is not None:
        raise ValueError("You cannot set --end unless you also set --start")

    batch_loader = EthereumBatchloader(jsonrpc_url=args.jsonrpc)

    logger.info(f"Materializing NFT events to datastore: {args.datastore}")
    logger.info(f"Block bounds: {bounds}")

    with yield_db_session_ctx() as db_session, contextlib.closing(
        sqlite3.connect(args.datastore)
    ) as moonstream_datastore:
        create_dataset(
            moonstream_datastore,
            db_session,
            event_type,
            bounds,
            args.batch_size,
        )


def handle_enrich(args: argparse.Namespace) -> None:

    batch_loader = EthereumBatchloader(jsonrpc_url=args.jsonrpc)

    logger.info(f"Enriching NFT events in datastore: {args.datastore}")

    with contextlib.closing(sqlite3.connect(args.datastore)) as moonstream_datastore:
        enrich(
            moonstream_datastore,
            EventType.TRANSFER,
            batch_loader,
            args.batch_size,
        )

        enrich(
            moonstream_datastore,
            EventType.MINT,
            batch_loader,
            args.batch_size,
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
        "--jsonrpc",
        default=default_web3_provider,
        type=str,
        help=f"Http uri provider to use when collecting data directly from the Ethereum blockchain (default: {default_web3_provider})",
    )
    parser_materialize.add_argument(
        "-t",
        "--type",
        choices=event_types,
        help="Type of event to materialize intermediate data for",
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

    parser_import_data = subcommands.add_parser(
        "import-data",
        description="Import data from another source NFTs dataset datastore. This operation is performed per table, and replaces the existing table in the target datastore.",
    )
    parser_import_data.add_argument(
        "--target",
        required=True,
        help="Datastore into which you want to import data",
    )
    parser_import_data.add_argument(
        "--source", required=True, help="Datastore from which you want to import data"
    )
    parser_import_data.add_argument(
        "--type",
        required=True,
        choices=event_types,
        help="Type of data you would like to import from source to target",
    )
    parser_import_data.add_argument(
        "-N",
        "--batch-size",
        type=int,
        default=10000,
        help="Batch size for database commits into target datastore.",
    )
    parser_import_data.set_defaults(func=handle_import_data)

    # Create dump of filtered data

    parser_filtered_copy = subcommands.add_parser(
        "filter-data",
        description="Create copy of database with applied filters.",
    )
    parser_filtered_copy.add_argument(
        "--target",
        required=True,
        help="Datastore into which you want to import data",
    )
    parser_filtered_copy.add_argument(
        "--source", required=True, help="Datastore from which you want to import data"
    )
    parser_filtered_copy.add_argument(
        "--start-time",
        required=False,
        type=int,
        help="Start timestamp.",
    )
    parser_filtered_copy.add_argument(
        "--end-time",
        required=False,
        type=int,
        help="End timestamp.",
    )

    parser_filtered_copy.set_defaults(func=handle_filter_data)

    parser_enrich = subcommands.add_parser(
        "enrich", description="enrich dataset from geth node"
    )
    parser_enrich.add_argument(
        "-d",
        "--datastore",
        required=True,
        help="Path to SQLite database representing the dataset",
    )
    parser_enrich.add_argument(
        "--jsonrpc",
        default=default_web3_provider,
        type=str,
        help=f"Http uri provider to use when collecting data directly from the Ethereum blockchain (default: {default_web3_provider})",
    )
    parser_enrich.add_argument(
        "-n",
        "--batch-size",
        type=int,
        default=1000,
        help="Number of events to process per batch",
    )
    parser_enrich.set_defaults(func=handle_enrich)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
