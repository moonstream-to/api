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


"""



    moonworm_tasks examples:


        {
            "entry_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/796293be-f764-4120-8108-e9ed60296576",
            "content_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/796293be-f764-4120-8108-e9ed60296576/content",
            "title": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
            "content": "{\n    \"inputs\": [\n        {\n            \"internalType\": \"uint256\",\n            \"name\": \"roundTripId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"internalType\": \"uint256\",\n            \"name\": \"firstParentId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"internalType\": \"uint256\",\n            \"name\": \"secondParentId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"internalType\": \"uint256[3]\",\n            \"name\": \"possibleClasses\",\n            \"type\": \"uint256[3]\"\n        },\n        {\n            \"internalType\": \"uint256[3]\",\n            \"name\": \"classProbabilities\",\n            \"type\": \"uint256[3]\"\n        },\n        {\n            \"internalType\": \"uint256\",\n            \"name\": \"owedRBW\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"internalType\": \"uint256\",\n            \"name\": \"owedUNIM\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"internalType\": \"uint256\",\n            \"name\": \"bundleId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"internalType\": \"uint256\",\n            \"name\": \"blockDeadline\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"internalType\": \"bytes\",\n            \"name\": \"signature\",\n            \"type\": \"bytes\"\n        }\n    ],\n    \"name\": \"beginBreedingWithSignature\",\n    \"outputs\": [],\n    \"stateMutability\": \"nonpayable\",\n    \"type\": \"function\",\n    \"selector\": \"0xd2df3a9e\"\n}",
            "tags": [
                "abi_method_hash:5e5203a6a4bdfd2f51d8983a6618a3f9",
                "abi_name:beginBreedingWithSignature",
                "abi_selector:0xd2df3a9e",
                "address:0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                "historical_crawl_status:in_progress",
                "moonworm_task_pickedup:True",
                "progress:28.87",
                "status:active",
                "subscription_type:polygon_smartcontract",
                "task_type:moonworm",
                "type:function"
            ],
            "created_at": "2023-07-24 19:24:25.956879+00:00",
            "updated_at": "2023-07-24 19:24:25.956879+00:00",
            "score": 1.0,
            "context_type": "bugout",
            "context_id": null,
            "context_url": null
        },
        {
            "entry_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/eff6fa6d-5f52-4520-9a0e-cbd342a97df6",
            "content_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/eff6fa6d-5f52-4520-9a0e-cbd342a97df6/content",
            "title": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
            "content": "{\n    \"anonymous\": false,\n    \"inputs\": [\n        {\n            \"indexed\": true,\n            \"internalType\": \"uint256\",\n            \"name\": \"roundTripId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"indexed\": true,\n            \"internalType\": \"address\",\n            \"name\": \"playerWallet\",\n            \"type\": \"address\"\n        }\n    ],\n    \"name\": \"HatchingReadyForTokenURI\",\n    \"type\": \"event\",\n    \"selector\": \"0xe624f790\"\n}",
            "tags": [
                "abi_method_hash:c7fa9120e377db29210840ac7d2b0231",
                "abi_name:HatchingReadyForTokenURI",
                "abi_selector:0xe624f790",
                "address:0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                "historical_crawl_status:in_progress",
                "moonworm_task_pickedup:True",
                "progress:0.04",
                "status:active",
                "subscription_type:polygon_smartcontract",
                "task_type:moonworm",
                "type:event"
            ],
            "created_at": "2023-07-24 19:24:25.956879+00:00",
            "updated_at": "2023-07-24 19:24:25.956879+00:00",
            "score": 1.0,
            "context_type": "bugout",
            "context_id": null,
            "context_url": null
        },
        {
            "entry_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/5421498e-00a0-4ae0-b09c-8fa9bf2c1a25",
            "content_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/5421498e-00a0-4ae0-b09c-8fa9bf2c1a25/content",
            "title": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
            "content": "{\n    \"anonymous\": false,\n    \"inputs\": [\n        {\n            \"indexed\": true,\n            \"internalType\": \"uint256\",\n            \"name\": \"roundTripId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"indexed\": true,\n            \"internalType\": \"address\",\n            \"name\": \"owner\",\n            \"type\": \"address\"\n        },\n        {\n            \"indexed\": true,\n            \"internalType\": \"address\",\n            \"name\": \"playerWallet\",\n            \"type\": \"address\"\n        }\n    ],\n    \"name\": \"HatchingCompleteV2\",\n    \"type\": \"event\",\n    \"selector\": \"0x68b73a42\"\n}",
            "tags": [
                "abi_method_hash:a947931677e8c02af0b609779f80fd32",
                "abi_name:HatchingCompleteV2",
                "abi_selector:0x68b73a42",
                "address:0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                "historical_crawl_status:in_progress",
                "moonworm_task_pickedup:True",
                "progress:0.04",
                "status:active",
                "subscription_type:polygon_smartcontract",
                "task_type:moonworm",
                "type:event"
            ],
            "created_at": "2023-07-24 19:24:25.956879+00:00",
            "updated_at": "2023-07-24 19:24:25.956879+00:00",
            "score": 1.0,
            "context_type": "bugout",
            "context_id": null,
            "context_url": null
        },
        {
            "entry_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/3bb9866c-070d-447a-8e7a-1575f76d89d9",
            "content_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/3bb9866c-070d-447a-8e7a-1575f76d89d9/content",
            "title": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
            "content": "{\n    \"anonymous\": false,\n    \"inputs\": [\n        {\n            \"indexed\": true,\n            \"internalType\": \"uint256\",\n            \"name\": \"roundTripId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"indexed\": true,\n            \"internalType\": \"bytes32\",\n            \"name\": \"vrfRequestId\",\n            \"type\": \"bytes32\"\n        },\n        {\n            \"indexed\": true,\n            \"internalType\": \"address\",\n            \"name\": \"owner\",\n            \"type\": \"address\"\n        },\n        {\n            \"indexed\": false,\n            \"internalType\": \"address\",\n            \"name\": \"playerWallet\",\n            \"type\": \"address\"\n        }\n    ],\n    \"name\": \"EvolutionRNGRequestedV2\",\n    \"type\": \"event\",\n    \"selector\": \"0x630211b1\"\n}",
            "tags": [
                "abi_method_hash:f25143e8e517004cfd5531b71dcdb2f2",
                "abi_name:EvolutionRNGRequestedV2",
                "abi_selector:0x630211b1",
                "address:0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                "historical_crawl_status:in_progress",
                "moonworm_task_pickedup:True",
                "progress:0.04",
                "status:active",
                "subscription_type:polygon_smartcontract",
                "task_type:moonworm",
                "type:event"
            ],
            "created_at": "2023-07-24 19:24:25.956879+00:00",
            "updated_at": "2023-07-24 19:24:25.956879+00:00",
            "score": 1.0,
            "context_type": "bugout",
            "context_id": null,
            "context_url": null
        },
        {
            "entry_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/e9009317-9942-4c52-8626-21cccb557faf",
            "content_url": "https://spire.bugout.dev/journals/8cebecca-bcaf-41b4-a37e-b084dfdbf968/entries/e9009317-9942-4c52-8626-21cccb557faf/content",
            "title": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
            "content": "{\n    \"anonymous\": false,\n    \"inputs\": [\n        {\n            \"indexed\": true,\n            \"internalType\": \"uint256\",\n            \"name\": \"roundTripId\",\n            \"type\": \"uint256\"\n        },\n        {\n            \"indexed\": true,\n            \"internalType\": \"uint256\",\n            \"name\": \"eggId\",\n            \"type\": \"uint256\"\n        }\n    ],\n    \"name\": \"BreedingComplete\",\n    \"type\": \"event\",\n    \"selector\": \"0x6a240f3d\"\n}",
            "tags": [
                "abi_method_hash:743e705e20ee4cdecc2771e4735f9c02",
                "abi_name:BreedingComplete",
                "abi_selector:0x6a240f3d",
                "address:0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                "historical_crawl_status:in_progress",
                "moonworm_task_pickedup:True",
                "progress:0.04",
                "status:active",
                "subscription_type:polygon_smartcontract",
                "task_type:moonworm",
                "type:event"
            ],
            "created_at": "2023-07-24 19:24:25.956879+00:00",
            "updated_at": "2023-07-24 19:24:25.956879+00:00",
            "score": 1.0,
            "context_type": "bugout",
            "context_id": null,
            "context_url": null
        }
"""


def get_moonworm_tasks_state(
    journal_id: str = MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    token: str = MOONSTREAM_ADMIN_ACCESS_TOKEN,
    blockchain: str = "ethereum",
):
    """
    Return list of tags depends on query and tag
    """

    entries = get_all_entries_from_search(
        journal_id=journal_id,
        search_query=f"#subscription_type:polygon_smartcontract #moonworm_task_pickedup:True",
        limit=100,
        token=token,
    )

    print(f"Found {len(entries)} moonworm tasks")

    ### loop over tasks split by historical_crawl_status:in_progress and historical_crawl_status:finished and historical_crawl_status:pending

    tasks = {
        "in_progress": {},
        "finished": {},
        "pending": {},
    }

    for entry in entries:
        historical_crawl_status = [
            tag for tag in entry.tags if tag.startswith("historical_crawl_status:")
        ]

        address = [tag for tag in entry.tags if tag.startswith("address:")]

        progress = [tag for tag in entry.tags if tag.startswith("progress:")]

        abi_name = [tag for tag in entry.tags if tag.startswith("abi_name:")]

        if len(historical_crawl_status) == 0:
            logger.warn(
                f"Unable to find historical_crawl_status in task: {entry.entry_url.split()[-1]}"
            )
            continue

        historical_crawl_status = historical_crawl_status[0].split(":")[1]
        address = address[0].split(":")[1]
        progress = progress[0].split(":")[1]
        abi_name = abi_name[0].split(":")[1]

        if historical_crawl_status not in tasks:
            tasks[historical_crawl_status] = {}
        if address not in tasks[historical_crawl_status]:
            tasks[historical_crawl_status][address] = {}

        if abi_name not in tasks[historical_crawl_status][address]:
            tasks[historical_crawl_status][address][abi_name] = progress

    return tasks
