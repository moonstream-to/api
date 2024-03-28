from enum import Enum
from typing import Dict, Union

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
    Base,
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


class Network(Enum):
    ethereum = "ethereum"
    polygon = "polygon"
    mumbai = "mumbai"
    xdai = "xdai"
    wyrm = "wyrm"
    zksync_era_testnet = "zksync_era_testnet"
    zksync_era = "zksync_era"
    zksync_era_sepolia = "zksync_era_sepolia"
    arbitrum_nova = "arbitrum_nova"
    arbitrum_sepolia = "arbitrum_sepolia"
    xai = "xai"
    avalanche = "avalanche"
    avalanche_fuji = "avalanche_fuji"


tx_raw_types = Union[
    EthereumTransaction,
    MumbaiTransaction,
    PolygonTransaction,
    WyrmTransaction,
    XDaiTransaction,
    ZkSyncEraTestnetTransaction,
    ZkSyncEraTransaction,
    ZkSyncEraSepoliaTransaction,
    ArbitrumNovaTransaction,
    ArbitrumSepoliaTransaction,
    XaiTransaction,
    AvalancheTransaction,
    AvalancheFujiTransaction,
]

MODELS: Dict[Network, Dict[str, Base]] = {
    Network.ethereum: {
        "blocks": EthereumBlock,
        "labels": EthereumLabel,
        "transactions": EthereumTransaction,
    },
    Network.mumbai: {
        "blocks": MumbaiBlock,
        "labels": MumbaiLabel,
        "transactions": MumbaiTransaction,
    },
    Network.polygon: {
        "blocks": PolygonBlock,
        "labels": PolygonLabel,
        "transactions": PolygonTransaction,
    },
    Network.xdai: {
        "blocks": XDaiBlock,
        "labels": XDaiLabel,
        "transactions": XDaiTransaction,
    },
    Network.wyrm: {
        "blocks": WyrmBlock,
        "labels": WyrmLabel,
        "transactions": WyrmTransaction,
    },
    Network.zksync_era_testnet: {
        "blocks": ZkSyncEraTestnetBlock,
        "labels": ZkSyncEraTestnetLabel,
        "transactions": ZkSyncEraTestnetTransaction,
    },
    Network.zksync_era: {
        "blocks": ZkSyncEraSepoliaBlock,
        "labels": ZkSyncEraSepoliaLabel,
        "transactions": ZkSyncEraSepoliaTransaction,
    },
    Network.zksync_era_sepolia: {
        "blocks": ZkSyncEraBlock,
        "labels": ZkSyncEraLabel,
        "transactions": ZkSyncEraTransaction,
    },
    Network.arbitrum_nova: {
        "blocks": ArbitrumNovaBlock,
        "labels": ArbitrumNovaLabel,
        "transactions": ArbitrumNovaTransaction,
    },
    Network.arbitrum_sepolia: {
        "blocks": ArbitrumSepoliaBlock,
        "labels": ArbitrumSepoliaLabel,
        "transactions": ArbitrumSepoliaTransaction,
    },
    Network.xai: {
        "blocks": XaiBlock,
        "labels": XaiLabel,
        "transactions": XaiTransaction,
    },
    Network.avalanche: {
        "blocks": AvalancheBlock,
        "labels": AvalancheLabel,
        "transactions": AvalancheTransaction,
    },
    Network.avalanche_fuji: {
        "blocks": AvalancheFujiBlock,
        "labels": AvalancheFujiLabel,
        "transactions": AvalancheFujiTransaction,
    },
}
