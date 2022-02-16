import hashlib
import json
from itertools import chain
import logging
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid

import boto3  # type: ignore

from bugout.data import BugoutSearchResults, BugoutSearchResult, BugoutResource
from bugout.journal import SearchOrder
from ens.utils import is_valid_ens_name  # type: ignore
from eth_utils.address import is_address  # type: ignore
from moonstreamdb.models import EthereumLabel
from sqlalchemy import text
from sqlalchemy.orm import Session
from web3 import Web3
from web3._utils.validation import validate_abi

from . import data
from .middleware import MoonstreamHTTPException
from .reporter import reporter
from .settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    ETHERSCAN_SMARTCONTRACTS_BUCKET,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_DATA_JOURNAL_ID,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
)
from .settings import bugout_client as bc

logger = logging.getLogger(__name__)


blockchain_by_subscription_id = {
    "ethereum_blockchain": "ethereum",
    "polygon_blockchain": "polygon",
    "ethereum_smartcontract": "ethereum",
    "polygon_smartcontract": "polygon",
}


class StatusAPIException(Exception):
    """
    Raised during checking Moonstream API statuses.
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
    s3_path: str,
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
                    f"does not exists in Abi {s3_path}"
                )
                raise MoonstreamHTTPException(status_code=400)
            if method.get("filters") and isinstance(method["filters"], dict):

                for input_argument_name, value in method["filters"].items():

                    if input_argument_name not in abi_functions[method["name"]]:
                        # Argument not exists
                        logger.error(
                            f"Error on dashboard resource validation type argument: {input_argument_name} of method:{method['name']} "
                            f" of subscription: {dashboard_subscription.subscription_id} has incorrect"
                            f"does not exists in Abi {s3_path}"
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
                    f"does not exists in Abi {s3_path}"
                )
                raise MoonstreamHTTPException(status_code=400)

            if event.get("filters") and isinstance(event["filters"], dict):

                for input_argument_name, value in event["filters"].items():

                    if input_argument_name not in abi_events[event["name"]]:
                        # Argument not exists
                        logger.error(
                            f"Error on dashboard resource validation type argument: {input_argument_name} of method:{event['name']} "
                            f" of subscription: {dashboard_subscription.subscription_id} has incorrect"
                            f"does not exists in Abi {s3_path}"
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

    s3_client = boto3.client("s3")

    bucket = MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET

    result_bytes = abi.encode("utf-8")
    result_key = f"{MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX}/{blockchain_by_subscription_id[resource.resource_data['subscription_type_id']]}/abi/{resource.resource_data['address']}/{resource.id}/abi.json"

    s3_client.put_object(
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

    try:
        existing_metods = bc.search(
            token=token,
            journal_id=journal_id,
            query=search_query,
            content=False,
            timeout=10.0,
            limit=limit,
            offset=offset,
        )
        results.extend(existing_metods.results)

    except Exception as e:
        reporter.error_report(e)

    if len(results) != existing_metods.total_results:

        for offset in range(limit, existing_metods.total_results, limit):
            existing_metods = bc.search(
                token=token,
                journal_id=journal_id,
                query=search_query,
                content=False,
                timeout=10.0,
                limit=limit,
                offset=offset,
            )
        results.extend(existing_metods.results)

    return results


def apply_moonworm_tasks(
    subscription_type: str,
    abi: Any,
    address: str,
) -> None:
    """
    Get list of subscriptions loads abi and apply them as moonworm tasks if it not exist
    """

    entries_pack = []

    try:
        entries = get_all_entries_from_search(
            journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
            search_query=f"tag:address:{address} tag:subscription_type:{subscription_type}",
            limit=100,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        )

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
                entries_pack.append(
                    {
                        "title": address,
                        "content": json.dumps(abi_hashes_dict[hash], indent=4),
                        "tags": [
                            f"address:{address}",
                            f"type:{abi_hashes_dict[hash]['type']}",
                            f"abi_method_hash:{hash}",
                            f"subscription_type:{subscription_type}",
                            f"abi_name:{abi_hashes_dict[hash]['name']}",
                            f"status:active",
                        ],
                    }
                )
    except Exception as e:
        reporter.error_report(e)

    if len(entries_pack) > 0:
        bc.create_entries_pack(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
            entries=entries_pack,
            timeout=15,
        )
