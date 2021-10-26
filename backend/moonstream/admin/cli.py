"""
Moonstream CLI
"""
import argparse
from typing import Optional

from ..settings import BUGOUT_BROOD_URL, BUGOUT_SPIRE_URL, MOONSTREAM_APPLICATION_ID
from . import subscription_types


def parse_boolean_arg(raw_arg: Optional[str]) -> Optional[bool]:
    if raw_arg is None:
        return None

    raw_arg_lower = raw_arg.lower()
    if raw_arg_lower in ["t", "true", "1", "y", "yes"]:
        return True
    return False


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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
