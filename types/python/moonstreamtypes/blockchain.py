from enum import Enum
from typing import Type, Union

from moonstreamdb.models import (
    AmoyBlock,
    AmoyLabel,
    AmoyTransaction,
    ArbitrumOneBlock,
    ArbitrumOneLabel,
    ArbitrumOneTransaction,
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

from moonstreamdbv3.models import (
    EthereumLabel as EthereumLabelV3,
    SepoliaLabel as SepoliaLabelV3,
    PolygonLabel as PolygonLabelV3,
    MumbaiLabel as MumbaiLabelV3,
    AmoyLabel as AmoyLabelV3,
    XDaiLabel as XDaiLabelV3,
    ZkSyncEraLabel as ZkSyncEraLabelV3,
    ZkSyncEraSepoliaLabel as ZkSyncEraSepoliaLabelV3,
    BaseLabel as BaseLabelV3,
    ArbitrumNovaLabel as ArbitrumNovaLabelV3,
    ArbitrumOneLabel as ArbitrumOneLabelV3,
    ArbitrumSepoliaLabel as ArbitrumSepoliaLabelV3,
    Game7OrbitArbitrumSepoliaLabel as Game7OrbitArbitrumSepoliaLabelV3,
    XaiLabel as XaiLabelV3,
    XaiSepoliaLabel as XaiSepoliaLabelV3,
    AvalancheLabel as AvalancheLabelV3,
    AvalancheFujiLabel as AvalancheFujiLabelV3,
    BlastLabel as BlastLabelV3,
    BlastSepoliaLabel as BlastSepoliaLabelV3,
    ProofOfPlayApexLabel as ProofOfPlayApexLabelV3,
    StarknetLabel as StarknetLabelV3,
    StarknetSepoliaLabel as StarknetSepoliaLabelV3,
    MantleLabel as MantleLabelV3,
    MantleSepoliaLabel as MantleSepoliaLabelV3,
)


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    SEPOLIA = "sepolia"
    POLYGON = "polygon"
    MUMBAI = "mumbai"
    AMOY = "amoy"
    XDAI = "xdai"
    WYRM = "wyrm"
    ZKSYNC_ERA = "zksync_era"
    ZKSYNC_ERA_TESTNET = "zksync_era_testnet"
    ZKSYNC_ERA_SEPOLIA = "zksync_era_sepolia"
    BASE = "base"
    ARBITRUM_ONE = "arbitrum_one"
    ARBITRUM_NOVA = "arbitrum_nova"
    ARBITRUM_SEPOLIA = "arbitrum_sepolia"
    GAME7_ORBIT_ARBITRUM_SEPOLIA = "game7_orbit_arbitrum_sepolia"
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


def get_block_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[
    Union[
        EthereumBlock,
        PolygonBlock,
        MumbaiBlock,
        AmoyBlock,
        XDaiBlock,
        WyrmBlock,
        ZkSyncEraTestnetBlock,
        ZkSyncEraBlock,
        ZkSyncEraSepoliaBlock,
        ArbitrumOneBlock,
        ArbitrumNovaBlock,
        ArbitrumSepoliaBlock,
        XaiBlock,
        XaiSepoliaBlock,
        AvalancheBlock,
        AvalancheFujiBlock,
        BlastBlock,
        BlastSepoliaBlock,
        ProofOfPlayApexBlock,
    ]
]:
    """
    Depends on provided blockchain type set proper blocks model.
    """
    block_model: Type[
        Union[
            EthereumBlock,
            PolygonBlock,
            MumbaiBlock,
            AmoyBlock,
            XDaiBlock,
            WyrmBlock,
            ZkSyncEraTestnetBlock,
            ZkSyncEraBlock,
            ZkSyncEraSepoliaBlock,
            ArbitrumOneBlock,
            ArbitrumNovaBlock,
            ArbitrumSepoliaBlock,
            XaiBlock,
            XaiSepoliaBlock,
            AvalancheBlock,
            AvalancheFujiBlock,
            BlastBlock,
            BlastSepoliaBlock,
            ProofOfPlayApexBlock,
        ]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        block_model = EthereumBlock
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        block_model = PolygonBlock
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        block_model = MumbaiBlock
    elif blockchain_type == AvailableBlockchainType.AMOY:
        block_model = AmoyBlock
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
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_ONE:
        block_model = ArbitrumOneBlock
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        block_model = ArbitrumNovaBlock
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        block_model = ArbitrumSepoliaBlock
    elif blockchain_type == AvailableBlockchainType.XAI:
        block_model = XaiBlock
    elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
        block_model = XaiSepoliaBlock
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        block_model = AvalancheBlock
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        block_model = AvalancheFujiBlock
    elif blockchain_type == AvailableBlockchainType.BLAST:
        block_model = BlastBlock
    elif blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA:
        block_model = BlastSepoliaBlock
    elif blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX:
        block_model = ProofOfPlayApexBlock
    else:
        raise Exception("Unsupported blockchain type provided")

    return block_model


def get_label_model(
    blockchain_type: AvailableBlockchainType,
    version: int = 2,
) -> Type[
    Union[
        EthereumLabel,
        PolygonLabel,
        MumbaiLabel,
        AmoyLabel,
        XDaiLabel,
        WyrmLabel,
        ZkSyncEraTestnetLabel,
        ZkSyncEraLabel,
        ZkSyncEraSepoliaLabel,
        ArbitrumOneLabel,
        ArbitrumNovaLabel,
        ArbitrumSepoliaLabel,
        XaiLabel,
        XaiSepoliaLabel,
        AvalancheLabel,
        AvalancheFujiLabel,
        BlastLabel,
        BlastSepoliaLabel,
        ProofOfPlayApexLabel,
        EthereumLabelV3,
        SepoliaLabelV3,
        PolygonLabelV3,
        MumbaiLabelV3,
        AmoyLabelV3,
        XDaiLabelV3,
        ZkSyncEraLabelV3,
        ZkSyncEraSepoliaLabelV3,
        BaseLabelV3,
        ArbitrumNovaLabelV3,
        ArbitrumOneLabelV3,
        ArbitrumSepoliaLabelV3,
        Game7OrbitArbitrumSepoliaLabelV3,
        XaiLabelV3,
        XaiSepoliaLabelV3,
        AvalancheLabelV3,
        AvalancheFujiLabelV3,
        BlastLabelV3,
        BlastSepoliaLabelV3,
        ProofOfPlayApexLabelV3,
        StarknetLabelV3,
        StarknetSepoliaLabelV3,
        MantleLabelV3,
        MantleSepoliaLabelV3,
    ]
]:
    """
    Depends on provided blockchain type set proper block label model.

    Available versions:
        - 2 -> moonstreamdb
        - 3 -> moonstreamdb-v3
    """
    label_model: Type[
        Union[
            EthereumLabel,
            PolygonLabel,
            MumbaiLabel,
            AmoyLabel,
            XDaiLabel,
            WyrmLabel,
            ZkSyncEraTestnetLabel,
            ZkSyncEraLabel,
            ZkSyncEraSepoliaLabel,
            ArbitrumOneLabel,
            ArbitrumNovaLabel,
            ArbitrumSepoliaLabel,
            XaiLabel,
            XaiSepoliaLabel,
            AvalancheLabel,
            AvalancheFujiLabel,
            BlastLabel,
            BlastSepoliaLabel,
            ProofOfPlayApexLabel,
            EthereumLabelV3,
            SepoliaLabelV3,
            PolygonLabelV3,
            MumbaiLabelV3,
            AmoyLabelV3,
            XDaiLabelV3,
            ZkSyncEraLabelV3,
            ZkSyncEraSepoliaLabelV3,
            BaseLabelV3,
            ArbitrumNovaLabelV3,
            ArbitrumOneLabelV3,
            ArbitrumSepoliaLabelV3,
            Game7OrbitArbitrumSepoliaLabelV3,
            XaiLabelV3,
            XaiSepoliaLabelV3,
            AvalancheLabelV3,
            AvalancheFujiLabelV3,
            BlastLabelV3,
            BlastSepoliaLabelV3,
            ProofOfPlayApexLabelV3,
            StarknetLabelV3,
            StarknetSepoliaLabelV3,
            MantleLabelV3,
            MantleSepoliaLabelV3,
        ]
    ]
    if version == 2:
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
        elif blockchain_type == AvailableBlockchainType.WYRM:
            label_model = WyrmLabel
        elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
            label_model = ZkSyncEraTestnetLabel
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
        else:
            raise Exception("Unsupported blockchain type provided")
    elif version == 3:
        if blockchain_type == AvailableBlockchainType.ETHEREUM:
            label_model = EthereumLabelV3
        elif blockchain_type == AvailableBlockchainType.SEPOLIA:
            label_model = SepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.POLYGON:
            label_model = PolygonLabelV3
        elif blockchain_type == AvailableBlockchainType.MUMBAI:
            label_model = MumbaiLabelV3
        elif blockchain_type == AvailableBlockchainType.AMOY:
            label_model = AmoyLabelV3
        elif blockchain_type == AvailableBlockchainType.XDAI:
            label_model = XDaiLabelV3
        elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
            label_model = ZkSyncEraLabelV3
        elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
            label_model = ZkSyncEraSepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.BASE:
            label_model = BaseLabelV3
        elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
            label_model = ArbitrumNovaLabelV3
        elif blockchain_type == AvailableBlockchainType.ARBITRUM_ONE:
            label_model = ArbitrumOneLabelV3
        elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
            label_model = ArbitrumSepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.GAME7_ORBIT_ARBITRUM_SEPOLIA:
            label_model = Game7OrbitArbitrumSepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.XAI:
            label_model = XaiLabelV3
        elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
            label_model = XaiSepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.AVALANCHE:
            label_model = AvalancheLabelV3
        elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
            label_model = AvalancheFujiLabelV3
        elif blockchain_type == AvailableBlockchainType.BLAST:
            label_model = BlastLabelV3
        elif blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA:
            label_model = BlastSepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX:
            label_model = ProofOfPlayApexLabelV3
        elif blockchain_type == AvailableBlockchainType.STARKNET:
            label_model = StarknetLabelV3
        elif blockchain_type == AvailableBlockchainType.STARKNET_SEPOLIA:
            label_model = StarknetSepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.MANTLE:
            label_model = MantleLabelV3
        elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
            label_model = MantleSepoliaLabelV3
        else:
            raise Exception("Unsupported blockchain type provided")
    else:
        raise Exception("Not existing version of moonstream database")
    return label_model


def get_transaction_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[
    Union[
        EthereumTransaction,
        PolygonTransaction,
        MumbaiTransaction,
        AmoyTransaction,
        XDaiTransaction,
        WyrmTransaction,
        ZkSyncEraTestnetTransaction,
        ZkSyncEraTransaction,
        ZkSyncEraSepoliaTransaction,
        ArbitrumOneTransaction,
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
]:
    """
    Depends on provided blockchain type set proper block transactions model.
    """
    transaction_model: Type[
        Union[
            EthereumTransaction,
            PolygonTransaction,
            MumbaiTransaction,
            AmoyTransaction,
            XDaiTransaction,
            WyrmTransaction,
            ZkSyncEraTestnetTransaction,
            ZkSyncEraTransaction,
            ZkSyncEraSepoliaTransaction,
            ArbitrumOneTransaction,
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
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        transaction_model = EthereumTransaction
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        transaction_model = PolygonTransaction
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        transaction_model = MumbaiTransaction
    elif blockchain_type == AvailableBlockchainType.AMOY:
        transaction_model = AmoyTransaction
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
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_ONE:
        transaction_model = ArbitrumOneTransaction
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        transaction_model = ArbitrumNovaTransaction
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        transaction_model = ArbitrumSepoliaTransaction
    elif blockchain_type == AvailableBlockchainType.XAI:
        transaction_model = XaiTransaction
    elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
        transaction_model = XaiSepoliaTransaction
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        transaction_model = AvalancheTransaction
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        transaction_model = AvalancheFujiTransaction
    elif blockchain_type == AvailableBlockchainType.BLAST:
        transaction_model = BlastTransaction
    elif blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA:
        transaction_model = BlastSepoliaTransaction
    elif blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX:
        transaction_model = ProofOfPlayApexTransaction
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
