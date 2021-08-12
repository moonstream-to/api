"""
Utilities for managing subscription type resources for a Moonstream application.
"""
import argparse
import json
from typing import Any, Dict, List, Optional
from bugout.app import Bugout

from bugout.data import BugoutResources, BugoutResource

from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
)


class ConflictingSubscriptionTypesError(Exception):
    """
    Raised when caller tries to add a resource that conflicts with an existing resource.
    """

    pass


class SubscriptionTypeNotFoundError(Exception):
    """
    Raised when a subscription type is expected to exist as a Brood resource but is not found.
    """


class UnexpectedError(Exception):
    pass


BUGOUT_RESOURCE_TYPE = "subscription_type"


def add_subscription_type(
    id: str,
    name: str,
    description: str,
    stripe_product_id: Optional[str] = None,
    stripe_price_id: Optional[str] = None,
    active: bool = False,
) -> Dict[str, Any]:
    """
    Add a new Moonstream subscription type as a Brood resource.

    Args:
    - id: Moonstream ID for the subscription type. Examples: "ethereum_blockchain", "ethereum_txpool",
      "ethereum_whalewatch", etc.
    - name: Human-friendly name for the subscription type, which can be displayed to users.
    - description: Detailed description of the subscription type for users who would like more
      information.
    - stripe_product_id: Optional product ID from Stripe account dashboard.
    - stripe_price_id: Optional price ID from Stripe account dashboard.
    - active: Set to True if you would like the subscription type to immediately be available for
      subscriptions. If you set this to False (which is the default), users will not be able to create
      subscriptions of this type until you later on set to true.
    """
    params = {"type": BUGOUT_RESOURCE_TYPE, "id": id}

    response: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
    )
    if response.resources:
        raise ConflictingSubscriptionTypesError(
            f"There is already a subscription_type with id: {id}"
        )

    subscription_data = {
        "type": BUGOUT_RESOURCE_TYPE,
        "id": id,
        "name": name,
        "description": description,
        "stripe_product_id": stripe_product_id,
        "stripe_price_id": stripe_price_id,
        "active": active,
    }

    resource = bc.create_resource(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        application_id=MOONSTREAM_APPLICATION_ID,
        resource_data=subscription_data,
    )

    return resource.resource_data


def cli_add_subscription_type(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes create".
    """
    result = add_subscription_type(
        args.id,
        args.name,
        args.description,
        args.stripe_product_id,
        args.stripe_price_id,
        args.active,
    )
    print(json.dumps(result))


def list_subscription_types() -> List[Dict[str, Any]]:
    """
    Lists all subscription types registered as Brood resources for this Moonstream application.
    """
    response = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params={"type": BUGOUT_RESOURCE_TYPE}
    )
    resources = response.resources
    return [resource.resource_data for resource in resources]


def cli_list_subscription_types(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes list".
    """
    results = list_subscription_types()
    print(json.dumps(results))


def get_subscription_type(id: str) -> Optional[BugoutResource]:
    """
    Retrieves the resource representing the subscription type with the given ID.

    Args:
    - id: Moonstream ID for the subscription type (not the Brood resource ID).
      Examples - "ethereum_blockchain", "ethereum_whalewatch", etc.

    Returns: None if there is no subscription type with that ID. Otherwise, returns the full
    Brood resource. To access the subscription type itself, use the "resource_data" member of the
    return value. If more than one subscription type is found with the given ID, raises a
    ConflictingSubscriptionTypesError.
    """
    response = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE, "id": id},
    )
    resources = response.resources

    if not resources:
        return None
    if len(resources) > 1:
        raise ConflictingSubscriptionTypesError(
            f"More than one resource with the given ID:\n{json.dumps(resources, indent=2)}"
        )
    return resources[0]


def cli_get_subscription_type(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes get".
    """
    resource = get_subscription_type(args.id)
    if resource is None:
        print(f"Could not find resource with ID: {id}")
    else:
        print(resource.json())


def update_subscription_type(
    id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    stripe_product_id: Optional[str] = None,
    stripe_price_id: Optional[str] = None,
    active: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Update a Moonstream subscription type using the Brood Resources API.

    Args:
    - id: Moonstream ID for the subscription type. Examples: "ethereum_blockchain", "ethereum_txpool",
      "ethereum_whalewatch", etc.
    - name: Human-friendly name for the subscription type, which can be displayed to users.
    - description: Detailed description of the subscription type for users who would like more
      information.
    - stripe_product_id: Optional product ID from Stripe account dashboard.
    - stripe_price_id: Optional price ID from Stripe account dashboard.
    - active: Set to True if you would like the subscription type to immediately be available for
      subscriptions. If you set this to False (which is the default), users will not be able to create
      subscriptions of this type until you later on set to true.
    """

    resource = get_subscription_type(id)
    if resource is None:
        raise SubscriptionTypeNotFoundError(
            f"Could not find subscription type with ID: {id}."
        )

    brood_resource_id = resource.id
    updated_resource_data = resource.resource_data
    if name is not None:
        updated_resource_data["name"] = name
    if description is not None:
        updated_resource_data["description"] = description
    if stripe_product_id is not None:
        updated_resource_data["stripe_product_id"] = stripe_product_id
    if stripe_price_id is not None:
        updated_resource_data["stripe_price_id"] = stripe_price_id
    if active is not None:
        updated_resource_data["active"] = active

    bc.delete_resource(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN, resource_id=brood_resource_id
    )
    new_resource = bc.create_resource(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        application_id=MOONSTREAM_APPLICATION_ID,
        resource_data=updated_resource_data,
    )

    return new_resource.resource_data


def cli_update_subscription_type(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes update".
    """
    result = update_subscription_type(
        args.id,
        args.name,
        args.description,
        args.stripe_product_id,
        args.stripe_price_id,
        args.active,
    )
    print(json.dumps(result))
