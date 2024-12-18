from enum import Enum
from typing import Type, Union

from moonstreamdb.models import (
    AmoyBlock,
    AmoyLabel,
    AmoyTransaction,
    ArbitrumNovaBlock,
    ArbitrumNovaLabel,
    ArbitrumNovaTransaction,
    ArbitrumOneBlock,
    ArbitrumOneLabel,
    ArbitrumOneTransaction,
    ArbitrumSepoliaBlock,
    ArbitrumSepoliaLabel,
    ArbitrumSepoliaTransaction,
    AvalancheBlock,
    AvalancheFujiBlock,
    AvalancheFujiLabel,
    AvalancheFujiTransaction,
    AvalancheLabel,
    AvalancheTransaction,
    B3Block,
    B3SepoliaBlock,
    BlastBlock,
    BlastLabel,
    BlastSepoliaBlock,
    BlastSepoliaLabel,
    BlastSepoliaTransaction,
    BlastTransaction,
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    MantleBlock,
    MantleLabel,
    MantleSepoliaBlock,
    MantleSepoliaLabel,
    MantleSepoliaTransaction,
    MantleTransaction,
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
from moonstreamdbv3.models import AmoyLabel as AmoyLabelV3
from moonstreamdbv3.models import ArbitrumNovaLabel as ArbitrumNovaLabelV3
from moonstreamdbv3.models import ArbitrumOneLabel as ArbitrumOneLabelV3
from moonstreamdbv3.models import ArbitrumSepoliaLabel as ArbitrumSepoliaLabelV3
from moonstreamdbv3.models import AvalancheFujiLabel as AvalancheFujiLabelV3
from moonstreamdbv3.models import AvalancheLabel as AvalancheLabelV3
from moonstreamdbv3.models import BaseLabel as BaseLabelV3
from moonstreamdbv3.models import BlastLabel as BlastLabelV3
from moonstreamdbv3.models import BlastSepoliaLabel as BlastSepoliaLabelV3
from moonstreamdbv3.models import EthereumLabel as EthereumLabelV3
from moonstreamdbv3.models import (
    Game7OrbitArbitrumSepoliaLabel as Game7OrbitArbitrumSepoliaLabelV3,
)
from moonstreamdbv3.models import Game7Label as Game7LabelV3
from moonstreamdbv3.models import Game7TestnetLabel as Game7TestnetLabelV3
from moonstreamdbv3.models import ImxZkevmLabel as ImxZkevmLabelV3
from moonstreamdbv3.models import ImxZkevmSepoliaLabel as ImxZkevmSepoliaLabelV3
from moonstreamdbv3.models import MantleLabel as MantleLabelV3
from moonstreamdbv3.models import MantleSepoliaLabel as MantleSepoliaLabelV3
from moonstreamdbv3.models import MumbaiLabel as MumbaiLabelV3
from moonstreamdbv3.models import PolygonLabel as PolygonLabelV3
from moonstreamdbv3.models import ProofOfPlayApexLabel as ProofOfPlayApexLabelV3
from moonstreamdbv3.models import SepoliaLabel as SepoliaLabelV3
from moonstreamdbv3.models import StarknetLabel as StarknetLabelV3
from moonstreamdbv3.models import StarknetSepoliaLabel as StarknetSepoliaLabelV3
from moonstreamdbv3.models import XaiLabel as XaiLabelV3
from moonstreamdbv3.models import XaiSepoliaLabel as XaiSepoliaLabelV3
from moonstreamdbv3.models import XDaiLabel as XDaiLabelV3
from moonstreamdbv3.models import ZkSyncEraLabel as ZkSyncEraLabelV3
from moonstreamdbv3.models import ZkSyncEraSepoliaLabel as ZkSyncEraSepoliaLabelV3
from moonstreamdbv3.models import B3Label as B3LabelV3
from moonstreamdbv3.models import B3SepoliaLabel as B3SepoliaLabelV3
from moonstreamdbv3.models import RoninLabel as RoninLabelV3
from moonstreamdbv3.models import RoninSaigonLabel as RoninSaigonLabelV3

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
    GAME7_TESTNET = "game7_testnet"
    GAME7 = "game7"
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
    IMX_ZKEVM = "imx_zkevm"
    IMX_ZKEVM_SEPOLIA = "imx_zkevm_sepolia"
    B3 = "b3"
    B3_SEPOLIA = "b3_sepolia"
    RONIN = "ronin"
    RONIN_SAIGON = "ronin_saigon"


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
        MantleBlock,
        MantleSepoliaBlock,
        B3Block,
        B3SepoliaBlock,
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
            MantleBlock,
            MantleSepoliaBlock,
            B3Block,
            B3SepoliaBlock,
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
    elif blockchain_type == AvailableBlockchainType.MANTLE:
        block_model = MantleBlock
    elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
        block_model = MantleSepoliaBlock
    elif blockchain_type == AvailableBlockchainType.B3:
        block_model = B3Block
    elif blockchain_type == AvailableBlockchainType.B3_SEPOLIA:
        block_model = B3SepoliaBlock
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
        MantleLabel,
        MantleSepoliaLabel,
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
        Game7TestnetLabelV3,
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
        ImxZkevmLabelV3,
        ImxZkevmSepoliaLabelV3,
        B3LabelV3,
        B3SepoliaLabelV3,
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
            MantleLabel,
            MantleSepoliaLabel,
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
            Game7TestnetLabelV3,
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
            ImxZkevmLabelV3,
            ImxZkevmSepoliaLabelV3,
            B3LabelV3,
            B3SepoliaLabelV3,
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
        elif blockchain_type == AvailableBlockchainType.MANTLE:
            label_model = MantleLabel
        elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
            label_model = MantleSepoliaLabel
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
        elif blockchain_type == AvailableBlockchainType.GAME7_TESTNET:
            label_model = Game7TestnetLabelV3
        elif blockchain_type == AvailableBlockchainType.GAME7:
            label_model = Game7LabelV3
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
        elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM:
            label_model = ImxZkevmLabelV3
        elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM_SEPOLIA:
            label_model = ImxZkevmSepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.B3:
            label_model = B3LabelV3
        elif blockchain_type == AvailableBlockchainType.B3_SEPOLIA:
            label_model = B3SepoliaLabelV3
        elif blockchain_type == AvailableBlockchainType.RONIN:
            label_model = RoninLabelV3
        elif blockchain_type == AvailableBlockchainType.RONIN_SAIGON:
            label_model = RoninSaigonLabelV3
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
        MantleTransaction,
        MantleSepoliaTransaction,
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
            MantleTransaction,
            MantleSepoliaTransaction,
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
    elif blockchain_type == AvailableBlockchainType.MANTLE:
        transaction_model = MantleTransaction
    elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
        transaction_model = MantleSepoliaTransaction
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
