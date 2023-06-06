import getpass
import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import web3
from eth_account.account import Account  # type: ignore
from eth_typing.evm import ChecksumAddress
from hexbytes.main import HexBytes
from web3 import Web3
from web3.contract import Contract, ContractFunction
from web3.providers.ipc import IPCProvider
from web3.providers.rpc import HTTPProvider
from web3.types import ABI, Nonce, TxParams, TxReceipt, Wei


class ContractConstructor:
    def __init__(self, *args: Any):
        self.args = args


def build_transaction(
    web3: Web3,
    builder: Union[ContractFunction, Any],
    sender: ChecksumAddress,
) -> Union[TxParams, Any]:
    """
    Builds transaction json with the given arguments. It is not submitting transaction
    Arguments:
    - web3: Web3 client
    - builder: ContractFunction or other class that has method buildTransaction(TxParams)
    - sender: `from` value of transaction, address which is sending this transaction
    - maxFeePerGas: Optional, max priority fee for dynamic fee transactions in Wei
    - maxPriorityFeePerGas: Optional the part of the fee that goes to the miner
    """

    transaction = builder.buildTransaction(
        {
            "from": sender,
            "nonce": get_nonce(web3, sender),
        }
    )
    return transaction


def get_nonce(web3: Web3, address: ChecksumAddress) -> Nonce:
    """
    Returns Nonce: number of transactions for given address
    """
    nonce = web3.eth.get_transaction_count(address)
    return nonce


def submit_transaction(
    web3: Web3, transaction: Union[TxParams, Any], signer_private_key: str
) -> HexBytes:

    """
    Signs and submits json transaction to blockchain from the name of signer
    """
    signed_transaction = web3.eth.account.sign_transaction(
        transaction, private_key=signer_private_key
    )
    return submit_signed_raw_transaction(web3, signed_transaction.rawTransaction)


def submit_signed_raw_transaction(
    web3: Web3, signed_raw_transaction: HexBytes
) -> HexBytes:
    """
    Submits already signed raw transaction.
    """
    transaction_hash = web3.eth.send_raw_transaction(signed_raw_transaction)
    return transaction_hash


def wait_for_transaction_receipt(web3: Web3, transaction_hash: HexBytes):
    return web3.eth.wait_for_transaction_receipt(transaction_hash)


def deploy_contract(
    web3: Web3,
    contract_bytecode: str,
    contract_abi: List[Dict[str, Any]],
    deployer: ChecksumAddress,
    deployer_private_key: str,
    constructor_arguments: Optional[List[Any]] = None,
) -> Tuple[HexBytes, ChecksumAddress]:
    """
    Deploys smart contract to blockchain
    Arguments:
    - web3: web3 client
    - contract_bytecode: Compiled smart contract bytecode
    - contract_abi: Json abi of contract. Must include `constructor` function
    - deployer: Address which is deploying contract. Deployer will pay transaction fee
    - deployer_private_key: Private key of deployer. Needed for signing and submitting transaction
    - constructor_arguments: arguments that are passed to `constructor` function  of the smart contract
    """
    contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    if constructor_arguments is None:
        transaction = build_transaction(web3, contract.constructor(), deployer)
    else:
        transaction = build_transaction(
            web3, contract.constructor(*constructor_arguments), deployer
        )

    transaction_hash = submit_transaction(web3, transaction, deployer_private_key)
    transaction_receipt = wait_for_transaction_receipt(web3, transaction_hash)
    contract_address = transaction_receipt.contractAddress
    return transaction_hash, web3.toChecksumAddress(contract_address)


def deploy_contract_from_constructor_function(
    web3: Web3,
    contract_bytecode: str,
    contract_abi: List[Dict[str, Any]],
    deployer: ChecksumAddress,
    deployer_private_key: str,
    constructor: ContractConstructor,
) -> Tuple[HexBytes, ChecksumAddress]:
    """
    Deploys smart contract to blockchain from constructor ContractFunction
    Arguments:
    - web3: web3 client
    - contract_bytecode: Compiled smart contract bytecode
    - contract_abi: Json abi of contract. Must include `constructor` function
    - deployer: Address which is deploying contract. Deployer will pay transaction fee
    - deployer_private_key: Private key of deployer. Needed for signing and submitting transaction
    - constructor:`constructor` function  of the smart contract
    """
    contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    transaction = build_transaction(
        web3, contract.constructor(*constructor.args), deployer
    )

    transaction_hash = submit_transaction(web3, transaction, deployer_private_key)
    transaction_receipt = wait_for_transaction_receipt(web3, transaction_hash)
    contract_address = transaction_receipt.contractAddress
    return transaction_hash, web3.toChecksumAddress(contract_address)


def decode_transaction_input(web3: Web3, transaction_input: str, abi: Dict[str, Any]):
    contract = web3.eth.contract(abi=abi)
    return contract.decode_function_input(transaction_input)


def read_keys_from_cli() -> Tuple[ChecksumAddress, str]:
    private_key = getpass.getpass(prompt="Enter private key of your address:")
    account = Account.from_key(private_key)
    return (Web3.toChecksumAddress(account.address), private_key)


def read_keys_from_env() -> Tuple[ChecksumAddress, str]:
    private_key = os.environ.get("MOONWORM_ETHEREUM_ADDRESS_PRIVATE_KEY")
    if private_key is None:
        raise ValueError(
            "MOONWORM_ETHEREUM_ADDRESS_PRIVATE_KEY env variable is not set"
        )
    try:
        account = Account.from_key(private_key)
        return (Web3.toChecksumAddress(account.address), private_key)
    except:
        raise ValueError(
            "Failed to initiate account from MOONWORM_ETHEREUM_ADDRESS_PRIVATE_KEY"
        )


def connect(web3_uri: str) -> Web3:
    web3_provider: Union[IPCProvider, HTTPProvider] = Web3.IPCProvider()
    if web3_uri.startswith("http://") or web3_uri.startswith("https://"):
        web3_provider = Web3.HTTPProvider(web3_uri)
    else:
        web3_provider = Web3.IPCProvider(web3_uri)
    web3_client = Web3(web3_provider)
    return web3_client


def read_web3_provider_from_env() -> Web3:
    provider_path = os.environ.get("MOONWORM_WEB3_PROVIDER_URI")
    if provider_path is None:
        raise ValueError("MOONWORM_WEB3_PROVIDER_URI env variable is not set")
    return connect(provider_path)


def read_web3_provider_from_cli() -> Web3:
    provider_path = input("Enter web3 uri path: ")
    return connect(provider_path)


def cast_to_python_type(evm_type: str) -> Callable:
    if evm_type.startswith(("uint", "int")):
        return int
    elif evm_type.startswith("bytes"):
        return bytes
    elif evm_type == "string":
        return str
    elif evm_type == "address":
        return Web3.toChecksumAddress
    elif evm_type == "bool":
        return bool
    else:
        raise ValueError(f"Cannot convert to python type {evm_type}")
