import json
import logging
from typing import List, Optional

import boto3
from moonstreamdb.models import (
    EthereumAddress,
    EthereumLabel,
)
from sqlalchemy.orm import Session

from . import data
from .settings import ETHERSCAN_SMARTCONTRACTS_BUCKET

logger = logging.getLogger(__name__)


def get_source_code(
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
        if label.label == "etherscan_smartcontract":
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
                logger.error(f"Failed to load smart contract {contract_address}")
    return None


def get_address_labels(
    db_session: Session, start: int, limit: int, addresses: Optional[List[str]] = None
) -> List[EthereumAddress]:
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
