from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from moonstreamdb.models import (
    EthereumAddress,
    EthereumLabel,
    EthereumTransaction,
    EthereumBlock,
)
from sqlalchemy.orm import Session


@dataclass
class BlockBounds:
    starting_block: int
    ending_block: Optional[int] = None


class EventType(Enum):
    TRANSFER = "nft_transfer"
    MINT = "nft_mint"


@dataclass
class NFTEvent:
    event_type: EventType
    nft_address: str
    token_id: str
    from_address: str
    to_address: str
    transaction_hash: str
    value: Optional[int] = None
    block_number: Optional[int] = None
    timestamp: Optional[int] = None


def get_rows(
    db_session: Session, event_type: EventType, bounds: Optional[BlockBounds] = None
) -> List[NFTEvent]:
    query = (
        db_session.query(
            EthereumLabel.label,
            EthereumAddress.address,
            EthereumLabel.label_data,
            EthereumLabel.transaction_hash,
        )
        .join(EthereumAddress, EthereumLabel.address_id == EthereumAddress.id)
        .outerjoin(
            EthereumTransaction,
            EthereumLabel.transaction_hash == EthereumTransaction.hash,
        )
        .filter(EthereumLabel.label == event_type.value)
        .limit(10)
    )
    return [
        NFTEvent(
            event_type=label,
            nft_address=address,
            token_id=label_data["tokenId"],
            from_address=label_data["from"],
            to_address=label_data["to"],
            transaction_hash=transaction_hash,
        )
        for label, address, label_data, transaction_hash in query
    ]
