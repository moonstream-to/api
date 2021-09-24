from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from psycopg2.errors import UniqueViolation  # type: ignore
from sqlalchemy import desc, Column
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query
from tqdm import tqdm
from web3 import Web3, IPCProvider, HTTPProvider
from web3.types import BlockData

from .settings import MOONSTREAM_IPC_PATH, MOONSTREAM_CRAWL_WORKERS
from moonstreamdb.db import yield_db_session, yield_db_session_ctx
from moonstreamdb.models import (
    EthereumBlock,
    EthereumAddress,
    EthereumTransaction,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


def add_block(db_session, block: Any) -> None:
    """
    Add block if doesn't presented in database.

    block: web3.types.BlockData
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


def add_block_transactions(db_session, block: Any) -> None:
    """
    Add block transactions.

    block: web3.types.BlockData
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


def crawl_blocks(blocks_numbers: List[int], with_transactions: bool = False) -> None:
    """
    Open database and geth sessions and fetch block data from blockchain.
    """
    web3_client = connect()
    with yield_db_session_ctx() as db_session:
        pbar = tqdm(total=len(blocks_numbers))
        for block_number in blocks_numbers:
            pbar.set_description(
                f"Crawling block {block_number} with txs: {with_transactions}"
            )
            try:
                block: BlockData = web3_client.eth.get_block(
                    block_number, full_transactions=with_transactions
                )
                add_block(db_session, block)

                if with_transactions:
                    add_block_transactions(db_session, block)

                db_session.commit()
            except IntegrityError as err:
                assert isinstance(err.orig, UniqueViolation)
                logger.warning(
                    "UniqueViolation error occurred, it means block already exists"
                )
            except Exception as err:
                db_session.rollback()
                message = f"Error adding block (number={block_number}) to database:\n{repr(err)}"
                raise EthereumBlockCrawlError(message)
            except:
                db_session.rollback()
                logger.error(
                    f"Interrupted while adding block (number={block_number}) to database."
                )
                raise
            pbar.update()
        pbar.close()


def check_missing_blocks(blocks_numbers: List[int], notransactions=False) -> List[int]:
    """
    Query block from postgres. If block does not presented in database,
    add to missing blocks numbers list.
    If arg notransactions=False, it checks correct number of transactions in
    database according to blockchain.
    """
    bottom_block = min(blocks_numbers[-1], blocks_numbers[0])
    top_block = max(blocks_numbers[-1], blocks_numbers[0])

    with yield_db_session_ctx() as db_session:
        if notransactions:
            blocks_exist_raw_query = (
                db_session.query(EthereumBlock.block_number)
                .filter(EthereumBlock.block_number >= bottom_block)
                .filter(EthereumBlock.block_number <= top_block)
            )
            blocks_exist = [[block[0]] for block in blocks_exist_raw_query.all()]
        else:
            corrupted_blocks = []
            blocks_exist_raw_query = (
                db_session.query(
                    EthereumBlock.block_number, func.count(EthereumTransaction.hash)
                )
                .join(
                    EthereumTransaction,
                    EthereumTransaction.block_number == EthereumBlock.block_number,
                )
                .filter(EthereumBlock.block_number >= bottom_block)
                .filter(EthereumBlock.block_number <= top_block)
                .group_by(EthereumBlock.block_number)
            )
            blocks_exist = [
                [block[0], block[1]] for block in blocks_exist_raw_query.all()
            ]

            web3_client = connect()

            blocks_exist_len = len(blocks_exist)
            pbar = tqdm(total=blocks_exist_len)
            pbar.set_description(f"Checking txs in {blocks_exist_len} blocks")

            for i, block_in_db in enumerate(blocks_exist):
                block = web3_client.eth.get_block(
                    block_in_db[0], full_transactions=True
                )
                if len(block.transactions) != block_in_db[1]:
                    corrupted_blocks.append(block_in_db[0])
                    # Delete existing corrupted block and add to missing list
                    del_block = (
                        db_session.query(EthereumBlock)
                        .filter(EthereumBlock.block_number == block_in_db[0])
                        .one()
                    )
                    db_session.delete(del_block)
                    del blocks_exist[i]
                pbar.update()
            pbar.close()

            db_session.commit()

            corrupted_blocks_len = len(corrupted_blocks)
            if corrupted_blocks_len > 0:
                logger.warning(
                    f"Removed {corrupted_blocks_len} corrupted blocks: {corrupted_blocks if corrupted_blocks_len <= 10 else '...'}"
                )

    missing_blocks_numbers = [
        block for block in blocks_numbers if block not in [i[0] for i in blocks_exist]
    ]
    return missing_blocks_numbers


def crawl_blocks_executor(
    block_numbers_list: List[int],
    with_transactions: bool = False,
    num_processes: int = MOONSTREAM_CRAWL_WORKERS,
) -> None:
    """
    Execute crawler in processes.

    Args:
    block_numbers_list - List of block numbers to add to database.
    with_transactions - If True, also adds transactions from those blocks to the ethereum_transactions table.
    num_processes - Number of processes to use to feed blocks into database.

    Returns nothing, but if there was an error processing the given blocks it raises an EthereumBlocksCrawlError.
    The error message is a list of all the things that went wrong in the crawl.
    """
    errors: List[BaseException] = []

    def record_error(f: Future) -> None:
        error = f.exception()
        if error is not None:
            errors.append(error)

    worker_indices = range(MOONSTREAM_CRAWL_WORKERS)
    worker_job_lists: List[List[Any]] = [[] for _ in worker_indices]
    for i, block_number in enumerate(block_numbers_list):
        worker_job_lists[i % MOONSTREAM_CRAWL_WORKERS].append(block_number)

    results: List[Future] = []
    if num_processes == 1:
        logger.warning("Executing block crawler in lazy mod")
        return crawl_blocks(block_numbers_list, with_transactions)
    else:
        with ThreadPoolExecutor(max_workers=MOONSTREAM_CRAWL_WORKERS) as executor:
            for worker in worker_indices:
                block_chunk = worker_job_lists[worker]
                logger.info(f"Spawned process for {len(block_chunk)} blocks")
                result = executor.submit(crawl_blocks, block_chunk, with_transactions)
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
        db_session: Session,
        identifying_column: Column,
        statistic_column: Column,
        aggregate_func: Callable,
        aggregate_label: str,
    ) -> Query:
        query = db_session.query(
            identifying_column, aggregate_func(statistic_column).label(aggregate_label)
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
            query.group_by(identifying_column).order_by(desc(aggregate_label)).limit(10)
        )

        return query

    results: Dict[str, Any] = {
        "date_range": {
            "start_time": date_range.start_time.isoformat(),
            "end_time": date_range.end_time.isoformat(),
            "include_start": date_range.include_start,
            "include_end": date_range.include_end,
        }
    }

    try:
        transactions_out_query = make_query(
            db_session,
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
            db_session,
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
            db_session,
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
            db_session,
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
