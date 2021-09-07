from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json
import logging
from hexbytes.main import HexBytes
from typing import Any, cast, Dict, List, Optional, Set, Tuple

from eth_typing.encoding import HexStr
from moonstreamdb.models import (
    EthereumAddress,
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
)
from sqlalchemy import and_, func, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, Query
from tqdm import tqdm
from web3 import Web3
from web3.types import FilterParams, LogReceipt
from web3._utils.events import get_event_data

# Default length (in blocks) of an Ethereum NFT crawl.
DEFAULT_CRAWL_LENGTH = 100

NFT_LABEL = "erc721"
MINT_LABEL = "nft_mint"
TRANSFER_LABEL = "nft_transfer"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Summary keys
SUMMARY_KEY_BLOCKS = "blocks"
SUMMARY_KEY_NUM_TRANSACTIONS = "num_transactions"
SUMMARY_KEY_TOTAL_VALUE = "total_value"
SUMMARY_KEY_NFT_TRANSFERS = "nft_transfers"
SUMMARY_KEY_NFT_TRANSFER_VALUE = "nft_transfer_value"
SUMMARY_KEY_NFT_MINTS = "nft_mints"
SUMMARY_KEY_NFT_PURCHASERS = "nft_owners"
SUMMARY_KEY_NFT_MINTERS = "nft_minters"

SUMMARY_KEYS = [
    SUMMARY_KEY_BLOCKS,
    SUMMARY_KEY_NUM_TRANSACTIONS,
    SUMMARY_KEY_TOTAL_VALUE,
    SUMMARY_KEY_NFT_TRANSFERS,
    SUMMARY_KEY_NFT_TRANSFER_VALUE,
    SUMMARY_KEY_NFT_MINTS,
    SUMMARY_KEY_NFT_PURCHASERS,
    SUMMARY_KEY_NFT_MINTERS,
]


# First abi is for old NFT's like crypto kitties
# The erc721 standart requieres that Transfer event is indexed for all arguments
# That is how we get distinguished from erc20 transfer events
erc721_transfer_event_abis = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "from", "type": "address"},
            {"indexed": False, "name": "to", "type": "address"},
            {"indexed": False, "name": "tokenId", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": True, "name": "tokenId", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
]

erc721_functions_abi = [
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
]


@dataclass
class NFTContract:
    address: str
    name: Optional[str] = None
    symbol: Optional[str] = None
    total_supply: Optional[str] = None


def get_erc721_contract_info(w3: Web3, address: str) -> NFTContract:
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(address), abi=erc721_functions_abi
    )
    name: Optional[str] = None
    try:
        name = contract.functions.name().call()
    except:
        logger.error(f"Could not get name for potential NFT contract: {address}")

    symbol: Optional[str] = None
    try:
        symbol = contract.functions.symbol().call()
    except:
        logger.error(f"Could not get symbol for potential NFT contract: {address}")

    totalSupply: Optional[str] = None
    try:
        totalSupply = contract.functions.totalSupply().call()
    except:
        logger.error(f"Could not get totalSupply for potential NFT contract: {address}")

    return NFTContract(
        address=address, name=name, symbol=symbol, total_supply=totalSupply
    )


# SHA3 hash of the string "Transfer(address,address,uint256)"
TRANSFER_EVENT_SIGNATURE = HexBytes(
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
)


@dataclass
class NFTTransferRaw:
    contract_address: str
    transfer_from: str
    transfer_to: str
    tokenId: int
    transfer_tx: HexBytes


@dataclass
class NFTTransfer:
    contract_address: str
    transfer_from: str
    transfer_to: str
    tokenId: int
    transfer_tx: str
    value: Optional[int] = None
    is_mint: bool = False


def get_value_by_tx(w3: Web3, tx_hash: HexBytes):
    print(f"Trying to get tx: {tx_hash.hex()}")
    tx = w3.eth.get_transaction(tx_hash)
    print("got it")
    return tx["value"]


def decode_nft_transfer_data(w3: Web3, log: LogReceipt) -> Optional[NFTTransferRaw]:
    for abi in erc721_transfer_event_abis:
        try:
            transfer_data = get_event_data(w3.codec, abi, log)
            nft_transfer = NFTTransferRaw(
                contract_address=transfer_data["address"],
                transfer_from=transfer_data["args"]["from"],
                transfer_to=transfer_data["args"]["to"],
                tokenId=transfer_data["args"]["tokenId"],
                transfer_tx=transfer_data["transactionHash"],
            )
            return nft_transfer
        except:
            continue
    return None


def get_nft_transfers(
    w3: Web3,
    from_block: Optional[int] = None,
    to_block: Optional[int] = None,
    contract_address: Optional[str] = None,
) -> List[NFTTransfer]:
    filter_params = FilterParams(topics=[cast(HexStr, TRANSFER_EVENT_SIGNATURE.hex())])

    if from_block is not None:
        filter_params["fromBlock"] = from_block

    if to_block is not None:
        filter_params["toBlock"] = to_block

    if contract_address is not None:
        filter_params["address"] = w3.toChecksumAddress(contract_address)

    logs = w3.eth.get_logs(filter_params)
    nft_transfers: List[NFTTransfer] = []
    for log in tqdm(logs, desc="Crawling NFT transfers from Ethereum node"):
        nft_transfer = decode_nft_transfer_data(w3, log)
        if nft_transfer is not None:
            kwargs = {
                **asdict(nft_transfer),
                "transfer_tx": nft_transfer.transfer_tx.hex(),
                "is_mint": nft_transfer.transfer_from
                == "0x0000000000000000000000000000000000000000",
            }

            parsed_transfer = NFTTransfer(**kwargs)  # type: ignore
            nft_transfers.append(parsed_transfer)
    return nft_transfers


def get_block_bounds(
    w3: Web3, from_block: Optional[int] = None, to_block: Optional[int] = None
) -> Tuple[int, int]:
    """
    Returns starting and ending blocks for an "nft ethereum" crawl subject to the following rules:
    1. Neither start nor end can be None.
    2. If both from_block and to_block are None, then start = end - DEFAULT_CRAWL_LENGTH + 1
    """
    end = to_block
    if end is None:
        end = w3.eth.get_block_number()

    start = from_block
    if start is None:
        start = end - DEFAULT_CRAWL_LENGTH + 1

    return start, end


def ensure_addresses(db_session: Session, addresses: Set[str]) -> Dict[str, int]:
    """
    Ensures that the given addresses are registered in the ethereum_addresses table of the given
    moonstreamdb database connection. Returns a mapping from the addresses to the ids of their
    corresponding row in the ethereum_addresses table.

    Returns address_ids for *every* address, not just the new ones.
    """
    if len(addresses) == 0:
        return {}

    # SQLAlchemy reference:
    # https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#using-postgresql-on-conflict-with-returning-to-return-upserted-orm-objects
    stmt = (
        insert(EthereumAddress)
        .values([{"address": address} for address in addresses])
        .on_conflict_do_nothing(index_elements=[EthereumAddress.address])
    )

    try:
        db_session.execute(stmt)
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise

    rows = (
        db_session.query(EthereumAddress)
        .filter(EthereumAddress.address.in_(addresses))
        .all()
    )
    address_ids = {address.address: address.id for address in rows}
    return address_ids


def label_erc721_addresses(
    w3: Web3, db_session: Session, address_ids: List[Tuple[str, int]]
) -> None:
    labels: List[EthereumLabel] = []
    for address, id in address_ids:
        try:
            contract_info = get_erc721_contract_info(w3, address)
            labels.append(
                EthereumLabel(
                    address_id=id,
                    label=NFT_LABEL,
                    label_data={
                        "name": contract_info.name,
                        "symbol": contract_info.symbol,
                        "totalSupply": contract_info.total_supply,
                    },
                )
            )
        except Exception as e:
            logger.error(f"Failed to get metadata of contract {address}")
            logger.error(e)
    try:
        db_session.bulk_save_objects(labels)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to save labels to db:\n{e}")


def label_key(label: EthereumLabel) -> Tuple[str, int, int, str, str]:
    return (
        label.transaction_hash,
        label.address_id,
        label.label_data["tokenId"],
        label.label_data["from"],
        label.label_data["to"],
    )


def label_transfers(
    db_session: Session, transfers: List[NFTTransfer], address_ids: Dict[str, int]
) -> None:
    """
    Adds "nft_mint" or "nft_transfer" to the (transaction, address) pair represented by each of the
    given NFTTransfer objects.
    """
    transaction_hashes: List[str] = []
    labels: List[EthereumLabel] = []
    for transfer in transfers:
        transaction_hash = transfer.transfer_tx
        transaction_hashes.append(transaction_hash)
        address_id = address_ids.get(transfer.contract_address)
        label = MINT_LABEL if transfer.is_mint else TRANSFER_LABEL
        row = EthereumLabel(
            address_id=address_id,
            transaction_hash=transaction_hash,
            label=label,
            label_data={
                "tokenId": transfer.tokenId,
                "from": transfer.transfer_from,
                "to": transfer.transfer_to,
            },
        )
        labels.append(row)

    existing_labels = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address_id.in_(address_ids.values()))
        .filter(EthereumLabel.transaction_hash.in_(transaction_hashes))
    ).all()
    existing_label_keys = {label_key(label) for label in existing_labels}

    new_labels = [
        label for label in labels if label_key(label) not in existing_label_keys
    ]

    try:
        db_session.bulk_save_objects(new_labels)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logger.error("Could not write transfer/mint labels to database")
        logger.error(e)


def add_labels(
    w3: Web3,
    db_session: Session,
    from_block: Optional[int] = None,
    to_block: Optional[int] = None,
    address: Optional[str] = None,
    batch_size: int = 100,
) -> None:
    """
    Crawls blocks between from_block and to_block checking for NFT mints and transfers.

    For each mint/transfer, if the contract address involved in the operation has not already been
    added to the ethereum_addresses table, this method adds it and labels the address with the NFT
    collection metadata.

    It also adds mint/transfer labels to each (transaction, contract address) pair describing the
    NFT operation they represent.

    ## NFT collection metadata labels

    Label has type "erc721".

    Label data:
    {
        "name": "<name of contract>",
        "symbol": "<symbol of contract>",
        "totalSupply": "<totalSupply of contract>"
    }

    ## Mint and transfer labels
    Adds labels to the database for each transaction that involved an NFT transfer. Adds the contract
    address in the address_id column of ethereum_labels.


    Labels (transaction, contract address) pair as:
    - "nft_mint" if the transaction minted a token on the NFT contract
    - "nft_transfer" if the transaction transferred a token on the NFT contract

    Label data will always be of the form:
    {
        "tokenId": "<ID of token minted/transferred on NFT contract>",
        "from": "<previous owner address>",
        "to": "<new owner address>"
    }

    Arguments:
    - w3: Web3 client
    - db_session: Connection to Postgres database with moonstreamdb schema
    - from_block and to_block: Blocks to crawl
    - address: Optional contract address representing an NFT collection to restrict the crawl to
    - batch_size: Number of mint/transfer transactions to label at a time (per database transaction)
    """
    assert batch_size > 0, f"Batch size must be positive (received {batch_size})"

    start, end = get_block_bounds(w3, from_block, to_block)
    transfers = get_nft_transfers(w3, start, end, address)

    batch_start = 0
    batch_end = batch_size

    address_ids: Dict[str, int] = {}

    pbar = tqdm(total=len(transfers))
    pbar.set_description("Processing NFT transfer")
    while batch_start < batch_end:
        job = transfers[batch_start:batch_end]
        contract_addresses = {transfer.contract_address for transfer in job}
        updated_address_ids = ensure_addresses(db_session, contract_addresses)
        for address, address_id in updated_address_ids.items():
            address_ids[address] = address_id

        labelled_address_ids = [
            label.address_id
            for label in (
                db_session.query(EthereumLabel)
                .filter(EthereumLabel.label == NFT_LABEL)
                .filter(EthereumLabel.address_id.in_(address_ids.values()))
                .all()
            )
        ]
        unlabelled_address_ids = [
            (address, address_id)
            for address, address_id in address_ids.items()
            if address_id not in labelled_address_ids
        ]

        # Add 'erc721' labels
        label_erc721_addresses(w3, db_session, unlabelled_address_ids)

        # Add mint/transfer labels to (transaction, contract_address) pairs
        label_transfers(db_session, job, updated_address_ids)

        # Update batch at end of iteration
        pbar.update(batch_end - batch_start)
        batch_start = batch_end
        batch_end = min(batch_end + batch_size, len(transfers))
    pbar.close()


def time_bounded_summary(
    db_session: Session,
    start_time: datetime,
    end_time: datetime,
) -> Dict[str, Any]:
    """
    Produces a summary of Ethereum NFT activity between the given start_time and end_time (inclusive).
    """
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())

    time_filter = and_(
        EthereumBlock.timestamp >= start_timestamp,
        EthereumBlock.timestamp <= end_timestamp,
    )

    transactions_query = (
        db_session.query(EthereumTransaction)
        .join(
            EthereumBlock,
            EthereumTransaction.block_number == EthereumBlock.block_number,
        )
        .filter(time_filter)
    )

    def nft_query(label: str) -> Query:
        query = (
            db_session.query(
                EthereumLabel.label,
                EthereumLabel.label_data,
                EthereumLabel.address_id,
                EthereumTransaction.hash,
                EthereumTransaction.value,
                EthereumBlock.block_number,
                EthereumBlock.timestamp,
            )
            .join(
                EthereumTransaction,
                EthereumLabel.transaction_hash == EthereumTransaction.hash,
            )
            .join(
                EthereumBlock,
                EthereumTransaction.block_number == EthereumBlock.block_number,
            )
            .filter(time_filter)
            .filter(EthereumLabel.label == label)
        )
        return query

    transfer_query = nft_query(TRANSFER_LABEL)
    mint_query = nft_query(MINT_LABEL)

    def holder_query(label: str) -> Query:
        query = (
            db_session.query(
                EthereumLabel.address_id.label("address_id"),
                EthereumLabel.label_data["to"].astext.label("owner_address"),
                EthereumLabel.label_data["tokenId"].astext.label("token_id"),
                EthereumTransaction.block_number.label("block_number"),
                EthereumTransaction.transaction_index.label("transaction_index"),
                EthereumTransaction.value.label("transfer_value"),
            )
            .join(
                EthereumTransaction,
                EthereumLabel.transaction_hash == EthereumTransaction.hash,
            )
            .join(
                EthereumBlock,
                EthereumTransaction.block_number == EthereumBlock.block_number,
            )
            .filter(EthereumLabel.label == label)
            .filter(time_filter)
            .order_by(
                # Without "transfer_value" and "owner_address" as sort keys, the final distinct query
                # does not seem to be deterministic.
                # Maybe relevant Stackoverflow post: https://stackoverflow.com/a/59410440
                text(
                    "address_id, token_id, block_number desc, transaction_index desc, transfer_value, owner_address"
                )
            )
            .distinct("address_id", "token_id")
        )
        return query

    purchaser_query = holder_query(TRANSFER_LABEL)
    minter_query = holder_query(MINT_LABEL)

    blocks_result: Dict[str, int] = {}
    min_block = (
        db_session.query(func.min(EthereumBlock.block_number))
        .filter(time_filter)
        .scalar()
    )
    max_block = (
        db_session.query(func.max(EthereumBlock.block_number))
        .filter(time_filter)
        .scalar()
    )
    if min_block is not None:
        blocks_result["start"] = min_block
    if max_block is not None:
        blocks_result["end"] = max_block

    num_transactions = transactions_query.distinct(EthereumTransaction.hash).count()
    num_transfers = transfer_query.distinct(EthereumTransaction.hash).count()

    total_value = db_session.query(
        func.sum(transactions_query.subquery().c.value)
    ).scalar()
    transfer_value = db_session.query(
        func.sum(transfer_query.subquery().c.value)
    ).scalar()

    num_minted = mint_query.distinct(EthereumTransaction.hash).count()

    num_purchasers = (
        db_session.query(purchaser_query.subquery())
        .distinct(text("owner_address"))
        .count()
    )

    num_minters = (
        db_session.query(minter_query.subquery())
        .distinct(text("owner_address"))
        .count()
    )

    result = {
        "date_range": {
            "start_time": start_time.isoformat(),
            "include_start": True,
            "end_time": end_time.isoformat(),
            "include_end": True,
        },
        SUMMARY_KEY_BLOCKS: blocks_result,
        SUMMARY_KEY_NUM_TRANSACTIONS: f"{num_transactions}",
        SUMMARY_KEY_TOTAL_VALUE: f"{total_value}",
        SUMMARY_KEY_NFT_TRANSFERS: f"{num_transfers}",
        SUMMARY_KEY_NFT_TRANSFER_VALUE: f"{transfer_value}",
        SUMMARY_KEY_NFT_MINTS: f"{num_minted}",
        SUMMARY_KEY_NFT_PURCHASERS: f"{num_purchasers}",
        SUMMARY_KEY_NFT_MINTERS: f"{num_minters}",
    }

    return result


def summary(db_session: Session, end_time: datetime) -> Dict[str, Any]:
    """
    Produces a summary of all Ethereum NFT activity:
    1. From 1 hour before end_time to end_time
    2. From 1 day before end_time to end_time
    3. From 1 week before end_time to end_time
    """
    start_times = {
        "hour": end_time - timedelta(hours=1),
        "day": end_time - timedelta(days=1),
        "week": end_time - timedelta(weeks=1),
    }
    summaries = {
        period: time_bounded_summary(db_session, start_time, end_time)
        for period, start_time in start_times.items()
    }

    def aggregate_summary(key: str) -> Dict[str, Any]:
        return {period: summary.get(key) for period, summary in summaries.items()}

    result = {
        summary_key: aggregate_summary(summary_key) for summary_key in SUMMARY_KEYS
    }
    result["crawled_at"] = end_time.isoformat()
    return result
