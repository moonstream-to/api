"""
Moonstream CLI
"""
import argparse
from distutils.util import strtobool
import json
from typing import List
import uuid

from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException

from .settings import (
    MOONSTREAM_SUBSCRIPTIONS_USER_TOKEN,
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
                token=MOONSTREAM_SUBSCRIPTIONS_USER_TOKEN, params=params
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
        except Exception as e:
            print("Unexpected Exception on request to brood")

        subscription_data = {
            "id": str(new_subscription_id),
            "name": args.name,
            "description": args.description,
            "subscription_plan_id": args.subscription_plan_id,
            "active": args.active,
        }

        # Add subscriptions

        resource_data = {"type": "subscription_type"}
        resource_data.update(subscription_data)

        try:

            resource: BugoutResource = bc.create_resource(
                token=MOONSTREAM_SUBSCRIPTIONS_USER_TOKEN,
                application_id=MOONSTREAM_APPLICATION_ID,
                resource_data=resource_data,
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
        "subscription", description="Moonstream subscription"
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
        "--descriptions",
        required=True,
        type=str,
        help="Description for user",
    )
    parser_subscription_create.add_argument(
        "-s",
        "--subscription_plan_id",
        required=False,
        type=str,
        help="Stripe sibscription id",
    )
    parser_subscription_create.add_argument(
        "--active",
        action="store_true",
        help="Set this flag to create a verified user",
    )
    parser_subscription_create.set_defaults(func=add_subscription_handler)
