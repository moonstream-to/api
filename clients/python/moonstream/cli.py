import argparse
import textwrap
import uuid

from .client import Moonstream


def handle_create_query(args: argparse.Namespace) -> None:
    client = Moonstream()

    query = ""
    with args.query_file:
        query = textwrap.indent(args.query_file.read(), "    ")

    client.create_query(args.token, query, args.name, args.public)


def main() -> None:
    """
    Execute the Moonstream client command line.
    """
    parser = argparse.ArgumentParser(
        description="Command-line interface for the Moonstream Python client library. This CLI allows you to use client functionality from your command line."
    )
    subparsers = parser.add_subparsers(title="Commands")

    create_query_parser = subparsers.add_parser("create-query")
    create_query_parser.add_argument(
        "-t",
        "--token",
        required=True,
        type=uuid.UUID,
        help="Access token for Moonstream API",
    )
    create_query_parser.add_argument(
        "--query-file",
        required=True,
        type=argparse.FileType("r"),
        help="File containing the query to add",
    )
    create_query_parser.add_argument(
        "-n", "--name", required=True, help="Name for the new query"
    )
    create_query_parser.add_argument(
        "--public",
        action="store_true",
        help="Set this flag if you want the query to be public",
    )
    create_query_parser.set_defaults(func=handle_create_query)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
