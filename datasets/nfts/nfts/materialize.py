import logging
import sqlite3
from typing import Any, Iterator, List, Optional
import json

from sqlalchemy.sql.expression import select

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

from .data import BlockBounds, EventType, NFTEvent, event_types
from .datastore import insert_events

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

    def put_to_batch(self, command: str, *params, **kwargs):
        """
        Put command request to batch
        """

        self.message_number += 1
        rpc = {
            "jsonrpc": "2.0",
            "id": self.message_number,
            "method": command,
            "params": [i for i in params],
        }

        self.requests_banch.append(rpc)

        self.commands.append(command)

    def send_message(self, payload):
        headers = {"Content-Type": "application/json"}

        try:
            r = requests.post(self.jrpc_url, headers=headers, data=payload)
        except Exception as e:
            print(e)
        return r

    def send_json_message(self, message):
        encoded_json = json.dumps(message)
        response = self.send_message(encoded_json.encode("utf8")).json()
        return response

    def process_batch(self):
        """
        Start processing batch of requests 
        return dict with banches of responces
        """

        responses = self.send_json_message(self.requests_banch)

        returned_objects = {}

        for i, response in enumerate(responses):
            if not returned_objects.get(self.commands[i]):
                returned_objects[self.commands[i]] = [response]
            else:
                returned_objects[self.commands[i]].append(response)

        self.commands.clear()
        self.requests_banch.clear()
        self.message_number = 0

        return returned_objects


def enrich_from_web3(web3_client: Web3, nft_event: NFTEvent) -> NFTEvent:
    """
    Adds block number, value, timestamp from web3 if they are None (because that transaction is missing in db)
    """
    if (
        nft_event.block_number is None
        or nft_event.value is None
        or nft_event.timestamp is None
    ):
        logger.info("Enriching from web3")
        transaction = web3_client.eth.get_transaction(nft_event.transaction_hash)
        nft_event.value = transaction["value"]
        nft_event.block_number = transaction["blockNumber"]
        block = web3_client.eth.get_block(transaction["blockNumber"])
        nft_event.timestamp = block["timestamp"]
    return nft_event


def get_events(
    db_session: Session,
    web3_client: Web3,
    event_type: EventType,
    bounds: Optional[BlockBounds] = None,
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

    offset = 0
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
            event = enrich_from_web3(web3_client, raw_event)
            yield event


def create_dataset(
    datastore_conn: sqlite3.Connection,
    db_session: Session,
    web3_client: Web3,
    event_type: EventType,
    bounds: Optional[BlockBounds] = None,
    batch_size: int = 1000,
    batch_loader: EthereumBatchloader = None,
) -> None:
    """
    Creates Moonstream NFTs dataset in the given SQLite datastore.
    """
    events = get_events(db_session, web3_client, event_type, bounds, batch_size)
    events_batch: List[NFTEvent] = []
    for event in tqdm(events, desc="Events processed", colour="#DD6E0F"):
        events_batch.append(event)
        if len(events_batch) == batch_size:
            logger.info("Writing batch of events to datastore")
            insert_events(datastore_conn, events_batch)
            events_batch = []
    logger.info("Writing remaining events to datastore")
    insert_events(datastore_conn, events_batch)

