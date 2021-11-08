import argparse
import contextlib
import logging
import os
import sqlite3
from shutil import copyfile
from typing import Optional


from moonstreamdb.db import yield_db_session_ctx

from .materialize import add_contract_deployments
from .datastore import setup_database
from .data import BlockBounds


def handle_initdb(args: argparse.Namespace) -> None:
    with contextlib.closing(sqlite3.connect(args.datastore)) as conn:
        setup_database(conn)


def handle_materialize(args: argparse.Namespace) -> None:
    bounds: Optional[BlockBounds] = None
    if args.start is not None:
        bounds = BlockBounds(starting_block=args.start, ending_block=args.end)
    elif args.end is not None:
        raise ValueError("You cannot set --end unless you also set --start")
    with yield_db_session_ctx() as db_session, contextlib.closing(
        sqlite3.connect(args.datastore)
    ) as datastore:
        add_contract_deployments(
            db_session, datastore, batch_size=args.batch_size, bounds=bounds
        )


def generate_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a database of contracts deployed on Ethereum."
    )
    subcommands = parser.add_subparsers(dest="subcommand", title="subcommands")

    parser_initdb = subcommands.add_parser(
        "initdb",
        description="Initialize an SQLite datastore for contract deployments",
    )
    parser_initdb.add_argument(
        "-d",
        "--datastore",
        required=True,
        help="Path to SQLite database representing the dataset",
    )
    parser_initdb.set_defaults(func=handle_initdb)

    parser_materialize = subcommands.add_parser(
        "materialize",
        description="Materialize the contract deployments database",
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
        default=10,
        help="Number of events to process per batch",
    )
    parser_materialize.set_defaults(func=handle_materialize)

    return parser
