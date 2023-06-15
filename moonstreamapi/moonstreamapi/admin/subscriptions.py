"""
Utilities for managing subscription resources for a Moonstream application.
"""
import argparse
import json
from typing import Dict, List, Optional, Union

from bugout.data import BugoutResources

from .. import reporter
from ..settings import BUGOUT_REQUEST_TIMEOUT_SECONDS, MOONSTREAM_ADMIN_ACCESS_TOKEN
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
