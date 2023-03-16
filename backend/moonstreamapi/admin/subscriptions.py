"""
Utilities for managing subscription resources for a Moonstream application.
"""
import argparse
import json
import uuid
from typing import Dict, List, Optional, Union, Any

from bugout.data import BugoutResources

from .. import reporter
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
)
from ..settings import bugout_client as bc


def migrate_subscriptions(
    match: Dict[str, Union[str, int]],
    update: Dict[str, Union[str, int]],
    descriptions: str,
    file: str,
    drop_keys: Optional[List[str]],
):
    """
    Search all subscriptinons and replace them one by one
    """

    response: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params=match,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    old_resources = [resource for resource in response.resources]

    new_resources = []

    reporter.custom_report(
        title="Subscription migration",
        content=descriptions,
        tags=["subscriptions", "migration", f"migration_file:{file}"],
    )
    print(f"Affected resources: {len(old_resources)}")

    for resource in old_resources:
        try:
            print(f"Updating resource: {resource.id}")

            new_resource = bc.update_resource(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                resource_id=resource.id,
                resource_data={"update": update, "drop_keys": drop_keys},
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
            new_resources.append(new_resource)
        except Exception as err:
            print(err)
            reporter.error_report(
                err,
                tags=[
                    "subscriptions",
                    "migration",
                    "error",
                    f"resource_id:{resource.id}",
                    f"migration_file:{file}",
                ],
            )

    return new_resources


def subscription_report(output_file: str, user_ids: Optional[List[str]]):
    """
    Returns a report of all subscriptions for a Moonstream application.
    """
    if user_ids is None:
        user_ids = []

    ### Get admin user id

    admin_user = bc.get_user(token=MOONSTREAM_ADMIN_ACCESS_TOKEN)

    admin_user_id = admin_user.id

    print(f"admin user :{admin_user.username}")

    ### Get all subscription resources type = "subscription"

    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    print(f"Admin own {len(resources.resources)} subscriptions")

    ### initial users_subscriptions, dashboards_by_user, stages is empty

    users_subscriptions: Dict[Union[str, uuid.UUID], Any] = {}

    dashboards_by_user: Dict[Union[str, uuid.UUID], Any] = {}

    ### Iterate over all subscriptions

    for resource in resources.resources:
        resource_data = resource.resource_data

        resource_data["subscription_id"] = resource.id

        if "user_id" not in resource_data:
            continue

        user_id = resource_data["user_id"]

        if user_id not in user_ids and len(user_ids) > 0:
            continue

        if user_id not in users_subscriptions:
            users_subscriptions[user_id] = []

        users_subscriptions[user_id].append(resource_data)

    print(f"parsed subscriptions: {resources.resources[0]}")

    print(f"parsed users: {len(users_subscriptions)}")

    ### create subscription report

    report: Dict[str, Any] = {}

    try:
        for user_id, subscriptions in users_subscriptions.items():
            user_id = str(user_id)

            for subscription in subscriptions:
                subscription_type_id = subscription["subscription_type_id"]
                address = subscription["address"]
                color = subscription["color"]
                label = subscription["label"]

                if user_id not in report:
                    report[user_id] = {
                        "user_id": user_id,
                        "subscription_addresses": {},
                        "total_subscriptions": 0,
                    }

                if address not in report[user_id]["subscription_addresses"]:
                    report[user_id]["subscription_addresses"][address] = {
                        "address": address,
                        "subscription_type_ids": [subscription_type_id],
                        "labels": [label],
                    }

                else:
                    report[user_id]["subscription_addresses"][address][
                        "subscription_type_ids"
                    ].append(subscription_type_id)
                    report[user_id]["subscription_addresses"][address]["labels"].append(
                        label
                    )

                report[user_id]["total_subscriptions"] += 1

        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)

    except Exception as err:
        print(err)
        reporter.error_report(
            err,
            tags=[
                "subscriptions",
                "report",
                "error",
            ],
        )


def all_subscription_report(output_file: str):
    """
    Returns a report of all subscriptions for a Moonstream application.
    """

    ### Get admin user id

    admin_user = bc.get_user(token=MOONSTREAM_ADMIN_ACCESS_TOKEN)

    admin_user_id = admin_user.id

    print(f"admin user :{admin_user.username}")

    ### Get all subscription resources type = "subscription"

    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    print(f"Admin own {len(resources.resources)} subscriptions")

    ### initial users_subscriptions, dashboards_by_user, stages is empty

    users_subscriptions: Dict[Union[str, uuid.UUID], Any] = {}

    dashboards_by_user: Dict[Union[str, uuid.UUID], Any] = {}

    ### Iterate over all subscriptions

    for resource in resources.resources:
        resource_data = resource.resource_data

        resource_data["subscription_id"] = resource.id

        if "user_id" not in resource_data:
            continue

        user_id = resource_data["user_id"]

        if user_id not in users_subscriptions:
            users_subscriptions[user_id] = []

        users_subscriptions[user_id].append(resource_data)

    print(f"parsed subscriptions: {resources.resources[0]}")

    print(f"parsed users: {len(users_subscriptions)}")

    ### create subscription report

    report: Dict[str, Any] = {"subscription_addresses": {}, "total_subscriptions": 0}

    users_top_subscriptions: Dict[str, Any] = {}

    addresses_subscriptions_top: Dict[str, Any] = {}

    try:
        for user_id, subscriptions in users_subscriptions.items():
            for subscription in subscriptions:
                subscription_type_id = subscription["subscription_type_id"]
                address = subscription["address"]
                color = subscription["color"]
                label = subscription["label"]

                if address not in report["subscription_addresses"]:
                    report["subscription_addresses"][address] = {
                        "address": address,
                        "subscription_type_ids": [subscription_type_id],
                        "labels": [label],
                    }

                else:
                    report["subscription_addresses"][address][
                        "subscription_type_ids"
                    ].append(subscription_type_id)
                    report["subscription_addresses"][address]["labels"].append(label)

                report["total_subscriptions"] += 1

            users_top_subscriptions[user_id] = {
                "total_subscriptions": len(subscriptions),
            }

        ### top 10 addresses

        addresses_subscriptions_top = {
            k: v["subscription_type_ids"]
            for k, v in sorted(
                report["subscription_addresses"].items(),
                key=lambda item: len(item[1]["subscription_type_ids"]),
                reverse=True,
            )
        }

        report["addresses_subscriptions_top"] = dict(
            list(addresses_subscriptions_top.items())[0:10]
        )

        ### sort users by total_subscriptions

        users_top_subscriptions = {
            k: v
            for k, v in sorted(
                users_top_subscriptions.items(),
                key=lambda item: item[1]["total_subscriptions"],
                reverse=True,
            )
        }

        report["users_top_subscriptions"] = users_top_subscriptions

        report["total_users"] = len(users_subscriptions)
        report["total_unique_addresses"] = len(report["subscription_addresses"])

        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)

    except Exception as err:
        print(err)
        reporter.error_report(
            err,
            tags=[
                "subscriptions",
                "report",
                "error",
            ],
        )
