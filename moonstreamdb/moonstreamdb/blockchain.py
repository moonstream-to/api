from enum import Enum
from typing import Type, Union

from .models import (
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    MumbaiBlock,
    MumbaiLabel,
    MumbaiTransaction,
    PolygonBlock,
    PolygonLabel,
    PolygonTransaction,
    WyrmBlock,
    WyrmLabel,
    WyrmTransaction,
    XDaiBlock,
    XDaiLabel,
    XDaiTransaction,
    ZkSyncEraTestnetBlock,
    ZkSyncEraTestnetLabel,
    ZkSyncEraTestnetTransaction,
    ZkSyncEraBlock,
    ZkSyncEraLabel,
    ZkSyncEraTransaction,
    StarknetBlock,
    StarknetTransaction,
    StarknetLabel,
)


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    MUMBAI = "mumbai"
    XDAI = "xdai"
    WYRM = "wyrm"
    ZKSYNC_ERA_TESTNET = "zksync_era_testnet"
    ZKSYNC_ERA = "zksync_era"
    STARKNET = "starknet"


def get_block_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[
    Union[
        EthereumBlock,
        PolygonBlock,
        MumbaiBlock,
        XDaiBlock,
        WyrmBlock,
        ZkSyncEraTestnetBlock,
        ZkSyncEraBlock,
        StarknetBlock,
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm, ZkSyncEra, ZkSyncEraTestnet
    set proper blocks model.
    """
    block_model: Type[
        Union[
            EthereumBlock,
            PolygonBlock,
            MumbaiBlock,
            XDaiBlock,
            WyrmBlock,
            ZkSyncEraTestnetBlock,
            ZkSyncEraBlock,
            StarknetBlock,
        ]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        block_model = EthereumBlock
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        block_model = PolygonBlock
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        block_model = MumbaiBlock
    elif blockchain_type == AvailableBlockchainType.XDAI:
        block_model = XDaiBlock
    elif blockchain_type == AvailableBlockchainType.WYRM:
        block_model = WyrmBlock
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
        block_model = ZkSyncEraTestnetBlock
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
        block_model = ZkSyncEraBlock
    elif blockchain_type == AvailableBlockchainType.STARKNET:
        block_model = StarknetBlock
    else:
        raise Exception("Unsupported blockchain type provided")

    return block_model


def get_label_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[
    Union[
        EthereumLabel,
        PolygonLabel,
        MumbaiLabel,
        XDaiLabel,
        WyrmLabel,
        ZkSyncEraTestnetLabel,
        ZkSyncEraLabel,
        StarknetLabel,
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm, ZkSyncEra, ZkSyncEraTestnet
    set proper block label model.
    """
    label_model: Type[
        Union[
            EthereumLabel,
            PolygonLabel,
            MumbaiLabel,
            XDaiLabel,
            WyrmLabel,
            ZkSyncEraTestnetLabel,
            ZkSyncEraLabel,
            StarknetLabel,
        ]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        label_model = EthereumLabel
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        label_model = PolygonLabel
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        label_model = MumbaiLabel
    elif blockchain_type == AvailableBlockchainType.XDAI:
        label_model = XDaiLabel
    elif blockchain_type == AvailableBlockchainType.WYRM:
        label_model = WyrmLabel
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
        label_model = ZkSyncEraTestnetLabel
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
        label_model = ZkSyncEraLabel
    elif blockchain_type == AvailableBlockchainType.STARKNET:
        label_model = StarknetLabel
    else:
        raise Exception("Unsupported blockchain type provided")

    return label_model


def get_transaction_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[
    Union[
        EthereumTransaction,
        PolygonTransaction,
        MumbaiTransaction,
        XDaiTransaction,
        WyrmTransaction,
        ZkSyncEraTestnetTransaction,
        ZkSyncEraTransaction,
        StarknetTransaction,
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm, ZkSyncEra, ZkSyncEraTestnet
    set proper block transactions model.
    """
    transaction_model: Type[
        Union[
            EthereumTransaction,
            PolygonTransaction,
            MumbaiTransaction,
            XDaiTransaction,
            WyrmTransaction,
            ZkSyncEraTestnetTransaction,
            ZkSyncEraTransaction,
            StarknetTransaction,
        ]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        transaction_model = EthereumTransaction
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        transaction_model = PolygonTransaction
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        transaction_model = MumbaiTransaction
    elif blockchain_type == AvailableBlockchainType.XDAI:
        transaction_model = XDaiTransaction
    elif blockchain_type == AvailableBlockchainType.WYRM:
        transaction_model = WyrmTransaction
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
        transaction_model = ZkSyncEraTestnetTransaction
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
        transaction_model = ZkSyncEraTransaction
    elif blockchain_type == AvailableBlockchainType.STARKNET:
        transaction_model = StarknetTransaction
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
