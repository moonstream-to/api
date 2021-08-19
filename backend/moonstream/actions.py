import logging

from typing import List, Optional

from moonstreamdb.models import (
    EthereumAddress,
    EthereumLabel,
)
from sqlalchemy.orm import Session

from . import data

logger = logging.getLogger(__name__)


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
