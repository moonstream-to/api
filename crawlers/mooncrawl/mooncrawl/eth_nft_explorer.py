from dataclasses import dataclass, asdict
from collections import defaultdict
from typing import Dict, List, Optional
from web3 import Web3
import web3
from web3.types import FilterParams
from web3._utils.events import get_event_data


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:18375"))

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


def get_erc721_contract_info(address: str) -> NFT_contract:
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(address), abi=erc721_functions_abi
    )
    return NFT_contract(
        address=address,
        name=contract.functions.name().call(),
        symbol=contract.functions.symbol().call(),
        total_supply=contract.functions.totalSupply().call(),
    )


transfer_event_signature = w3.sha3(text="Transfer(address,address,uint256)").hex()


@dataclass
class NFTTransferRaw:
    contract_address: str
    transfer_from: str
    transfer_to: str
    tokenId: int
    transfer_tx: bytes


@dataclass
class NFTTransfer:
    contract_address: str
    transfer_from: str
    transfer_to: str
    tokenId: int
    transfer_tx: str
    value: Optional[int] = None
    is_mint: bool = False


def get_value_by_tx(tx_hash):
    print(f"Trying to get tx: {tx_hash.hex()}")
    tx = w3.eth.get_transaction(tx_hash)
    print("got it")
    return tx["value"]


def decode_nft_transfer_data(log) -> Optional[NFTTransferRaw]:
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
    block_number_from: int, contract_address: Optional[str] = None
) -> List[NFTTransfer]:
    filter_params = FilterParams(
        fromBlock=block_number_from, topics=[transfer_event_signature]
    )

    if contract_address is not None:
        filter_params["address"] = w3.toChecksumAddress(contract_address)

    logs = w3.eth.get_logs(filter_params)
    nft_transfers: List[NFTTransfer] = []
    tx_value: Dict[bytes, List[NFTTransferRaw]] = defaultdict(list)
    for log in logs:
        nft_transfer = decode_nft_transfer_data(log)
        if nft_transfer is not None:
            tx_value[nft_transfer.transfer_tx].append(nft_transfer)

    for tx_hash, transfers in tx_value.items():
        # value = get_value_by_tx(tx_hash)
        value = 0
        for transfer in transfers:
            kwargs = {
                **asdict(transfer),
                "transfer_tx": transfer.transfer_tx.hex(),
                "is_mint": transfer.transfer_from
                == "0x0000000000000000000000000000000000000000",
                "value": value,
            }
            parsed_transfer = NFTTransfer(**kwargs)

            nft_transfers.append(parsed_transfer)
    return nft_transfers


cryptoKittiesAddress = "0x06012c8cf97BEaD5deAe237070F9587f8E7A266d"
transfesrs = get_nft_transfers(
    w3.eth.block_number - 120,
)

print(transfesrs)
print(f"Total nft transfers: {len(transfesrs)}")
minted = list(filter(lambda transfer: transfer.is_mint == True, transfesrs))
# print(minted)
print(f"Minted count: {len(minted)}")
