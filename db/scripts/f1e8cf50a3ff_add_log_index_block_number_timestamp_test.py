import argparse
import os
from typing import Any, Dict, Optional


from typing import Any, Dict, Optional
from sqlalchemy import create_engine


def ethereum_labels_copy_check(args: argparse.Namespace) -> None:

    engine = create_engine(args.database)
    connection = engine.connect()

    # check counts in 2 tables

    count_original = connection.execute(
        """
        select count(*) from ethereum_labels;
    """
    ).fetchall()[0][0]

    count_new_labels = connection.execute(
        """
        select count(*) from ethereum_labels_v2;
    """
    ).fetchall()[0][0]
    if count_original == count_new_labels:
        print(f"Count check passed")
    else:
        print(f"Tables recors counts mismatch")

    print(
        f"etherium_labels count:{count_original}, ethereum_labels_v2 count:{count_new_labels}"
    )

    # check random selected rows
    original_table_rows_select = connection.execute(
        """
        select id from ethereum_labels TABLESAMPLE BERNOULLI (0.1) limit 1000;
    """
    ).fetchall()

    ids = [str(row[0]) for row in original_table_rows_select]

    ids_str = "', '".join(ids)

    # check

    original_table_rows_select = connection.execute(
        """
            SELECT
                id,
                label,
                label_data,
                created_at,
                transaction_hash,
                address
            FROM
                ethereum_labels_v2
                where id IN ('{}')
            EXCEPT 
            SELECT
                ethereum_labels.id as id,
                ethereum_labels.label as label,
                ethereum_labels.label_data as label_data,
                ethereum_labels.created_at as created_at,
                ethereum_labels.transaction_hash as transaction_hash,
                ethereum_addresses.address as address
            FROM
                ethereum_labels
                left join ethereum_addresses ON ethereum_labels.address_id = ethereum_addresses.id
                where ethereum_labels.id IN ('{}');
    """.format(
            ids_str, ids_str
        )
    ).fetchall()

    if original_table_rows_select:
        print("Error rows data from sample missmatch")
    else:
        print("Rows sample is correct")


def main() -> None:
    parser = argparse.ArgumentParser(description="Migration check")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Subcommands")

    parser_migration_check = subcommands.add_parser(
        "ethereum_migration_check",
        description="Check for migration between tables.",
    )
    parser_migration_check.set_defaults(
        func=lambda _: parser_migration_check.print_help()
    )
    subparsers_migration_check = parser_migration_check.add_subparsers()

    parser_ethereum_migration_check = subparsers_migration_check.add_parser(
        "run",
        description="Run check of tables",
    )

    parser_ethereum_migration_check.add_argument(
        "--database", type=str, required=True, help="Database for check."
    )

    parser_ethereum_migration_check.set_defaults(func=ethereum_labels_copy_check)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
