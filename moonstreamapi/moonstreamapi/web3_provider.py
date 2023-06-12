import logging
from uuid import UUID

from typing import Any, Optional, Union
from web3 import Web3
from web3.eth import AsyncEth
from web3.middleware import geth_poa_middleware
from web3.providers.ipc import IPCProvider
from web3.providers.rpc import HTTPProvider
from web3.providers.async_rpc import AsyncHTTPProvider

from .settings import (
    MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI,
    NB_ACCESS_ID_HEADER,
    NB_DATA_SOURCE_HEADER,
    MOONSTREAM_POLYGON_WEB3_PROVIDER_URI,
    MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI,
    MOONSTREAM_XDAI_WEB3_PROVIDER_URI,
    MOONSTREAM_WYRM_WEB3_PROVIDER_URI,
    support_interfaces,
)
from moonstreamdb.blockchain import AvailableBlockchainType

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
    async_: bool = False,
) -> Web3:

    request_kwargs: Any = None
    if access_id is not None:
        request_kwargs = {
            "headers": {
                NB_ACCESS_ID_HEADER: str(access_id),
                NB_DATA_SOURCE_HEADER: "blockchain",
                "Content-Type": "application/json",
            }
        }

    if web3_uri is None:
        if blockchain_type == AvailableBlockchainType.ETHEREUM:
            web3_uri = MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.POLYGON:
            web3_uri = MOONSTREAM_POLYGON_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.MUMBAI:
            web3_uri = MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.XDAI:
            web3_uri = MOONSTREAM_XDAI_WEB3_PROVIDER_URI
        elif blockchain_type == AvailableBlockchainType.WYRM:
            web3_uri = MOONSTREAM_WYRM_WEB3_PROVIDER_URI
        else:
            raise Exception("Wrong blockchain type provided for web3 URI")

    print(f"Connecting to {web3_uri}")
    if web3_uri.startswith("http://") or web3_uri.startswith("https://"):
        request_kwargs["timeout"] = WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS
        web3_client = Web3(HTTPProvider(web3_uri, request_kwargs=request_kwargs))  # type: ignore
    else:
        web3_client = Web3(Web3.IPCProvider(web3_uri))
    # web3_client = Web3(web3_provider)

    # Inject --dev middleware if it is not Ethereum mainnet
    # Docs: https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    if blockchain_type != AvailableBlockchainType.ETHEREUM:
        web3_client.middleware_onion.inject(geth_poa_middleware, layer=0)

    return web3_client


def check_if_smartcontract(
    blockchain_type: AvailableBlockchainType,
    address: str,
    access_id: Optional[str] = None,
):
    """
    Checks if address is a smart contract on blockchain
    """
    web3_client = connect(blockchain_type, access_id=UUID(access_id))

    code = web3_client.eth.getCode(address)
    if code != b"":
        return True

    return False


def multicall(
    web3_client: Web3,
    calls: list,
    method: str = "tryAggregate",
    block_identifier: Optional[int] = None,
) -> list:
    """
    Calls multicall contract with given calls and returns list of results
    """
    multicall_contract = web3_client.eth.contract(
        address=Web3.toChecksumAddress("0xeefba1e63905ef1d7acba5a8513c70307c1ce441"),
        abi=[
            {
                "inputs": [{"internalType": "bytes", "name": "data", "type": "bytes"}],
                "name": "tryAggregate",
                "outputs": [
                    {"internalType": "bool", "name": "success", "type": "bool"},
                    {"internalType": "bytes", "name": "result", "type": "bytes"},
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "bytes", "name": "data", "type": "bytes"}],
                "name": "aggregate",
                "outputs": [
                    {"internalType": "bool", "name": "success", "type": "bool"},
                    {"internalType": "bytes", "name": "result", "type": "bytes"},
                ],
                "stateMutability": "payable",
                "type": "function",
            },
        ],
    )
    return getattr(multicall_contract.functions, method)(calls).call(
        block_identifier=block_identifier
    )


def get_list_of_support_interfaces(
    blockchain_type: AvailableBlockchainType,
    address: str,
    access_id: Optional[str] = None,
):
    """
    Returns list of interfaces supported by given address
    """
    web3_client = connect(blockchain_type, access_id=UUID(access_id))

    contract = web3_client.eth.contract(
        address=Web3.toChecksumAddress(address),
        abi=[
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
    )

    calls = []

    for interaface in support_interfaces:
        calls.append(
            (
                contract.address,
                contract.encodeABI(
                    fn_name="supportsInterface", args=[interaface["selector"]]
                ),
            )
        )
    try:
        multicall_result = multicall(
            web3_client,
            calls,
        )
    except Exception as e:
        logger.error(f"Error while getting list of support interfaces: {e}")

    result = []

    for i, interface in enumerate(support_interfaces):
        info = {
            "name": interface["name"],
            "selector": interface["selector"],
            "supported": False,
        }
        if multicall_result[i][0]:
            info["supported"] = True

        result.append(info)

    return result
