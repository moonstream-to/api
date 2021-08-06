import argparse

from .db import yield_db_session_ctx
from .models import EthereumLabel


def labels_add_handler(args: argparse.Namespace) -> None:
    pass


def labels_list_handler(args: argparse.Namespace) -> None:
    """
    Return list of all labels.
    """
    with yield_db_session_ctx() as db_session:
        labels = db_session.query(EthereumLabel).all()

    print(labels.json())


def main():
    parser = argparse.ArgumentParser(description="Crawls address identities CLI")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Crawlers commands")

    parser_labels = subcommands.add_parser("labels", description="Meta labels commands")
    parser_labels.set_defaults(func=lambda _: parser_labels.print_help())
    subcommands_labels = parser_labels.add_subparsers(
        description="Database meta labels commands"
    )

    parser_labels_add = subcommands_labels.add_parser(
        "add", description="Add new label command"
    )
    parser_labels_add.add_argument(
        "-a",
        "--address",
        required=True,
        help="Address attach to",
    )
    parser_labels_add.add_argument(
        "-l",
        "--label",
        required=True,
        help="New label name",
    )
    parser_labels_add.set_defaults(func=labels_add_handler)

    parser_labels_list = subcommands_labels.add_parser(
        "list", description="List all meta labels command"
    )
    parser_labels_list.set_defaults(func=labels_list_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
