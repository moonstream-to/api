from dataclasses import is_dataclass
import logging
import sqlite3
from typing import Any, cast, Iterator, List, Optional, Set
import json

from moonstreamdb.models import (
    EthereumAddress,
    EthereumLabel,
    EthereumTransaction,
    EthereumBlock,
)
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from tqdm import tqdm
from web3 import Web3
import requests

from .data import BlockBounds, EventType, NFTEvent, NFTMetadata, event_types
from .datastore import (
    get_checkpoint_offset,
    insert_address_metadata,
    insert_checkpoint,
    insert_events,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EthereumBatchloader:
    def __init__(self, jsonrpc_url) -> None:
        self.jsonrpc_url = jsonrpc_url
        self.message_number = 0
        self.commands: List[Any] = []
        self.requests_banch: List[Any] = []

    def load_blocks(self, block_list: List[int], with_transactions: bool):
        """
        Request list of blocks
        """
        rpc = [
            {
                "jsonrpc": "2.0",
                "id": index,
                "method": "eth_getBlockByNumber",
                "params": params_single,
            }
            for index, params_single in enumerate(
                [[hex(block_number), with_transactions] for block_number in block_list]
            )
        ]
        response = self.send_json_message(rpc)
        return response

    def load_transactions(self, transaction_hashes: List[str]):
        """
        Request list of transactions
        """

        rpc = [
            {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "id": index,
                "params": [tx_hash],
            }
            for index, tx_hash in enumerate(transaction_hashes)
        ]
        response = self.send_json_message(rpc)
        return response

    def send_message(self, payload):
        headers = {"Content-Type": "application/json"}

        try:
            r = requests.post(
                self.jsonrpc_url, headers=headers, data=payload, timeout=300
            )
        except Exception as e:
            print(e)
        return r

    def send_json_message(self, message):
        encoded_json = json.dumps(message)
        raw_response = self.send_message(encoded_json.encode("utf8"))
        response = raw_response.json()
        return response


def enrich_from_web3(
    nft_events: List[NFTEvent],
    batch_loader: EthereumBatchloader,
    bounds: Optional[BlockBounds] = None,
) -> List[NFTEvent]:
    """
    Adds block number, value, timestamp from web3 if they are None (because that transaction is missing in db)
    """
    transactions_to_query = set()
    indices_to_update: List[int] = []
    for index, nft_event in enumerate(nft_events):
        if (
            nft_event.block_number is None
            or nft_event.value is None
            or nft_event.timestamp is None
        ):
            transactions_to_query.add(nft_event.transaction_hash)
            indices_to_update.append(index)

    if len(transactions_to_query) == 0:
        return nft_events
    logger.info("Calling JSON RPC API")
    jsonrpc_transactions_response = batch_loader.load_transactions(
        list(transactions_to_query)
    )
    transactions_map = {
        result["result"]["hash"]: (
            int(result["result"]["value"], 16),
            int(result["result"]["blockNumber"], 16),
        )
        for result in jsonrpc_transactions_response
    }

    blocks_to_query: Set[int] = set()
    for index in indices_to_update:
        nft_events[index].value, nft_events[index].block_number = transactions_map[
            nft_events[index].transaction_hash
        ]
        blocks_to_query.add(cast(int, nft_events[index].block_number))

    if len(blocks_to_query) == 0:
        return nft_events
    jsonrpc_blocks_response = batch_loader.load_blocks(list(blocks_to_query), False)
    blocks_map = {
        int(result["result"]["number"], 16): int(result["result"]["timestamp"], 16)
        for result in jsonrpc_blocks_response
    }
    for index in indices_to_update:
        nft_events[index].timestamp = blocks_map[cast(int, nft_event.block_number)]

    def check_bounds(event: NFTEvent) -> bool:
        if bounds is None:
            return True
        is_admissible = True
        if event.block_number < bounds.starting_block:
            is_admissible = False
        if bounds.ending_block is not None and event.block_number > bounds.ending_block:
            is_admissible = False
        return is_admissible

    admissible_events = [event for event in nft_events if check_bounds(event)]
    return admissible_events


def add_events(
    datastore_conn: sqlite3.Connection,
    db_session: Session,
    event_type: EventType,
    batch_loader: EthereumBatchloader,
    initial_offset=0,
    bounds: Optional[BlockBounds] = None,
    batch_size: int = 10,
) -> None:
    raw_created_at_list = (
        db_session.query(EthereumLabel.created_at)
        .filter(EthereumLabel.label == event_type.value)
        .order_by(EthereumLabel.created_at.asc())
        .distinct(EthereumLabel.created_at)
    ).all()

    created_at_list = [
        created_at[0] for created_at in raw_created_at_list[initial_offset:]
    ]
    query = (
        db_session.query(
            EthereumLabel.id,
            EthereumLabel.label,
            EthereumAddress.address,
            EthereumLabel.label_data,
            EthereumLabel.transaction_hash,
            EthereumTransaction.value,
            EthereumTransaction.block_number,
            EthereumBlock.timestamp,
        )
        .filter(EthereumLabel.label == event_type.value)
        .join(EthereumAddress, EthereumLabel.address_id == EthereumAddress.id)
        .outerjoin(
            EthereumTransaction,
            EthereumLabel.transaction_hash == EthereumTransaction.hash,
        )
        .outerjoin(
            EthereumBlock,
            EthereumTransaction.block_number == EthereumBlock.block_number,
        )
        .order_by(
            EthereumLabel.created_at.asc(),
        )
    )
    if bounds is not None:
        time_filters = [EthereumTransaction.block_number >= bounds.starting_block]
        if bounds.ending_block is not None:
            time_filters.append(EthereumTransaction.block_number <= bounds.ending_block)
        bounds_filters = [EthereumTransaction.hash == None, and_(*time_filters)]

        query = query.filter(or_(*bounds_filters))

    pbar = tqdm(total=(len(raw_created_at_list)))
    pbar.set_description(f"Processing created ats")
    pbar.update(initial_offset)
    batch_start = 0
    batch_end = batch_start + batch_size
    while batch_start <= len(created_at_list):

        events = query.filter(
            EthereumLabel.created_at.in_(created_at_list[batch_start : batch_end + 1])
        ).all()
        if not events:
            continue

        raw_events_batch = []
        for (
            event_id,
            label,
            address,
            label_data,
            transaction_hash,
            value,
            block_number,
            timestamp,
        ) in events:
            raw_event = NFTEvent(
                event_id=event_id,
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
            raw_events_batch.append(raw_event)

        logger.info(f"Adding {len(raw_events_batch)} to database")
        insert_events(
            datastore_conn, enrich_from_web3(raw_events_batch, batch_loader, bounds)
        )
        insert_checkpoint(datastore_conn, event_type, batch_end + initial_offset)
        pbar.update(batch_end - batch_start + 1)
        batch_start = batch_end + 1
        batch_end = min(batch_end + batch_size, len(created_at_list))


def create_dataset(
    datastore_conn: sqlite3.Connection,
    db_session: Session,
    event_type: EventType,
    batch_loader: EthereumBatchloader,
    bounds: Optional[BlockBounds] = None,
    batch_size: int = 10,
) -> None:
    """
    Creates Moonstream NFTs dataset in the given SQLite datastore.
    """
    offset = get_checkpoint_offset(datastore_conn, event_type)
    if offset is not None:
        logger.info(f"Found checkpoint for {event_type.value}: offset = {offset}")
    else:
        offset = 0
        logger.info(f"Did not found any checkpoint for {event_type.value}")

    if event_type == EventType.ERC721:
        add_contracts_metadata(datastore_conn, db_session, offset, batch_size)
    else:
        add_events(
            datastore_conn,
            db_session,
            event_type,
            batch_loader,
            offset,
            bounds,
            batch_size,
        )


def add_contracts_metadata(
    datastore_conn: sqlite3.Connection,
    db_session: Session,
    initial_offset: int = 0,
    batch_size: int = 1000,
) -> None:
    logger.info("Adding erc721 contract metadata")
    query = (
        db_session.query(EthereumLabel.label_data, EthereumAddress.address)
        .filter(EthereumLabel.label == EventType.ERC721.value)
        .join(EthereumAddress, EthereumLabel.address_id == EthereumAddress.id)
        .order_by(EthereumLabel.created_at, EthereumLabel.address_id)
    )

    offset = initial_offset
    while True:
        events = query.offset(offset).limit(batch_size).all()
        if not events:
            break
        offset += len(events)

        events_batch: List[NFTMetadata] = []
        for label_data, address in events:
            events_batch.append(
                NFTMetadata(
                    address=address,
                    name=label_data.get("name", None),
                    symbol=label_data.get("symbol", None),
                )
            )
        insert_address_metadata(datastore_conn, events_batch)
        insert_checkpoint(datastore_conn, EventType.ERC721, offset)
        logger.info(f"Already added {offset}")

    logger.info(f"Added total of {offset-initial_offset} nfts metadata")
