import logging
from typing import Any, Callable, Dict, Optional, Union
from uuid import UUID

from eth_abi import decode_single, encode_single
from eth_utils import function_signature_to_4byte_selector
from moonstreamtypes.blockchain import AvailableBlockchainType
from web3 import Web3
from web3._utils.abi import normalize_event_input_types
from web3.contract import ContractFunction
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider

from .settings import (
    MOONSTREAM_AMOY_WEB3_PROVIDER_URI,
    MOONSTREAM_ARBITRUM_NOVA_WEB3_PROVIDER_URI,
    MOONSTREAM_ARBITRUM_ONE_WEB3_PROVIDER_URI,
    MOONSTREAM_ARBITRUM_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_AVALANCHE_FUJI_WEB3_PROVIDER_URI,
    MOONSTREAM_AVALANCHE_WEB3_PROVIDER_URI,
    MOONSTREAM_BLAST_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_BLAST_WEB3_PROVIDER_URI,
    MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI,
    MOONSTREAM_IMX_ZKEVM_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_IMX_ZKEVM_WEB3_PROVIDER_URI,
    MOONSTREAM_MANTLE_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_MANTLE_WEB3_PROVIDER_URI,
    MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI,
    MOONSTREAM_POLYGON_WEB3_PROVIDER_URI,
    MOONSTREAM_PROOFOFPLAY_APEX_WEB3_PROVIDER_URI,
    MOONSTREAM_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_WYRM_WEB3_PROVIDER_URI,
    MOONSTREAM_XAI_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_XAI_WEB3_PROVIDER_URI,
    MOONSTREAM_XDAI_WEB3_PROVIDER_URI,
    MOONSTREAM_ZKSYNC_ERA_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_ZKSYNC_ERA_TESTNET_WEB3_PROVIDER_URI,
    MOONSTREAM_ZKSYNC_ERA_WEB3_PROVIDER_URI,
    MOONSTREAM_GAME7_TESTNET_WEB3_PROVIDER_URI,
    MOONSTREAM_B3_WEB3_PROVIDER_URI,
    MOONSTREAM_B3_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_GAME7_WEB3_PROVIDER_URI,
    MOONSTREAM_GAME7_TESTNET_WEB3_PROVIDER_URI,
    MOONSTREAM_SEPOLIA_WEB3_PROVIDER_URI,
    MOONSTREAM_IMX_ZKEVM_WEB3_PROVIDER_URI,
    MOONSTREAM_IMX_ZKEVM_SEPOLIA_WEB3_PROVIDER_URI,
    NB_ACCESS_ID_HEADER,
    multicall_contract_abi,
    multicall_contracts,
)

logger = logging.getLogger(__name__)

moonstream_web3_provider = Web3(
    Web3.HTTPProvider(MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI)
)


def yield_web3_provider() -> Web3:
    return moonstream_web3_provider


WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS = 10


def connect(
    blockchain_type: AvailableBlockchainType,
    web3_uri: Optional[str] = None,
    access_id: Optional[UUID] = None,
    user_token: Optional[UUID] = None,
) -> Web3:
    request_kwargs: Dict[str, Any] = {}

    if blockchain_type != AvailableBlockchainType.WYRM:
        request_kwargs = {
            "headers": {
                "Content-Type": "application/json",
            }
        }

        if access_id is not None:
            request_kwargs["headers"][NB_ACCESS_ID_HEADER] = str(access_id)
        elif user_token is not None:
            request_kwargs["headers"]["Authorization"] = f"Bearer {user_token}"

    if web3_uri is None:
        if blockchain_type == AvailableBlockchainType.ETHEREUM:
            web3_uri = MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.SEPOLIA:
            web3_uri = MOONSTREAM_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.POLYGON:
            web3_uri = MOONSTREAM_POLYGON_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.MUMBAI:
            web3_uri = MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.AMOY:
            web3_uri = MOONSTREAM_AMOY_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.XDAI:
            web3_uri = MOONSTREAM_XDAI_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.WYRM:
            web3_uri = MOONSTREAM_WYRM_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
            web3_uri = MOONSTREAM_ZKSYNC_ERA_TESTNET_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
            web3_uri = MOONSTREAM_ZKSYNC_ERA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
            web3_uri = MOONSTREAM_ZKSYNC_ERA_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.ARBITRUM_ONE:
            web3_uri = MOONSTREAM_ARBITRUM_ONE_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
            web3_uri = MOONSTREAM_ARBITRUM_NOVA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
            web3_uri = MOONSTREAM_ARBITRUM_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.XAI:
            web3_uri = MOONSTREAM_XAI_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
            web3_uri = MOONSTREAM_XAI_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.AVALANCHE:
            web3_uri = MOONSTREAM_AVALANCHE_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
            web3_uri = MOONSTREAM_AVALANCHE_FUJI_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.BLAST:
            web3_uri = MOONSTREAM_BLAST_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA:
            web3_uri = MOONSTREAM_BLAST_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX:
            web3_uri = MOONSTREAM_PROOFOFPLAY_APEX_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.MANTLE:
            web3_uri = MOONSTREAM_MANTLE_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
            web3_uri = MOONSTREAM_MANTLE_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM:
            web3_uri = MOONSTREAM_IMX_ZKEVM_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM_SEPOLIA:
            web3_uri = MOONSTREAM_IMX_ZKEVM_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.GAME7_TESTNET:
            web3_uri = MOONSTREAM_GAME7_TESTNET_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.B3:
            web3_uri = MOONSTREAM_B3_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.B3_SEPOLIA:
            web3_uri = MOONSTREAM_B3_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.SEPOLIA:
            web3_uri = MOONSTREAM_SEPOLIA_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.GAME7:
            web3_uri = MOONSTREAM_GAME7_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.GAME7_TESTNET:
            web3_uri = MOONSTREAM_GAME7_TESTNET_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM:
            web3_uri = MOONSTREAM_IMX_ZKEVM_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM_SEPOLIA:
            web3_uri = MOONSTREAM_IMX_ZKEVM_SEPOLIA_WEB3_PROVIDER_URI
        else:
            raise Exception("Wrong blockchain type provided for web3 URI")

    if web3_uri.startswith("http://") or web3_uri.startswith("https://"):
        request_kwargs["timeout"] = WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS
        web3_client = Web3(HTTPProvider(web3_uri, request_kwargs=request_kwargs))  # type: ignore
    else:
        web3_client = Web3(Web3.IPCProvider(web3_uri))

    if blockchain_type != AvailableBlockchainType.ETHEREUM:
        web3_client.middleware_onion.inject(geth_poa_middleware, layer=0)

    return web3_client


def multicall(
    web3_client: Web3,
    blockchain_type: AvailableBlockchainType,
    calls: list,
    method: str = "tryAggregate",
    block_identifier: Union[str, int, bytes, None] = "latest",
) -> list:
    """
    Calls multicall contract with given calls and returns list of results
    """

    multicall_contract = web3_client.eth.contract(
        address=Web3.toChecksumAddress(multicall_contracts[blockchain_type]),
        abi=multicall_contract_abi,
    )

    return multicall_contract.get_function_by_name(method)(False, calls).call(
        block_identifier=block_identifier
    )


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


class FunctionInput:
    def __init__(self, name: str, value: Any, solidity_type: str):
        self.name = name
        self.value = value
        self.solidity_type = solidity_type


class FunctionSignature:
    def __init__(self, function: ContractFunction):
        self.name = function.abi["name"]
        self.inputs = [
            {"name": arg["name"], "type": arg["type"]}
            for arg in normalize_event_input_types(function.abi.get("inputs", []))
        ]
        self.input_types_signature = "({})".format(
            ",".join([inp["type"] for inp in self.inputs])
        )
        self.output_types_signature = "({})".format(
            ",".join(
                [
                    arg["type"]
                    for arg in normalize_event_input_types(
                        function.abi.get("outputs", [])
                    )
                ]
            )
        )

        self.signature = "{}{}".format(self.name, self.input_types_signature)

        self.fourbyte = function_signature_to_4byte_selector(self.signature)

    def encode_data(self, args=None) -> bytes:
        return (
            self.fourbyte + encode_single(self.input_types_signature, args)
            if args
            else self.fourbyte
        )

    def decode_data(self, output):
        return decode_single(self.output_types_signature, output)
