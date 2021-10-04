"""
Tools to build derived relations from raw data (nfts, transfers, mints relations).

For example:
- Current owner of each token
- Current value of each token
"""
import logging
from typing import List, Tuple
import sqlite3


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class LastValue:
    """
    Stores the last seen value in a given column. This is meant to be used as an aggregate function.
    We use it, for example, to get the current owner of an NFT (inside a given window of time).
    """

    def __init__(self):
        self.value = None

    def step(self, value):
        self.value = value

    def finalize(self):
        return self.value


def ensure_custom_aggregate_functions(conn: sqlite3.Connection) -> None:
    """
    Loads custom aggregate functions to an active SQLite3 connection.
    """
    conn.create_aggregate("last_value", 1, LastValue)


def current_owners(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Requires a connection to a dataset in which the raw data (esp. transfers) has already been
    loaded.
    """
    ensure_custom_aggregate_functions(conn)
    drop_existing_current_owners_query = "DROP TABLE IF EXISTS current_owners;"
    current_owners_query = """
    CREATE TABLE current_owners AS
        SELECT nft_address, token_id, CAST(last_value(to_address) AS TEXT) AS owner FROM transfers
        GROUP BY nft_address, token_id;"""
    cur = conn.cursor()
    try:
        cur.execute(drop_existing_current_owners_query)
        cur.execute(current_owners_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: current_owners")
        logger.error(e)


def current_values_distribution(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Requires a connection to a dataset in which the raw data (esp. transfers) has already been
    loaded.
    """
    ensure_custom_aggregate_functions(conn)
    drop_existing_values_distribution_query = (
        "DROP TABLE IF EXISTS market_values_distribution;"
    )
    current_values_distribution_query = """
    CREATE TABLE market_values_distribution AS
        select nft_address as address, market_value as value,  CUME_DIST() over (PARTITION BY nft_address ORDER BY market_value) as cumulate_value from current_market_values;"""
    cur = conn.cursor()
    try:
        cur.execute(drop_existing_values_distribution_query)
        cur.execute(current_values_distribution_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: current_owners")
        logger.error(e)
