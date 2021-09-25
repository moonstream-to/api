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
from web3 import Web3


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


def preproccess(
    db_session: Session, web3_client: Web3, nft_events: List[NFTEvent]
) -> List[NFTEvent]:
    """
    Adds block number, value, timestamp from web3 if they are None (because that transaction is missing in db)
    """
    for nft_event in nft_events:
        if nft_event.block_number is None:
            transaction = web3_client.eth.get_transaction(nft_event.transaction_hash)
            nft_event.value = transaction["value"]
            nft_event.block_number = transaction["blockNumber"]
            block = web3_client.eth.get_block(transaction["blockNumber"])
            nft_event.timestamp = block["timestamp"]
    return nft_events


def get_rows(
    db_session: Session, event_type: EventType, bounds: Optional[BlockBounds] = None
) -> List[NFTEvent]:
    query = (
        db_session.query(
            EthereumLabel.label,
            EthereumAddress.address,
            EthereumLabel.label_data,
            EthereumLabel.transaction_hash,
            EthereumTransaction.value,
            EthereumTransaction.block_number,
            EthereumBlock.timestamp,
        )
        .join(EthereumAddress, EthereumLabel.address_id == EthereumAddress.id)
        .outerjoin(
            EthereumTransaction,
            EthereumLabel.transaction_hash == EthereumTransaction.hash,
        )
        .outerjoin(
            EthereumBlock,
            EthereumTransaction.block_number == EthereumBlock.block_number,
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
            value=value,
            block_number=block_number,
            timestamp=timestamp,
        )
        for label, address, label_data, transaction_hash, value, block_number, timestamp in query
    ]
