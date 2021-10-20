import argparse
import json

from .db import yield_db_session_ctx
from .models import EthereumLabel


def labels_add_handler(args: argparse.Namespace) -> None:
    """
    Add new label for ethereum address.
    """
    try:
        label_data = json.loads(args.data)
    except ValueError as err:
        print(str(err))
        raise ValueError("Unable to parse data as dictionary")

    with yield_db_session_ctx() as db_session:

        label = EthereumLabel(
            label=args.label, address=str(args.address), label_data=label_data
        )
        db_session.add(label)
        db_session.commit()

        print(
            json.dumps(
                {
                    "id": str(label.id),
                    "label": str(label.label),
                    "address_id": str(label.address),
                    "label_data": str(label.label_data),
                    "created_at": str(label.created_at),
                }
            )
        )


def labels_list_handler(args: argparse.Namespace) -> None:
    """
    Return list of all labels.
    """
    with yield_db_session_ctx() as db_session:
        query = db_session.query(EthereumLabel)
        if str(args.address) is not None:
            query = query.filter(EthereumLabel.address == str(args.address))
        labels = query.all()

    print(
        json.dumps(
            [
                {
                    "id": str(label.id),
                    "label": str(label.label),
                    "address_id": str(label.address_id),
                    "label_data": str(label.label_data),
                    "created_at": str(label.created_at),
                }
                for label in labels
            ]
        )
    )


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
    parser_labels_add.add_argument(
        "-d",
        "--data",
        help="New label data",
    )
    parser_labels_add.set_defaults(func=labels_add_handler)

    parser_labels_list = subcommands_labels.add_parser(
        "list", description="List all meta labels command"
    )
    parser_labels_list.add_argument(
        "-a",
        "--address",
        help="Filter address",
    )
    parser_labels_list.set_defaults(func=labels_list_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
