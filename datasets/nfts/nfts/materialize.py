import sqlite3
from typing import Iterator, List, Optional

from moonstreamdb.models import (
    EthereumAddress,
    EthereumLabel,
    EthereumTransaction,
    EthereumBlock,
)
from sqlalchemy.orm import Session
from tqdm import tqdm
from web3 import Web3

from .data import BlockBounds, EventType, NFTEvent, event_types
from .datastore import insert_events


def enrich_from_web3(web3_client: Web3, nft_event: NFTEvent) -> NFTEvent:
    """
    Adds block number, value, timestamp from web3 if they are None (because that transaction is missing in db)
    """
    if (
        nft_event.block_number is None
        or nft_event.value is None
        or nft_event.timestamp is None
    ):
        transaction = web3_client.eth.get_transaction(nft_event.transaction_hash)
        nft_event.value = transaction["value"]
        nft_event.block_number = transaction["blockNumber"]
        block = web3_client.eth.get_block(transaction["blockNumber"])
        nft_event.timestamp = block["timestamp"]
    return nft_event


def get_events_from_db(
    db_session: Session, event_type: EventType, bounds: Optional[BlockBounds] = None
) -> Iterator[NFTEvent]:
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
        .limit(5)
    )

    for (
        label,
        address,
        label_data,
        transaction_hash,
        value,
        block_number,
        timestamp,
    ) in query:
        yield NFTEvent(
            event_type=event_types[label],
            nft_address=address,
            token_id=label_data["tokenId"],
            from_address=label_data["from"],
            to_address=label_data["to"],
            transaction_hash=transaction_hash,
            value=value,
            block_number=block_number,
            timestamp=timestamp,
        )


def create_dataset(
    datastore_conn: sqlite3.Connection,
    db_session: Session,
    web3_client: Web3,
    event_type: EventType,
    batch_size: int = 1000,
) -> None:
    """
    Creates Moonstream NFTs dataset in the given SQLite datastore.
    """
    events = map(
        lambda e: enrich_from_web3(web3_client, e),
        get_events_from_db(db_session, event_type),
    )
    events_batch: List[NFTEvent] = []
    for event in tqdm(events):
        print(event)
        events_batch.append(event)
        if len(events_batch) == batch_size:
            insert_events(datastore_conn, events_batch)
            events_batch = []
    insert_events(datastore_conn, events_batch)
