"""
This module provides tools to interact with and maintain a SQLite database which acts/should act as
a datastore for a Moonstream NFTs dataset.
"""
import logging
import sqlite3
from typing import Any, List, Tuple, Optional

from .data import EventType, NFTEvent, nft_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


event_tables = {EventType.TRANSFER: "transfers", EventType.MINT: "mints"}

CREATE_NFTS_TABLE_QUERY = """CREATE TABLE nfts
    (
        address TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
        name TEXT,
        symbol TEXT
    );
"""

CREATE_CHECKPOINT_TABLE_QUERY = """CREATE TABLE checkpoint
    (   
        event_type STRING,
        offset INTEGER,
        transaction_hash STRING
    );
"""


def create_events_table_query(event_type: EventType) -> str:
    creation_query = f"""
CREATE TABLE {event_tables[event_type]}
    (
        transaction_hash TEXT,
        block_number INTEGER,
        nft_address TEXT REFERENCES nfts(address),
        token_id TEXT,
        from_address TEXT,
        to_address TEXT,
        transaction_value INTEGER,
        timestamp INTEGER,
        UNIQUE (transaction_hash, nft_address, from_address, to_address, token_id)
    );
    """
    return creation_query


def setup_database(conn: sqlite3.Connection) -> None:
    """
    Sets up the schema of the Moonstream NFTs dataset in the given SQLite database.
    """
    cur = conn.cursor()
    cur.execute(CREATE_NFTS_TABLE_QUERY)
    cur.execute(create_events_table_query(EventType.TRANSFER))
    cur.execute(create_events_table_query(EventType.MINT))
    cur.execute(CREATE_CHECKPOINT_TABLE_QUERY)
    conn.commit()


def insert_events_query(event_type: EventType) -> str:
    """
    Generates a query which inserts NFT events into the appropriate events table.
    """
    query = f"""
INSERT INTO {event_tables[event_type]}(
    transaction_hash,
    block_number,
    nft_address,
    token_id,
    from_address,
    to_address,
    transaction_value,
    timestamp
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    return query


def nft_event_to_tuple(event: NFTEvent) -> Tuple[Any]:
    """
    Converts an NFT event into a tuple for use with sqlite cursor executemany. This includes
    dropping e.g. the event_type field.
    """
    return (
        str(event.transaction_hash),
        str(event.block_number),
        str(event.nft_address),
        str(event.token_id),
        str(event.from_address),
        str(event.to_address),
        str(event.value),
        str(event.timestamp),
    )


def get_checkpoint_offset(
    conn: sqlite3.Connection, event_type: EventType
) -> Optional[int]:
    cur = conn.cursor()
    response = cur.execute(
        f"SELECT * from checkpoint  where event_type='{event_type.value}' order by rowid desc limit 1"
    )
    for row in response:
        return row[1]
    return None


def insert_checkpoint(
    conn: sqlite3.Connection, event_type: EventType, offset: int, transaction_hash: str
):
    query = f"""
    INSERT INTO checkpoint (
        event_type,
        offset,
        transaction_hash
        ) VALUES (?, ?, ?)
        """
    cur = conn.cursor()
    cur.execute(query, [event_type.value, offset, transaction_hash])


def insert_events(conn: sqlite3.Connection, events: List[NFTEvent]) -> None:
    """
    Inserts the given events into the appropriate events table in the given SQLite database.

    This method works with batches of events.
    """
    cur = conn.cursor()
    try:
        transfers = [
            nft_event_to_tuple(event)
            for event in events
            if event.event_type == EventType.TRANSFER
        ]
        cur.executemany(insert_events_query(EventType.TRANSFER), transfers)
        mints = [
            nft_event_to_tuple(event)
            for event in events
            if event.event_type == EventType.MINT
        ]
        # transfers = []
        # mints = []
        # for event in events:
        #     if event.event_type == EventType.TRANSFER:
        #         transfers.append(nft_event_to_tuple(event))
        #     elif event.event_type == EventType.MINT:
        #         mints.append(nft_event_to_tuple(event))
        cur.executemany(insert_events_query(EventType.TRANSFER), transfers)
        cur.executemany(insert_events_query(EventType.MINT), mints)

        conn.commit()
    except Exception as e:
        logger.error(f"FAILED TO SAVE :{events}")
        conn.rollback()
        raise e
