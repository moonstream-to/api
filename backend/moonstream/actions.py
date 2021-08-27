import json
import logging
from typing import Dict, Any, List, Optional

import boto3  # type: ignore
from moonstreamdb.models import (
    EthereumAddress,
    EthereumLabel,
)
from sqlalchemy.orm import Session

from . import data
from .settings import ETHERSCAN_SMARTCONTRACTS_BUCKET

logger = logging.getLogger(__name__)
ETHERSCAN_SMARTCONTRACT_LABEL_NAME = "etherscan_smartcontract"


def get_contract_source_info(
    db_session: Session, contract_address: str
) -> Optional[data.EthereumSmartContractSourceInfo]:
    query = db_session.query(EthereumAddress.id).filter(
        EthereumAddress.address == contract_address
    )
    id = query.one_or_none()
    if id is None:
        return None
    labels = (
        db_session.query(EthereumLabel).filter(EthereumLabel.address_id == id[0]).all()
    )

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
            except:
                logger.error(f"Failed to load smart contract {object_uri}")
    return None


class AdressType:
    UNKNOWN = 0
    REGULAR = 1
    TOKEN = 2
    SMART_CONTRACT = 3
    NFT = 4
    EXCHANGE = 5


class LabelNames:
    ETHERSCAN_SMARTCONTRACT = "etherscan_smartcontract"
    COINMARKETCAP_TOKEN = "coinmarketcap_token"
    EXCHANGE = "excange"


# TODO(yhtiyar):
# What to do if there is address is both token and smart contract?
def get_ethereum_address_info(
    db_session: Session, address: str
) -> Optional[data.EthereumAddressInfo]:
    query = db_session.query(EthereumAddress.id).filter(
        EthereumAddress.address == address
    )
    id = query.one_or_none()
    if id is None:
        return None
    labels = (
        db_session.query(EthereumLabel).filter(EthereumLabel.address_id == id[0]).all()
    )
    address_info = data.EthereumAddressInfo(address=address)
    for label in labels:
        if label.label == LabelNames.ETHERSCAN_SMARTCONTRACT:
            address_info.address_type = AdressType.SMART_CONTRACT
            address_info.details.name = label.label_data["name"]
            address_info.details.external_URL = (
                f"https://etherscan.io/address/{address}"
            )
        elif label.label == LabelNames.COINMARKETCAP_TOKEN:
            address_info.address_type = AdressType.TOKEN
            address_info.details.name = label.label_data["name"]
            address_info.details.symbol = label.label_data["symbol"]
            address_info.details.external_URL = label.label_data["coinmarketcap_url"]
        elif label.label == LabelNames.EXCHANGE:
            address_info.address_type = AdressType.EXCHANGE
            address_info.details.name = label.label_data["name"]
            address_info.details.symbol = label.label_data["label"]
        else:
            print(f"unknown label {label.label}")

    return address_info


def get_address_labels(
    db_session: Session, start: int, limit: int, addresses: Optional[str] = None
) -> data.AddressListLabelsResponse:
    """
    Attach labels to addresses.
    """
    query = db_session.query(EthereumAddress)
    if addresses is not None:
        addresses_list = addresses.split(",")
        query = query.filter(EthereumAddress.address.in_(addresses_list))

    addresses_obj = query.order_by(EthereumAddress.id).slice(start, start + limit).all()

    addresses_response = data.AddressListLabelsResponse(addresses=[])

    for address in addresses_obj:
        labels_obj = (
            db_session.query(EthereumLabel)
            .filter(EthereumLabel.address_id == address.id)
            .all()
        )
        addresses_response.addresses.append(
            data.AddressLabelsResponse(
                address=address.address,
                labels=[
                    data.AddressLabelResponse(
                        label=label.label, label_data=label.label_data
                    )
                    for label in labels_obj
                ],
            )
        )

    return addresses_response
