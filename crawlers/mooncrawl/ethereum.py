from concurrent.futures import Future, ProcessPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime
from os import close
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from sqlalchemy import desc, Column
from sqlalchemy import func
from sqlalchemy.orm import Session, Query
from web3 import Web3, IPCProvider, HTTPProvider
from web3.types import BlockData

from .settings import MOONSTREAM_IPC_PATH, MOONSTREAM_CRAWL_WORKERS
from moonstreamdb.db import yield_db_session, yield_db_session_ctx
from moonstreamdb.models import (
    EthereumBlock,
    EthereumAddress,
    EthereumTransaction,
)


class EthereumBlockCrawlError(Exception):
    """
    Raised when there is a problem crawling Ethereum blocks.
    """


@dataclass
class DateRange:
    start_time: datetime
    end_time: datetime
    include_start: bool
    include_end: bool


def connect(web3_uri: Optional[str] = MOONSTREAM_IPC_PATH):
    web3_provider: Union[IPCProvider, HTTPProvider] = Web3.IPCProvider()
    if web3_uri is not None:
        if web3_uri.startswith("http://") or web3_uri.startswith("https://"):
            web3_provider = Web3.HTTPProvider(web3_uri)
        else:
            web3_provider = Web3.IPCProvider(web3_uri)
    web3_client = Web3(web3_provider)
    return web3_client


def add_block(db_session, block: BlockData) -> None:
    """
    Add block if doesn't presented in database.
    """
    block_obj = EthereumBlock(
        block_number=block.number,
        difficulty=block.difficulty,
        extra_data=block.extraData.hex(),
        gas_limit=block.gasLimit,
        gas_used=block.gasUsed,
        hash=block.hash.hex(),
        logs_bloom=block.logsBloom.hex(),
        miner=block.miner,
        nonce=block.nonce.hex(),
        parent_hash=block.parentHash.hex(),
        receipt_root=block.get("receiptRoot", ""),
        uncles=block.sha3Uncles.hex(),
        size=block.size,
        state_root=block.stateRoot.hex(),
        timestamp=block.timestamp,
        total_difficulty=block.totalDifficulty,
        transactions_root=block.transactionsRoot.hex(),
    )
    db_session.add(block_obj)


def add_block_transactions(db_session, block: BlockData) -> None:
    """
    Add block transactions.
    """
    for tx in block.transactions:
        tx_obj = EthereumTransaction(
            hash=tx.hash.hex(),
            block_number=block.number,
            from_address=tx["from"],
            to_address=tx.to,
            gas=tx.gas,
            gas_price=tx.gasPrice,
            input=tx.input,
            nonce=tx.nonce,
            transaction_index=tx.transactionIndex,
            value=tx.value,
        )
        db_session.add(tx_obj)


def get_latest_blocks(confirmations: int = 0) -> Tuple[Optional[int], int]:
    """
    Retrieve the latest block from the connected node (connection is created by the connect() method).

    If confirmations > 0, and the latest block on the node has block number N, this returns the block
    with block_number (N - confirmations)
    """
    web3_client = connect()
    latest_block_number: int = web3_client.eth.block_number
    if confirmations > 0:
        latest_block_number -= confirmations

    with yield_db_session_ctx() as db_session:
        latest_stored_block_row = (
            db_session.query(EthereumBlock.block_number)
            .order_by(EthereumBlock.block_number.desc())
            .first()
        )
        latest_stored_block_number = (
            None if latest_stored_block_row is None else latest_stored_block_row[0]
        )

    return latest_stored_block_number, latest_block_number


def crawl_blocks(
    blocks_numbers: List[int], with_transactions: bool = False, verbose: bool = False
) -> None:
    """
    Open database and geth sessions and fetch block data from blockchain.
    """
    web3_client = connect()
    with yield_db_session_ctx() as db_session:
        for block_number in blocks_numbers:
            try:
                block: BlockData = web3_client.eth.get_block(
                    block_number, full_transactions=with_transactions
                )
                add_block(db_session, block)

                if with_transactions:
                    add_block_transactions(db_session, block)

                db_session.commit()
            except Exception as err:
                db_session.rollback()
                message = f"Error adding block (number={block_number}) to database:\n{repr(err)}"
                raise EthereumBlockCrawlError(message)
            except:
                db_session.rollback()
                print(
                    f"Interrupted while adding block (number={block_number}) to database."
                )
                raise

            if verbose:
                print(f"Added block: {block_number}")


def check_missing_blocks(blocks_numbers: List[int]) -> List[int]:
    """
    Query block from postgres. If block does not presented in database,
    add to missing blocks numbers list.
    """
    bottom_block = min(blocks_numbers[-1], blocks_numbers[0])
    top_block = max(blocks_numbers[-1], blocks_numbers[0])
    with yield_db_session_ctx() as db_session:
        blocks_exist_raw = (
            db_session.query(EthereumBlock.block_number)
            .filter(EthereumBlock.block_number >= bottom_block)
            .filter(EthereumBlock.block_number <= top_block)
            .all()
        )
    blocks_exist = [block[0] for block in blocks_exist_raw]
    missing_blocks_numbers = [
        block for block in blocks_numbers if block not in blocks_exist
    ]
    return missing_blocks_numbers


def crawl_blocks_executor(
    block_numbers_list: List[int],
    with_transactions: bool = False,
    verbose: bool = False,
    num_processes: int = MOONSTREAM_CRAWL_WORKERS,
) -> None:
    """
    Execute crawler in processes.

    Args:
    block_numbers_list - List of block numbers to add to database.
    with_transactions - If True, also adds transactions from those blocks to the ethereum_transactions table.
    verbose - Print logs to stdout?
    num_processes - Number of processes to use to feed blocks into database.

    Returns nothing, but if there was an error processing the given blocks it raises an EthereumBlocksCrawlError.
    The error message is a list of all the things that went wrong in the crawl.
    """
    errors: List[Exception] = []

    def record_error(f: Future) -> None:
        error = f.exception()
        if error is not None:
            errors.append(error)

    worker_indices = range(MOONSTREAM_CRAWL_WORKERS)
    worker_job_lists = [[] for _ in worker_indices]
    for i, block_number in enumerate(block_numbers_list):
        worker_job_lists[i % MOONSTREAM_CRAWL_WORKERS].append(block_number)

    results: List[Future] = []
    if num_processes == 1:
        return crawl_blocks(block_numbers_list, with_transactions, verbose)
    else:
        with ProcessPoolExecutor(max_workers=MOONSTREAM_CRAWL_WORKERS) as executor:
            for worker in worker_indices:
                if verbose:
                    print(f"Spawned process for {len(worker_job_lists[worker])} blocks")
                result = executor.submit(
                    crawl_blocks,
                    worker_job_lists[worker],
                    with_transactions,
                )
                result.add_done_callback(record_error)
                results.append(result)

        wait(results)
        if len(errors) > 0:
            error_messages = "\n".join([f"- {error}" for error in errors])
            message = f"Error processing blocks in list:\n{error_messages}"
            raise EthereumBlockCrawlError(message)


def process_contract_deployments() -> List[Tuple[str, str]]:
    """
    Checks for new smart contracts that have been deployed to the blockchain but not registered in
    the smart contract registry.

    If it finds any such smart contracts, it retrieves their addresses from the transaction receipts
    and registers them in the smart contract registry.

    Returns a list of pairs of the form [..., ("<transaction_hash>", "<contract_address>"), ...].
    """
    web3_client = connect()
    results: List[Tuple[str, str]] = []
    with yield_db_session_ctx() as db_session:
        current_offset = 0
        limit = 10
        transactions_remaining = True
        existing_contract_transaction_hashes = db_session.query(
            EthereumAddress.transaction_hash
        )

        while transactions_remaining:
            contract_deployments = (
                db_session.query(EthereumTransaction)
                .order_by(desc(EthereumTransaction.block_number))
                .filter(
                    EthereumTransaction.hash.notin_(
                        existing_contract_transaction_hashes
                    )
                )
                .filter(EthereumTransaction.to_address == None)
                .limit(limit)
                .offset(current_offset)
                .all()
            )
            if contract_deployments:
                for deployment in contract_deployments:
                    receipt = web3_client.eth.get_transaction_receipt(deployment.hash)
                    contract_address = receipt.get("contractAddress")
                    if contract_address is not None:
                        results.append((deployment.hash, contract_address))
                        db_session.add(
                            EthereumAddress(
                                transaction_hash=deployment.hash,
                                address=contract_address,
                            )
                        )
                db_session.commit()
            else:
                transactions_remaining = False

            current_offset += limit

    return results


def trending(
    date_range: DateRange, db_session: Optional[Session] = None
) -> Dict[str, Any]:
    close_db_session = False
    if db_session is None:
        close_db_session = True
        db_session = next(yield_db_session())

    start_timestamp = int(date_range.start_time.timestamp())
    end_timestamp = int(date_range.end_time.timestamp())

    def make_query(
        transaction_column: Column,
        aggregate_column: Column,
        aggregate_func: Callable,
        aggregate_label: str,
    ) -> Query:
        query = db_session.query(
            transaction_column, aggregate_func(aggregate_column).label(aggregate_label)
        ).join(
            EthereumBlock,
            EthereumTransaction.block_number == EthereumBlock.block_number,
        )
        if date_range.include_start:
            query = query.filter(EthereumBlock.timestamp >= start_timestamp)
        else:
            query = query.filter(EthereumBlock.timestamp > start_timestamp)

        if date_range.include_end:
            query = query.filter(EthereumBlock.timestamp <= end_timestamp)
        else:
            query = query.filter(EthereumBlock.timestamp < end_timestamp)

        query = (
            query.group_by(transaction_column).order_by(desc(aggregate_label)).limit(10)
        )

        return query

    results: Dict[str, Any] = {}

    try:
        transactions_out_query = make_query(
            EthereumTransaction.from_address,
            EthereumTransaction.hash,
            func.count,
            "transactions_out",
        )
        transactions_out = transactions_out_query.all()
        results["transactions_out"] = [
            {"address": row[0], "statistic": row[1]} for row in transactions_out
        ]

        transactions_in_query = make_query(
            EthereumTransaction.to_address,
            EthereumTransaction.hash,
            func.count,
            "transactions_in",
        )
        transactions_in = transactions_in_query.all()
        results["transactions_in"] = [
            {"address": row[0], "statistic": row[1]} for row in transactions_in
        ]

        value_out_query = make_query(
            EthereumTransaction.from_address,
            EthereumTransaction.value,
            func.sum,
            "value_out",
        )
        value_out = value_out_query.all()
        results["value_out"] = [
            {"address": row[0], "statistic": int(row[1])} for row in value_out
        ]

        value_in_query = make_query(
            EthereumTransaction.to_address,
            EthereumTransaction.value,
            func.sum,
            "value_in",
        )
        value_in = value_in_query.all()
        results["value_in"] = [
            {"address": row[0], "statistic": int(row[1])} for row in value_in
        ]

        pass
    finally:
        if close_db_session:
            db_session.close()

    return results
