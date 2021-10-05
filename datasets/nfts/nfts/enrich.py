import logging
import sqlite3
from typing import Any, cast, Iterator, List, Optional, Set
import json

from tqdm import tqdm
import requests

from .data import BlockBounds, EventType, NFTEvent, event_types
from .datastore import (
    get_checkpoint_offset,
    get_events_for_enrich,
    insert_address_metadata,
    insert_checkpoint,
    insert_events,
    update_events_batch,
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
            raise e
        return r

    def send_json_message(self, message):
        encoded_json = json.dumps(message)
        raw_response = self.send_message(encoded_json.encode("utf8"))
        response = raw_response.json()
        return response


def enrich_from_web3(
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
            nft_event.block_number == "None"
            or nft_event.value == "None"
            or nft_event.timestamp == "None"
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

    return nft_events


def enrich(
    datastore_conn: sqlite3.Connection,
    event_type: EventType,
    batch_loader: EthereumBatchloader,
    batch_size: int = 1000,
) -> None:
    events = get_events_for_enrich(datastore_conn, event_type)
    events_batch = []
    for event in tqdm(events, f"Processing events for {event_type.value} event type"):
        events_batch.append(event)
        if len(events_batch) == batch_size:
            logger.info("Getting data from JSONrpc")
            enriched_events = enrich_from_web3(
                events_batch,
                batch_loader,
            )
            update_events_batch(datastore_conn, enriched_events)
            events_batch = []

    logger.info("Getting data from JSONrpc")
    enriched_events = enrich_from_web3(
        events_batch,
        batch_loader,
    )
    update_events_batch(datastore_conn, enriched_events)
