"""
Functions to access various data in the NFTs dataset.
"""
import sqlite3
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import scipy.sparse
from tqdm import tqdm

from .datastore import event_tables, EventType

# TODO(yhtiyar): Add this table to the dataset
CONTRACTS = "contracts"

TRANSFERS = "transfers"


# CURRENT_OWNERS = "current_owners"
# CURRENT_MARKET_VALUES = "current_market_values"
# TRANSFER_STATISTICS_BY_ADDRESS = "transfer_statistics_by_address"
# MINT_HOLDING_TIMES = "mint_holding_times"
# TRANSFER_HOLDING_TIMES = "transfer_holding_times"
# OWNERSHIP_TRANSITIONS = "ownership_transitions"

AVAILABLE_DATAFRAMES = {
    CONTRACTS: """Describes the NFT and ERC20 contracts represented in this dataset, with a type, name, symbol, decimals (for erc20) if they were available at time of crawl.

Columns:
1. address: The Ethereum address of the NFT contract.
2. name: The name of the collection of NFTs that the contract represents.
3. symbol: The symbol of the collection of NFTs that the contract represents.
""",
    # TODO (yhtiyar): update description for the contracts
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
    CURRENT_OWNERS: f"""This table is derived from the {CONTRACTS}, {MINTS}, and {TRANSFERS} tables. It represents the current owner of each token in the dataset.

Columns:
1. nft_address: The address of the NFT collection containing the token whose ownership we are denoting.
2. token_id: The ID of the token (inside the collection) whose ownership we are denoting.
3. owner: The address that owned the token at the time of construction of this dataset.
""",
    CURRENT_MARKET_VALUES: f"""This table is derived from the {CONTRACTS}, {MINTS}, and {TRANSFERS} tables. It represents the current market value (in WEI) of each token in the dataset.

Columns:
1. nft_address: The address of the NFT collection containing the token whose market value we are denoting.
2. token_id: The ID of the token (inside the collection) whose market value we are denoting.
3. market_value: The estimated market value of the token at the time of construction of this dataset.

For this dataset, we estimate the market value as the last non-zero transaction value for a transfer involving this token.
This estimate may be inaccurate for some transfers (e.g. multiple token transfers made by an escrow contract in a single transaction)
but ought to be reasonably accurate for a large majority of tokens.
""",
    TRANSFER_STATISTICS_BY_ADDRESS: f"""This table is derived from the {CONTRACTS}, {MINTS}, and {TRANSFERS} tables. For each address that participated in
at least one NFT transfer between April 1, 2021 and September 25, 2021, this table shows exactly how many NFTs that address transferred to
other addresses and how many NFT transfers that address was the recipient of.

Columns:
1. address: An Ethereum address that participated in at least one NFT transfer between April 1, 2021 and September 25, 2021.
2. transfers_out: The number of NFTs that the given address transferred to any other address between April 1, 2021 and September 25, 2021.
3. transfers_in: The number of NFTs that any other address transferred to given address between April 1, 2021 and September 25, 2021.
""",
}


AVAILABLE_MATRICES = {
    OWNERSHIP_TRANSITIONS: f"""{OWNERSHIP_TRANSITIONS} is an adjacency matrix which counts the number of times that a token was transferred from a source address (indexed by the rows of the matrix) to a target address (indexed by the columns of the matrix).

These counts only include data about mints and transfers made between April 1, 2021 and September 25, 2021. We also denote the current owners of an NFT as having transitioned
the NFT from themselves back to themselves. This gives some estimate of an owner retaining the NFT in the given time period.

Load this matrix as follows:
>>> indexed_addresses, transitions = ds.load_ownership_transitions()

- "indexed_addresses" is a list denoting the address that each index (row/column) in the matrix represents.
- "transitions" is a numpy ndarray containing the matrix, with source addresses on the row axis and target addresses on the column axis.
"""
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
            f'Load using:\n>>> {name}_df = ds.load_dataframe(<sqlite connection or path to sqlite db>, "{name}")'
        )
        print("")
        print(explanation)
        print("- - -")

    for name, explanation in AVAILABLE_MATRICES.items():
        print(f"\nMatrix: {name}")
        print("")
        print(explanation)
        print("- - -")


class FromSQLite:
    def __init__(self, datafile: str) -> None:
        """
        Initialize an NFTs dataset instance by connecting it to a SQLite database containing the data.
        """
        self.conn = sqlite3.connect(datafile)
        self.ownership_transitions: Optional[
            Tuple[List[str], scipy.sparse.spmatrix]
        ] = None
        self.ownership_transition_probabilities: Optional[
            Tuple[List[str], scipy.sparse.spmatrix]
        ] = None

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

    def load_ownership_transitions(
        self, force: bool = False
    ) -> Tuple[List[str], scipy.sparse.spmatrix]:
        """
        Loads ownership transitions adjacency matrix from SQLite database.

        To learn more about this matrix, run:
        >>> nfts.dataset.explain()
        """
        if self.ownership_transitions is not None and not force:
            return self.ownership_transitions
        cur = self.conn.cursor()
        address_indexes_query = """
WITH all_addresses AS (
    SELECT from_address AS address FROM ownership_transitions
    UNION
    SELECT to_address AS address FROM ownership_transitions
)
SELECT DISTINCT(all_addresses.address) AS address FROM all_addresses ORDER BY address ASC;
"""
        addresses = [row[0] for row in cur.execute(address_indexes_query)]
        num_addresses = len(addresses)
        address_indexes = {address: i for i, address in enumerate(addresses)}

        adjacency_matrix = scipy.sparse.dok_matrix((num_addresses, num_addresses))
        adjacency_query = "SELECT from_address, to_address, num_transitions FROM ownership_transitions;"

        rows = cur.execute(adjacency_query)
        for from_address, to_address, num_transitions in tqdm(
            rows, desc="Ownership transitions (adjacency matrix)"
        ):
            from_index = address_indexes[from_address]
            to_index = address_indexes[to_address]
            adjacency_matrix[from_index, to_index] = num_transitions

        self.ownership_transitions = (addresses, adjacency_matrix)
        return self.ownership_transitions

    def load_ownership_transition_probabilities(
        self,
        force: bool = False,
    ) -> Tuple[List[str], scipy.sparse.spmatrix]:
        """
        Returns transition probabilities of ownership transitions, with each entry A_{i,j} denoting the
        probability that the address represented by row i transferred and NFT to the address represented by row[j].
        """
        if self.ownership_transition_probabilities is not None and not force:
            return self.ownership_transition_probabilities

        addresses, adjacency_matrix = self.load_ownership_transitions(force)

        # Sum of the entries in each row:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.spmatrix.sum.html#scipy.sparse.spmatrix.sum
        row_sums = adjacency_matrix.sum(axis=1)

        # Convert adjacency matrix to matrix of transition probabilities.
        # We cannot do this by simply dividing transition_probabilites /= row_sums because that tries
        # to coerce the matrix into a dense numpy ndarray and requires terabytes of memory.
        transition_probabilities = adjacency_matrix.copy()
        for i, j in zip(*transition_probabilities.nonzero()):
            transition_probabilities[i, j] = (
                transition_probabilities[i, j] / row_sums[i]
            )

        # Now we identify and remove burn addresses from this data.

        self.ownership_transition_probabilities = (addresses, transition_probabilities)
        return self.ownership_transition_probabilities
