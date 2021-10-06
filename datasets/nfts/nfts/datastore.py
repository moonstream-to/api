"""
This module provides tools to interact with and maintain a SQLite database which acts/should act as
a datastore for a Moonstream NFTs dataset.
"""
import logging
import sqlite3
from typing import Any, cast, List, Tuple, Optional

from tqdm import tqdm

from .data import EventType, NFTEvent, NFTMetadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


event_tables = {EventType.TRANSFER: "transfers", EventType.MINT: "mints"}

CREATE_NFTS_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS nfts
    (
        address TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
        name TEXT,
        symbol TEXT,
        UNIQUE(address, name, symbol)
    );
"""

BACKUP_NFTS_TABLE_QUERY = "ALTER TABLE nfts RENAME TO nfts_backup;"
DROP_BACKUP_NFTS_TABLE_QUERY = "DROP TABLE IF EXISTS nfts_backup;"
SELECT_NFTS_QUERY = "SELECT address, name, symbol FROM nfts;"

CREATE_CHECKPOINT_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS checkpoint
    (
        event_type STRING,
        offset INTEGER
    );
"""


def create_events_table_query(event_type: EventType) -> str:
    creation_query = f"""
CREATE TABLE IF NOT EXISTS {event_tables[event_type]}
    (
        event_id TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
        transaction_hash TEXT,
        block_number INTEGER,
        nft_address TEXT REFERENCES nfts(address),
        token_id TEXT,
        from_address TEXT,
        to_address TEXT,
        transaction_value INTEGER,
        timestamp INTEGER
    );
    """
    return creation_query


def backup_events_table_query(event_type: EventType) -> str:
    backup_query = f"ALTER TABLE {event_tables[event_type]} RENAME TO {event_tables[event_type]}_backup;"
    return backup_query


def drop_backup_events_table_query(event_type: EventType) -> str:
    drop_query = f"DROP TABLE IF EXISTS {event_tables[event_type]}_backup;"
    return drop_query


def select_events_table_query(event_type: EventType) -> str:
    selection_query = f"""
SELECT
    event_id,
    transaction_hash,
    nft_address,
    token_id,
    from_address,
    to_address,
    transaction_value,
    block_number,
    timestamp
FROM {event_tables[event_type]};
    """

    return selection_query


def get_events_for_enrich(
    conn: sqlite3.Connection, event_type: EventType
) -> List[NFTEvent]:
    def select_query(event_type: EventType) -> str:
        selection_query = f"""
    SELECT
        event_id,
        transaction_hash,
        block_number,
        nft_address,
        token_id,
        from_address,
        to_address,
        transaction_value,
        timestamp
    FROM {event_tables[event_type]} WHERE block_number = 'None';
        """

        return selection_query

    logger.info(f"Loading {event_tables[event_type]} table events for enrich")
    cur = conn.cursor()
    cur.execute(select_query(event_type))

    events: List[NFTEvent] = []

    for row in cur:
        (
            event_id,
            transaction_hash,
            block_number,
            nft_address,
            token_id,
            from_address,
            to_address,
            value,
            timestamp,
        ) = cast(
            Tuple[
                str,
                str,
                Optional[int],
                str,
                str,
                str,
                str,
                Optional[int],
                Optional[int],
            ],
            row,
        )
        event = NFTEvent(
            event_id=event_id,
            event_type=event_type,  # Original argument to this function
            nft_address=nft_address,
            token_id=token_id,
            from_address=from_address,
            to_address=to_address,
            transaction_hash=transaction_hash,
            value=value,
            block_number=block_number,
            timestamp=timestamp,
        )
        events.append(event)
    logger.info(f"Found {len(events)} events to enrich")
    return events


def update_events_batch(conn: sqlite3.Connection, events: List[NFTEvent]) -> None:
    def replace_query(event_type: EventType) -> str:
        query = f"""
    REPLACE INTO {event_tables[event_type]}(
        event_id,
        transaction_hash,
        block_number,
        nft_address,
        token_id,
        from_address,
        to_address,
        transaction_value,
        timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return query

    logger.info("Updating events in sqlite")
    cur = conn.cursor()
    try:
        transfers = [
            nft_event_to_tuple(event)
            for event in events
            if event.event_type == EventType.TRANSFER
        ]

        mints = [
            nft_event_to_tuple(event)
            for event in events
            if event.event_type == EventType.MINT
        ]

        cur.executemany(replace_query(EventType.TRANSFER), transfers)
        cur.executemany(replace_query(EventType.MINT), mints)

        conn.commit()
    except Exception as e:
        logger.error(f"FAILED TO replace!!! :{events}")
        conn.rollback()
        raise e


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
INSERT OR IGNORE INTO {event_tables[event_type]}(
    event_id,
    transaction_hash,
    block_number,
    nft_address,
    token_id,
    from_address,
    to_address,
    transaction_value,
    timestamp
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    return query


def nft_event_to_tuple(
    event: NFTEvent,
) -> Tuple[str, str, str, str, str, str, str, str, str]:
    """
    Converts an NFT event into a tuple for use with sqlite cursor executemany. This includes
    dropping e.g. the event_type field.
    """
    return (
        str(event.event_id),
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


def delete_checkpoints(
    conn: sqlite3.Connection, event_type: EventType, commit: bool = True
) -> None:
    cur = conn.cursor()
    cur.execute(f"DELETE FROM checkpoint where event_type='{event_type.value}';")
    if commit:
        try:
            conn.commit()
        except:
            conn.rollback()
            raise


def insert_checkpoint(conn: sqlite3.Connection, event_type: EventType, offset: int):
    query = f"""
INSERT INTO checkpoint (
    event_type,
    offset
) VALUES (?, ?)
        """
    cur = conn.cursor()
    cur.execute(query, [event_type.value, offset])
    conn.commit()


def insert_address_metadata(
    conn: sqlite3.Connection, metadata_list: List[NFTMetadata]
) -> None:
    cur = conn.cursor()
    query = f"""
INSERT INTO nfts (
    address,
    name,
    symbol
) VALUES (?, ?, ?)
    """
    try:
        nfts = [
            (metadata.address, metadata.name, metadata.symbol)
            for metadata in metadata_list
        ]
        cur.executemany(query, nfts)
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to save :\n {metadata_list}")
        conn.rollback()
        raise e


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

        mints = [
            nft_event_to_tuple(event)
            for event in events
            if event.event_type == EventType.MINT
        ]

        cur.executemany(insert_events_query(EventType.TRANSFER), transfers)
        cur.executemany(insert_events_query(EventType.MINT), mints)

        conn.commit()
    except Exception as e:
        logger.error(f"FAILED TO SAVE :{events}")
        conn.rollback()
        raise e


def import_data(
    target_conn: sqlite3.Connection,
    source_conn: sqlite3.Connection,
    event_type: EventType,
    batch_size: int = 1000,
) -> None:
    """
    Imports the data correspondong to the given event type from the source database into the target
    database.

    Any existing data of that type in the target database is first deleted. It is a good idea to
    create a backup copy of your target database before performing this operation.
    """
    target_cur = target_conn.cursor()
    drop_backup_query = DROP_BACKUP_NFTS_TABLE_QUERY
    backup_table_query = BACKUP_NFTS_TABLE_QUERY
    create_table_query = CREATE_NFTS_TABLE_QUERY
    source_selection_query = SELECT_NFTS_QUERY
    if event_type != EventType.ERC721:
        drop_backup_query = drop_backup_events_table_query(event_type)
        backup_table_query = backup_events_table_query(event_type)
        create_table_query = create_events_table_query(event_type)
        source_selection_query = select_events_table_query(event_type)

    target_cur.execute(drop_backup_query)
    target_cur.execute(backup_table_query)
    target_cur.execute(create_table_query)
    target_conn.commit()

    source_cur = source_conn.cursor()
    source_cur.execute(source_selection_query)

    batch: List[Any] = []

    for row in tqdm(source_cur, desc="Rows processed"):
        if event_type == EventType.ERC721:
            batch.append(NFTMetadata(*cast(Tuple[str, str, str], row)))
        else:
            # Order matches select query returned by select_events_table_query
            (
                event_id,
                transaction_hash,
                nft_address,
                token_id,
                from_address,
                to_address,
                value,
                block_number,
                timestamp,
            ) = cast(
                Tuple[
                    str,
                    str,
                    str,
                    str,
                    str,
                    str,
                    Optional[int],
                    Optional[int],
                    Optional[int],
                ],
                row,
            )
            event = NFTEvent(
                event_id=event_id,
                event_type=event_type,  # Original argument to this function
                nft_address=nft_address,
                token_id=token_id,
                from_address=from_address,
                to_address=to_address,
                transaction_hash=transaction_hash,
                value=value,
                block_number=block_number,
                timestamp=timestamp,
            )
            batch.append(event)

        if len(batch) == batch_size:
            if event_type == EventType.ERC721:
                insert_address_metadata(target_conn, cast(List[NFTMetadata], batch))
            else:
                insert_events(target_conn, cast(List[NFTEvent], batch))

    if event_type == EventType.ERC721:
        insert_address_metadata(target_conn, cast(List[NFTMetadata], batch))
    else:
        insert_events(target_conn, cast(List[NFTEvent], batch))

    target_cur.execute(CREATE_CHECKPOINT_TABLE_QUERY)
    target_conn.commit()

    source_offset = get_checkpoint_offset(source_conn, event_type)
    if source_offset is not None:
        delete_checkpoints(target_conn, event_type, commit=False)
        insert_checkpoint(target_conn, event_type, source_offset)


def filter_data(
    sqlite_db: sqlite3.Connection,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
):
    """
    Run Deletes query depends on filters
    """

    cur = sqlite_db.cursor()
    print(f"Remove by timestamp <= {start_time}")
    if start_time:
        cur.execute(f"DELETE from transfers where timestamp <= {start_time}")
        print(f"Transfers filtered out: {cur.rowcount}")
        sqlite_db.commit()
        cur.execute(f"DELETE from mints where timestamp <= {start_time}")
        print(f"Mints filtered out: {cur.rowcount}")
        sqlite_db.commit()

    print(f"Remove by timestamp >= {end_time}")
    if end_time:
        cur.execute(f"DELETE from transfers where timestamp >= {end_time}")
        print(f"Transfers filtered out: {cur.rowcount}")
        sqlite_db.commit()
        cur.execute(f"DELETE from mints where timestamp >= {end_time}")
        print(f"Mints filtered out: {cur.rowcount}")
        sqlite_db.commit()
