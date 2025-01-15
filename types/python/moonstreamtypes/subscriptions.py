from enum import Enum

from .blockchain import AvailableBlockchainType


class SubscriptionTypes(Enum):
    ETHEREUM_BLOCKCHAIN = "ethereum_smartcontract"
    SEPOLIA_BLOCKCHAIN = "sepolia_smartcontract"
    POLYGON_BLOCKCHAIN = "polygon_smartcontract"
    MUMBAI_BLOCKCHAIN = "mumbai_smartcontract"
    AMOY_BLOCKCHAIN = "amoy_smartcontract"
    XDAI_BLOCKCHAIN = "xdai_smartcontract"
    WYRM_BLOCKCHAIN = "wyrm_smartcontract"
    ZKSYNC_ERA_TESTNET_BLOCKCHAIN = "zksync_era_testnet_smartcontract"
    ZKSYNC_ERA_BLOCKCHAIN = "zksync_era_smartcontract"
    ZKSYNC_ERA_SEPOLIA_BLOCKCHAIN = "zksync_era_sepolia_smartcontract"
    BASE_BLOCKCHAIN = "base_smartcontract"
    ARBITRUM_ONE_BLOCKCHAIN = "arbitrum_one_smartcontract"
    ARBITRUM_NOVA_BLOCKCHAIN = "arbitrum_nova_smartcontract"
    ARBITRUM_SEPOLIA_BLOCKCHAIN = "arbitrum_sepolia_smartcontract"
    GAME7_ORBIT_ARBITRUM_SEPOLIA_BLOCKCHAIN = (
        "game7_orbit_arbitrum_sepolia_smartcontract"
    )
    GAME7_TESTNET_BLOCKCHAIN = "game7_testnet_smartcontract"
    GAME7_BLOCKCHAIN = "game7_smartcontract"
    XAI_BLOCKCHAIN = "xai_smartcontract"
    XAI_SEPOLIA_BLOCKCHAIN = "xai_sepolia_smartcontract"
    AVALANCHE_BLOCKCHAIN = "avalanche_smartcontract"
    AVALANCHE_FUJI_BLOCKCHAIN = "avalanche_fuji_smartcontract"
    BLAST_BLOCKCHAIN = "blast_smartcontract"
    BLAST_SEPOLIA_BLOCKCHAIN = "blast_sepolia_smartcontract"
    PROOFOFPLAY_APEX_BLOCKCHAIN = "proofofplay_apex_smartcontract"
    STARKNET_BLOCKCHAIN = "starknet_smartcontract"
    STARKNET_SEPOLIA_BLOCKCHAIN = "starknet_sepolia_smartcontract"
    MANTLE_BLOCKCHAIN = "mantle_smartcontract"
    MANTLE_SEPOLIA_BLOCKCHAIN = "mantle_sepolia_smartcontract"
    IMX_ZKEVM_BLOCKCHAIN = "imx_zkevm_smartcontract"
    IMX_ZKEVM_SEPOLIA_BLOCKCHAIN = "imx_zkevm_sepolia_smartcontract"
    B3_BLOCKCHAIN = "b3_smartcontract"
    B3_SEPOLIA_BLOCKCHAIN = "b3_sepolia_smartcontract"
    RONIN_BLOCKCHAIN = "ronin_smartcontract"
    RONIN_SAIGON_BLOCKCHAIN = "ronin_saigon_smartcontract"

def blockchain_type_to_subscription_type(
    blockchain_type: AvailableBlockchainType,
) -> SubscriptionTypes:
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        return SubscriptionTypes.ETHEREUM_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.SEPOLIA:
        return SubscriptionTypes.SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        return SubscriptionTypes.POLYGON_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        return SubscriptionTypes.MUMBAI_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.AMOY:
        return SubscriptionTypes.AMOY_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.XDAI:
        return SubscriptionTypes.XDAI_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.WYRM:
        return SubscriptionTypes.WYRM_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_TESTNET:
        return SubscriptionTypes.ZKSYNC_ERA_TESTNET_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA:
        return SubscriptionTypes.ZKSYNC_ERA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ZKSYNC_ERA_SEPOLIA:
        return SubscriptionTypes.ZKSYNC_ERA_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.BASE:
        return SubscriptionTypes.BASE_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_ONE:
        return SubscriptionTypes.ARBITRUM_ONE_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        return SubscriptionTypes.ARBITRUM_NOVA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        return SubscriptionTypes.ARBITRUM_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.GAME7_ORBIT_ARBITRUM_SEPOLIA:
        return SubscriptionTypes.GAME7_ORBIT_ARBITRUM_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.GAME7_TESTNET:
        return SubscriptionTypes.GAME7_TESTNET_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.GAME7:
        return SubscriptionTypes.GAME7_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.XAI:
        return SubscriptionTypes.XAI_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.XAI_SEPOLIA:
        return SubscriptionTypes.XAI_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.AVALANCHE:
        return SubscriptionTypes.AVALANCHE_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.AVALANCHE_FUJI:
        return SubscriptionTypes.AVALANCHE_FUJI_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.BLAST:
        return SubscriptionTypes.BLAST_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.BLAST_SEPOLIA:
        return SubscriptionTypes.BLAST_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.PROOFOFPLAY_APEX:
        return SubscriptionTypes.PROOFOFPLAY_APEX_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.STARKNET:
        return SubscriptionTypes.STARKNET_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.STARKNET_SEPOLIA:
        return SubscriptionTypes.STARKNET_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.MANTLE:
        return SubscriptionTypes.MANTLE_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.MANTLE_SEPOLIA:
        return SubscriptionTypes.MANTLE_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM:
        return SubscriptionTypes.IMX_ZKEVM_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.IMX_ZKEVM_SEPOLIA:
        return SubscriptionTypes.IMX_ZKEVM_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.B3:
        return SubscriptionTypes.B3_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.B3_SEPOLIA:
        return SubscriptionTypes.B3_SEPOLIA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.RONIN:
        return SubscriptionTypes.RONIN_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.RONIN_SAIGON:
        return SubscriptionTypes.RONIN_SAIGON_BLOCKCHAIN
    else:
        raise ValueError(f"Unknown blockchain type: {blockchain_type}")


subscription_id_by_blockchain = {
    "ethereum": "ethereum_smartcontract",
    "sepolia": "sepolia_smartcontract",
    "polygon": "polygon_smartcontract",
    "mumbai": "mumbai_smartcontract",
    "amoy": "amoy_smartcontract",
    "xdai": "xdai_smartcontract",
    "wyrm": "wyrm_smartcontract",
    "zksync_era_testnet": "zksync_era_testnet_smartcontract",
    "zksync_era": "zksync_era_smartcontract",
    "zksync_era_sepolia": "zksync_era_sepolia_smartcontract",
    "base": "base_smartcontract",
    "arbitrum_one": "arbitrum_one_smartcontract",
    "arbitrum_nova": "arbitrum_nova_smartcontract",
    "arbitrum_sepolia": "arbitrum_sepolia_smartcontract",
    "game7_orbit_arbitrum_sepolia": "game7_orbit_arbitrum_sepolia_smartcontract",
    "game7_testnet": "game7_testnet_smartcontract",
    "game7": "game7_smartcontract",
    "xai": "xai_smartcontract",
    "xai_sepolia": "xai_sepolia_smartcontract",
    "avalanche": "avalanche_smartcontract",
    "avalanche_fuji": "avalanche_fuji_smartcontract",
    "blast": "blast_smartcontract",
    "blast_sepolia": "blast_sepolia_smartcontract",
    "proofofplay_apex": "proofofplay_apex_smartcontract",
    "starknet": "starknet_smartcontract",
    "starknet_sepolia": "starknet_sepolia_smartcontract",
    "mantle": "mantle_smartcontract",
    "mantle_sepolia": "mantle_sepolia_smartcontract",
    "imx_zkevm": "imx_zkevm_smartcontract",
    "imx_zkevm_sepolia": "imx_zkevm_sepolia_smartcontract",
    "b3": "b3_smartcontract",
    "b3_sepolia": "b3_sepolia_smartcontract",
    "ronin": "ronin_smartcontract",
    "ronin_saigon": "ronin_saigon_smartcontract",
}

blockchain_by_subscription_id = {
    "ethereum_blockchain": "ethereum",
    "sepolia_blockchain": "sepolia",
    "polygon_blockchain": "polygon",
    "mumbai_blockchain": "mumbai",
    "amoy_blockchain": "amoy",
    "xdai_blockchain": "xdai",
    "wyrm_blockchain": "wyrm",
    "zksync_era_testnet_blockchain": "zksync_era_testnet",
    "zksync_era_blockchain": "zksync_era",
    "zksync_era_sepolia_blockchain": "zksync_era_sepolia",
    "base_blockchain": "base",
    "arbitrum_one_blockchain": "arbitrum_one",
    "arbitrum_nova_blockchain": "arbitrum_nova",
    "arbitrum_sepolia_blockchain": "arbitrum_sepolia",
    "game7_orbit_arbitrum_sepolia_blockchain": "game7_orbit_arbitrum_sepolia",
    "game7_testnet_blockchain": "game7_testnet",
    "game7_blockchain": "game7",
    "xai_blockchain": "xai",
    "xai_sepolia_blockchain": "xai_sepolia",
    "avalanche_blockchain": "avalanche",
    "avalanche_fuji_blockchain": "avalanche_fuji",
    "blast_blockchain": "blast",
    "blast_sepolia_blockchain": "blast_sepolia",
    "proofofplay_apex_blockchain": "proofofplay_apex",
    "starknet_blockchain": "starknet",
    "starknet_sepolia_blockchain": "starknet_sepolia",
    "mantle_blockchain": "mantle",
    "mantle_sepolia_blockchain": "mantle_sepolia",
    "imx_zkevm_blockchain": "imx_zkevm",
    "imx_zkevm_sepolia_blockchain": "imx_zkevm_sepolia",
    "ethereum_smartcontract": "ethereum",
    "polygon_smartcontract": "polygon",
    "mumbai_smartcontract": "mumbai",
    "amoy_smartcontract": "amoy",
    "xdai_smartcontract": "xdai",
    "wyrm_smartcontract": "wyrm",
    "zksync_era_testnet_smartcontract": "zksync_era_testnet",
    "zksync_era_smartcontract": "zksync_era",
    "zksync_era_sepolia_smartcontract": "zksync_era_sepolia",
    "base_smartcontract": "base",
    "arbitrum_one_smartcontract": "arbitrum_one",
    "arbitrum_nova_smartcontract": "arbitrum_nova",
    "arbitrum_sepolia_smartcontract": "arbitrum_sepolia",
    "game7_orbit_arbitrum_sepolia_smartcontract": "game7_orbit_arbitrum_sepolia",
    "game7_testnet_smartcontract": "game7_testnet",
    "xai_smartcontract": "xai",
    "xai_sepolia_smartcontract": "xai_sepolia",
    "avalanche_smartcontract": "avalanche",
    "avalanche_fuji_smartcontract": "avalanche_fuji",
    "blast_smartcontract": "blast",
    "blast_sepolia_smartcontract": "blast_sepolia",
    "proofofplay_apex_smartcontract": "proofofplay_apex",
    "starknet_smartcontract": "starknet",
    "starknet_sepolia_smartcontract": "starknet_sepolia",
    "mantle_smartcontract": "mantle",
    "mantle_sepolia_smartcontract": "mantle_sepolia",
    "imx_zkevm_smartcontract": "imx_zkevm",
    "imx_zkevm_sepolia_smartcontract": "imx_zkevm_sepolia",
    "b3_smartcontract": "b3",
    "b3_sepolia_smartcontract": "b3_sepolia",
    "ronin_smartcontract": "ronin",
    "ronin_saigon_smartcontract": "ronin_saigon",
}
