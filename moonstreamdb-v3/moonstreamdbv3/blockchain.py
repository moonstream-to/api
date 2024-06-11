from enum import Enum
from typing import Type, Union


from .models import (
    EthereumLabel,
    SepoliaLabel,
    PolygonLabel,
    MumbaiLabel,
    AmoyLabel,
    XDaiLabel,
    ZkSyncEraLabel,
    ZkSyncEraSepoliaLabel,
    BaseLabel,
    ArbitrumNovaLabel,
    ArbitrumOneLabel,
    ArbitrumSepoliaLabel,
    Game7OrbitArbitrumSepoliaLabel,
    XaiLabel,
    XaiSepoliaLabel,
    AvalancheLabel,
    AvalancheFujiLabel,
    BlastLabel,
    BlastSepoliaLabel,
    ProofOfPlayApexLabel,
    StarknetLabel,
    StarknetSepoliaLabel,
    MantleLabel,
    MantleSepoliaLabel,
)


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    MUMBAI = "mumbai"
    AMOY = "amoy"
    XDAI = "xdai"
    ZKSYNC_ERA = "zksync_era"
    ZKSYNC_ERA_TESTNET = "zksync_era_testnet"
    ZKSYNC_ERA_SEPOLIA = "zksync_era_sepolia"
    ARBITRUM_ONE = "arbitrum_one"
    ARBITRUM_NOVA = "arbitrum_nova"
    ARBITRUM_SEPOLIA = "arbitrum_sepolia"
    XAI = "xai"
    XAI_SEPOLIA = "xai_sepolia"
    AVALANCHE = "avalanche"
    AVALANCHE_FUJI = "avalanche_fuji"
    BLAST = "blast"
    BLAST_SEPOLIA = "blast_sepolia"
    PROOFOFPLAY_APEX = "proofofplay_apex"
    STARKNET = "starknet"
    STARKNET_SEPOLIA = "starknet_sepolia"
    MANTLE = "mantle"
    MANTLE_SEPOLIA = "mantle_sepolia"
    GAME7_ORBIT_ARBITRUM_SEPOLIA = "game7_orbit_arbitrum_sepolia"


def get_label_model(blockchain_type: AvailableBlockchainType) -> Type[
    Union[
        EthereumLabel,
        SepoliaLabel,
        PolygonLabel,
        MumbaiLabel,
        AmoyLabel,
        XDaiLabel,
        ZkSyncEraLabel,
        ZkSyncEraSepoliaLabel,
        BaseLabel,
        ArbitrumNovaLabel,
        ArbitrumOneLabel,
        ArbitrumSepoliaLabel,
        Game7OrbitArbitrumSepoliaLabel,
        XaiLabel,
        XaiSepoliaLabel,
        AvalancheLabel,
        AvalancheFujiLabel,
        BlastLabel,
        BlastSepoliaLabel,
        ProofOfPlayApexLabel,
        StarknetLabel,
        StarknetSepoliaLabel,
        MantleLabel,
        MantleSepoliaLabel,
    ]
]:
    """
    Depends on provided blockchain type set proper blocks model.
    """

    label_model: Type[
        Union[
            EthereumLabel,
            SepoliaLabel,
            PolygonLabel,
            MumbaiLabel,
            AmoyLabel,
            XDaiLabel,
            ZkSyncEraLabel,
            ZkSyncEraSepoliaLabel,
            BaseLabel,
            ArbitrumNovaLabel,
            ArbitrumOneLabel,
            ArbitrumSepoliaLabel,
            Game7OrbitArbitrumSepoliaLabel,
            XaiLabel,
            XaiSepoliaLabel,
            AvalancheLabel,
            AvalancheFujiLabel,
            BlastLabel,
            BlastSepoliaLabel,
            ProofOfPlayApexLabel,
            StarknetLabel,
            StarknetSepoliaLabel,
            MantleLabel,
            MantleSepoliaLabel,
        ]
    ]

    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        label_model = EthereumLabel
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        label_model = PolygonLabel
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        label_model = MumbaiLabel
    elif blockchain_type == AvailableBlockchainType.AMOY:
        label_model = AmoyLabel
    elif blockchain_type == AvailableBlockchainType.XDAI:
        label_model = XDaiLabel
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
        label_model = ZkSyncEraLabel
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
        label_model = ZkSyncEraSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_ONE:
        label_model = ArbitrumOneLabel
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        label_model = ArbitrumNovaLabel
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        label_model = ArbitrumSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.XAI:
        label_model = XaiLabel
    elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
        label_model = XaiSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        label_model = AvalancheLabel
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        label_model = AvalancheFujiLabel
    elif blockchain_type == AvailableBlockchainType.BLAST:
        label_model = BlastLabel
    elif blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA:
        label_model = BlastSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX:
        label_model = ProofOfPlayApexLabel
    elif blockchain_type == AvailableBlockchainType.STARKNET:
        label_model = StarknetLabel
    elif blockchain_type == AvailableBlockchainType.STARKNET_SEPOLIA:
        label_model = StarknetSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.MANTLE:
        label_model = MantleLabel
    elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
        label_model = MantleSepoliaLabel
    elif blockchain_type == AvailableBlockchainType.GAME7_ORBIT_ARBITRUM_SEPOLIA:
        label_model = Game7OrbitArbitrumSepoliaLabel
    else:
        raise ValueError(f"Unknown blockchain type: {blockchain_type}")

    return label_model
