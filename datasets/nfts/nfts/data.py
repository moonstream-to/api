"""
Data structures used in (and as part of the maintenance of) the Moonstream NFTs dataset
"""
from dataclasses import dataclass
from enum import Enum
from os import name
from typing import Optional


@dataclass
class BlockBounds:
    starting_block: int
    ending_block: Optional[int] = None


class EventType(Enum):
    TRANSFER = "nft_transfer"
    MINT = "nft_mint"
    ERC721 = "erc721"


event_types = {event_type.value: event_type for event_type in EventType}


def nft_event(raw_event: str) -> EventType:
    try:
        return event_types[raw_event]
    except KeyError:
        raise ValueError(f"Unknown nft event type: {raw_event}")


@dataclass
class NFTEvent:
    event_id: str
    event_type: EventType
    nft_address: str
    token_id: str
    from_address: str
    to_address: str
    transaction_hash: str
    value: Optional[int] = None
    block_number: Optional[int] = None
    timestamp: Optional[int] = None


@dataclass
class NFTMetadata:
    address: str
    name: str
    symbol: str
