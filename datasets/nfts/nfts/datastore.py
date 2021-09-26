"""
This module provides tools to interact with and maintain a SQLite database which acts/should act as
a datastore for a Moonstream NFTs dataset.
"""

import sqlite3
from typing import Any, List, Tuple

from .data import EventType, NFTEvent

event_tables = {EventType.TRANSFER: "transfers", EventType.MINT: "mints"}

CREATE_NFTS_TABLE_QUERY = """CREATE TABLE nfts
    (
        address TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
        name TEXT,
        symbol TEXT
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
        value INT,
        timestamp INT
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
    value,
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
        event.transaction_hash,
        event.block_number,
        event.nft_address,
        event.token_id,
        event.from_address,
        event.to_address,
        int(event.value),
        event.timestamp,
    )


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
        cur.executemany(insert_events_query(EventType.MINT), mints)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
