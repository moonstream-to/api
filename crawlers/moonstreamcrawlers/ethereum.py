from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional

from web3 import Web3
from web3.types import BlockData

from .settings import MOONSTREAM_IPC_PATH, MOONSTREAM_CRAWL_WORKERS
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumBlock, EthereumTransaction


def connect(ipc_path: Optional[str] = MOONSTREAM_IPC_PATH):
    web3_client = Web3(Web3.IPCProvider(ipc_path))
    return web3_client


def add_block(db_session, block: BlockData, block_number: int) -> None:
    """
    Add block if doesn't presented in database.
    """
    block_exist = (
        db_session.query(EthereumBlock)
        .filter(EthereumBlock.block_number == block_number)
        .one_or_none()
    )
    if block_exist is not None and block_exist.hash == block.hash.hex():
        print(f"Block: {block_number} exists")
        return
    if block_exist is not None and block_exist.hash != block.hash.hex():
        print(f"Block: {block_number} exists, but incorrect")
        db_session.delete(block_exist)

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
    print(f"Added new block: {block_number}")
    return


def add_block_transaction(db_session, block_number, tx) -> None:
    """
    Add block transaction if doesn't presented in database.
    """
    tx_exist = (
        db_session.query(EthereumTransaction)
        .filter(EthereumTransaction.hash == tx.hash.hex())
        .one_or_none()
    )
    if tx_exist is not None:
        return
    tx_obj = EthereumTransaction(
        hash=tx.hash.hex(),
        block_number=block_number,
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


def process_blocks(blocks_numbers: List[int], with_transactions: bool = False):
    """
    Open database and geth sessions and fetch block data from blockchain.
    """
    web3_client = connect()
    for block_number in blocks_numbers:
        with yield_db_session_ctx() as db_session:
            block: BlockData = web3_client.eth.get_block(
                block_number, full_transactions=with_transactions
            )
            add_block(db_session, block, block_number)
            if with_transactions:
                for tx in block.transactions:
                    add_block_transaction(db_session, block.number, tx)
            db_session.commit()


def crawl(block_numbers_list: List[int], with_transactions: bool = False):
    """
    Execute crawler.
    """
    with ProcessPoolExecutor(max_workers=MOONSTREAM_CRAWL_WORKERS) as executor:
        for worker in range(1, MOONSTREAM_CRAWL_WORKERS + 1):
            print(
                f"Added executor for list of blocks with len: {len(block_numbers_list[worker-1::MOONSTREAM_CRAWL_WORKERS])}"
            )
            executor.submit(
                process_blocks,
                block_numbers_list[worker - 1 :: MOONSTREAM_CRAWL_WORKERS],
                with_transactions,
            )
