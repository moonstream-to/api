import hashlib
import json
import logging
import uuid
from collections import OrderedDict
from enum import Enum
from itertools import chain
from typing import Any, Dict, List, Optional, Union

import boto3  # type: ignore
from bugout.data import (
    BugoutJournal,
    BugoutJournals,
    BugoutResource,
    BugoutResources,
    BugoutSearchResult,
    BugoutSearchResults,
)
from bugout.exceptions import BugoutResponseException
from bugout.journal import SearchOrder
from ens.utils import is_valid_ens_name  # type: ignore
from eth_utils.address import is_address  # type: ignore
from moonstreamdb.blockchain import AvailableBlockchainType
from moonstreamdb.models import EthereumLabel
from slugify import slugify  # type: ignore
from sqlalchemy import text
from sqlalchemy.orm import Session
from web3 import Web3
from web3._utils.validation import validate_abi

from . import data
from .middleware import MoonstreamHTTPException
from .reporter import reporter
from .selectors_storage import selectors
from .settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    ETHERSCAN_SMARTCONTRACTS_BUCKET,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_DATA_JOURNAL_ID,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
)
from .settings import bugout_client as bc
from .settings import multicall_contracts, support_interfaces, supportsInterface_abi
from .web3_provider import FunctionSignature, connect, multicall

logger = logging.getLogger(__name__)


blockchain_by_subscription_id = {
    "ethereum_blockchain": "ethereum",
    "polygon_blockchain": "polygon",
    "mumbai_blockchain": "mumbai",
    "xdai_blockchain": "xdai",
    "wyrm_blockchain": "wyrm",
    "zksync_era_testnet_blockchain": "zksync_era_testnet",
    "ethereum_smartcontract": "ethereum",
    "polygon_smartcontract": "polygon",
    "mumbai_smartcontract": "mumbai",
    "xdai_smartcontract": "xdai",
    "wyrm_smartcontract": "wyrm",
    "zksync_era_testnet_smartcontract": "zksync_era_testnet",
}


class StatusAPIException(Exception):
    """
    Raised during checking Moonstream API statuses.
    """


class NameNormalizationException(Exception):
    """
    Raised on actions when slugify can't normalize name.
    """


class ResourceQueryFetchException(Exception):
    """
    Exception in queries API
    """


class EntityJournalNotFoundException(Exception):
    """
    Raised when journal (collection prev.) with entities not found.
    """


class AddressNotSmartContractException(Exception):
    """
    Raised when address not are smart contract
    """


class LabelNames(Enum):
    ETHERSCAN_SMARTCONTRACT = "etherscan_smartcontract"
    COINMARKETCAP_TOKEN = "coinmarketcap_token"
    ERC721 = "erc721"


def get_contract_source_info(
    db_session: Session, contract_address: str
) -> Optional[data.EthereumSmartContractSourceInfo]:
    label = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == contract_address)
        .filter(EthereumLabel.label == LabelNames.ETHERSCAN_SMARTCONTRACT.value)
        .one_or_none()
    )
    if label is None:
        return None

    object_uri = label.label_data["object_uri"]
    key = object_uri.split("s3://etherscan-smart-contracts/")[1]
    s3 = boto3.client("s3")
    bucket = ETHERSCAN_SMARTCONTRACTS_BUCKET
    try:
        raw_obj = s3.get_object(Bucket=bucket, Key=key)
        obj_data = json.loads(raw_obj["Body"].read().decode("utf-8"))["data"]
        contract_source_info = data.EthereumSmartContractSourceInfo(
            name=obj_data["ContractName"],
            source_code=obj_data["SourceCode"],
            compiler_version=obj_data["CompilerVersion"],
            abi=obj_data["ABI"],
        )
        return contract_source_info
    except Exception as e:
        logger.error(f"Failed to load smart contract {object_uri}")
        reporter.error_report(e)

    return None


def get_ens_name(web3: Web3, address: str) -> Optional[str]:
    try:
        checksum_address = web3.toChecksumAddress(address)
    except:
        raise ValueError(f"{address} is invalid ethereum address is passed")
    try:
        ens_name = web3.ens.name(checksum_address)
        return ens_name
    except Exception as e:
        reporter.error_report(e, ["web3", "ens"])
        logger.error(
            f"Cannot get ens name for address {checksum_address}. Probably node is down"
        )
        raise e


def get_ens_address(web3: Web3, name: str) -> Optional[str]:
    if not is_valid_ens_name(name):
        raise ValueError(f"{name} is not valid ens name")

    try:
        ens_checksum_address = web3.ens.address(name)
        if ens_checksum_address is not None:
            ordinary_address = ens_checksum_address.lower()
            return ordinary_address
        return None
    except Exception as e:
        reporter.error_report(e, ["web3", "ens"])
        logger.error(f"Cannot get ens address for name {name}. Probably node is down")
        raise e


def get_ethereum_address_info(
    db_session: Session, web3: Web3, address: str
) -> Optional[data.EthereumAddressInfo]:
    if not is_address(address):
        raise ValueError(f"Invalid ethereum address : {address}")

    address_info = data.EthereumAddressInfo(address=address)

    try:
        address_info.ens_name = get_ens_name(web3, address)
    except:
        pass

    etherscan_address_url = f"https://etherscan.io/address/{address}"
    etherscan_token_url = f"https://etherscan.io/token/{address}"
    blockchain_com_url = f"https://www.blockchain.com/eth/address/{address}"

    coinmarketcap_label: Optional[EthereumLabel] = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label == LabelNames.COINMARKETCAP_TOKEN.value)
        .order_by(text("created_at desc"))
        .limit(1)
        .one_or_none()
    )

    if coinmarketcap_label is not None:
        address_info.token = data.EthereumTokenDetails(
            name=coinmarketcap_label.label_data["name"],
            symbol=coinmarketcap_label.label_data["symbol"],
            external_url=[
                coinmarketcap_label.label_data["coinmarketcap_url"],
                etherscan_token_url,
                blockchain_com_url,
            ],
        )

    # Checking for smart contract
    etherscan_label: Optional[EthereumLabel] = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label == LabelNames.ETHERSCAN_SMARTCONTRACT.value)
        .order_by(text("created_at desc"))
        .limit(1)
        .one_or_none()
    )
    if etherscan_label is not None:
        address_info.smart_contract = data.EthereumSmartContractDetails(
            name=etherscan_label.label_data["name"],
            external_url=[etherscan_address_url, blockchain_com_url],
        )

    # Checking for NFT
    # Checking for smart contract
    erc721_label: Optional[EthereumLabel] = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label == LabelNames.ERC721.value)
        .order_by(text("created_at desc"))
        .limit(1)
        .one_or_none()
    )
    if erc721_label is not None:
        address_info.nft = data.EthereumNFTDetails(
            name=erc721_label.label_data.get("name"),
            symbol=erc721_label.label_data.get("symbol"),
            total_supply=erc721_label.label_data.get("totalSupply"),
            external_url=[etherscan_token_url, blockchain_com_url],
        )
    return address_info


def get_address_labels(
    db_session: Session, start: int, limit: int, addresses: Optional[str] = None
) -> data.AddressListLabelsResponse:
    """
    Attach labels to addresses.
    """
    if addresses is not None:
        addresses_list = addresses.split(",")
        addresses_obj = addresses_list[start : start + limit]
    else:
        addresses_obj = []

    addresses_response = data.AddressListLabelsResponse(addresses=[])

    for address in addresses_obj:
        labels_obj = (
            db_session.query(EthereumLabel)
            .filter(EthereumLabel.address == address)
            .all()
        )
        addresses_response.addresses.append(
            data.AddressLabelsResponse(
                address=address,
                labels=[
                    data.AddressLabelResponse(
                        label=label.label, label_data=label.label_data
                    )
                    for label in labels_obj
                ],
            )
        )

    return addresses_response


def create_onboarding_resource(
    token: uuid.UUID,
    resource_data: Dict[str, Any] = {
        "type": data.USER_ONBOARDING_STATE,
        "steps": {
            "welcome": 0,
            "subscriptions": 0,
            "stream": 0,
        },
        "is_complete": False,
    },
) -> BugoutResource:
    resource = bc.create_resource(
        token=token,
        application_id=MOONSTREAM_APPLICATION_ID,
        resource_data=resource_data,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    return resource


def check_api_status():
    crawl_types_timestamp: Dict[str, Any] = {
        "ethereum_txpool": None,
        "ethereum_trending": None,
    }
    for crawl_type in crawl_types_timestamp.keys():
        try:
            search_results: BugoutSearchResults = bc.search(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_DATA_JOURNAL_ID,
                query=f"tag:crawl_type:{crawl_type}",
                limit=1,
                content=False,
                timeout=10.0,
                order=SearchOrder.DESCENDING,
            )
            if len(search_results.results) == 1:
                crawl_types_timestamp[crawl_type] = search_results.results[0].created_at
        except Exception:
            raise StatusAPIException(
                f"Unable to get status for crawler with type: {crawl_type}"
            )

    return crawl_types_timestamp


def json_type(evm_type: str) -> type:
    if evm_type.startswith(("uint", "int")):
        return int
    elif evm_type.startswith("bytes") or evm_type == "string" or evm_type == "address":
        return str
    elif evm_type == "bool":
        return bool
    else:
        raise ValueError(f"Cannot convert to python type {evm_type}")


def dashboards_abi_validation(
    dashboard_subscription: data.DashboardMeta,
    abi: Any,
):
    """
    Validate current dashboard subscription : https://github.com/bugout-dev/moonstream/issues/345#issuecomment-953052444
    with contract abi on S3

    """

    # maybe its over but not found beter way
    abi_functions = {
        item["name"]: {inputs["name"]: inputs["type"] for inputs in item["inputs"]}
        for item in abi
        if item["type"] == "function"
    }
    if not dashboard_subscription.all_methods:
        for method in dashboard_subscription.methods:
            if method["name"] not in abi_functions:
                # Method not exists
                logger.error(
                    f"Error on dashboard resource validation method:{method['name']}"
                    f" of subscription: {dashboard_subscription.subscription_id}"
                    f"does not exists in Abi "
                )
                raise MoonstreamHTTPException(status_code=400)
            if method.get("filters") and isinstance(method["filters"], dict):
                for input_argument_name, value in method["filters"].items():
                    if input_argument_name not in abi_functions[method["name"]]:
                        # Argument not exists
                        logger.error(
                            f"Error on dashboard resource validation type argument: {input_argument_name} of method:{method['name']} "
                            f" of subscription: {dashboard_subscription.subscription_id} has incorrect"
                            f"does not exists in Abi"
                        )
                        raise MoonstreamHTTPException(status_code=400)

                    if not isinstance(
                        value,
                        json_type(abi_functions[method["name"]][input_argument_name]),
                    ):
                        # Argument has incorrect type
                        logger.error(
                            f"Error on dashboard resource validation type argument: {input_argument_name} of method:{method['name']} "
                            f" of subscription: {dashboard_subscription.subscription_id} has incorrect type {type(value)}"
                            f" when {abi_functions[method['name']][input_argument_name]} required."
                        )
                        raise MoonstreamHTTPException(status_code=400)
    abi_events = {
        item["name"]: {inputs["name"]: inputs["type"] for inputs in item["inputs"]}
        for item in abi
        if item["type"] == "event"
    }

    if not dashboard_subscription.all_events:
        for event in dashboard_subscription.events:
            if event["name"] not in abi_events:
                logger.error(
                    f"Error on dashboard resource validation event:{event['name']}"
                    f" of subscription: {dashboard_subscription.subscription_id}"
                    f"does not exists in Abi"
                )
                raise MoonstreamHTTPException(status_code=400)

            if event.get("filters") and isinstance(event["filters"], dict):
                for input_argument_name, value in event["filters"].items():
                    if input_argument_name not in abi_events[event["name"]]:
                        # Argument not exists
                        logger.error(
                            f"Error on dashboard resource validation type argument: {input_argument_name} of method:{event['name']} "
                            f" of subscription: {dashboard_subscription.subscription_id} has incorrect"
                            f"does not exists in Abi"
                        )
                        raise MoonstreamHTTPException(status_code=400)

                    if not isinstance(
                        value,
                        json_type(abi_events[event["name"]][input_argument_name]),
                    ):
                        logger.error(
                            f"Error on dashboard resource validation type argument: {input_argument_name} of method:{event['name']} "
                            f" of subscription: {dashboard_subscription.subscription_id} has incorrect type {type(value)}"
                            f" when {abi_events[event['name']][input_argument_name]} required."
                        )
                        raise MoonstreamHTTPException(status_code=400)
    return True


def validate_abi_json(abi: Any) -> None:
    """
    Transform string to json and run validation
    """

    try:
        validate_abi(abi)
    except ValueError as e:
        raise MoonstreamHTTPException(status_code=400, detail=e)
    except:
        raise MoonstreamHTTPException(
            status_code=400, detail="Error on abi valiadation."
        )


def upload_abi_to_s3(
    resource: BugoutResource,
    abi: str,
    update: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Uploading ABI to s3 bucket. Return object for updating resource.

    """

    s3 = boto3.client("s3")

    bucket = MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET

    result_bytes = abi.encode("utf-8")
    result_key = f"{MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX}/{blockchain_by_subscription_id[resource.resource_data['subscription_type_id']]}/abi/{resource.resource_data['address']}/{resource.id}/abi.json"

    s3.put_object(
        Body=result_bytes,
        Bucket=bucket,
        Key=result_key,
        ContentType="application/json",
        Metadata={"Moonstream": "Abi data"},
    )

    update["abi"] = True

    update["bucket"] = MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET
    update["s3_path"] = result_key

    return update


def get_all_entries_from_search(
    journal_id: str, search_query: str, limit: int, token: str
) -> List[BugoutSearchResult]:
    """
    Get all required entries from journal using search interface
    """
    offset = 0

    results: List[BugoutSearchResult] = []

    existing_methods = bc.search(
        token=token,
        journal_id=journal_id,
        query=search_query,
        content=False,
        timeout=10.0,
        limit=limit,
        offset=offset,
    )
    results.extend(existing_methods.results) # type: ignore

    if len(results) != existing_methods.total_results:
        for offset in range(limit, existing_methods.total_results, limit):
            existing_methods = bc.search(
                token=token,
                journal_id=journal_id,
                query=search_query,
                content=False,
                timeout=10.0,
                limit=limit,
                offset=offset,
            )
        results.extend(existing_methods.results) # type: ignore

    return results


def apply_moonworm_tasks(
    subscription_type: str,
    abi: Any,
    address: str,
    entries_limit: int = 100,
) -> None:
    """
    Get list of subscriptions loads abi and apply them as moonworm tasks if it not exist
    """

    moonworm_abi_tasks_entries_pack = []

    try:
        entries = get_all_entries_from_search(
            journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
            search_query=f"tag:address:{address} tag:subscription_type:{subscription_type}",
            limit=entries_limit,  # load per request
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        )

        # create historical crawl task in journal

        # will use create_entries_pack for creating entries in journal

        existing_tags = [entry.tags for entry in entries]

        existing_hashes = [
            tag.split(":")[-1]
            for tag in chain(*existing_tags)
            if "abi_method_hash" in tag
        ]

        abi_hashes_dict = {
            hashlib.md5(json.dumps(method).encode("utf-8")).hexdigest(): method
            for method in abi
            if (method["type"] in ("event", "function"))
            and (method.get("stateMutability", "") != "view")
        }

        for hash in abi_hashes_dict:
            if hash not in existing_hashes:
                abi_selector = Web3.keccak(
                    text=abi_hashes_dict[hash]["name"]
                    + "("
                    + ",".join(
                        map(lambda x: x["type"], abi_hashes_dict[hash]["inputs"])
                    )
                    + ")"
                )[:4].hex()

                moonworm_abi_tasks_entries_pack.append(
                    {
                        "title": address,
                        "content": json.dumps(abi_hashes_dict[hash], indent=4),
                        "tags": [
                            f"address:{address}",
                            f"type:{abi_hashes_dict[hash]['type']}",
                            f"abi_method_hash:{hash}",
                            f"abi_selector:{abi_selector}",
                            f"subscription_type:{subscription_type}",
                            f"abi_name:{abi_hashes_dict[hash]['name']}",
                            f"status:active",
                            f"task_type:moonworm",
                            f"moonworm_task_pickedup:False",  # True if task picked up by moonworm-crawler(default each 120 sec)
                            f"historical_crawl_status:pending",  # pending, in_progress, done
                            f"progress:0",  # 0-100 %
                        ],
                    }
                )
    except Exception as e:
        logger.error(f"Error get moonworm tasks: {str(e)}")
        reporter.error_report(e)

    if len(moonworm_abi_tasks_entries_pack) > 0:
        try:
            bc.create_entries_pack(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
                entries=moonworm_abi_tasks_entries_pack,
                timeout=25,
            )
        except Exception as e:
            logger.error(f"Error create moonworm tasks: {str(e)}")
            reporter.error_report(e)


def name_normalization(query_name: str) -> str:
    """
    Sanitize provided query name.
    """
    try:
        normalized_query_name = slugify(
            query_name, max_length=50, lowercase=False, separator="_"
        )
    except Exception as e:
        logger.error(f"Error in query normalization. Error: {e}")
        raise NameNormalizationException(f"Can't normalize name:{query_name}")

    return normalized_query_name


def get_query_by_name(query_name: str, token: uuid.UUID) -> str:
    """
    Fetch query_id from Brood resources.
    """
    try:
        query_name = name_normalization(query_name)
    except Exception:
        raise NameNormalizationException("Unable to normalize query name")

    params = {"type": data.BUGOUT_RESOURCE_QUERY_RESOLVER, "name": query_name}
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error get query, error: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    available_queries: Dict[str, str] = {
        resource.resource_data["name"]: resource.resource_data["entry_id"]
        for resource in resources.resources
    }

    if query_name not in available_queries:
        raise MoonstreamHTTPException(status_code=404, detail="Query not found.")

    query_id = available_queries[query_name]

    return query_id


def get_entity_subscription_journal_id(
    resource_type: str,
    token: Union[uuid.UUID, str],
    user_id: uuid.UUID,
    create_if_not_exist: bool = False,
) -> str:
    """
    Get collection_id (journal_id) from brood resources. If journal not exist and create_if_not_exist is True
    """

    params = {
        "type": resource_type,
        "user_id": str(user_id),
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({user_id}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if len(resources.resources) == 0:
        if not create_if_not_exist:
            raise EntityJournalNotFoundException("Subscription journal not found.")
        journal_id = generate_journal_for_user(resource_type, token, user_id)

        return journal_id

    else:
        resource = resources.resources[0]
    return resource.resource_data["collection_id"]


def generate_journal_for_user(
    resource_type: str,
    token: Union[uuid.UUID, str],
    user_id: uuid.UUID,
) -> str:
    try:
        # Try get journal

        journals: BugoutJournals = bc.list_journals(token=token)

        available_journals: Dict[str, str] = {
            journal.name: str(journal.id) for journal in journals.journals
        }

        subscription_journal_name = f"subscriptions_{user_id}"

        if subscription_journal_name not in available_journals:
            journal: BugoutJournal = bc.create_journal(
                token=token, name=subscription_journal_name
            )
            journal_id = str(journal.id)
        else:
            journal_id = available_journals[subscription_journal_name]
    except Exception as e:
        logger.error(f"Error create journal, error: {str(e)}")
        raise MoonstreamHTTPException(
            status_code=500, detail="Can't create journal for subscriptions"
        )

    resource_data = {
        "type": resource_type,
        "user_id": str(user_id),
        "collection_id": journal_id,
    }

    try:
        bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data=resource_data,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating subscription resource: {str(e)}")
        logger.error(
            f"Required create resource data: {resource_data}, and grand access to journal: {journal_id}, for user: {user_id}"
        )
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    try:
        bc.update_journal_scopes(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=journal_id,
            holder_type="user",
            holder_id=user_id,
            permission_list=[
                "journals.read",
                "journals.entries.read",
                "journals.entries.create",
                "journals.entries.update",
                "journals.entries.delete",
            ],
        )
        logger.info(
            f"Grand access to journal: {journal_id}, for user: {user_id} successfully"
        )
    except Exception as e:
        logger.error(f"Error updating journal scopes: {str(e)}")
        logger.error(
            f"Required grand access to journal: {journal_id}, for user: {user_id}"
        )
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return journal_id


def generate_s3_access_links(
    method_name: str,
    bucket: str,
    key: str,
    http_method: str,
    expiration: int = 300,
) -> str:
    s3 = boto3.client("s3")
    stats_presigned_url = s3.generate_presigned_url(
        method_name,
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expiration,
        HttpMethod=http_method,
    )

    return stats_presigned_url


def query_parameter_hash(params: Dict[str, Any]) -> str:
    """
    Generate a hash of the query parameters
    """

    hash = hashlib.md5(
        json.dumps(OrderedDict(params), sort_keys=True).encode("utf-8")
    ).hexdigest()

    return hash


def get_list_of_support_interfaces(
    blockchain_type: AvailableBlockchainType,
    address: str,
    user_token: uuid.UUID,
    multicall_method: str = "tryAggregate",
):
    """
    Returns list of interfaces supported by given address
    """

    _, _, is_contract = check_if_smart_contract(
        blockchain_type=blockchain_type, address=address, user_token=user_token
    )

    if not is_contract:
        raise AddressNotSmartContractException(f"Address not are smart contract")

    web3_client = connect(blockchain_type, user_token=user_token)

    contract = web3_client.eth.contract(
        address=Web3.toChecksumAddress(address),
        abi=supportsInterface_abi,
    )

    calls = []

    list_of_interfaces = list(selectors.keys())

    list_of_interfaces.sort()

    for interaface in list_of_interfaces:
        calls.append(
            (
                contract.address,
                FunctionSignature(contract.get_function_by_name("supportsInterface"))
                .encode_data([bytes.fromhex(interaface)])
                .hex(),
            )
        )

    result = {}

    if blockchain_type in multicall_contracts:
        calls = []

        list_of_interfaces = list(selectors.keys())

        list_of_interfaces.sort()

        for interface in list_of_interfaces:
            calls.append(
                (
                    contract.address,
                    FunctionSignature(
                        contract.get_function_by_name("supportsInterface")
                    )
                    .encode_data([bytes.fromhex(interface)])
                    .hex(),
                )
            )

        try:
            multicall_result = multicall(
                web3_client=web3_client,
                blockchain_type=blockchain_type,
                calls=calls,
                method=multicall_method,
            )
        except Exception as e:
            logger.error(f"Error while getting list of support interfaces: {e}")

        for i, selector in enumerate(list_of_interfaces):
            if multicall_result[i][0]:
                supported = FunctionSignature(
                    contract.get_function_by_name("supportsInterface")
                ).decode_data(multicall_result[i][1])

                if supported[0]:
                    result[selectors[selector]["name"]] = {  # type: ignore
                        "selector": selector,
                        "abi": selectors[selector]["abi"],  # type: ignore
                    }

    else:
        general_interfaces = ["IERC165", "IERC721", "IERC1155", "IERC20"]

        basic_selectors = {
            interface["name"]: selector
            for selector, interface in selectors.items()
            if interface["name"] in general_interfaces
        }

        for selector_name in basic_selectors:
            selector_result = contract.get_function_by_name("supportsInterface").call(
                bytes.fromhex(selectors[selector_name])
            )
            if selector_result:
                result[selector_name] = {
                    "selector": basic_selectors[selector_name],
                    "abi": selectors[selectors[selector_name]]["abi"],
                }

    return result


def check_if_smart_contract(
    blockchain_type: AvailableBlockchainType,
    address: str,
    user_token: uuid.UUID,
):
    """
    Checks if address is a smart contract on blockchain
    """
    web3_client = connect(blockchain_type, user_token=user_token)

    is_contract = False

    code = web3_client.eth.getCode(address)
    if code != b"":
        is_contract = True

    return blockchain_type, address, is_contract
