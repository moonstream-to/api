"""
Tools to build derived relations from raw data (nfts, transfers, mints relations).

For example:
- Current owner of each token
- Current value of each token
"""
import logging
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


class QuantileFunction:
    """Split vlues to quantiles"""

    def __init__(self, num_quantiles) -> None:
        self.divider = 1 / num_quantiles

    def __call__(self, value):
        if value is None or value == "None":
            value = 0
        quantile = self.divider
        try:
            while value > quantile:
                quantile += self.divider

            if quantile > 1:
                quantile = 1

            return quantile

        except Exception as err:
            print(err)
            raise


def ensure_custom_aggregate_functions(conn: sqlite3.Connection) -> None:
    """
    Loads custom aggregate functions to an active SQLite3 connection.
    """
    conn.create_aggregate("last_value", 1, LastValue)
    conn.create_aggregate("last_nonzero_value", 1, LastNonzeroValue)
    conn.create_function("quantile_10", 1, QuantileFunction(10))
    conn.create_function("quantile_25", 1, QuantileFunction(25))


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


def current_values_distribution(conn: sqlite3.Connection) -> None:
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
            current_market_values.nft_address as address,
            current_market_values.token_id as token_id,
            CAST(current_market_values.market_value as REAL) / max_values.max_value as relative_value
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
        logger.error("Could not create derived dataset: transfer_statistics_by_address")
        logger.error(e)


def quantile_generating(conn: sqlite3.Connection):
    """
    Create quantile wich depends on setted on class defenition
    """
    ensure_custom_aggregate_functions(conn)
    drop_calculate_10_quantiles = (
        "DROP TABLE IF EXISTS transfer_values_quantile_10_distribution_per_address;"
    )
    calculate_10_quantiles = """
    CREATE TABLE transfer_values_quantile_10_distribution_per_address AS
    select
            cumulate.address as address,
            CAST(quantile_10(cumulate.relative_value) as TEXT) as quantiles,
            cumulate.relative_value as relative_value
        from
        (
                select
                    current_market_values.nft_address as address,
                    COALESCE(
                        CAST(current_market_values.market_value as REAL) / max_values.max_value,
                        0
                    ) as relative_value
                from
                    current_market_values
                    inner join (
                        select
                            current_market_values.nft_address,
                            max(market_value) as max_value
                        from
                            current_market_values
                        group by
                            current_market_values.nft_address
                    ) as max_values on current_market_values.nft_address = max_values.nft_address
        ) as cumulate
    """
    drop_calculate_25_quantiles = (
        "DROP TABLE IF EXISTS transfer_values_quantile_25_distribution_per_address;"
    )
    calculate_25_quantiles = """
    CREATE TABLE transfer_values_quantile_25_distribution_per_address AS
    select
            cumulate.address as address,
            CAST(quantile_25(cumulate.relative_value) as TEXT) as quantiles,
            cumulate.relative_value as relative_value
        from
        (
                select
                    current_market_values.nft_address as address,
                    COALESCE(
                        CAST(current_market_values.market_value as REAL) / max_values.max_value,
                        0
                    ) as relative_value
                from
                    current_market_values
                    inner join (
                        select
                            current_market_values.nft_address,
                            max(market_value) as max_value
                        from
                            current_market_values
                        group by
                            current_market_values.nft_address
                    ) as max_values on current_market_values.nft_address = max_values.nft_address
        ) as cumulate
    """
    cur = conn.cursor()
    try:
        print("Creating transfer_values_quantile_10_distribution_per_address")
        cur.execute(drop_calculate_10_quantiles)
        cur.execute(calculate_10_quantiles)
        print("Creating transfer_values_quantile_25_distribution_per_address")
        cur.execute(drop_calculate_25_quantiles)
        cur.execute(calculate_25_quantiles)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: quantile_generating")
        logger.error(e)


def transfers_mints_connection_table(conn: sqlite3.Connection):
    """
    Create cinnection transfers and mints
    """

    drop_transfers_mints_connection = "DROP TABLE IF EXISTS transfers_mints;"
    transfers_mints_connection = """
    CREATE TABLE transfers_mints as
    select
        transfers.event_id as transfer_id,
        mints.mint_id as mint_id
    from
        transfers
        inner join (
            select
                Max(posable_mints.mints_time) as mint_time,
                posable_mints.transfer_id as transfer_id
            from
                (
                    select
                        mint_id,
                        mints.timestamp as mints_time,
                        transfers.token_id,
                        transfers.timestamp,
                        transfers.event_id as transfer_id
                    from
                        transfers
                        inner join (
                            select
                                mints.event_id as mint_id,
                                mints.nft_address,
                                mints.token_id,
                                mints.timestamp
                            from
                                mints
                            group by
                                mints.nft_address,
                                mints.token_id,
                                mints.timestamp
                        ) as mints on transfers.nft_address = mints.nft_address
                        and transfers.token_id = mints.token_id
                        and mints.timestamp <= transfers.timestamp
                ) as posable_mints
            group by
                posable_mints.transfer_id
        ) as mint_time on mint_time.transfer_id = transfers.event_id
        inner join (
            select
                mints.event_id as mint_id,
                mints.nft_address,
                mints.token_id,
                mints.timestamp
            from
                mints
        ) as mints on transfers.nft_address = mints.nft_address
        and transfers.token_id = mints.token_id
        and mints.timestamp = mint_time.mint_time;
    """
    cur = conn.cursor()
    try:
        cur.execute(drop_transfers_mints_connection)
        cur.execute(transfers_mints_connection)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(
            "Could not create derived dataset: transfers_mints_connection_table"
        )
        logger.error(e)


def mint_holding_times(conn: sqlite3.Connection):

    drop_mints_holding_table = "DROP TABLE IF EXISTS mint_holding_times;"
    mints_holding_table = """
    CREATE TABLE mint_holding_times AS
    SELECT
        days_after_minted.days as days,
        count(*) as num_holds
    from
        (
            SELECT
                mints.nft_address,
                mints.token_id,
                (
                    firsts_transfers.firts_transfer - mints.timestamp
                ) / 86400 as days
            from
                mints
                inner join (
                    select
                        transfers_mints.mint_id,
                        transfers.nft_address,
                        transfers.token_id,
                        min(transfers.timestamp) as firts_transfer
                    from
                        transfers
                    inner join transfers_mints on transfers_mints.transfer_id = transfers.event_id
                    group by
                        transfers.nft_address,
                        transfers.token_id,
                        transfers_mints.mint_id
                ) as firsts_transfers on firsts_transfers.mint_id = mints.event_id
        ) as days_after_minted
    group by days;
    """
    cur = conn.cursor()
    try:
        cur.execute(drop_mints_holding_table)
        cur.execute(mints_holding_table)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: mint_holding_times")
        logger.error(e)


def transfer_holding_times(conn: sqlite3.Connection):
    """
    Create distributions of holding times beetween transfers
    """
    drop_transfer_holding_times = "DROP TABLE IF EXISTS transfer_holding_times;"
    transfer_holding_times = """
    CREATE TABLE transfer_holding_times AS
    select days_beetween.days as days, count(*) as num_holds
        from (SELECT
            middle.address,
            middle.token_id,
            (middle.LEAD - middle.timestamp) / 86400 as days
        from
            (
                SELECT
                    nft_address AS address,
                    token_id as token_id,
                    timestamp as timestamp,
                    LEAD(timestamp, 1, Null) OVER (
                        PARTITION BY nft_address,
                        token_id
                        ORDER BY
                            timestamp
                    ) as LEAD
                FROM
                    transfers
            ) as middle
        where
            LEAD is not Null
        ) as days_beetween
        group by days;
    """
    cur = conn.cursor()
    try:
        cur.execute(drop_transfer_holding_times)
        cur.execute(transfer_holding_times)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Could not create derived dataset: transfer_holding_times")
        logger.error(e)


def ownership_transitions(conn: sqlite3.Connection) -> None:
    """
    Derives a table called ownership_transitions which counts the number of transitions in ownership
    from address A to address B for each pair of addresses (A, B) for which there was at least
    one transfer from A to B.

    Requires the following tables:
    - transfers
    - current_owners
    """
    table_name = "ownership_transitions"
    drop_ownership_transitions = f"DROP TABLE IF EXISTS {table_name};"
    # TODO(zomglings): Adding transaction_value below causes integer overflow. Might be worth trying MEAN instead of SUM for value transferred.
    create_ownership_transitions = f"""
CREATE TABLE {table_name} AS
WITH transitions(from_address, to_address, transition) AS (
    SELECT current_owners.owner as from_address, current_owners.owner as to_address, 1 as transition FROM current_owners
    UNION ALL
    SELECT transfers.from_address as from_address, transfers.to_address as to_address, 1 as transition FROM transfers
)
SELECT
    transitions.from_address,
    transitions.to_address,
    sum(transitions.transition) as num_transitions
FROM transitions GROUP BY transitions.from_address, transitions.to_address;
"""
    cur = conn.cursor()
    try:
        cur.execute(drop_ownership_transitions)
        cur.execute(create_ownership_transitions)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Could not create derived dataset: {table_name}")
        logger.error(e)
