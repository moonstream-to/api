from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, cast, Dict, List, Optional
from hexbytes.main import HexBytes

from eth_typing.encoding import HexStr
from tqdm import tqdm
from web3 import Web3
from web3.types import FilterParams, LogReceipt
from web3._utils.events import get_event_data


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


def summary(
    w3: Web3,
    from_block: Optional[int] = None,
    to_block: Optional[int] = None,
    address: Optional[str] = None,
) -> Dict[str, Any]:
    if to_block is None:
        to_block = w3.eth.get_block_number()

    # By default, let us summarize 100 blocks worth of NFT transfers
    if from_block is None:
        from_block = to_block - 99

    start_block = w3.eth.get_block(from_block)
    start_time = datetime.utcfromtimestamp(start_block.timestamp).isoformat()
    end_block = w3.eth.get_block(to_block)
    end_time = datetime.utcfromtimestamp(end_block.timestamp).isoformat()

    transfers = get_nft_transfers(w3, from_block, to_block, address)
    num_mints = sum(transfer.is_mint for transfer in transfers)

    result = {
        "date_range": {
            "start_time": start_time,
            "include_start": True,
            "end_time": end_time,
            "include_end": True,
        },
        "blocks": {
            "start": from_block,
            "end": to_block,
        },
        "num_transfers": len(transfers),
        "num_mints": num_mints,
    }

    return result
