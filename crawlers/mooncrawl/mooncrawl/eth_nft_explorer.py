from dataclasses import dataclass
from typing import List, Optional
from web3 import Web3
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
class NFT_transfer:
    contract_address: str
    transfer_from: str
    transfer_to: str
    tokenId: int
    transfer_tx: str
    is_mint: bool = False


def decode_nft_transfer_data(log) -> Optional[NFT_transfer]:
    for abi in erc721_transfer_event_abis:
        try:
            transfer_data = get_event_data(w3.codec, abi, log)
            nft_transfer = NFT_transfer(
                contract_address=transfer_data["address"],
                transfer_from=transfer_data["args"]["from"],
                transfer_to=transfer_data["args"]["to"],
                tokenId=transfer_data["args"]["tokenId"],
                transfer_tx=transfer_data["transactionHash"].hex(),
            )
            if (
                nft_transfer.transfer_from
                == "0x0000000000000000000000000000000000000000"  # Blackhole address
            ):
                nft_transfer.is_mint = True
            return nft_transfer
        except:
            continue
    return None


def get_nft_transfers(
    block_number_from: int, contract_address: Optional[str] = None
) -> List[NFT_transfer]:
    filter_params = FilterParams(
        fromBlock=block_number_from, topics=[transfer_event_signature]
    )

    if contract_address is not None:
        filter_params["address"] = w3.toChecksumAddress(contract_address)

    logs = w3.eth.get_logs(filter_params)
    nft_transfers: List[NFT_transfer] = []
    for log in logs:
        nft_transfer = decode_nft_transfer_data(log)
        if nft_transfer is not None:
            nft_transfers.append(nft_transfer)
    return nft_transfers


cryptoKittiesAddress = "0x06012c8cf97BEaD5deAe237070F9587f8E7A266d"
transfesrs = get_nft_transfers(
    w3.eth.block_number - 1000, "0x2aea4add166ebf38b63d09a75de1a7b94aa24163"
)

print(transfesrs)
print(f"Total nft transfers: {len(transfesrs)}")
minted = list(filter(lambda transfer: transfer.is_mint == True, transfesrs))
# print(minted)
print(f"Minted count: {len(minted)}")
