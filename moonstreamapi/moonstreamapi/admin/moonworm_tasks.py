import logging
import json

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException


from ..actions import get_all_entries_from_search, apply_moonworm_tasks
from ..settings import MOONSTREAM_ADMIN_ACCESS_TOKEN, MOONSTREAM_MOONWORM_TASKS_JOURNAL
from ..settings import bugout_client as bc

logger = logging.getLogger(__name__)


def get_list_of_addresses():
    """
    Return list of addresses of tasks
    """

    entries = get_all_entries_from_search(
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        search_query=f"?tag:type:event ?tag:type:function",
        limit=100,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
    )

    addresses = set()

    for entry in entries:
        addresses.add(entry.title)

    print(addresses)


def add_subscription(id: str):
    """
    Return list of tags depends on query and tag
    """

    try:
        subscription_resource: BugoutResource = bc.get_resource(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            resource_id=id,
        )

    except BugoutResponseException as e:
        logging.error(f"Bugout error: {str(e)}")
    except Exception as e:
        logger.error(f"Error get resource: {str(e)}")

    s3_client = boto3.client("s3")

    if subscription_resource.resource_data["abi"] is not None:
        bucket = subscription_resource.resource_data["bucket"]
        key = subscription_resource.resource_data["s3_path"]

        if bucket is None or key is None:
            logger.error(f"Error subscription not have s3 path to abi")

        s3_path = f"s3://{bucket}/{key}"

        try:
            response = s3_client.get_object(
                Bucket=bucket,
                Key=key,
            )

        except s3_client.exceptions.NoSuchKey as e:
            logger.error(
                f"Error getting Abi for subscription {str(id)} S3 {s3_path} does not exist : {str(e)}"
            )

        abi = json.loads(response["Body"].read())

        apply_moonworm_tasks(
            subscription_type=subscription_resource.resource_data[
                "subscription_type_id"
            ],
            abi=abi,
            address=subscription_resource.resource_data["address"],
        )
    else:
        logging.info("For apply to moonworm tasks subscriptions must have an abi.")
