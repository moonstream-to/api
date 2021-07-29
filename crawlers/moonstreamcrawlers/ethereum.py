from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple

from sqlalchemy import desc
from web3 import Web3
from web3.types import BlockData

from .settings import MOONSTREAM_IPC_PATH, MOONSTREAM_CRAWL_WORKERS
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import (
    EthereumBlock,
    EthereumSmartContract,
    EthereumTransaction,
)


def connect(ipc_path: str = MOONSTREAM_IPC_PATH):
    web3_client = Web3(Web3.IPCProvider(ipc_path))
    return web3_client


def add_block(db_session, block: BlockData, block_number: int) -> None:
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
    print(f"Added new block: {block_number}")


def add_block_transaction(db_session, block_number: int, tx) -> None:
    """
    Add block transaction if doesn't presented in database.
    """
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


def check_missing_blocks(blocks_numbers: List[int]):
    missing_blocks_numbers = []
    for block_number in blocks_numbers:
        with yield_db_session_ctx() as db_session:
            block_exist = (
                db_session.query(EthereumBlock)
                .filter(EthereumBlock.block_number == block_number)
                .one_or_none()
            )
            if block_exist is None:
                missing_blocks_numbers.append(block_number)
    return missing_blocks_numbers


def crawl(block_numbers_list: List[int], with_transactions: bool = False) -> None:
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
        while transactions_remaining:
            contract_deployments = (
                db_session.query(EthereumTransaction)
                .order_by(desc(EthereumTransaction.block_number))
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
                            EthereumSmartContract(
                                transaction_hash=deployment.hash,
                                address=contract_address,
                            )
                        )
                db_session.commit()
            else:
                transactions_remaining = False

            current_offset += limit

    return results
