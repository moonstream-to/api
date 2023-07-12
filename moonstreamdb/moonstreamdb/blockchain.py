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
)


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    MUMBAI = "mumbai"
    XDAI = "xdai"
    WYRM = "wyrm"
    ZKSYNC_ERA_TESTNET = "zksync_era_testnet"


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
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm
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
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm
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
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm
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
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
