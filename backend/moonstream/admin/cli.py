"""
Moonstream CLI
"""
import argparse

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException

from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
)


class BroodResourcesInteractionException(Exception):
    pass


class UnExpectedException(Exception):
    pass


def add_subscription_handler(args: argparse.Namespace) -> None:
    """
    Handler for "groups subscription add" subcommand.
    """
    new_subscription_id = 0
    params = {"type": "subscription_type"}

    try:
        # resolve index
        try:
            resources: BugoutResources = bc.list_resources(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
            )
            new_subscription_id = (
                max(
                    [
                        int(resource.resource_data["id"])
                        for resource in resources.resources
                    ]
                )
                + 1
            )
        except BugoutResponseException as e:
            if e.detail != "Resources not found":
                raise BroodResourcesInteractionException(
                    f"status_code={e.status_code}, detail={e.detail}"
                )
            # If Brood returns 404, then we want to continue execution of the outer try block
            # with new_subscription_id as 0. That's why we don't have an "else" condition here.
        except Exception as e:
            print("Unexpected Exception on request to brood")
            raise

        subscription_data = {
            "type": "subscription_type",
            "id": str(new_subscription_id),
            "name": args.name,
            "description": args.description,
            "stripe_product_id": args.stripe_product_id,
            "stripe_price_id": args.stripe_price_id,
            "active": args.active,
        }

        try:
            bc.create_resource(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                application_id=MOONSTREAM_APPLICATION_ID,
                resource_data=subscription_data,
            )
        except BugoutResponseException as e:
            print(f"status_code={e.status_code}, detail={e.detail}")
            raise BroodResourcesInteractionException(
                f"status_code={e.status_code}, detail={e.detail}"
            )
        except Exception as e:
            print(f"Exception in create brood resource error:{e}")
            raise UnExpectedException("Error in resource creating")

    except Exception as e:
        print(e)


def main() -> None:
    parser = argparse.ArgumentParser(description="Moonstream CLI")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Moonstream commands")

    parser_subscription = subcommands.add_parser(
        "subscription-type", description="Manage Moonstream subscription types"
    )
    parser_subscription.set_defaults(func=lambda _: parser_subscription.print_help())
    subcommands_subscription = parser_subscription.add_subparsers(
        description="Moonstream subscription commands"
    )

    # Subscriptions command parser
    parser_subscription_create = subcommands_subscription.add_parser(
        "create", description="Create Moonstream subscription"
    )
    parser_subscription_create.add_argument(
        "-n",
        "--name",
        required=True,
        type=str,
        help="Title of that subscription",
    )
    parser_subscription_create.add_argument(
        "-d",
        "--description",
        required=True,
        type=str,
        help="Description for user",
    )
    parser_subscription_create.add_argument(
        "--stripe-product-id",
        required=False,
        default=None,
        type=str,
        help="Stripe product id",
    )
    parser_subscription_create.add_argument(
        "--stripe-price-id",
        required=False,
        default=None,
        type=str,
        help="Stripe price id",
    )
    parser_subscription_create.add_argument(
        "--active",
        action="store_true",
        help="Set this flag to create a verified user",
    )
    parser_subscription_create.set_defaults(func=add_subscription_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
