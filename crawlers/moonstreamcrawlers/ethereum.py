from concurrent.futures import Future, ProcessPoolExecutor, wait
from typing import List, Optional

from web3 import Web3
from web3.types import BlockData

from .settings import MOONSTREAM_IPC_PATH, MOONSTREAM_CRAWL_WORKERS
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumBlock, EthereumTransaction


def connect(ipc_path: Optional[str] = MOONSTREAM_IPC_PATH):
    web3_client = Web3(Web3.IPCProvider(ipc_path))
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


def get_latest_blocks(with_transactions: bool = False) -> None:
    web3_client = connect()
    block_latest: BlockData = web3_client.eth.get_block(
        "latest", full_transactions=with_transactions
    )
    with yield_db_session_ctx() as db_session:
        block_number_latest_exist = (
            db_session.query(EthereumBlock.block_number)
            .order_by(EthereumBlock.block_number.desc())
            .first()
        )

    return block_number_latest_exist, block_latest.number


def crawl_blocks(
    blocks_numbers: List[int], with_transactions: bool = False, verbose: bool = False
) -> None:
    """
    Open database and geth sessions and fetch block data from blockchain.
    """
    web3_client = connect()
    for block_number in blocks_numbers:
        with yield_db_session_ctx() as db_session:
            block: BlockData = web3_client.eth.get_block(
                block_number, full_transactions=with_transactions
            )
            add_block(db_session, block)

            if with_transactions:
                add_block_transactions(db_session, block)

            db_session.commit()

            if verbose:
                print(f"Added {block_number} block")


def check_missing_blocks(blocks_numbers: List[int]) -> List[int]:
    """
    Query block from postgres. If block does not presented in database,
    add to missing blocks numbers list.
    """
    missing_blocks_numbers = []
    for block_number in blocks_numbers:
        with yield_db_session_ctx() as db_session:
            block_exist = (
                db_session.query(EthereumBlock.block_number)
                .filter(EthereumBlock.block_number == block_number)
                .one_or_none()
            )
            if block_exist is None:
                missing_blocks_numbers.append(block_number)
    return missing_blocks_numbers


def crawl_blocks_executor(
    block_numbers_list: List[int],
    with_transactions: bool = False,
    verbose: bool = False,
) -> None:
    """
    Execute crawler in processes.
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
    print("Errors:")
    for error in errors:
        print(f"- {error}")
