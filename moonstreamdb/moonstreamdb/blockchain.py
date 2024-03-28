from enum import Enum
from typing import Type, Union

from .models import (
    ArbitrumNovaBlock,
    ArbitrumNovaLabel,
    ArbitrumNovaTransaction,
    ArbitrumSepoliaBlock,
    ArbitrumSepoliaLabel,
    ArbitrumSepoliaTransaction,
    AvalancheBlock,
    AvalancheFujiBlock,
    AvalancheFujiLabel,
    AvalancheFujiTransaction,
    AvalancheLabel,
    AvalancheTransaction,
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
    XaiBlock,
    XaiLabel,
    XaiTransaction,
    XDaiBlock,
    XDaiLabel,
    XDaiTransaction,
    ZkSyncEraBlock,
    ZkSyncEraLabel,
    ZkSyncEraSepoliaBlock,
    ZkSyncEraSepoliaLabel,
    ZkSyncEraSepoliaTransaction,
    ZkSyncEraTestnetBlock,
    ZkSyncEraTestnetLabel,
    ZkSyncEraTestnetTransaction,
    ZkSyncEraTransaction,
)


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    MUMBAI = "mumbai"
    XDAI = "xdai"
    WYRM = "wyrm"
    ZKSYNC_ERA = "zksync_era"
    ZKSYNC_ERA_TESTNET = "zksync_era_testnet"
    ZKSYNC_ERA_SEPOLIA = "zksync_era_sepolia"
    ARBITRUM_NOVA = "arbitrum_nova"
    ARBITRUM_SEPOLIA = "arbitrum_sepolia"
    XAI = "xai"
    AVALANCHE = "avalanche"
    AVALANCHE_FUJI = "avalanche_fuji"


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
        ZkSyncEraSepoliaBlock,
        ArbitrumNovaBlock,
        ArbitrumSepoliaBlock,
        XaiBlock,
        AvalancheBlock,
        AvalancheFujiBlock,
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm, ZkSyncEra, ZkSyncEraTestnet, ArbitrumNovaBlock, ArbitrumSepoliaBlock, XaiBlock
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
            ZkSyncEraSepoliaBlock,
            ArbitrumNovaBlock,
            ArbitrumSepoliaBlock,
            XaiBlock,
            AvalancheBlock,
            AvalancheFujiBlock,
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
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
        block_model = ZkSyncEraSepoliaBlock
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        block_model = ArbitrumNovaBlock
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        block_model = ArbitrumSepoliaBlock
    elif blockchain_type == AvailableBlockchainType.XAI:
        block_model = XaiBlock
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        block_model = AvalancheBlock
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        block_model = AvalancheFujiBlock
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
        ZkSyncEraSepoliaLabel,
        ArbitrumNovaLabel,
        ArbitrumSepoliaLabel,
        XaiLabel,
        AvalancheLabel,
        AvalancheFujiLabel,
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm, ZkSyncEra, ZkSyncEraTestnet, ArbitrumNovaLabel, ArbitrumSepoliaLabel, XaiLabel
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
            ZkSyncEraSepoliaLabel,
            ArbitrumNovaLabel,
            ArbitrumSepoliaLabel,
            XaiLabel,
            AvalancheLabel,
            AvalancheFujiLabel,
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
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
        label_model = ZkSyncEraSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        label_model = ArbitrumNovaLabel
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        label_model = ArbitrumSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.XAI:
        label_model = XaiLabel
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        label_model = AvalancheLabel
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        label_model = AvalancheFujiLabel

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
        ZkSyncEraSepoliaTransaction,
        ArbitrumNovaTransaction,
        ArbitrumSepoliaTransaction,
        XaiTransaction,
        AvalancheTransaction,
        AvalancheFujiTransaction,
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm, ZkSyncEra, ZkSyncEraTestnet, ArbitrumNovaTransaction, ArbitrumSepoliaTransaction, XaiTransaction
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
            ZkSyncEraSepoliaTransaction,
            ArbitrumNovaTransaction,
            ArbitrumSepoliaTransaction,
            XaiTransaction,
            AvalancheTransaction,
            AvalancheFujiTransaction,
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
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
        transaction_model = ZkSyncEraSepoliaTransaction
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        transaction_model = ArbitrumNovaTransaction
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        transaction_model = ArbitrumSepoliaTransaction
    elif blockchain_type == AvailableBlockchainType.XAI:
        transaction_model = XaiTransaction
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        transaction_model = AvalancheTransaction
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        transaction_model = AvalancheFujiTransaction
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
