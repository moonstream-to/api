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
from sqlalchemy import or_
from sqlalchemy.orm import Session
from tqdm import tqdm
from web3 import Web3
import requests

from .data import BlockBounds, EventType, NFTEvent, event_types, nft_event
from .datastore import get_checkpoint_offset, insert_checkpoint, insert_events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EthereumBatchloader:
    def __init__(self, jrpc_url) -> None:

        self.jrpc_url = jrpc_url
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
            r = requests.post(self.jrpc_url, headers=headers, data=payload, timeout=300)
        except Exception as e:
            print(e)
        return r

    def send_json_message(self, message):
        encoded_json = json.dumps(message)
        raw_response = self.send_message(encoded_json.encode("utf8"))
        response = raw_response.json()
        return response


def enrich_from_web3(
    web3_client: Web3,
    nft_events: List[NFTEvent],
    batch_loader: EthereumBatchloader,
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
    jrpc_response = batch_loader.load_transactions(list(transactions_to_query))
    breakpoint()
    transactions_map = {
        result["result"]["hash"]: (
            int(result["result"]["value"], 16),
            int(result["result"]["blockNumber"], 16),
        )
        for result in jrpc_response
    }

    blocks_to_query: Set[int] = set()
    for index in indices_to_update:
        nft_events[index].value, nft_events[index].block_number = transactions_map[
            nft_events[index].transaction_hash
        ]
        blocks_to_query.add(cast(int, nft_events[index].block_number))

    if len(blocks_to_query) == 0:
        return nft_events
    jrpc_response = batch_loader.load_blocks(list(blocks_to_query), False)
    blocks_map = {
        int(result["result"]["number"], 16): int(result["result"]["timestamp"], 16)
        for result in jrpc_response
    }
    for index in indices_to_update:
        nft_events[index].timestamp = blocks_map[cast(int, nft_event.block_number)]
    return nft_events


def get_events(
    db_session: Session,
    event_type: EventType,
    bounds: Optional[BlockBounds] = None,
    initial_offset: int = 0,
    batch_size: int = 1000,
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
        .order_by(EthereumLabel.created_at)
    )
    if bounds is not None:
        bounds_filters = [
            EthereumTransaction.hash == None,
            EthereumTransaction.block_number >= bounds.starting_block,
        ]
        if bounds.ending_block is not None:
            bounds_filters.append(
                EthereumTransaction.block_number <= bounds.ending_block
            )
        query = query.filter(or_(*bounds_filters))
    offset = initial_offset
    while True:
        events = query.offset(offset).limit(batch_size).all()
        if not events:
            break
        offset += batch_size
        for (
            label,
            address,
            label_data,
            transaction_hash,
            value,
            block_number,
            timestamp,
        ) in events:
            raw_event = NFTEvent(
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
            yield raw_event


def create_dataset(
    datastore_conn: sqlite3.Connection,
    db_session: Session,
    web3_client: Web3,
    event_type: EventType,
    batch_loader: EthereumBatchloader,
    bounds: Optional[BlockBounds] = None,
    batch_size: int = 1000,
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

    raw_events = get_events(db_session, event_type, bounds, offset, batch_size)
    raw_events_batch: List[NFTEvent] = []

    for event in tqdm(raw_events, desc="Events processed", colour="#DD6E0F"):
        raw_events_batch.append(event)
        if len(raw_events_batch) == batch_size:
            logger.info("Writing batch of events to datastore")

            insert_events(datastore_conn, raw_events_batch)
            offset += batch_size

            insert_checkpoint(
                datastore_conn, event_type, offset, event.transaction_hash
            )
            raw_events_batch = []
    logger.info("Writing remaining events to datastore")
    insert_events(
        datastore_conn, enrich_from_web3(web3_client, raw_events_batch, batch_loader)
    )
