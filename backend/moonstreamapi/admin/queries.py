"""
Utilities for managing subscription type resources for a Moonstream application.
"""
import argparse
import json

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException
from moonstream.client import Moonstream  # type: ignore
import logging
from typing import Dict, Any

from ..data import BUGOUT_RESOURCE_QUERY_RESOLVER
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_QUERIES_JOURNAL_ID,
)
from ..settings import bugout_client as bc


logger = logging.getLogger(__name__)


def ensure_queries_tags(args: argparse.Namespace) -> None:

    """
    Check all queries resources and check if they entry have all required tags.
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


def get_users(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Return all users with queries count.
    """

    params = {"type": BUGOUT_RESOURCE_QUERY_RESOLVER}
    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
    )

    users = {}
    for resource in resources.resources:
        user_id = resource.resource_data["user_id"]
        if user_id not in users:
            users[user_id] = {
                "user_id": user_id,
                "user_name": resource.resource_data["user"],
                "queries_count": 1,
            }
        else:
            users[user_id]["queries_count"] += 1

    logger.info(f"Users: {json.dumps(users, indent=4)}")

    return users


def get_user_queries(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Return all queries for user.
    """

    params = {"type": BUGOUT_RESOURCE_QUERY_RESOLVER}
    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
    )

    queries = {}

    for resource in resources.resources:
        user_id = resource.resource_data["user_id"]
        if user_id == args.user_id:
            queries[resource.resource_data["entry_id"]] = {
                "query_name": resource.resource_data["name"]
            }

    # get entries
    for query_id in queries:
        entry = bc.get_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            entry_id=query_id,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

        queries[query_id]["entry"] = entry

        if "preapprove" in entry.tags:
            queries[query_id]["status"] = "preapprove"
        elif "approved" in entry.tags:
            queries[query_id]["status"] = "approved"

    for query_id in queries:
        print(
            f"{query_id} name: {queries[query_id]['entry'].title} status: {queries[query_id]['status']}"
        )

    return queries


def copy_queries(args: argparse.Namespace) -> None:
    """
    Copy all queries from one user to another.
    """

    from_user_id = args.from_user_id

    to_user_token = args.to_user_token

    params = {"type": BUGOUT_RESOURCE_QUERY_RESOLVER}
    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
    )

    queries = {}
    for resource in resources.resources:
        user_id = resource.resource_data["user_id"]
        if user_id == from_user_id:
            queries[resource.resource_data["entry_id"]] = {
                "query_id": resource.resource_data["entry_id"],
                "query_name": resource.resource_data["name"],
                "user_id": user_id,
                "user_name": resource.resource_data["user"],
            }

    # get entries
    for query_id in queries:
        entry = bc.get_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            entry_id=query_id,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

        queries[query_id]["entry"] = entry

    client = Moonstream()

    for query_id, query in queries.items():

        # create query via bugout client
        try:
            created_query = client.create_query(
                token=to_user_token,
                name=query["query_name"],
                query=query["entry"].content,
            )

        except Exception as e:
            logger.error(f"Error getting entry {query_id} err: {e}")
            continue

        logger.info(f"Created query {created_query.id} {created_query.name}")

        if (
            "preapprove" not in query["entry"].tags
            and "approved" in query["entry"].tags
        ):
            # Delete preapprove tag

            try:
                bc.delete_tag(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    entry_id=created_query.id,
                    journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
                    tag="preapprove",
                    timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
                )
            except BugoutResponseException as e:
                logger.error(f"Error in applind tags to query entry: {str(e)}")
                continue
            except Exception as e:
                logger.error(
                    f"Error in applind tags to query entry: {str(e)} unknown error"
                )
                continue

            print(f"Delete preapprove tag for {created_query.id}")

            try:
                bc.create_tags(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    entry_id=created_query.id,
                    journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
                    tags=["approved"],
                    timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
                )
            except BugoutResponseException as e:
                logger.error(f"Error in applind tags to query entry: {str(e)}")
                continue
            except Exception as e:
                logger.error(
                    f"Error in applind tags to query entry: {str(e)} unknown error"
                )
                continue

            logger.info(f"Add approved tag for {created_query.id}")
