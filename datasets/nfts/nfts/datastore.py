"""
This module provides tools to interact with and maintain a SQLite database which acts/should act as
a datastore for a Moonstream NFTs dataset.
"""
from ctypes import Union
import json
import logging
import sqlite3
from typing import Any, cast, List, Tuple, Optional

from tqdm import tqdm
from .data import (
    NftTransaction,
    NftApprovalEvent,
    NftTransferEvent,
    NftApprovalForAllEvent,
    Erc20TransferEvent,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_transactions_table_query(tabel_name) -> str:
    creation_query = f"""
CREATE TABLE IF NOT EXISTS {tabel_name}
    (   
        blockchainType TEXT NOT NULL,
        transactionHash TEXT NOT NULL,
        blockNumber INTEGER NOT NULL,
        blockTimestamp INTEGER NOT NULL,
        contractAddress TEXT,
        from_address TEXT NOT NULL,
        functionName TEXT NOT NULL,
        functionArgs JSON NOT NULL,
        value INTEGER NOT NULL,
        gasUsed INTEGER NOT NULL,
        gasPrice INTEGER NOT NULL,
        maxFeePerGas INTEGER,
        maxPriorityFeePerGas INTEGER,
        UNIQUE(blockchainType, transactionHash)        
    );
    """
    return creation_query


def create_approvals_table_query(tabel_name) -> str:
    creation_query = f"""
CREATE TABLE IF NOT EXISTS {tabel_name}
    (   
       blockchainType TEXT NOT NULL,
       tokenAddress TEXT NOT NULL,
       owner TEXT NOT NULL,
       approved TEXT NOT NULL,
       tokenId TEXT NOT NULL,
       transactionHash TEXT NOT NULL,
       logIndex INTEGER NOT NULL,
       UNIQUE(blockchainType, transactionHash, logIndex)
    );
    """
    return creation_query


def create_approval_for_all_table_query(tabel_name) -> str:
    creation_query = f"""
CREATE TABLE IF NOT EXISTS {tabel_name}
    (   
        blockchainType TEXT NOT NULL,
        tokenAddress TEXT NOT NULL,
        owner TEXT NOT NULL,
        approved BOOL NOT NULL,
        operator TEXT NOT NULL,
        transactionHash TEXT NOT NULL,
        logIndex INTEGER NOT NULL,
        UNIQUE(blockchainType, transactionHash, logIndex)
    );
    """
    return creation_query


def create_transfers_table_query(tabel_name) -> str:
    creation_query = f"""
CREATE TABLE IF NOT EXISTS {tabel_name}
    (   
        blockchainType TEXT NOT NULL,
        tokenAddress TEXT NOT NULL,
        from_address TEXT NOT NULL,
        to_address TEXT NOT NULL,
        tokenId TEXT NOT NULL,
        transactionHash TEXT NOT NULL,
        logIndex INTEGER NOT NULL,
        UNIQUE(blockchainType, transactionHash, logIndex)
    );
    """
    return creation_query


def create_erc20_transfers_table_query(tabel_name) -> str:
    creation_query = f"""
CREATE TABLE IF NOT EXISTS {tabel_name}
    (   
        blockchainType TEXT NOT NULL,
        tokenAddress TEXT NOT NULL,
        from_address TEXT NOT NULL,
        to_address TEXT NOT NULL,
        value INTEGER NOT NULL,
        transactionHash TEXT NOT NULL,
        logIndex INTEGER NOT NULL,
        UNIQUE(blockchainType, transactionHash, logIndex)
    );
    """
    return creation_query


def insertTransactionQuery(tabel_name):
    query = f"""
INSERT INTO {tabel_name}
    (
        blockchainType,
        transactionHash,
        blockNumber,
        blockTimestamp,
        contractAddress,
        from_address,
        functionName,
        functionArgs,
        value,
        gasUsed,
        gasPrice,
        maxFeePerGas,
        maxPriorityFeePerGas
    )
VALUES
    (
       ?,?,?,?,?,?,?,?,?,?,?,?,?
    );
    """
    return query


def insert_nft_approval_query(tabel_name):
    query = f"""
INSERT INTO {tabel_name}
    (
        blockchainType,
        tokenAddress,
        owner,
        approved,
        tokenId,
        transactionHash,
        logIndex
    )
VALUES
    (
         ?,?,?,?,?,?,?
    );
    """
    return query


def insert_nft_approval_for_all_query(tabel_name):
    query = f"""
INSERT INTO {tabel_name}
    (
        blockchainType,
        tokenAddress,
        owner,
        approved,
        operator,
        transactionHash,
        logIndex
    )  
VALUES
    (
        ?,?,?,?,?,?, ?
    );
    """
    return query


def insert_nft_transfers_query(tabel_name):
    query = f"""
INSERT INTO {tabel_name}
    (
        blockchainType,
        tokenAddress,
        from_address,
        to_address,
        tokenId,
        transactionHash,
        logIndex
    )
VALUES

    (
        ?,?,?,?,?,?,?
    );
    """
    return query


def insert_erc20_transfer_query(tabel_name):
    query = f"""
INSERT INTO {tabel_name}
    (
        blockchainType,
        tokenAddress,
        from_address,
        to_address,
        value,
        transactionHash,
        logIndex
    )
VALUES
    (
        ?,?,?,?,?,?,?
    );
    """
    return query


def create_blockchain_type_index_query(tabel_name) -> str:
    creation_query = f"""
CREATE INDEX IF NOT EXISTS {tabel_name}_blockchainType ON {tabel_name} (blockchainType);
    """
    return creation_query


def nft_transaction_to_tuple(nft_transaction: NftTransaction) -> Tuple[Any]:
    """
    Converts a NftTransaction object to a tuple which can be inserted into the database.
    """
    return (
        nft_transaction.blockchain_type,
        nft_transaction.transaction_hash,
        nft_transaction.block_number,
        nft_transaction.block_timestamp,
        nft_transaction.contract_address,
        nft_transaction.caller_address,
        nft_transaction.function_name,
        json.dumps(nft_transaction.function_args),
        str(nft_transaction.value),
        str(nft_transaction.gas_used),
        str(nft_transaction.gas_price),
        str(nft_transaction.max_fee_per_gas),
        str(nft_transaction.max_priority_fee_per_gas),
    )


def nft_approval_to_tuple(nft_approval: NftApprovalEvent) -> Tuple[Any]:
    """
    Converts a NftApprovalEvent object to a tuple which can be inserted into the database.
    """
    return (
        nft_approval.blockchain_type,
        nft_approval.token_address,
        nft_approval.owner,
        nft_approval.approved,
        str(nft_approval.token_id),
        nft_approval.transaction_hash,
        nft_approval.log_index,
    )


def nft_approval_for_all_to_tuple(
    nft_approval_for_all: NftApprovalForAllEvent,
) -> Tuple[Any]:
    """
    Converts a NftApprovalForAllEvent object to a tuple which can be inserted into the database.
    """
    return (
        nft_approval_for_all.blockchain_type,
        nft_approval_for_all.token_address,
        nft_approval_for_all.owner,
        nft_approval_for_all.approved,
        nft_approval_for_all.operator,
        nft_approval_for_all.transaction_hash,
        nft_approval_for_all.log_index,
    )


def nft_transfer_to_tuple(nft_transfer: NftTransferEvent) -> Tuple[Any]:
    """
    Converts a NftTransferEvent object to a tuple which can be inserted into the database.
    """
    return (
        nft_transfer.blockchain_type,
        nft_transfer.token_address,
        nft_transfer.from_address,
        nft_transfer.to_address,
        str(nft_transfer.token_id),
        nft_transfer.transaction_hash,
        nft_transfer.log_index,
    )


def erc20_nft_transfer_to_tuple(
    erc20_nft_transfer: Erc20TransferEvent,
) -> Tuple[Any]:
    """
    Converts a Erc20NftTransferEvent object to a tuple which can be inserted into the database.
    """
    return (
        erc20_nft_transfer.blockchain_type,
        erc20_nft_transfer.token_address,
        erc20_nft_transfer.from_address,
        erc20_nft_transfer.to_address,
        str(erc20_nft_transfer.value),
        erc20_nft_transfer.transaction_hash,
        erc20_nft_transfer.log_index,
    )


def insert_transactions(
    conn: sqlite3.Connection, transactions: List[NftTransaction]
) -> None:
    """
    Inserts the given NftTransaction objects into the database.
    """
    cur = conn.cursor()

    query = insertTransactionQuery("transactions")

    cur.executemany(
        query,
        [nft_transaction_to_tuple(nft_transaction) for nft_transaction in transactions],
    )

    conn.commit()


def insert_events(
    conn: sqlite3.Connection,
    events: list,
) -> None:
    """
    Inserts the given NftApprovalForAllEvent, NftApprovalEvent, or NftTransferEvent objects into the database.
    """
    cur = conn.cursor()

    nft_transfers = []
    erc20_transfers = []
    approvals = []
    approvals_for_all = []

    for event in events:
        if isinstance(event, NftApprovalEvent):
            approvals.append(nft_approval_to_tuple(event))
        elif isinstance(event, NftApprovalForAllEvent):
            approvals_for_all.append(nft_approval_for_all_to_tuple(event))
        elif isinstance(event, NftTransferEvent):
            nft_transfers.append(nft_transfer_to_tuple(event))
        elif isinstance(event, Erc20TransferEvent):
            erc20_transfers.append(erc20_nft_transfer_to_tuple(event))
        else:
            raise ValueError(f"Unknown event type: {type(event)}")

    if len(nft_transfers) > 0:
        query = insert_nft_transfers_query("transfers")
        cur.executemany(
            query,
            nft_transfers,
        )

    if len(approvals) > 0:
        query = insert_nft_approval_query("approvals")
        cur.executemany(
            query,
            approvals,
        )

    if len(approvals_for_all) > 0:
        query = insert_nft_approval_for_all_query("approvals_for_all")
        cur.executemany(query, approvals_for_all)

    if len(erc20_transfers) > 0:
        query = insert_erc20_transfer_query("erc20_transfers")
        cur.executemany(query, erc20_transfers)

    conn.commit()


def get_last_saved_block(
    conn: sqlite3.Connection, blockchain_type: str
) -> Optional[int]:
    """
    Returns the last block number that was saved to the database.
    """
    cur = conn.cursor()

    query = f"SELECT MAX(blockNumber) FROM transactions WHERE blockchainType = '{blockchain_type}'"

    cur.execute(query)
    result = cur.fetchone()

    return result[0]


def setup_database(conn: sqlite3.Connection) -> None:
    """
    Sets up the schema of the Moonstream NFTs dataset in the given SQLite database.
    """
    cur = conn.cursor()

    cur.execute(create_transactions_table_query("transactions"))
    cur.execute(create_approvals_table_query("approvals"))
    cur.execute(create_approval_for_all_table_query("approvals_for_all"))
    cur.execute(create_transfers_table_query("transfers"))
    cur.execute(create_erc20_transfers_table_query("erc20_transfers"))

    cur.execute(create_blockchain_type_index_query("transactions"))
    cur.execute(create_blockchain_type_index_query("approvals"))
    cur.execute(create_blockchain_type_index_query("approvals_for_all"))
    cur.execute(create_blockchain_type_index_query("transfers"))
    cur.execute(create_blockchain_type_index_query("erc20_transfers"))

    conn.commit()
