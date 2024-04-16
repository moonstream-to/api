from enum import Enum

from .blockchain import AvailableBlockchainType


class SubscriptionTypes(Enum):
    POLYGON_BLOCKCHAIN = "polygon_smartcontract"
    ETHEREUM_BLOCKCHAIN = "ethereum_smartcontract"
    MUMBAI_BLOCKCHAIN = "mumbai_smartcontract"
    AMOY_BLOCKCHAIN = "amoy_smartcontract"
    XDAI_BLOCKCHAIN = "xdai_smartcontract"
    WYRM_BLOCKCHAIN = "wyrm_smartcontract"
    ZKSYNC_ERA_TESTNET_BLOCKCHAIN = "zksync_era_testnet_smartcontract"
    ZKSYNC_ERA_BLOCKCHAIN = "zksync_era_smartcontract"
    ZKSYNC_ERA_SEPOLIA_BLOCKCHAIN = "zksync_era_sepolia_smartcontract"
    ARBITRUM_NOVA_BLOCKCHAIN = "arbitrum_nova_smartcontract"
    ARBITRUM_SEPOLIA_BLOCKCHAIN = "arbitrum_sepolia_smartcontract"
    XAI_BLOCKCHAIN = "xai_smartcontract"
    XAI_SEPOLIA_BLOCKCHAIN = "xai_sepolia_smartcontract"
    AVALANCHE_BLOCKCHAIN = "avalanche_smartcontract"
    AVALANCHE_FUJI_BLOCKCHAIN = "avalanche_fuji_smartcontract"
    BLAST_BLOCKCHAIN = "blast_smartcontract"
    BLAST_SEPOLIA_BLOCKCHAIN = "blast_sepolia_smartcontract"
    PROOFOFPLAY_APEX_BLOCKCHAIN = "proofofplay_apex_smartcontract"


def blockchain_type_to_subscription_type(
    blockchain_type: AvailableBlockchainType,
) -> SubscriptionTypes:
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        return SubscriptionTypes.ETHEREUM_BLOCKCHAIN
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
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_NOVA:
        return SubscriptionTypes.ARBITRUM_NOVA_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.ARBITRUM_SEPOLIA:
        return SubscriptionTypes.ARBITRUM_SEPOLIA_BLOCKCHAIN
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
    else:
        raise ValueError(f"Unknown blockchain type: {blockchain_type}")


subscription_id_by_blockchain = {
    "ethereum": "ethereum_smartcontract",
    "polygon": "polygon_smartcontract",
    "mumbai": "mumbai_smartcontract",
    "amoy": "amoy_smartcontract",
    "xdai": "xdai_smartcontract",
    "wyrm": "wyrm_smartcontract",
    "zksync_era_testnet": "zksync_era_testnet_smartcontract",
    "zksync_era": "zksync_era_smartcontract",
    "zksync_era_sepolia": "zksync_era_sepolia_smartcontract",
    "arbitrum_nova": "arbitrum_nova_smartcontract",
    "arbitrum_sepolia": "arbitrum_sepolia_smartcontract",
    "xai": "xai_smartcontract",
    "xai_sepolia": "xai_sepolia_smartcontract",
    "avalanche": "avalanche_smartcontract",
    "avalanche_fuji": "avalanche_fuji_smartcontract",
    "blast": "blast_smartcontract",
    "blast_sepolia": "blast_sepolia_smartcontract",
    "proofofplay_apex": "proofofplay_apex_smartcontract",
}

blockchain_by_subscription_id = {
    "ethereum_blockchain": "ethereum",
    "polygon_blockchain": "polygon",
    "mumbai_blockchain": "mumbai",
    "amoy_blockchain": "amoy",
    "xdai_blockchain": "xdai",
    "wyrm_blockchain": "wyrm",
    "zksync_era_testnet_blockchain": "zksync_era_testnet",
    "zksync_era_blockchain": "zksync_era",
    "zksync_era_sepolia_blockchain": "zksync_era_sepolia",
    "arbitrum_nova_blockchain": "arbitrum_nova",
    "arbitrum_sepolia_blockchain": "arbitrum_sepolia",
    "xai_blockchain": "xai",
    "xai_sepolia_blockchain": "xai_sepolia",
    "avalanche_blockchain": "avalanche",
    "avalanche_fuji_blockchain": "avalanche_fuji",
    "blast_blockchain": "blast",
    "blast_sepolia_blockchain": "blast_sepolia",
    "proofofplay_apex_blockchain": "proofofplay_apex",
    "ethereum_smartcontract": "ethereum",
    "polygon_smartcontract": "polygon",
    "mumbai_smartcontract": "mumbai",
    "amoy_smartcontract": "amoy",
    "xdai_smartcontract": "xdai",
    "wyrm_smartcontract": "wyrm",
    "zksync_era_testnet_smartcontract": "zksync_era_testnet",
    "zksync_era_smartcontract": "zksync_era",
    "zksync_era_sepolia_smartcontract": "zksync_era_sepolia",
    "arbitrum_nova_smartcontract": "arbitrum_nova",
    "arbitrum_sepolia_smartcontract": "arbitrum_sepolia",
    "xai_smartcontract": "xai",
    "xai_sepolia_smartcontract": "xai_sepolia",
    "avalanche_smartcontract": "avalanche",
    "avalanche_fuji_smartcontract": "avalanche_fuji",
    "blast_smartcontract": "blast",
    "blast_sepolia_smartcontract": "blast_sepolia",
    "proofofplay_apex_smartcontract": "proofofplay_apex",
}
