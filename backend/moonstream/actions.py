import json
import logging
from typing import Optional, Dict, Any, Union
from enum import Enum
import uuid

import boto3  # type: ignore
from bugout.data import BugoutSearchResults
from bugout.journal import SearchOrder
from moonstreamdb.models import (
    EthereumLabel,
)
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import data
from .reporter import reporter
from .middleware import MoonstreamHTTPException
from .settings import ETHERSCAN_SMARTCONTRACTS_BUCKET
from bugout.data import BugoutResource
from .settings import (
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
)

logger = logging.getLogger(__name__)
ETHERSCAN_SMARTCONTRACT_LABEL_NAME = "etherscan_smartcontract"


class StatusAPIException(Exception):
    """
    Raised during checking Moonstream API statuses.
    """


def get_contract_source_info(
    db_session: Session, contract_address: str
) -> Optional[data.EthereumSmartContractSourceInfo]:
    labels = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == contract_address)
        .all()
    )
    if not labels:
        return None

    for label in labels:
        if label.label == ETHERSCAN_SMARTCONTRACT_LABEL_NAME:
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


class LabelNames(Enum):
    ETHERSCAN_SMARTCONTRACT = "etherscan_smartcontract"
    COINMARKETCAP_TOKEN = "coinmarketcap_token"
    ERC721 = "erc721"


def get_ethereum_address_info(
    db_session: Session, address: str
) -> Optional[data.EthereumAddressInfo]:

    address_info = data.EthereumAddressInfo(address=address)
    etherscan_address_url = f"https://etherscan.io/address/{address}"
    etherscan_token_url = f"https://etherscan.io/token/{address}"
    blockchain_com_url = f"https://www.blockchain.com/eth/address/{address}"
    # Checking for token:
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
