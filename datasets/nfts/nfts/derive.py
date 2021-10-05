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


class LastNonzeroValue:
    """
    Stores the last non-zero value in a given column. This is meant to be used as an aggregate
    function. We use it, for example, to get the current market value of an NFT (inside a given
    window of time).
    """

    def __init__(self):
        self.value = 0

    def step(self, value):
        if value != 0:
            self.value = value

    def finalize(self):
        return self.value


def ensure_custom_aggregate_functions(conn: sqlite3.Connection) -> None:
    """
    Loads custom aggregate functions to an active SQLite3 connection.
    """
    conn.create_aggregate("last_value", 1, LastValue)
    conn.create_aggregate("last_nonzero_value", 1, LastNonzeroValue)


def current_owners(conn: sqlite3.Connection) -> None:
    """
    Requires a connection to a dataset in which the raw data (esp. transfers) has already been
    loaded.
    """
    ensure_custom_aggregate_functions(conn)
    drop_existing_current_owners_query = "DROP TABLE IF EXISTS current_owners;"
    current_owners_query = """
    CREATE TABLE current_owners AS
        SELECT nft_address, token_id, last_value(to_address) AS owner FROM
        (
            SELECT * FROM mints
            UNION ALL
            SELECT * FROM transfers
        )
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


def current_market_values(conn: sqlite3.Connection) -> None:
    """
    Requires a connection to a dataset in which the raw data (esp. transfers) has already been
    loaded.
    """
    ensure_custom_aggregate_functions(conn)
    drop_existing_current_market_values_query = (
        "DROP TABLE IF EXISTS current_market_values;"
    )
    current_market_values_query = """
    CREATE TABLE current_market_values AS
        SELECT nft_address, token_id, last_nonzero_value(transaction_value) AS market_value FROM
        (
            SELECT * FROM mints
            UNION ALL
            SELECT * FROM transfers
        )
        GROUP BY nft_address, token_id;"""
    cur = conn.cursor()
    try:
        cur.execute(drop_existing_current_market_values_query)
        cur.execute(current_market_values_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: current_market_values")


def current_values_distribution(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Requires a connection to a dataset in which current_market_values has already been loaded.
    """
    ensure_custom_aggregate_functions(conn)
    drop_existing_values_distribution_query = (
        "DROP TABLE IF EXISTS market_values_distribution;"
    )
    current_values_distribution_query = """
        CREATE TABLE market_values_distribution AS
        select
            nft_address as address,
            current_market_values.token_id as token_id,
            CAST(current_market_values.market_value as REAL) / max_values.max_value as 
        from
            current_market_values
            inner join (
                select
                    nft_address,
                    max(market_value) as max_value
                from
                    current_market_values
                group by
                    nft_address
            ) as max_values on current_market_values.nft_address = max_values.nft_address;
    """
    cur = conn.cursor()
    try:
        cur.execute(drop_existing_values_distribution_query)
        cur.execute(current_values_distribution_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: current_values_distribution")
        logger.error(e)


def transfer_statistics_by_address(conn: sqlite3.Connection) -> None:
    """
    Create transfer in and transfer out for each address.
    """
    drop_existing_transfer_statistics_by_address_query = (
        "DROP TABLE IF EXISTS transfer_statistics_by_address;"
    )
    transfer_statistics_by_address_query = """
        CREATE TABLE transfer_statistics_by_address AS
        SELECT
            address,
            sum(transfer_out) as transfers_out,
            sum(transfer_in) as transfers_in
        from
            (
                SELECT
                    from_address as address,
                    1 as transfer_out,
                    0 as transfer_in
                from
                    transfers
                UNION
                ALL
                select
                    to_address as address,
                    0 as transfer_out,
                    1 as transfer_in
                from
                    transfers
            )
        group by
            address;
        """
    cur = conn.cursor()
    try:
        cur.execute(drop_existing_transfer_statistics_by_address_query)
        cur.execute(transfer_statistics_by_address_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: current_values_distribution")
        logger.error(e)
