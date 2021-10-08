"""
Functions to access various data in the NFTs dataset.
"""
import sqlite3
from typing import Dict

import pandas as pd

from .datastore import event_tables, EventType

# TODO(zomglings): Make it so that table names are parametrized by importable variables. The way
# things are now, we have to be very careful if we ever rename a table in our dataset. We should
# also propagate the name change here.
NFTS = "nfts"
MINTS = event_tables[EventType.MINT]
TRANSFERS = event_tables[EventType.TRANSFER]
CURRENT_OWNERS = "current_owners"
CURRENT_MARKET_VALUES = "current_market_values"
TRANSFER_STATISTICS_BY_ADDRESS = "transfer_statistics_by_address"
MINT_HOLDING_TIMES = "mint_holding_times"
TRANSFER_HOLDING_TIMES = "transfer_holding_times"

AVAILABLE_DATAFRAMES = {
    NFTS: """Describes the NFT contracts represented in this dataset, with a name and symbol if they were available at time of crawl.

Columns:
1. address: The Ethereum address of the NFT contract.
2. name: The name of the collection of NFTs that the contract represents.
3. symbol: The symbol of the collection of NFTs that the contract represents.
""",
    MINTS: """All token mint events crawled in this dataset.

Columns:
1. event_id: A unique event ID associated with the event.
2. transaction_hash: The hash of the transaction which triggered the event.
3. block_number: The transaction block in which the transaction was mined.
4. nft_address: The address of the NFT collection containing the minted token.
5. token_id: The ID of the token that was minted.
6. from_address: The "from" address for the transfer event. For a mint, this should be the 0 address: 0x0000000000000000000000000000000000000000.
7. to_address: The "to" address for the transfer event. This represents the owner of the freshly minted token.
8. transaction_value: The amount of WEI that were sent with the transaction in which the token was minted.
9. timestamp: The time at which the mint operation was mined into the blockchain (this is the timestamp for the mined block).
""",
    TRANSFERS: """All token transfer events crawled in this dataset.

Columns:
1. event_id: A unique event ID associated with the event.
2. transaction_hash: The hash of the transaction which triggered the event.
3. block_number: The transaction block in which the transaction was mined.
4. nft_address: The address of the NFT collection containing the transferred token.
5. token_id: The ID of the token that was transferred.
6. from_address: The "from" address for the transfer event. This is the address that owned the token at the *start* of the transfer.
7. to_address: The "to" address for the transfer event. This is the address that owned the token at the *end* of the transfer.
8. transaction_value: The amount of WEI that were sent with the transaction in which the token was transferred.
9. timestamp: The time at which the transfer operation was mined into the blockchain (this is the timestamp for the mined block).
""",
    CURRENT_OWNERS: f"""This table is derived from the {NFTS}, {MINTS}, and {TRANSFERS} tables. It represents the current owner of each token in the dataset.

Columns:
1. nft_address: The address of the NFT collection containing the token whose ownership we are denoting.
2. token_id: The ID of the token (inside the collection) whose ownership we are denoting.
3. owner: The address that owned the token at the time of construction of this dataset.
""",
    CURRENT_MARKET_VALUES: f"""This table is derived from the {NFTS}, {MINTS}, and {TRANSFERS} tables. It represents the current market value (in WEI) of each token in the dataset.

Columns:
1. nft_address: The address of the NFT collection containing the token whose market value we are denoting.
2. token_id: The ID of the token (inside the collection) whose market value we are denoting.
3. market_value: The estimated market value of the token at the time of construction of this dataset.

For this dataset, we estimate the market value as the last non-zero transaction value for a transfer involving this token.
This estimate may be inaccurate for some transfers (e.g. multiple token transfers made by an escrow contract in a single transaction)
but ought to be reasonably accurate for a large majority of tokens.
""",
    TRANSFER_STATISTICS_BY_ADDRESS: f"""This table is derived from the {NFTS}, {MINTS}, and {TRANSFERS} tables. For each address that participated in
at least one NFT transfer between April 1, 2021 and September 25, 2021, this table shows exactly how many NFTs that address transferred to
other addresses and how many NFT transfers that address was the recipient of.

Columns:
1. address: An Ethereum address that participated in at least one NFT transfer between April 1, 2021 and September 25, 2021.
2. transfers_out: The number of NFTs that the given address transferred to any other address between April 1, 2021 and September 25, 2021.
3. transfers_in: The number of NFTs that any other address transferred to given address between April 1, 2021 and September 25, 2021.
""",
}


def explain() -> None:
    """
    Explains the structure of the dataset.
    """
    preamble = """
The Moonstream NFTs dataset
===========================

To load the NFTs dataset from a SQLite file, run:
>>> ds = nfts.dataset.FromSQLite(<path to sqlite database>)

This dataset consists of the following dataframes:"""

    print(preamble)
    for name, explanation in AVAILABLE_DATAFRAMES.items():
        print(f"\nDataframe: {name}")
        print(
            f'Load using:\n\t{name}_df = ds.load_dataframe(<sqlite connection or path to sqlite db>, "{name}")'
        )
        print("")
        print(explanation)
        print("- - -")


class FromSQLite:
    def __init__(self, datafile: str) -> None:
        """
        Initialize an NFTs dataset instance by connecting it to a SQLite database containing the data.
        """
        self.conn = sqlite3.connect(datafile)

    def load_dataframe(self, name: str) -> pd.DataFrame:
        """
        Loads one of the available dataframes. To learn more about the available dataframes, run:
        >>> nfts.dataset.explain()
        """
        if name not in AVAILABLE_DATAFRAMES:
            raise ValueError(
                f"Invalid dataframe: {name}. Please choose from one of the available dataframes: {','.join(AVAILABLE_DATAFRAMES)}."
            )
        df = pd.read_sql_query(f"SELECT * FROM {name};", self.conn)
        return df

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """
        Load all the datasets and return them in a dictionary with the keys being the dataframe names.
        """
        dfs = {f"{name}_df": self.load_dataframe(name) for name in AVAILABLE_DATAFRAMES}
        return dfs
