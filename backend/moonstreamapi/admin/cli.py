"""
Moonstream CLI
"""
import argparse
import json
import logging
import os
from posix import listdir
from typing import Optional

from sqlalchemy.orm import with_expression

from moonstreamdb.db import SessionLocal

from ..settings import BUGOUT_BROOD_URL, BUGOUT_SPIRE_URL, MOONSTREAM_APPLICATION_ID
from ..web3_provider import yield_web3_provider

from . import subscription_types, subscriptions, moonworm_tasks
from .migrations import checksum_address, update_dashboard_subscription_key


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MIGRATIONS_FOLDER = "./moonstream/admin/migrations"


def parse_boolean_arg(raw_arg: Optional[str]) -> Optional[bool]:
    if raw_arg is None:
        return None

    raw_arg_lower = raw_arg.lower()
    if raw_arg_lower in ["t", "true", "1", "y", "yes"]:
        return True
    return False


def migrations_list(args: argparse.Namespace) -> None:
    migrations_overview = f"""

- id: 20211101
name: {checksum_address.__name__}
description: {checksum_address.__doc__}
    """
    logger.info(migrations_overview)
    json_migrations_oreview = "Available migrations files."
    for file in os.listdir(MIGRATIONS_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(MIGRATIONS_FOLDER, file), "r") as migration_file:
                json_migrations_oreview += "\n\n"

                migration = json.load(migration_file)
                json_migrations_oreview = "\n".join(
                    (json_migrations_oreview, f"- id: {migration['id']}")
                )
                json_migrations_oreview = "\n".join(
                    (json_migrations_oreview, f"  file: {file}")
                )
                json_migrations_oreview = "\n".join(
                    (
                        json_migrations_oreview,
                        f"  description: {migration['description']}",
                    )
                )

    logger.info(json_migrations_oreview)


def migrations_run(args: argparse.Namespace) -> None:
    web3_session = yield_web3_provider()
    db_session = SessionLocal()
    try:
        if args.id == 20211101:
            logger.info("Starting update of subscriptions in Brood resource...")
            checksum_address.checksum_all_subscription_addresses(web3_session)
            logger.info("Starting update of ethereum_labels in database...")
            checksum_address.checksum_all_labels_addresses(db_session, web3_session)
        elif args.id == 20211202:
            update_dashboard_subscription_key.update_dashboard_resources_key()
        else:
            drop_keys = []

            if args.file is not None:

                with open(args.file) as migration_json_file:
                    migration_json = json.load(migration_json_file)

                if (
                    "match" not in migration_json
                    or "update" not in migration_json[args.command]
                    or "description" not in migration_json
                ):
                    print(
                        'Migration file plan have incorrect format require specified {"match": {},"description": "","upgrade": { "update": {}, "drop_keys": [] }, "downgrade": { "update": {}, "drop_keys": [] }}'
                    )
                    return

                match = migration_json["match"]
                description = migration_json["description"]
                update = migration_json[args.command]["update"]
                file = args.file

                if "drop_keys" in migration_json[args.command]:
                    drop_keys = migration_json[args.command]["drop_keys"]

                subscriptions.migrate_subscriptions(
                    match=match,
                    descriptions=description,
                    update=update,
                    drop_keys=drop_keys,
                    file=file,
                )

            else:
                print("Specified ID or migration FILE is required.")
                return
    finally:
        db_session.close()


def moonworm_tasks_list_handler(args: argparse.Namespace) -> None:

    moonworm_tasks.get_list_of_addresses()


def moonworm_tasks_add_subscription_handler(args: argparse.Namespace) -> None:

    moonworm_tasks.add_subscription(args.id)


def main() -> None:
    cli_description = f"""Moonstream Admin CLI

Please make sure that the following environment variables are set in your environment and exported to
subprocesses:
1. MOONSTREAM_APPLICATION_ID
2. MOONSTREAM_ADMIN_ACCESS_TOKEN

Current Moonstream application ID: {MOONSTREAM_APPLICATION_ID}

This CLI is configured to work with the following API URLs:
- Brood: {BUGOUT_BROOD_URL} (override by setting BUGOUT_BROOD_URL environment variable)
- Spire: {BUGOUT_SPIRE_URL} (override by setting BUGOUT_SPIRE_URL environment variable)
"""
    parser = argparse.ArgumentParser(
        description=cli_description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Moonstream commands")

    parser_subscription_types = subcommands.add_parser(
        "subtypes", description="Manage Moonstream subscription types"
    )
    parser_subscription_types.set_defaults(
        func=lambda _: parser_subscription_types.print_help()
    )
    subcommands_subscription_types = parser_subscription_types.add_subparsers()

    parser_subscription_types_create = subcommands_subscription_types.add_parser(
        "create", description="Create subscription type"
    )
    parser_subscription_types_create.add_argument(
        "-i", "--id", required=True, type=str, help="ID for the subscription type"
    )
    parser_subscription_types_create.add_argument(
        "-n",
        "--name",
        required=True,
        type=str,
        help="Human-friendly name for the subscription type",
    )
    parser_subscription_types_create.add_argument(
        "-d",
        "--description",
        required=True,
        type=str,
        help="Detailed description of the subscription type",
    )
    parser_subscription_types_create.add_argument(
        "-c",
        "--choices",
        nargs="*",
        help="Available subscription options for from builder.",
        required=True,
    )
    parser_subscription_types_create.add_argument(
        "--icon",
        required=True,
        help="URL to the icon representing this subscription type",
    )
    parser_subscription_types_create.add_argument(
        "--stripe-product-id",
        required=False,
        default=None,
        type=str,
        help="Stripe product id",
    )
    parser_subscription_types_create.add_argument(
        "--stripe-price-id",
        required=False,
        default=None,
        type=str,
        help="Stripe price id",
    )
    parser_subscription_types_create.add_argument(
        "--active",
        action="store_true",
        help="Set this flag to mark the subscription as active",
    )
    parser_subscription_types_create.set_defaults(
        func=subscription_types.cli_create_subscription_type
    )

    parser_subscription_types_list = subcommands_subscription_types.add_parser(
        "list", description="List subscription types"
    )
    parser_subscription_types_list.add_argument(
        "--active",
        action="store_true",
        help="Set this flag to only list active subscription types",
    )
    parser_subscription_types_list.set_defaults(
        func=subscription_types.cli_list_subscription_types
    )

    parser_subscription_types_get = subcommands_subscription_types.add_parser(
        "get", description="Get a subscription type by its ID"
    )
    parser_subscription_types_get.add_argument(
        "-i",
        "--id",
        required=True,
        help="ID of the subscription type you would like information about",
    )
    parser_subscription_types_get.set_defaults(
        func=subscription_types.cli_get_subscription_type
    )

    parser_subscription_types_update = subcommands_subscription_types.add_parser(
        "update", description="Create subscription type"
    )
    parser_subscription_types_update.add_argument(
        "-i", "--id", required=True, type=str, help="ID for the subscription type"
    )
    parser_subscription_types_update.add_argument(
        "-n",
        "--name",
        required=False,
        default=None,
        type=str,
        help="Human-friendly name for the subscription type",
    )
    parser_subscription_types_update.add_argument(
        "-d",
        "--description",
        required=False,
        default=None,
        type=str,
        help="Detailed description of the subscription type",
    )
    parser_subscription_types_update.add_argument(
        "-c",
        "--choices",
        nargs="*",
        help="Available subscription options for form builder.",
        required=False,
    )
    parser_subscription_types_update.add_argument(
        "--icon",
        required=False,
        default=None,
        help="URL to the icon representing this subscription type",
    )
    parser_subscription_types_update.add_argument(
        "--stripe-product-id",
        required=False,
        default=None,
        type=str,
        help="Stripe product id",
    )
    parser_subscription_types_update.add_argument(
        "--stripe-price-id",
        required=False,
        default=None,
        type=str,
        help="Stripe price id",
    )
    parser_subscription_types_update.add_argument(
        "--active",
        required=False,
        type=parse_boolean_arg,
        default=None,
        help="Mark the subscription as active (True) or inactive (False).",
    )
    parser_subscription_types_update.set_defaults(
        func=subscription_types.cli_update_subscription_type
    )

    parser_subscription_types_delete = subcommands_subscription_types.add_parser(
        "delete", description="Delete a subscription type by its ID"
    )
    parser_subscription_types_delete.add_argument(
        "-i",
        "--id",
        required=True,
        help="ID of the subscription type you would like to delete.",
    )
    parser_subscription_types_delete.set_defaults(
        func=subscription_types.cli_delete_subscription_type
    )

    parser_subscription_types_canonicalize = subcommands_subscription_types.add_parser(
        "ensure-canonical",
        description="Ensure that the connected Brood API contains resources for each of the canonical subscription types",
    )
    parser_subscription_types_canonicalize.set_defaults(
        func=subscription_types.cli_ensure_canonical_subscription_types
    )

    parser_migrations = subcommands.add_parser(
        "migrations", description="Manage database, resource and etc migrations"
    )
    parser_migrations.set_defaults(func=lambda _: parser_migrations.print_help())
    subcommands_migrations = parser_migrations.add_subparsers(
        description="Migration commands"
    )
    parser_migrations_list = subcommands_migrations.add_parser(
        "list", description="List migrations"
    )
    parser_migrations_list.set_defaults(func=migrations_list)
    parser_migrations_run = subcommands_migrations.add_parser(
        "run", description="Run migration"
    )
    parser_migrations_run.add_argument(
        "-i", "--id", required=False, type=int, help="Provide migration ID"
    )
    parser_migrations_run.add_argument(
        "-f", "--file", required=False, type=str, help="path to file"
    )
    parser_migrations_run.add_argument(
        "-c",
        "--command",
        default="upgrade",
        choices=["upgrade", "downgrade"],
        type=str,
        help="Command for migration",
    )
    parser_migrations_run.set_defaults(func=migrations_run)

    parser_moonworm_tasks = subcommands.add_parser(
        "moonworm-tasks", description="Manage tasks for moonworm journal."
    )

    parser_moonworm_tasks.set_defaults(func=lambda _: parser_migrations.print_help())
    subcommands_moonworm_tasks = parser_moonworm_tasks.add_subparsers(
        description="Moonworm taks commands"
    )
    parser_moonworm_tasks_list = subcommands_moonworm_tasks.add_parser(
        "list", description="Return list of addresses in moonworm journal."
    )

    parser_moonworm_tasks_list.set_defaults(func=moonworm_tasks_list_handler)

    parser_moonworm_tasks_add = subcommands_moonworm_tasks.add_parser(
        "add_subscription", description="Manage tasks for moonworm journal."
    )

    parser_moonworm_tasks_add.add_argument(
        "-i",
        "--id",
        type=str,
        help="Id of subscription for add to moonworm tasks.",
    )

    parser_moonworm_tasks_add.set_defaults(func=moonworm_tasks_add_subscription_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
