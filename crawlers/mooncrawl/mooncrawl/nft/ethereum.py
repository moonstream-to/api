from dataclasses import dataclass, asdict
from datetime import datetime
from hexbytes.main import HexBytes
from typing import Any, cast, Dict, List, Optional, Set, Tuple

from eth_typing.encoding import HexStr
from moonstreamdb.models import EthereumAddress, EthereumLabel, EthereumTransaction
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from tqdm import tqdm
from web3 import Web3
from web3.types import FilterParams, LogReceipt
from web3._utils.events import get_event_data


# Default length (in blocks) of an Ethereum NFT crawl.
DEFAULT_CRAWL_LENGTH = 100

NFT_LABEL = "erc721"
MINT_LABEL = "nft_mint"
TRANSFER_LABEL = "nft_transfer"

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
class NFT_contract:
    address: str
    name: str
    symbol: str
    total_supply: str


def get_erc721_contract_info(w3: Web3, address: str) -> NFT_contract:
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(address), abi=erc721_functions_abi
    )
    return NFT_contract(
        address=address,
        name=contract.functions.name().call(),
        symbol=contract.functions.symbol().call(),
        total_supply=contract.functions.totalSupply().call(),
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
    for log in tqdm(logs):
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
):
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
        except:
            print(f"Failed to get metadata of contract {address}")
    try:
        db_session.bulk_save_objects(labels)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Failed to save labels to db:\n{e}")


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

    Label data: {"name": "<name of contract>", "symbol": "<symbol of contract>", "totalSupply": "<totalSupply of contract>"}

    ## Mint and transfer labels
    Adds labels to the database for each transaction that involved an NFT transfer. Adds the contract
    address in the address_id column of ethereum_labels.


    Labels (transaction, contract address) pair as:
    - "nft_mint" if the transaction minted a token on the NFT contract
    - "nft_transfer" if the transaction transferred a token on the NFT contract

    Label data will always be of the form: {"token_id": "<ID of token minted/transferred on NFT contract>"}

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

    with tqdm(total=len(transfers)) as pbar:
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

            # Adding 'erc721' labels
            label_erc721_addresses(w3, db_session, unlabelled_address_ids)

            # Update batch at end of iteration
            pbar.update(batch_end - batch_start)
            batch_start = batch_end
            batch_end = min(batch_end + batch_size, len(transfers))


def summary(
    w3: Web3,
    from_block: Optional[int] = None,
    to_block: Optional[int] = None,
    address: Optional[str] = None,
) -> Dict[str, Any]:
    start, end = get_block_bounds(w3, from_block, to_block)
    start_block = w3.eth.get_block(start)
    start_time = datetime.utcfromtimestamp(start_block.timestamp).isoformat()
    end_block = w3.eth.get_block(end)
    end_time = datetime.utcfromtimestamp(end_block.timestamp).isoformat()

    transfers = get_nft_transfers(w3, start, end, address)
    num_mints = sum(transfer.is_mint for transfer in transfers)

    result = {
        "date_range": {
            "start_time": start_time,
            "include_start": True,
            "end_time": end_time,
            "include_end": True,
        },
        "blocks": {
            "start": start,
            "end": end,
        },
        "num_transfers": len(transfers),
        "num_mints": num_mints,
    }

    return result
