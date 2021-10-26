import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set, Tuple, cast

from eth_typing.encoding import HexStr
from hexbytes.main import HexBytes
from moonstreamdb.models import EthereumBlock, EthereumLabel, EthereumTransaction
from sqlalchemy import and_, func, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Query, Session
from tqdm import tqdm
from web3 import Web3
from web3._utils.events import get_event_data
from web3.types import FilterParams, LogReceipt

from ..reporter import reporter

# Default length (in blocks) of an Ethereum NFT crawl.
DEFAULT_CRAWL_LENGTH = 100

NFT_LABEL = "erc721"
MINT_LABEL = "nft_mint"
TRANSFER_LABEL = "nft_transfer"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Summary keys
SUMMARY_KEY_ID = "summary_id"
SUMMARY_KEY_ARGS = "args"
SUMMARY_KEY_START_BLOCK = "start_block"
SUMMARY_KEY_END_BLOCK = "end_block"
SUMMARY_KEY_NUM_BLOCKS = "num_blocks"
SUMMARY_KEY_NUM_TRANSACTIONS = "num_transactions"
SUMMARY_KEY_TOTAL_VALUE = "total_value"
SUMMARY_KEY_NFT_TRANSFERS = "nft_transfers"
SUMMARY_KEY_NFT_TRANSFER_VALUE = "nft_transfer_value"
SUMMARY_KEY_NFT_MINTS = "nft_mints"
SUMMARY_KEY_NFT_PURCHASERS = "nft_owners"
SUMMARY_KEY_NFT_MINTERS = "nft_minters"

SUMMARY_KEYS = [
    SUMMARY_KEY_ID,
    SUMMARY_KEY_ARGS,
    SUMMARY_KEY_START_BLOCK,
    SUMMARY_KEY_END_BLOCK,
    SUMMARY_KEY_NUM_BLOCKS,
    SUMMARY_KEY_NUM_TRANSACTIONS,
    SUMMARY_KEY_TOTAL_VALUE,
    SUMMARY_KEY_NFT_TRANSFERS,
    SUMMARY_KEY_NFT_TRANSFER_VALUE,
    SUMMARY_KEY_NFT_MINTS,
    SUMMARY_KEY_NFT_PURCHASERS,
    SUMMARY_KEY_NFT_MINTERS,
]


# The erc721 standart requieres that Transfer event is indexed for all arguments
# That is how we get distinguished from erc20 transfer events
# Second abi is for old NFT's like crypto kitties
erc721_transfer_event_abis = [
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

    return NFTContract(
        address=address,
        name=name,
        symbol=symbol,
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
    for log in tqdm(logs, desc=f"Processing logs for blocks {from_block}-{to_block}"):
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


def label_erc721_addresses(w3: Web3, db_session: Session, addresses: List[str]) -> None:
    labels: List[EthereumLabel] = []
    for address in addresses:
        try:
            contract_info = get_erc721_contract_info(w3, address)

            # Postgres cannot store the following unicode code point in a string: \u0000
            # Therefore, we replace that code point with the empty string to avoid errors:
            # https://stackoverflow.com/a/31672314
            contract_name: Optional[str] = None
            if contract_info.name is not None:
                contract_name = contract_info.name.replace("\\u0000", "").replace(
                    "\x00", ""
                )
            contract_symbol: Optional[str] = None
            if contract_info.symbol is not None:
                contract_symbol = contract_info.symbol.replace("\\u0000", "").replace(
                    "\x00", ""
                )

            labels.append(
                EthereumLabel(
                    address=address,
                    label=NFT_LABEL,
                    label_data={
                        "name": contract_name,
                        "symbol": contract_symbol,
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
        logger.error(f"Failed to save erc721 labels to db:\n{e}")
        raise e


def label_key(label: EthereumLabel) -> Tuple[str, int, int, str, str]:
    return (
        label.transaction_hash,
        label.address,
        label.label_data["tokenId"],
        label.label_data["from"],
        label.label_data["to"],
    )


def label_transfers(
    db_session: Session, transfers: List[NFTTransfer], addresses: Set[str]
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
        label = MINT_LABEL if transfer.is_mint else TRANSFER_LABEL
        row = EthereumLabel(
            address=transfer.contract_address,
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
        .filter(EthereumLabel.address.in_(addresses))
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
        raise e


def add_labels(
    w3: Web3,
    db_session: Session,
    from_block: Optional[int] = None,
    to_block: Optional[int] = None,
    contract_address: Optional[str] = None,
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

    batch_start = start
    batch_end = min(start + batch_size - 1, end)

    # TODO(yhtiyar): Make address_ids as global cache to fast up crawling
    # address_ids: Dict[str, int] = {}
    # For now quitting this idea because some contracts have unicode escapes
    # in their names, and global cache will fuck up not only that batch labeling
    # but later ones as well

    pbar = tqdm(total=(end - start + 1))
    pbar.set_description(f"Labeling blocks {start}-{end}")
    while batch_start <= batch_end:
        job = get_nft_transfers(
            w3,
            from_block=batch_start,
            to_block=batch_end,
            contract_address=contract_address,
        )
        contract_addresses = {transfer.contract_address for transfer in job}

        labelled_address = [
            label.address
            for label in (
                db_session.query(EthereumLabel)
                .filter(EthereumLabel.label == NFT_LABEL)
                .filter(EthereumLabel.address.in_(contract_addresses))
                .all()
            )
        ]
        unlabelled_address = [
            address for address in contract_addresses if address not in labelled_address
        ]

        # Add 'erc721' labels
        try:
            label_erc721_addresses(w3, db_session, unlabelled_address)
        except Exception as e:
            reporter.error_report(
                e,
                [
                    "nft_crawler",
                    "erc721_label",
                    f"batch_start:{batch_start}",
                    f"batch_end:{batch_end}",
                ],
            )

        # Add mint/transfer labels to (transaction, contract_address) pairs
        try:
            label_transfers(db_session, job, contract_addresses)
        except Exception as e:
            reporter.error_report(
                e,
                [
                    "nft_crawler",
                    "nft_transfer",
                    f"batch_start:{batch_start}",
                    f"batch_end:{batch_end}",
                ],
            )

        # Update batch at end of iteration
        pbar.update(batch_end - batch_start + 1)
        batch_start = batch_end + 1
        batch_end = min(batch_end + batch_size, end)
    pbar.close()


def block_bounded_summary(
    db_session: Session,
    start_block: int,
    end_block: int,
) -> Dict[str, Any]:
    """
    Produces a summary of Ethereum NFT activity between the given start_time and end_time (inclusive).
    """
    summary_id = f"nft-ethereum-start-{start_block}-end-{end_block}"

    block_filter = and_(
        EthereumBlock.block_number >= start_block,
        EthereumBlock.block_number <= end_block,
    )

    transactions_query = (
        db_session.query(EthereumTransaction)
        .join(
            EthereumBlock,
            EthereumTransaction.block_number == EthereumBlock.block_number,
        )
        .filter(block_filter)
    )

    def nft_query(label: str) -> Query:
        query = (
            db_session.query(
                EthereumLabel.label,
                EthereumLabel.label_data,
                EthereumLabel.address,
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
            .filter(block_filter)
            .filter(EthereumLabel.label == label)
        )
        return query

    transfer_query = nft_query(TRANSFER_LABEL)
    mint_query = nft_query(MINT_LABEL)

    def holder_query(label: str) -> Query:
        query = (
            db_session.query(
                EthereumLabel.address.label("address"),
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
            .filter(block_filter)
            .order_by(
                # Without "transfer_value" and "owner_address" as sort keys, the final distinct query
                # does not seem to be deterministic.
                # Maybe relevant Stackoverflow post: https://stackoverflow.com/a/59410440
                text(
                    "address, token_id, block_number desc, transaction_index desc, transfer_value, owner_address"
                )
            )
            .distinct("address", "token_id")
        )
        return query

    purchaser_query = holder_query(TRANSFER_LABEL)
    minter_query = holder_query(MINT_LABEL)

    blocks = (
        db_session.query(EthereumBlock)
        .filter(block_filter)
        .order_by(EthereumBlock.block_number.asc())
    )
    first_block = None
    last_block = None
    num_blocks = 0
    for block in blocks:
        if num_blocks == 0:
            min_block = block
        max_block = block
        num_blocks += 1

    start_time = None
    end_time = None
    if min_block is not None:
        first_block = min_block.block_number
        start_time = datetime.fromtimestamp(
            min_block.timestamp, timezone.utc
        ).isoformat()
    if max_block is not None:
        last_block = max_block.block_number
        end_time = datetime.fromtimestamp(max_block.timestamp, timezone.utc).isoformat()

    num_transactions = transactions_query.distinct(EthereumTransaction.hash).count()
    num_transfers = transfer_query.distinct(EthereumTransaction.hash).count()

    total_value = db_session.query(
        func.sum(transactions_query.subquery().c.value)
    ).scalar()
    transfer_value = db_session.query(
        func.sum(transfer_query.subquery().c.value)
    ).scalar()

    num_minted = mint_query.count()

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
            "start_time": start_time,
            "include_start": True,
            "end_time": end_time,
            "include_end": True,
        },
        SUMMARY_KEY_ID: summary_id,
        SUMMARY_KEY_ARGS: {"start": start_block, "end": end_block},
        SUMMARY_KEY_START_BLOCK: first_block,
        SUMMARY_KEY_END_BLOCK: last_block,
        SUMMARY_KEY_NUM_BLOCKS: num_blocks,
        SUMMARY_KEY_NUM_TRANSACTIONS: f"{num_transactions}",
        SUMMARY_KEY_TOTAL_VALUE: f"{total_value}",
        SUMMARY_KEY_NFT_TRANSFERS: f"{num_transfers}",
        SUMMARY_KEY_NFT_TRANSFER_VALUE: f"{transfer_value}",
        SUMMARY_KEY_NFT_MINTS: f"{num_minted}",
        SUMMARY_KEY_NFT_PURCHASERS: f"{num_purchasers}",
        SUMMARY_KEY_NFT_MINTERS: f"{num_minters}",
    }

    return result


def summary(db_session: Session, start_block: int, end_block: int) -> Dict[str, Any]:
    """
    Produces a summary of all Ethereum NFT activity:
        From 1 hour before end_time to end_time
    """

    result = block_bounded_summary(db_session, start_block, end_block)
    result["crawled_at"] = datetime.utcnow().isoformat()
    return result
