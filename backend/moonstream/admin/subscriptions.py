"""
Utilities for managing subscription resources for a Moonstream application.
"""
import argparse
import json
from typing import Dict, List, Optional, Union

from bugout.data import BugoutResources, BugoutResource
from sqlalchemy.sql.expression import update

from ..data import SubscriptionTypeResourceData
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
)


def migrate_subscriptions(
    match: Dict[str, Union[str, int]],
    update: Dict[str, Union[str, int]],
    drop_keys: Optional[Dict[str, Union[str, int]]],
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

    for resource in old_resources:

        new_resource = bc.update_resource(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            resource_id=resource.id,
            resource_data={"update": update, "drop_keys": drop_keys},
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        new_resources.append(new_resource)

    return new_resources


def cli_migrate_subscriptions(args: argparse.Namespace) -> None:
    """
    Handler for subscriptions migrate.
    """

    drop_keys = None

    if args.file is not None:
        with open(args.file) as migration_json_file:
            migration_json = json.load(migration_json_file)

        if "match" not in migration_json or "update" not in migration_json:
            print(
                "Migration file plan have incorrect format require specified {match:{}, update:{}, drop_keys: Optional}"
            )
            return

        match = migration_json["match"]
        update = migration_json["update"]

        if drop_keys in migration_json:
            drop_keys = migration_json["drop_keys"]

    elif args.match is not None and args.update is not None:

        match = json.loads(args.update)

        update = json.loads(args.match)

        if args.drop_keys is not None:
            drop_keys = json.loads(args.drop_keys)

    else:
        print("Specified file or --match and --update is required.")
        return

    migrate_subscriptions(match=match, update=update, drop_keys=drop_keys)
