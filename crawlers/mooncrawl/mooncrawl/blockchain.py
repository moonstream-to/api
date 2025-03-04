import logging
from concurrent.futures import Future, ThreadPoolExecutor, wait
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from uuid import UUID

from moonstreamtypes.blockchain import (
    AvailableBlockchainType,
    get_block_model,
    get_transaction_model,
)
from moonstreamdb.models import EthereumBlock, EthereumTransaction
from psycopg2.errors import UniqueViolation  # type: ignore
from sqlalchemy import Column, desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session
from tqdm import tqdm
from web3 import HTTPProvider, IPCProvider, Web3
from web3.middleware import geth_poa_middleware  # type: ignore
from web3.types import BlockData

from .data import DateRange
from .db import yield_db_session, yield_db_session_ctx
from .settings import (
    MOONSTREAM_CRAWL_WORKERS,
    MOONSTREAM_NODE_AMOY_A_EXTERNAL_URI,
    MOONSTREAM_NODE_ARBITRUM_ONE_A_EXTERNAL_URI,
    MOONSTREAM_NODE_ARBITRUM_NOVA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_ARBITRUM_SEPOLIA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_AVALANCHE_A_EXTERNAL_URI,
    MOONSTREAM_NODE_AVALANCHE_FUJI_A_EXTERNAL_URI,
    MOONSTREAM_NODE_BLAST_A_EXTERNAL_URI,
    MOONSTREAM_NODE_BLAST_SEPOLIA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_ETHEREUM_A_EXTERNAL_URI,
    MOONSTREAM_NODE_MUMBAI_A_EXTERNAL_URI,
    MOONSTREAM_NODE_POLYGON_A_EXTERNAL_URI,
    MOONSTREAM_NODE_PROOFOFPLAY_APEX_A_EXTERNAL_URI,
    MOONSTREAM_NODE_XAI_A_EXTERNAL_URI,
    MOONSTREAM_NODE_XAI_SEPOLIA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_XDAI_A_EXTERNAL_URI,
    MOONSTREAM_NODE_ZKSYNC_ERA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_ZKSYNC_ERA_SEPOLIA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_STARKNET_A_EXTERNAL_URI,
    MOONSTREAM_NODE_STARKNET_SEPOLIA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_MANTLE_A_EXTERNAL_URI,
    MOONSTREAM_NODE_MANTLE_SEPOLIA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_GAME7_ORBIT_ARBITRUM_SEPOLIA_A_EXTERNAL_URI,
    MOONSTREAM_NODE_IMX_ZKEVM_A_EXTERNAL_URI,
    MOONSTREAM_NODE_GAME7_TESTNET_A_EXTERNAL_URI,
    MOONSTREAM_NODE_GAME7_A_EXTERNAL_URI,
    MOONSTREAM_NODE_SEPOLIA_A_EXTERNAL_URI,
    WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BlockCrawlError(Exception):
    """
    Raised when there is a problem crawling blocks.
    """


default_uri_mapping = {
    AvailableBlockchainType.ETHEREUM: MOONSTREAM_NODE_ETHEREUM_A_EXTERNAL_URI,
    AvailableBlockchainType.POLYGON: MOONSTREAM_NODE_POLYGON_A_EXTERNAL_URI,
    AvailableBlockchainType.MUMBAI: MOONSTREAM_NODE_MUMBAI_A_EXTERNAL_URI,
    AvailableBlockchainType.AMOY: MOONSTREAM_NODE_AMOY_A_EXTERNAL_URI,
    AvailableBlockchainType.XDAI: MOONSTREAM_NODE_XDAI_A_EXTERNAL_URI,
    AvailableBlockchainType.ZKSYNC_ERA: MOONSTREAM_NODE_ZKSYNC_ERA_A_EXTERNAL_URI,
    AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA: MOONSTREAM_NODE_ZKSYNC_ERA_SEPOLIA_A_EXTERNAL_URI,
    AvailableBlockchainType.ARBITRUM_ONE: MOONSTREAM_NODE_ARBITRUM_ONE_A_EXTERNAL_URI,
    AvailableBlockchainType.ARBITRUM_NOVA: MOONSTREAM_NODE_ARBITRUM_NOVA_A_EXTERNAL_URI,
    AvailableBlockchainType.ARBITRUM_SEPOLIA: MOONSTREAM_NODE_ARBITRUM_SEPOLIA_A_EXTERNAL_URI,
    AvailableBlockchainType.XAI: MOONSTREAM_NODE_XAI_A_EXTERNAL_URI,
    AvailableBlockchainType.XAI_SEPOLIA: MOONSTREAM_NODE_XAI_SEPOLIA_A_EXTERNAL_URI,
    AvailableBlockchainType.AVALANCHE: MOONSTREAM_NODE_AVALANCHE_A_EXTERNAL_URI,
    AvailableBlockchainType.AVALANCHE_FUJI: MOONSTREAM_NODE_AVALANCHE_FUJI_A_EXTERNAL_URI,
    AvailableBlockchainType.BLAST: MOONSTREAM_NODE_BLAST_A_EXTERNAL_URI,
    AvailableBlockchainType.BLAST_SEPOLIA: MOONSTREAM_NODE_BLAST_SEPOLIA_A_EXTERNAL_URI,
    AvailableBlockchainType.PROOFOFPLAY_APEX: MOONSTREAM_NODE_PROOFOFPLAY_APEX_A_EXTERNAL_URI,
    AvailableBlockchainType.STARKNET: MOONSTREAM_NODE_STARKNET_A_EXTERNAL_URI,
    AvailableBlockchainType.STARKNET_SEPOLIA: MOONSTREAM_NODE_STARKNET_SEPOLIA_A_EXTERNAL_URI,
    AvailableBlockchainType.MANTLE: MOONSTREAM_NODE_MANTLE_A_EXTERNAL_URI,
    AvailableBlockchainType.MANTLE_SEPOLIA: MOONSTREAM_NODE_MANTLE_SEPOLIA_A_EXTERNAL_URI,
    AvailableBlockchainType.GAME7_ORBIT_ARBITRUM_SEPOLIA: MOONSTREAM_NODE_GAME7_ORBIT_ARBITRUM_SEPOLIA_A_EXTERNAL_URI,
    AvailableBlockchainType.IMX_ZKEVM: MOONSTREAM_NODE_IMX_ZKEVM_A_EXTERNAL_URI,
    AvailableBlockchainType.GAME7_TESTNET: MOONSTREAM_NODE_GAME7_TESTNET_A_EXTERNAL_URI,
    AvailableBlockchainType.GAME7: MOONSTREAM_NODE_GAME7_A_EXTERNAL_URI,
    AvailableBlockchainType.SEPOLIA: MOONSTREAM_NODE_SEPOLIA_A_EXTERNAL_URI,
}


def connect(
    blockchain_type: Optional[AvailableBlockchainType] = None,
    web3_uri: Optional[str] = None,
    version: int = 2,
) -> Web3:
    if blockchain_type is None and web3_uri is None:
        raise Exception("Both blockchain_type and web3_uri could not be None")

    web3_provider: Union[IPCProvider, HTTPProvider] = Web3.IPCProvider()

    request_kwargs: Dict[str, Any] = {"headers": {"Content-Type": "application/json"}}
    if web3_uri is None:
        web3_uri = default_uri_mapping.get(blockchain_type)  # type: ignore
        if web3_uri is None:
            raise Exception("Wrong blockchain type provided for web3 URI")

    if web3_uri.startswith("http://") or web3_uri.startswith("https://"):
        request_kwargs["timeout"] = WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS
        web3_provider = Web3.HTTPProvider(web3_uri, request_kwargs=request_kwargs)
    else:
        web3_provider = Web3.IPCProvider(web3_uri)
    web3_client = Web3(web3_provider)

    # Inject --dev middleware if it is not Ethereum mainnet
    # Docs: https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    if blockchain_type != AvailableBlockchainType.ETHEREUM:
        web3_client.middleware_onion.inject(geth_poa_middleware, layer=0)

    return web3_client


def hex_to_int(hex_str: Optional[str] = None) -> Optional[int]:
    if hex_str is None:
        return None
    elif hex_str.startswith("0x"):
        return int(hex_str, 16)
    else:
        return int(hex_str)


def add_block(db_session, block: Any, blockchain_type: AvailableBlockchainType) -> None:
    """
    Add block if doesn't presented in database.

    block: web3.types.BlockData

    - BlockData.extraData - doesn't exist at Polygon mainnet
    - Nonce - doesn't exist at XDai blockchain
    """
    block_model = get_block_model(blockchain_type)

    block_obj = block_model(
        block_number=block.number,
        difficulty=block.difficulty,
        extra_data=(
            None
            if block.get("extraData", None) is None
            else block.get("extraData").hex()
        ),
        gas_limit=block.gasLimit,
        gas_used=block.gasUsed,
        base_fee_per_gas=block.get("baseFeePerGas", None),
        hash=block.hash.hex(),
        logs_bloom=block.logsBloom.hex(),
        miner=block.miner,
        nonce=None if block.get("nonce", None) is None else block.get("nonce").hex(),
        parent_hash=block.parentHash.hex(),
        receipt_root=block.get("receiptsRoot", ""),
        uncles=block.sha3Uncles.hex(),
        size=block.size,
        state_root=block.stateRoot.hex(),
        timestamp=block.timestamp,
        total_difficulty=block.get("totalDifficulty", None),
        transactions_root=block.transactionsRoot.hex(),
    )
    if blockchain_type == AvailableBlockchainType.XDAI:
        block_obj.author = block.author
    elif (
        blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET
        or blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA
        or blockchain_type == AvailableBlockchainType.ZKSYNC_ERA
    ):
        block_obj.mix_hash = block.get("mixHash", "")
        block_obj.sha3_uncles = block.get("sha3Uncles", "")
        block_obj.l1_batch_number = (
            int(block.get("l1BatchNumber"), 0)
            if block.get("l1BatchNumber") is not None
            else None
        )
        block_obj.l1_batch_timestamp = (
            int(block.get("l1BatchTimestamp"), 0)
            if block.get("l1BatchTimestamp") is not None
            else None
        )
    elif (
        blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA
        or blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA
        or blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX
        or blockchain_type == AvailableBlockchainType.ARBITRUM_ONE
    ):
        block_obj.sha3_uncles = block.get("sha3Uncles", "")
        block_obj.l1_block_number = hex_to_int(block.get("l1BlockNumber"))
        block_obj.send_count = hex_to_int(block.get("sendCount"))
        block_obj.send_root = block.get("sendRoot", "")
        block_obj.mix_hash = block.get("mixHash", "")
    elif (
        blockchain_type == AvailableBlockchainType.XAI
        or blockchain_type == AvailableBlockchainType.XAI_SEPOLIA
    ):
        block_obj.sha3_uncles = block.get("sha3Uncles", "")
        block_obj.l1_block_number = hex_to_int(block.get("l1BlockNumber"))
        block_obj.send_count = hex_to_int(block.get("sendCount"))
        block_obj.send_root = block.get("sendRoot", "")
        block_obj.mix_hash = block.get("mixHash", "")
    elif (
        blockchain_type == AvailableBlockchainType.AVALANCHE
        or blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI
    ):
        block_obj.mix_hash = block.get("mixHash", "")
        block_obj.block_extra_data = block.get("blockExtraData")
        block_obj.block_gas_cost = block.get("blockGasCost")
        block_obj.ext_data_gas_used = block.get("extDataGasUsed", "")
        block_obj.ext_data_hash = block.get("extDataHash", "")
    elif (
        blockchain_type == AvailableBlockchainType.BLAST
        or blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA
    ):
        block_obj.sha3_uncles = block.get("sha3Uncles", "")
        block_obj.mix_hash = block.get("mixHash", "")
        block_obj.withdrawals_root = block.get("withdrawalsRoot", "")

    db_session.add(block_obj)


def add_block_transactions(
    db_session, block: Any, blockchain_type: AvailableBlockchainType
) -> None:
    """
    Add block transactions.

    block: web3.types.BlockData
    """
    transaction_model = get_transaction_model(blockchain_type)
    for tx in block.transactions:
        tx_obj = transaction_model(
            hash=tx.hash.hex(),
            block_number=block.number,
            from_address=tx["from"],
            to_address=tx.to,
            gas=tx.gas,
            gas_price=tx.gasPrice,
            max_fee_per_gas=tx.get("maxFeePerGas", None),
            max_priority_fee_per_gas=tx.get("maxPriorityFeePerGas", None),
            input=tx.input,
            nonce=tx.nonce,
            transaction_index=tx.transactionIndex,
            transaction_type=int(tx["type"], 0) if tx.get("type") is not None else None,
            value=tx.value,
        )
        if (
            blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET
            or blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA
            or blockchain_type == AvailableBlockchainType.ZKSYNC_ERA
        ):
            tx_obj.l1_batch_number = (
                int(tx.get("l1BatchNumber"), 0)
                if tx.get("l1BatchNumber") is not None
                else None
            )
            tx_obj.l1_batch_tx_index = (
                int(tx.get("l1BatchTxIndex"), 0)
                if tx.get("l1BatchTxIndex") is not None
                else None
            )
        if (
            blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA
            or blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA
            or blockchain_type == AvailableBlockchainType.XAI
            or blockchain_type == AvailableBlockchainType.XAI_SEPOLIA
            or blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX
            or blockchain_type == AvailableBlockchainType.ARBITRUM_ONE
        ):
            tx_obj.y_parity = hex_to_int(tx.get("yParity"))

        db_session.add(tx_obj)


def get_latest_blocks(
    blockchain_type: AvailableBlockchainType,
    confirmations: int = 0,
    web3_uri: Optional[str] = None,
) -> Tuple[Optional[int], int]:
    """
    Retrieve the latest block from the connected node (connection is created by the connect(AvailableBlockchainType) method).

    If confirmations > 0, and the latest block on the node has block number N, this returns the block
    with block_number (N - confirmations)
    """
    web3_client = connect(blockchain_type, web3_uri=web3_uri)
    latest_block_number: int = web3_client.eth.block_number
    if confirmations > 0:
        latest_block_number -= confirmations

    block_model = get_block_model(blockchain_type)
    with yield_db_session_ctx() as db_session:
        latest_stored_block_row = (
            db_session.query(block_model.block_number)
            .order_by(block_model.block_number.desc())
            .first()
        )
        latest_stored_block_number = (
            None if latest_stored_block_row is None else latest_stored_block_row[0]
        )

    return latest_stored_block_number, latest_block_number


def crawl_blocks(
    blockchain_type: AvailableBlockchainType,
    blocks_numbers: List[int],
    with_transactions: bool = False,
    web3_uri: Optional[str] = None,
) -> None:
    """
    Open database and geth sessions and fetch block data from blockchain.
    """
    web3_client = connect(blockchain_type, web3_uri=web3_uri)
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
                add_block(db_session, block, blockchain_type)

                if with_transactions:
                    add_block_transactions(db_session, block, blockchain_type)

                db_session.commit()
            except IntegrityError as err:
                db_session.rollback()
                assert isinstance(err.orig, UniqueViolation)
                logger.error(
                    "UniqueViolation error occurred, it means block already exists"
                )
            except Exception as err:
                db_session.rollback()
                message = f"Error adding block (number={block_number}) to database:\n{repr(err)}"
                raise BlockCrawlError(message)
            except:
                db_session.rollback()
                logger.error(
                    f"Interrupted while adding block (number={block_number}) to database."
                )
                raise
            pbar.update()
        pbar.close()


def check_missing_blocks(
    blockchain_type: AvailableBlockchainType,
    blocks_numbers: List[int],
    notransactions=False,
    web3_uri: Optional[str] = None,
) -> List[int]:
    """
    Query block from postgres. If block does not presented in database,
    add to missing blocks numbers list.
    If arg notransactions=False, it checks correct number of transactions in
    database according to blockchain.
    """
    bottom_block = min(blocks_numbers[-1], blocks_numbers[0])
    top_block = max(blocks_numbers[-1], blocks_numbers[0])

    block_model = get_block_model(blockchain_type)
    transaction_model = get_transaction_model(blockchain_type)
    with yield_db_session_ctx() as db_session:
        if notransactions:
            blocks_exist_raw_query = (
                db_session.query(block_model.block_number)
                .filter(block_model.block_number >= bottom_block)
                .filter(block_model.block_number <= top_block)
            )
            blocks_exist = [[block[0]] for block in blocks_exist_raw_query.all()]
        else:
            corrupted_blocks = []
            blocks_exist_raw_query = (
                db_session.query(
                    block_model.block_number, func.count(transaction_model.hash)
                )
                .join(
                    transaction_model,
                    transaction_model.block_number == block_model.block_number,
                )
                .filter(block_model.block_number >= bottom_block)
                .filter(block_model.block_number <= top_block)
                .group_by(block_model.block_number)
            )
            blocks_exist = [
                [block[0], block[1]] for block in blocks_exist_raw_query.all()
            ]

            web3_client = connect(blockchain_type, web3_uri=web3_uri)

            blocks_exist_len = len(blocks_exist)
            pbar = tqdm(total=blocks_exist_len)
            pbar.set_description(f"Checking txs in {blocks_exist_len} blocks")

            for i, block_in_db in enumerate(blocks_exist):
                block = web3_client.eth.get_block(
                    block_in_db[0], full_transactions=True
                )
                if len(block.transactions) != block_in_db[1]:  # type: ignore
                    corrupted_blocks.append(block_in_db[0])
                    # Delete existing corrupted block and add to missing list
                    del_block = (
                        db_session.query(block_model)
                        .filter(block_model.block_number == block_in_db[0])
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
    blockchain_type: AvailableBlockchainType,
    block_numbers_list: List[int],
    with_transactions: bool = False,
    num_processes: int = MOONSTREAM_CRAWL_WORKERS,
    web3_uri: Optional[str] = None,
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
        return crawl_blocks(
            blockchain_type, block_numbers_list, with_transactions, web3_uri=web3_uri
        )
    else:
        with ThreadPoolExecutor(max_workers=MOONSTREAM_CRAWL_WORKERS) as executor:
            for worker in worker_indices:
                block_chunk = worker_job_lists[worker]
                logger.info(f"Spawned process for {len(block_chunk)} blocks")
                result = executor.submit(
                    crawl_blocks,
                    blockchain_type,
                    block_chunk,
                    with_transactions,
                    web3_uri,
                )
                result.add_done_callback(record_error)
                results.append(result)

        wait(results)
        if len(errors) > 0:
            error_messages = "\n".join([f"- {error}" for error in errors])
            message = f"Error processing blocks in list:\n{error_messages}"
            raise BlockCrawlError(message)


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
