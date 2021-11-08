import logging
import sqlite3

from dataclasses import dataclass
from typing import List
from .data import ContractDeployment


CREATE_CONTRACT_DEPLOYMENTS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS contract_deployments (
    id INTEGER PRIMARY KEY,
    transaction_hash TEXT NOT NULL,
    block_number INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    contract_address TEXT NOT NULL,
    deployer_address TEXT NOT NULL,
    gas_used INTEGER NOT NULL,
    gas_price INTEGER NOT NULL,
    transaction_fee INTEGER NOT NULL,
    )
"""

CREATE_CHECKPOINT_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS checkpoint
    (
        label STRING,
        offset INTEGER
    );
"""


def setup_database(conn: sqlite3.Connection):
    """
    Create the database tables if they don't exist.
    """
    cur = conn.cursor()
    cur.execute(CREATE_CONTRACT_DEPLOYMENTS_TABLE_QUERY)
    cur.execute(CREATE_CHECKPOINT_TABLE_QUERY)
    conn.commit()


def insert_contract_deployments(
    conn: sqlite3.Connection, contract_deployments: List[ContractDeployment]
):
    """
    Insert a list of contract deployments into the database.
    """
    cur = conn.cursor()
    for contract_deployment in contract_deployments:
        cur.execute(
            "INSERT INTO contract_deployments (transaction_hash, block_number, timestamp, contract_address, deployer_address, gas_used, gas_price, transaction_fee) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                contract_deployment.transaction_hash,
                contract_deployment.block_number,
                contract_deployment.block_timestamp,
                contract_deployment.address,
                contract_deployment.deployer_address,
                contract_deployment.gas_used,
                contract_deployment.gas_price,
                contract_deployment.transaction_fee,
            ),
        )
    conn.commit()


def load_checkpoint(conn: sqlite3.Connection, label: str) -> int:
    """
    Load the checkpoint with the given label.
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT offset FROM checkpoint WHERE label = ?",
        (label,),
    )
    row = cur.fetchone()
    if row is None:
        return 0
    else:
        return row[0]


def save_checkpoint(conn: sqlite3.Connection, label: str, offset: int):
    """
    Save the checkpoint with the given label.
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO checkpoint (label, offset) VALUES (?, ?)",
        (label, offset),
    )
    conn.commit()
