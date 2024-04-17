from enum import Enum
from typing import Dict, Union

from .blockchain import AvailableBlockchainType
from .models import (
    AmoyBlock,
    AmoyLabel,
    AmoyTransaction,
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
    BlastBlock,
    BlastLabel,
    BlastSepoliaBlock,
    BlastSepoliaLabel,
    BlastSepoliaTransaction,
    BlastTransaction,
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    MumbaiBlock,
    MumbaiLabel,
    MumbaiTransaction,
    PolygonBlock,
    PolygonLabel,
    PolygonTransaction,
    ProofOfPlayApexBlock,
    ProofOfPlayApexLabel,
    ProofOfPlayApexTransaction,
    WyrmBlock,
    WyrmLabel,
    WyrmTransaction,
    XaiBlock,
    XaiLabel,
    XaiSepoliaBlock,
    XaiSepoliaLabel,
    XaiSepoliaTransaction,
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
    amoy = "amoy"
    xdai = "xdai"
    wyrm = "wyrm"
    zksync_era_testnet = "zksync_era_testnet"
    zksync_era = "zksync_era"
    zksync_era_sepolia = "zksync_era_sepolia"
    arbitrum_nova = "arbitrum_nova"
    arbitrum_sepolia = "arbitrum_sepolia"
    xai = "xai"
    xai_sepolia = "xai_sepolia"
    avalanche = "avalanche"
    avalanche_fuji = "avalanche_fuji"
    blast = "blast"
    blast_sepolia = "blast_sepolia"
    proofofplay_apex = "proofofplay_apex"


tx_raw_types = Union[
    EthereumTransaction,
    MumbaiTransaction,
    AmoyTransaction,
    PolygonTransaction,
    WyrmTransaction,
    XDaiTransaction,
    ZkSyncEraTestnetTransaction,
    ZkSyncEraTransaction,
    ZkSyncEraSepoliaTransaction,
    ArbitrumNovaTransaction,
    ArbitrumSepoliaTransaction,
    XaiTransaction,
    XaiSepoliaTransaction,
    AvalancheTransaction,
    AvalancheFujiTransaction,
    BlastTransaction,
    BlastSepoliaTransaction,
    ProofOfPlayApexTransaction,
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
    Network.amoy: {
        "blocks": AmoyBlock,
        "labels": AmoyLabel,
        "transactions": AmoyTransaction,
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
    Network.xai_sepolia: {
        "blocks": XaiSepoliaBlock,
        "labels": XaiSepoliaLabel,
        "transactions": XaiSepoliaTransaction,
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
    Network.blast: {
        "blocks": BlastBlock,
        "labels": BlastLabel,
        "transactions": BlastTransaction,
    },
    Network.blast_sepolia: {
        "blocks": BlastSepoliaBlock,
        "labels": BlastSepoliaLabel,
        "transactions": BlastSepoliaTransaction,
    },
    Network.proofofplay_apex: {
        "blocks": ProofOfPlayApexBlock,
        "labels": ProofOfPlayApexLabel,
        "transactions": ProofOfPlayApexTransaction,
    },
}


def blockchain_type_to_network_type(
    blockchain_type: AvailableBlockchainType,
) -> Network:
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        return Network.ethereum
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        return Network.polygon
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        return Network.mumbai
    elif blockchain_type == AvailableBlockchainType.AMOY:
        return Network.amoy
    elif blockchain_type == AvailableBlockchainType.XDAI:
        return Network.xdai
    elif blockchain_type == AvailableBlockchainType.WYRM:
        return Network.wyrm
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
        return Network.zksync_era_testnet
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
        return Network.zksync_era
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
        return Network.zksync_era_sepolia
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        return Network.arbitrum_nova
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        return Network.arbitrum_sepolia
    elif blockchain_type == AvailableBlockchainType.XAI:
        return Network.xai
    elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
        return Network.xai_sepolia
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        return Network.avalanche
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        return Network.avalanche_fuji
    elif blockchain_type == AvailableBlockchainType.BLAST:
        return Network.blast
    elif blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA:
        return Network.blast_sepolia
    elif blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX:
        return Network.proofofplay_apex
    else:
        raise ValueError(f"Unknown blockchain type: {blockchain_type}")
