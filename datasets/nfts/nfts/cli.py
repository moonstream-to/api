import argparse
import contextlib
import logging
import os
import sqlite3
from typing import Optional, Union

from moonstreamdb.db import yield_db_session_ctx
from web3 import Web3, IPCProvider, HTTPProvider

from .data import event_types, nft_event, BlockBounds
from .datastore import setup_database
from .materialize import create_dataset, EthereumBatchloader


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def web3_connection(web3_uri: Optional[str] = None) -> Web3:
    """
    Connect to the given web3 provider. You may specify a web3 provider either as a path to an IPC
    socket on your filesystem or as an HTTP(S) URI to a JSON RPC provider.

    If web3_uri is not provided or is set to None, this function attempts to use the default behavior
    of the web3.py IPCProvider (one of the steps is looking for .ethereum/geth.ipc, but there may be others).
    """
    web3_provider: Union[IPCProvider, HTTPProvider] = Web3.IPCProvider()
    if web3_uri is not None:
        if web3_uri.startswith("http://") or web3_uri.startswith("https://"):
            web3_provider = Web3.HTTPProvider(web3_uri)
        else:
            web3_provider = Web3.IPCProvider(web3_uri)
    web3_client = Web3(web3_provider)
    return web3_client


def handle_initdb(args: argparse.Namespace) -> None:
    with contextlib.closing(sqlite3.connect(args.datastore)) as conn:
        setup_database(conn)


def handle_materialize(args: argparse.Namespace) -> None:
    event_type = nft_event(args.type)
    bounds: Optional[BlockBounds] = None
    if args.start is not None:
        bounds = BlockBounds(starting_block=args.start, ending_block=args.end)
    elif args.end is not None:
        raise ValueError("You cannot set --end unless you also set --start")

    batch_loader = EthereumBatchloader(jrpc_url=args.jrpc)

    logger.info(f"Materializing NFT events to datastore: {args.datastore}")
    logger.info(f"Block bounds: {bounds}")

    with yield_db_session_ctx() as db_session, contextlib.closing(
        sqlite3.connect(args.datastore)
    ) as moonstream_datastore:
        create_dataset(
            moonstream_datastore,
            db_session,
            args.web3,
            event_type,
            bounds,
            args.batch_size,
            batch_loader
        )


def main() -> None:
    """
    "nfts" command handler.

    When reading this code, to find the definition of any of the "nfts" subcommands, grep for comments
    of the form:
    # Command: nfts <subcommand>
    """
    default_web3_provider = os.environ.get("MOONSTREAM_WEB3_PROVIDER")

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
        "--web3",
        default=default_web3_provider,
        type=web3_connection,
        help=f"Web3 provider to use when collecting data directly from the Ethereum blockchain (default: {default_web3_provider})",
    )
    parser_materialize.add_argument(
        "--jrpc",
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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
