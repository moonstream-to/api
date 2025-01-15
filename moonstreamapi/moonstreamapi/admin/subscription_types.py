"""
Utilities for managing subscription type resources for a Moonstream application.
"""

import argparse
import json
from typing import Dict, List, Optional

from bugout.data import BugoutResource, BugoutResources
from sqlalchemy.sql.expression import update

from ..data import SubscriptionTypeResourceData
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
)
from ..settings import bugout_client as bc

CANONICAL_SUBSCRIPTION_TYPES = {
    "ethereum_smartcontract": SubscriptionTypeResourceData(
        id="ethereum_smartcontract",
        name="Ethereum smartcontracts",
        blockchain="ethereum",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Ethereum blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-purple.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "sepolia_smartcontract": SubscriptionTypeResourceData(
        id="sepolia_smartcontract",
        name="Sepolia smartcontracts",
        blockchain="sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Sepolia blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-purple.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "polygon_smartcontract": SubscriptionTypeResourceData(
        id="polygon_smartcontract",
        name="Polygon smartcontracts",
        blockchain="polygon",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Polygon blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/matic-token-inverted-icon.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "proofofplay_apex_smartcontract": SubscriptionTypeResourceData(
        id="proofofplay_apex_smartcontract",
        name="Proof of Play Apex smartcontracts",
        blockchain="proofofplay_apex",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Proof of Play Apex blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-purple.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "mumbai_smartcontract": SubscriptionTypeResourceData(
        id="mumbai_smartcontract",
        name="Mumbai smartcontracts",
        blockchain="mumbai",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Mumbai blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/matic-token-inverted-icon.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "amoy_smartcontract": SubscriptionTypeResourceData(
        id="amoy_smartcontract",
        name="Amoy smartcontracts",
        blockchain="amoy",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Amoy blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/matic-token-inverted-icon.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "xdai_smartcontract": SubscriptionTypeResourceData(
        id="xdai_smartcontract",
        name="XDai smartcontract",
        blockchain="xdai",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of XDai blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/xdai-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "wyrm_smartcontract": SubscriptionTypeResourceData(
        id="wyrm_smartcontract",
        name="Wyrm smartcontract",
        blockchain="wyrm",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Wyrm blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/great-wyrm-network-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "zksync_era_smartcontract": SubscriptionTypeResourceData(
        id="zksync_era_smartcontract",
        name="zkSync Era smartcontract",
        blockchain="zksync_era",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of zkSync Era blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/zksync-era-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "zksync_era_testnet_smartcontract": SubscriptionTypeResourceData(
        id="zksync_era_testnet_smartcontract",
        name="zkSync Era testnet smartcontract",
        blockchain="zksync_era_testnet",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of zkSync Era testnet blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/zksync-era-testnet-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "zksync_era_sepolia_smartcontract": SubscriptionTypeResourceData(
        id="zksync_era_sepolia_smartcontract",
        name="zkSync Era Sepolia smartcontract",
        blockchain="zksync_era_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of zkSync Era Sepolia blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/zksync-era-testnet-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "arbitrum_one_smartcontract": SubscriptionTypeResourceData(
        id="arbitrum_one_smartcontract",
        name="Arbitrum One smartcontract",
        blockchain="arbitrum_one",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Arbitrum One blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/arbitrum-one-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "arbitrum_nova_smartcontract": SubscriptionTypeResourceData(
        id="arbitrum_nova_smartcontract",
        name="Arbitrum Nova smartcontract",
        blockchain="arbitrum_nova",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Arbitrum Nova blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/arbitrum-nova-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "arbitrum_sepolia_smartcontract": SubscriptionTypeResourceData(
        id="arbitrum_sepolia_smartcontract",
        name="Arbitrum Sepolia smartcontract",
        blockchain="arbitrum_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Arbitrum Sepolia blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/arbitrum-sepolia-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "xai_smartcontract": SubscriptionTypeResourceData(
        id="xai_smartcontract",
        name="Xai smartcontract",
        blockchain="xai",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Xai blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/xai-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "xai_sepolia_smartcontract": SubscriptionTypeResourceData(
        id="xai_sepolia_smartcontract",
        name="Xai Sepolia smartcontract",
        blockchain="xai_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Xai Sepolia blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/xai-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "avalanche_smartcontract": SubscriptionTypeResourceData(
        id="avalanche_smartcontract",
        name="Avalanche smartcontract",
        blockchain="avalanche",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Avalanche blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/avalanche-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "avalanche_fuji_smartcontract": SubscriptionTypeResourceData(
        id="avalanche_fuji_smartcontract",
        name="Avalanche Fuji smartcontract",
        blockchain="avalanche_fuji",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Avalanche Fuji blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/avalanche-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "blast_smartcontract": SubscriptionTypeResourceData(
        id="blast_smartcontract",
        name="Blast smartcontract",
        blockchain="blast",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Blast blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/blast-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "blast_sepolia_smartcontract": SubscriptionTypeResourceData(
        id="blast_sepolia_smartcontract",
        name="Blast Sepolia smartcontract",
        blockchain="blast_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Blast Sepolia blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/blast-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "mantle_smartcontract": SubscriptionTypeResourceData(
        id="mantle_smartcontract",
        name="Mantle smartcontract",
        blockchain="mantle",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Mantle blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/mantle-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "mantle_sepolia_smartcontract": SubscriptionTypeResourceData(
        id="mantle_sepolia_smartcontract",
        name="Mantle Sepolia smartcontract",
        blockchain="mantle_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Mantle Sepolia blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/mantle-sepolia-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "imx_zkevm_smartcontract": SubscriptionTypeResourceData(
        id="imx_zkevm_smartcontract",
        name="Immutable zkEvm smartcontracts",
        blockchain="imx_zkevm",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Immutable zkEvm blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/immutable-zkevm-icon-grey.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "imx_zkevm_sepolia_smartcontract": SubscriptionTypeResourceData(
        id="imx_zkevm_sepolia_smartcontract",
        name="Immutable zkEvm Sepolia smartcontracts",
        blockchain="imx_zkevm_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Immutable zkEvm Sepolia blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/immutable-zkevm-icon-grey.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "game7_smartcontract": SubscriptionTypeResourceData(
        id="game7_smartcontract",
        name="Game7 smartcontracts",
        blockchain="game7",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Game7 blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/game7-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "game7_testnet_smartcontract": SubscriptionTypeResourceData(
        id="game7_testnet_smartcontract",
        name="Game7 Testnet smartcontracts",
        blockchain="game7_testnet",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of Game7 testnet blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/game7-testnet-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "b3_smartcontract": SubscriptionTypeResourceData(
        id="b3_smartcontract",
        name="B3 smartcontracts",
        blockchain="b3",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of B3 blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/b3-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "b3_sepolia_smartcontract": SubscriptionTypeResourceData(
        id="b3_sepolia_smartcontract",
        name="B3 Sepolia smartcontracts",
        blockchain="b3_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Contracts events and tx_calls of contract of B3 Sepolia blockchain.",
        icon_url="https://static.simiotics.com/moonstream/assets/b3-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "ethereum_blockchain": SubscriptionTypeResourceData(
        id="ethereum_blockchain",
        name="Ethereum transactions",
        blockchain="ethereum",
        choices=["input:address", "tag:erc721"],
        description="Transactions that have been mined into the Ethereum blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-purple.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "polygon_blockchain": SubscriptionTypeResourceData(
        id="polygon_blockchain",
        name="Polygon transactions",
        blockchain="polygon",
        choices=["input:address", "tag:erc721"],
        description="Transactions that have been mined into the Polygon blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/matic-token-inverted-icon.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "proofofplay_apex_blockchain": SubscriptionTypeResourceData(
        id="proofofplay_apex_blockchain",
        name="Proof of Play Apex transactions",
        blockchain="proofofplay_apex",
        choices=["input:address", "tag:erc721"],
        description="Transactions that have been mined into the Proof of Play Apex blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-purple.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "mumbai_blockchain": SubscriptionTypeResourceData(
        id="mumbai_blockchain",
        name="Mumbai transactions",
        blockchain="mumbai",
        choices=["input:address", "tag:erc721"],
        description="Transactions that have been mined into the Mumbai blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/matic-token-inverted-icon.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "amoy_blockchain": SubscriptionTypeResourceData(
        id="amoy_blockchain",
        name="Amoy transactions",
        blockchain="amoy",
        choices=["input:address", "tag:erc721"],
        description="Transactions that have been mined into the Amoy blockchain",
        icon_url="https://static.simiotics.com/moonstream/assets/matic-token-inverted-icon.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "xdai_blockchain": SubscriptionTypeResourceData(
        id="xdai_blockchain",
        name="XDai transactions",
        blockchain="xdai",
        choices=["input:address", "tag:erc721"],
        description="Gnosis chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/xdai-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "wyrm_blockchain": SubscriptionTypeResourceData(
        id="wyrm_blockchain",
        name="Wyrm transactions",
        blockchain="wyrm",
        choices=["input:address", "tag:erc721"],
        description="Wyrm chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/great-wyrm-network-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "zksync_era_blockchain": SubscriptionTypeResourceData(
        id="zksync_era_blockchain",
        name="zkSync Era transactions",
        blockchain="zksync_era",
        choices=["input:address", "tag:erc721"],
        description="ZkSync Era chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/zksync-era-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "zksync_era_testnet_blockchain": SubscriptionTypeResourceData(
        id="zksync_era_testnet_blockchain",
        name="zkSync Era testnet transactions",
        blockchain="zksync_era_testnet",
        choices=["input:address", "tag:erc721"],
        description="ZkSync Era testnet chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/zksync-era-testnet-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "zksync_era_sepolia_blockchain": SubscriptionTypeResourceData(
        id="zksync_era_sepolia_blockchain",
        name="zkSync Era Sepolia transactions",
        blockchain="zksync_era_sepolia",
        choices=["input:address", "tag:erc721"],
        description="ZkSync Era Sepolia chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/zksync-era-testnet-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "arbitrum_one_blockchain": SubscriptionTypeResourceData(
        id="arbitrum_one_blockchain",
        name="Arbitrum One transactions",
        blockchain="arbitrum_one",
        choices=["input:address", "tag:erc721"],
        description="Arbitrum One chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/arbitrum-one-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "arbitrum_nova_blockchain": SubscriptionTypeResourceData(
        id="arbitrum_nova_blockchain",
        name="Arbitrum Nova transactions",
        blockchain="arbitrum_nova",
        choices=["input:address", "tag:erc721"],
        description="Arbitrum Nova chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/arbitrum-nova-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "arbitrum_sepolia_blockchain": SubscriptionTypeResourceData(
        id="arbitrum_sepolia_blockchain",
        name="Arbitrum Sepolia transactions",
        blockchain="arbitrum_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Arbitrum Sepolia chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/arbitrum-sepolia-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "xai_blockchain": SubscriptionTypeResourceData(
        id="xai_blockchain",
        name="Xai smartcontract",
        blockchain="xai",
        choices=["input:address", "tag:erc721"],
        description="Xai chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/xai-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "xai_sepolia_blockchain": SubscriptionTypeResourceData(
        id="xai_sepolia_blockchain",
        name="Xai Sepolia transactions",
        blockchain="xai_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Xai Sepolia chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/xai-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "avalanche_blockchain": SubscriptionTypeResourceData(
        id="avalanche_blockchain",
        name="Avalanche transactions",
        blockchain="avalanche",
        choices=["input:address", "tag:erc721"],
        description="Avalanche chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/avalanche-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "avalanche_fuji_blockchain": SubscriptionTypeResourceData(
        id="avalanche_fuji_blockchain",
        name="Avalanche Fuji transactions",
        blockchain="avalanche_fuji",
        choices=["input:address", "tag:erc721"],
        description="Avalanche Fuji chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/avalanche-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "blast_blockchain": SubscriptionTypeResourceData(
        id="blast_blockchain",
        name="Blast transactions",
        blockchain="blast",
        choices=["input:address", "tag:erc721"],
        description="Blast chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/blast-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "blast_sepolia_blockchain": SubscriptionTypeResourceData(
        id="blast_sepolia_blockchain",
        name="Blast Sepolia transactions",
        blockchain="blast_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Blast Sepolia chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/blast-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "ethereum_whalewatch": SubscriptionTypeResourceData(
        id="ethereum_whalewatch",
        name="Ethereum whale watch",
        blockchain="ethereum",
        description="Ethereum accounts that have experienced a lot of recent activity",
        choices=[],
        # Icon taken from: https://www.maxpixel.net/Whale-Cetacean-Wildlife-Symbol-Ocean-Sea-Black-99310
        icon_url="https://static.simiotics.com/moonstream/assets/whalewatch.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "ethereum_txpool": SubscriptionTypeResourceData(
        id="ethereum_txpool",
        name="Ethereum transaction pool",
        blockchain="ethereum",
        description="Transactions that have been submitted into the Ethereum transaction pool but not necessarily mined yet",
        choices=["input:address", "tag:erc721"],
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-rainbow.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "externaly_owned_account": SubscriptionTypeResourceData(
        id="externaly_owned_account",
        name="Externally owned account",
        blockchain="Any",
        description="Externally owned account",
        choices=[],
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-rainbow.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "mantle_blockchain": SubscriptionTypeResourceData(
        id="mantle_blockchain",
        name="Mantle smartcontract",
        blockchain="mantle",
        choices=["input:address", "tag:erc721"],
        description="Mantle chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/mantle-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "mantle_sepolia_blockchain": SubscriptionTypeResourceData(
        id="mantle_sepolia_blockchain",
        name="Mantle Sepolia transactions",
        blockchain="mantle_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Mantle Sepolia chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/mantle-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "sepolia_blockchain": SubscriptionTypeResourceData(
        id="sepolia_blockchain",
        name="Sepolia transactions",
        blockchain="sepolia",
        choices=["input:address", "tag:erc721"],
        description="Sepolia chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/ethereum/eth-diamond-purple.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "imx_zkevm_blockchain": SubscriptionTypeResourceData(
        id="imx_zkevm_blockchain",
        name="Immutable zkEvm transactions",
        blockchain="imx_zkevm",
        choices=["input:address", "tag:erc721"],
        description="Immutable zkEvm chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/immutable-zkevm-icon-grey.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "imx_zkevm_sepolia_blockchain": SubscriptionTypeResourceData(
        id="imx_zkevm_sepolia_blockchain",
        name="Immutable zkEvm Sepolia transactions",
        blockchain="imx_zkevm_sepolia",
        choices=["input:address", "tag:erc721"],
        description="Immutable zkEvm Sepolia chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/immutable-zkevm-icon-grey.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=False,
    ),
    "ronin_smartcontract": SubscriptionTypeResourceData(
        id="ronin_smartcontract",
        name="Ronin smartcontracts",
        blockchain="ronin",
        choices=["input:address", "tag:erc721"],
        description="Ronin chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/ronin-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
    "ronin_saigon_smartcontract": SubscriptionTypeResourceData(
        id="ronin_saigon_smartcontract",
        name="Ronin Saigon smartcontracts",
        blockchain="ronin_saigon",
        choices=["input:address", "tag:erc721"],
        description="Ronin Saigon chain transactions subscription.",
        icon_url="https://static.simiotics.com/moonstream/assets/ronin-saigon-token-logo.png",
        stripe_product_id=None,
        stripe_price_id=None,
        active=True,
    ),
}


class ConflictingSubscriptionTypesError(Exception):
    """
    Raised when caller tries to add a resource that conflicts with an existing resource.
    """

    pass


class SubscriptionTypeNotFoundError(Exception):
    """
    Raised when a subscription type is expected to exist as a Brood resource but is not found.
    """


class UnexpectedError(Exception):
    pass


BUGOUT_RESOURCE_TYPE = "subscription_type"


def create_subscription_type(
    id: str,
    name: str,
    description: str,
    icon_url: str,
    choices: List[str] = [],
    blockchain: Optional[str] = None,
    stripe_product_id: Optional[str] = None,
    stripe_price_id: Optional[str] = None,
    active: bool = False,
) -> BugoutResource:
    """
    Add a new Moonstream subscription type as a Brood resource.

    Args:
    - id: Moonstream ID for the subscription type. Examples: "ethereum_blockchain", "ethereum_txpool",
      "ethereum_whalewatch", etc.
    - name: Human-friendly name for the subscription type, which can be displayed to users.
    - description: Detailed description of the subscription type for users who would like more
      information.
    - icon_url: URL to the icon for this subscription type
    - stripe_product_id: Optional product ID from Stripe account dashboard.
    - stripe_price_id: Optional price ID from Stripe account dashboard.
    - active: Set to True if you would like the subscription type to immediately be available for
      subscriptions. If you set this to False (which is the default), users will not be able to create
      subscriptions of this type until you later on set to true.
    """
    params = {"type": BUGOUT_RESOURCE_TYPE, "id": id}

    response: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params=params,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    if response.resources:
        raise ConflictingSubscriptionTypesError(
            f"There is already a subscription_type with id: {id}"
        )

    subscription_data = {
        "type": BUGOUT_RESOURCE_TYPE,
        "id": id,
        "name": name,
        "description": description,
        "choices": choices,
        "blockchain": blockchain,
        "icon_url": icon_url,
        "stripe_product_id": stripe_product_id,
        "stripe_price_id": stripe_price_id,
        "active": active,
    }

    resource = bc.create_resource(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        application_id=MOONSTREAM_APPLICATION_ID,
        resource_data=subscription_data,
    )

    return resource


def cli_create_subscription_type(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes create".
    """
    result = create_subscription_type(
        args.id,
        args.name,
        args.description,
        args.blockchain,
        args.icon,
        args.choices,
        args.stripe_product_id,
        args.stripe_price_id,
        args.active,
    )
    print(result.json())


def list_subscription_types(active_only: bool = False) -> BugoutResources:
    """
    Lists all subscription types registered as Brood resources for this Moonstream application.

    Args:
    - active_only: Set this to true if you only want to list active subscription types. By default,
      all subscription types are listed, be they active or inactive.
    """
    response = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    # TODO(kompotkot): Currently, we cannot filter using non-string fields in Brood resources. This means
    # that we have to implement the active_only filter in this API instead of just setting a query parameter
    # in the Brood API call. This should be fixed.
    if not active_only:
        return response

    active_resources = [
        resource for resource in response.resources if resource.resource_data["active"]
    ]
    return BugoutResources(resources=active_resources)


def cli_list_subscription_types(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes list".
    """
    results = list_subscription_types(args.active)
    print(results.json())


def get_subscription_type(id: str) -> Optional[BugoutResource]:
    """
    Retrieves the resource representing the subscription type with the given ID.

    Args:
    - id: Moonstream ID for the subscription type (not the Brood resource ID).
      Examples - "ethereum_blockchain", "ethereum_whalewatch", etc.

    Returns: None if there is no subscription type with that ID. Otherwise, returns the full
    Brood resource. To access the subscription type itself, use the "resource_data" member of the
    return value. If more than one subscription type is found with the given ID, raises a
    ConflictingSubscriptionTypesError.
    """
    response = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE, "id": id},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    resources = response.resources

    if not resources:
        return None
    if len(resources) > 1:
        raise ConflictingSubscriptionTypesError(
            f"More than one resource with the given ID:\n{json.dumps(resources, indent=2)}"
        )
    return resources[0]


def cli_get_subscription_type(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes get".
    """
    resource = get_subscription_type(args.id)
    if resource is None:
        print(f"Could not find resource with ID: {id}")
    else:
        print(resource.json())


def update_subscription_type(
    id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    choices: Optional[List[str]] = None,
    blockchain: Optional[str] = None,
    icon_url: Optional[str] = None,
    stripe_product_id: Optional[str] = None,
    stripe_price_id: Optional[str] = None,
    active: Optional[bool] = None,
) -> BugoutResource:
    """
    Update a Moonstream subscription type using the Brood Resources API.

    Args:
    - id: Moonstream ID for the subscription type. Examples: "ethereum_blockchain", "ethereum_txpool",
      "ethereum_whalewatch", etc.
    - name: Human-friendly name for the subscription type, which can be displayed to users.
    - description: Detailed description of the subscription type for users who would like more
      information.
    - icon_url: URL to the icon for this subscription type
    - stripe_product_id: Optional product ID from Stripe account dashboard.
    - stripe_price_id: Optional price ID from Stripe account dashboard.
    - active: Set to True if you would like the subscription type to immediately be available for
      subscriptions. If you set this to False (which is the default), users will not be able to create
      subscriptions of this type until you later on set to true.
    """

    resource = get_subscription_type(id)
    if resource is None:
        raise SubscriptionTypeNotFoundError(
            f"Could not find subscription type with ID: {id}."
        )

    brood_resource_id = resource.id
    updated_resource_data = resource.resource_data
    if name is not None:
        updated_resource_data["name"] = name
    if description is not None:
        updated_resource_data["description"] = description
    if choices is not None:
        updated_resource_data["choices"] = choices
    if blockchain is not None:
        updated_resource_data["blockchain"] = blockchain
    if icon_url is not None:
        updated_resource_data["icon_url"] = icon_url
    if stripe_product_id is not None:
        updated_resource_data["stripe_product_id"] = stripe_product_id
    if stripe_price_id is not None:
        updated_resource_data["stripe_price_id"] = stripe_price_id
    if active is not None:
        updated_resource_data["active"] = active

    # TODO(zomglings): This was written with an outdated bugout-python client.
    # New client has an update_resource method which is what we should be using
    # here.

    try:
        new_resource = bc.update_resource(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            resource_id=brood_resource_id,
            resource_data={"update": updated_resource_data},
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

    except Exception as e:
        raise ConflictingSubscriptionTypesError(
            f"Unable to delete old subscription type with ID: {id}. Error:\n{repr(e)}"
        )

    return new_resource


def cli_update_subscription_type(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes update".
    """
    result = update_subscription_type(
        args.id,
        args.name,
        args.description,
        args.choices,
        args.blockchain,
        args.icon,
        args.stripe_product_id,
        args.stripe_price_id,
        args.active,
    )
    print(result.json())


def delete_subscription_type(id: str) -> Optional[BugoutResource]:
    """
    Deletes the subscription type resource with the given ID.

    Args:
    - id: Moonstream ID of the subscription type you would like to delete. Examples - "ethereum_blockchain",
      "ethereum_whalewatch", etc.

    Returns: The BugoutResource that was deleted. If no such resource existed in the first place, returns
    None. If multiple resources existed with the given Moonstream ID, raises a ConflictingSubscriptionTypesError
    and does not delete anything!
    """
    # ConflictingSubscriptionTypesError raised here if there are multiple resources with the given id.
    resource = get_subscription_type(id)
    if resource is None:
        return None

    resource = bc.delete_resource(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        resource_id=resource.id,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    return resource


def cli_delete_subscription_type(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes delete".
    """
    result = delete_subscription_type(args.id)
    if result is None:
        print(f"Could not find resource with ID: {id}")
    else:
        print(result.json())


def ensure_canonical_subscription_types() -> BugoutResources:
    """
    Ensures that the connected Brood API has at least the canonical subscription types. If any of the
    canonical subscription types does not exist as a Brood resource, this API creates the corresponding
    resource. If any of the canonical subscription types exists as a Brood resource but has been modified,
    this method does not change it on the server.

    Args: None

    Returns: A list of the resources representing the canonical subscription types as they exist
    on the connected Brood API.
    """
    existing_canonical_subscription_types: Dict[str, BugoutResource] = {}
    for id, canonical_subscription_type in CANONICAL_SUBSCRIPTION_TYPES.items():
        resource = get_subscription_type(canonical_subscription_type.id)
        if resource is not None:
            existing_canonical_subscription_types[id] = resource

    for id in CANONICAL_SUBSCRIPTION_TYPES.keys():
        if existing_canonical_subscription_types.get(id) is None:
            canonical_subscription_type = CANONICAL_SUBSCRIPTION_TYPES[id]
            resource = create_subscription_type(
                id,
                canonical_subscription_type.name,
                canonical_subscription_type.description,
                canonical_subscription_type.icon_url,
                canonical_subscription_type.choices,
                canonical_subscription_type.blockchain,
                canonical_subscription_type.stripe_product_id,
                canonical_subscription_type.stripe_price_id,
                canonical_subscription_type.active,
            )
            existing_canonical_subscription_types[id] = resource
        else:
            canonical_subscription_type = CANONICAL_SUBSCRIPTION_TYPES[id]
            resource = update_subscription_type(
                id,
                canonical_subscription_type.name,
                canonical_subscription_type.description,
                canonical_subscription_type.choices,
                canonical_subscription_type.blockchain,
                canonical_subscription_type.icon_url,
                canonical_subscription_type.stripe_product_id,
                canonical_subscription_type.stripe_price_id,
                canonical_subscription_type.active,
            )
            existing_canonical_subscription_types[id] = resource

    return BugoutResources(
        resources=list(existing_canonical_subscription_types.values())
    )


def cli_ensure_canonical_subscription_types(args: argparse.Namespace) -> None:
    """
    Handler for "mnstr subtypes ensure-canonical
    """
    resources = ensure_canonical_subscription_types()
    print(resources.json())
