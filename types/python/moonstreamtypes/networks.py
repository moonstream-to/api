from enum import Enum
from typing import Dict, Union

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
from moonstreamdbv3.models import Game7TestnetLabel as Game7TestnetLabelV3
from moonstreamdbv3.models import Game7Label as Game7LabelV3
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

from .blockchain import AvailableBlockchainType


class Network(Enum):
    ethereum = "ethereum"
    sepolia = "sepolia"
    polygon = "polygon"
    mumbai = "mumbai"
    amoy = "amoy"
    xdai = "xdai"
    wyrm = "wyrm"
    zksync_era_testnet = "zksync_era_testnet"
    zksync_era = "zksync_era"
    zksync_era_sepolia = "zksync_era_sepolia"
    base = "base"
    arbitrum_one = "arbitrum_one"
    arbitrum_nova = "arbitrum_nova"
    arbitrum_sepolia = "arbitrum_sepolia"
    game7_orbit_arbitrum_sepolia = "game7_orbit_arbitrum_sepolia"
    game7_testnet = "game7_testnet"
    game7 = "game7"
    xai = "xai"
    xai_sepolia = "xai_sepolia"
    avalanche = "avalanche"
    avalanche_fuji = "avalanche_fuji"
    blast = "blast"
    blast_sepolia = "blast_sepolia"
    proofofplay_apex = "proofofplay_apex"
    starknet = "starknet"
    starknet_sepolia = "starknet_sepolia"
    mantle = "mantle"
    mantle_sepolia = "mantle_sepolia"
    imx_zkevm = "imx_zkevm"
    imx_zkevm_sepolia = "imx_zkevm_sepolia"
    b3 = "b3"
    b3_sepolia = "b3_sepolia"
    ronin = "ronin"
    ronin_saigon = "ronin_saigon"


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
    Network.arbitrum_one: {
        "blocks": ArbitrumOneBlock,
        "labels": ArbitrumOneLabel,
        "transactions": ArbitrumOneTransaction,
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
    Network.mantle: {
        "blocks": MantleBlock,
        "labels": MantleLabel,
        "transactions": MantleTransaction,
    },
    Network.mantle_sepolia: {
        "blocks": MantleSepoliaBlock,
        "labels": MantleSepoliaLabel,
        "transactions": MantleSepoliaTransaction,
    },
}

MODELS_V3: Dict[Network, Dict[str, Base]] = {
    Network.ethereum: {
        "labels": EthereumLabelV3,
    },
    Network.sepolia: {
        "labels": SepoliaLabelV3,
    },
    Network.polygon: {
        "labels": PolygonLabelV3,
    },
    Network.mumbai: {
        "labels": MumbaiLabelV3,
    },
    Network.amoy: {
        "labels": AmoyLabelV3,
    },
    Network.xdai: {
        "labels": XDaiLabelV3,
    },
    Network.zksync_era: {
        "labels": ZkSyncEraLabelV3,
    },
    Network.zksync_era_sepolia: {
        "labels": ZkSyncEraSepoliaLabelV3,
    },
    Network.base: {
        "labels": BaseLabelV3,
    },
    Network.arbitrum_nova: {
        "labels": ArbitrumNovaLabelV3,
    },
    Network.arbitrum_sepolia: {
        "labels": ArbitrumSepoliaLabelV3,
    },
    Network.arbitrum_one: {
        "labels": ArbitrumOneLabelV3,
    },
    Network.game7_orbit_arbitrum_sepolia: {
        "labels": Game7OrbitArbitrumSepoliaLabelV3,
    },
    Network.game7_testnet: {
        "labels": Game7TestnetLabelV3,
    },
    Network.game7: {
        "labels": Game7LabelV3,
    },
    Network.xai: {
        "labels": XaiLabelV3,
    },
    Network.xai_sepolia: {
        "labels": XaiSepoliaLabelV3,
    },
    Network.avalanche: {
        "labels": AvalancheLabelV3,
    },
    Network.avalanche_fuji: {
        "labels": AvalancheFujiLabelV3,
    },
    Network.blast: {
        "labels": BlastLabelV3,
    },
    Network.blast_sepolia: {
        "labels": BlastSepoliaLabelV3,
    },
    Network.proofofplay_apex: {
        "labels": ProofOfPlayApexLabelV3,
    },
    Network.starknet: {
        "labels": StarknetLabelV3,
    },
    Network.starknet_sepolia: {
        "labels": StarknetSepoliaLabelV3,
    },
    Network.mantle: {
        "labels": MantleLabelV3,
    },
    Network.mantle_sepolia: {
        "labels": MantleSepoliaLabelV3,
    },
    Network.imx_zkevm: {
        "labels": ImxZkevmLabelV3,
    },
    Network.imx_zkevm_sepolia: {
        "labels": ImxZkevmSepoliaLabelV3,
    },
    Network.b3: {
        "labels": B3LabelV3,
    },
    Network.b3_sepolia: {
        "labels": B3SepoliaLabelV3,
    },
    Network.ronin: {
        "labels": RoninLabelV3,
    },
    Network.ronin_saigon: {
        "labels": RoninSaigonLabelV3,
    },
}


## Used only in crawlers
def blockchain_type_to_network_type(
    blockchain_type: AvailableBlockchainType,
) -> Network:
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        return Network.ethereum
    elif blockchain_type == AvailableBlockchainType.SEPOLIA:
        return Network.sepolia
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
    elif blockchain_type == AvailableBlockchainType.BASE:
        return Network.base
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_ONE:
        return Network.arbitrum_one
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        return Network.arbitrum_nova
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        return Network.arbitrum_sepolia
    elif blockchain_type == AvailableBlockchainType.GAME7_ORBIT_ARBITRUM_SEPOLIA:
        return Network.game7_orbit_arbitrum_sepolia
    elif blockchain_type == AvailableBlockchainType.GAME7_TESTNET:
        return Network.game7_testnet
    elif blockchain_type == AvailableBlockchainType.GAME7:
        return Network.game7
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
    elif blockchain_type == AvailableBlockchainType.STARKNET:
        return Network.starknet
    elif blockchain_type == AvailableBlockchainType.STARKNET_SEPOLIA:
        return Network.starknet_sepolia
    elif blockchain_type == AvailableBlockchainType.MANTLE:
        return Network.mantle
    elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
        return Network.mantle_sepolia
    elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM:
        return Network.imx_zkevm
    elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM_SEPOLIA:
        return Network.imx_zkevm_sepolia
    elif blockchain_type == AvailableBlockchainType.B3:
        return Network.b3
    elif blockchain_type == AvailableBlockchainType.B3_SEPOLIA:
        return Network.b3_sepolia
    elif blockchain_type == AvailableBlockchainType.RONIN:
        return Network.ronin
    elif blockchain_type == AvailableBlockchainType.RONIN_SAIGON:
        return Network.ronin_saigon
    else:
        raise ValueError(f"Unknown blockchain type: {blockchain_type}")
