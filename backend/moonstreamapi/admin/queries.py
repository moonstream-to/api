"""
Utilities for managing subscription type resources for a Moonstream application.
"""
import argparse

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException

from ..data import BUGOUT_RESOURCE_QUERY_RESOLVER
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_QUERIES_JOURNAL_ID,
)
from ..settings import bugout_client as bc


def ensure_queries_tags(args: argparse.Namespace) -> BugoutResources:

    """
    Check all queries resources and check if they entry have all required tags.

    Resource structure:
    {'entry_id': <entry_id>,
    'name': <query_name>,
    'type': 'query_name_resolver',
    'user': <user_name>,
    'user_id': <user_id>}

    """
    params = {"type": BUGOUT_RESOURCE_QUERY_RESOLVER}
    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
    )

    for resource in resources.resources:

        if "entry_id" not in resource.resource_data:
            print(f"Missing entry_id for {resource.id}")
            continue
        if "name" not in resource.resource_data:
            print(f"Missing name for {resource.id}")
            continue
        if "type" not in resource.resource_data:
            print(f"Missing type for {resource.id}")
            continue
        if "user" not in resource.resource_data:
            print(f"Missing user for {resource.id}")
            continue
        if "user_id" not in resource.resource_data:
            print(f"Missing user_id for {resource.id}")
            continue

        # get entry
        try:
            entry = bc.get_entry(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                entry_id=resource.resource_data["entry_id"],
                journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )

        except BugoutResponseException as e:
            print(f"Error getting entry {resource.resource_data['entry_id']} err: {e}")
            continue

        print(
            f"Entry {entry.id} {entry.title} {entry.journal_url} user: {resource.resource_data['user']}"
        )
        required_tags = ["user_name", "query_name", "user_id", "query_id"]
        for tag in entry.tags:

            tag_prefix = tag.split(":")[0]

            print(tag_prefix)
            if tag_prefix in required_tags:
                required_tags.remove(tag_prefix)

        print(f"Missing tags for {resource.resource_data['entry_id']}: {required_tags}")

        tags_for_update = []
        if len(required_tags) > 0:

            for required_tag in required_tags:
                if required_tag == "user_name":
                    tag_value = resource.resource_data["user"]
                elif required_tag == "query_name":
                    tag_value = resource.resource_data["name"]
                elif required_tag == "user_id":
                    tag_value = resource.resource_data["user_id"]
                elif required_tag == "query_id":
                    tag_value = resource.resource_data["entry_id"]

                tag = f"{required_tag}:{tag_value}"
                tags_for_update.append(tag)

            bc.update_tags(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                entry_id=resource.resource_data["entry_id"],
                journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
                tags=tags_for_update,
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
