import os
from typing import Dict, Optional

from bugout.app import Bugout
from moonstreamdb.blockchain import AvailableBlockchainType

# Bugout
BUGOUT_BROOD_URL = os.environ.get("BUGOUT_BROOD_URL", "https://auth.bugout.dev")
BUGOUT_SPIRE_URL = os.environ.get("BUGOUT_SPIRE_URL", "https://spire.bugout.dev")
BUGOUT_SPIRE_EXTERNAL_URL = os.environ.get(
    "BUGOUT_SPIRE_EXTERNAL_URL", "https://spire.bugout.dev"
)


bugout_client = Bugout(
    brood_api_url=BUGOUT_BROOD_URL, spire_api_url=BUGOUT_SPIRE_EXTERNAL_URL
)

BUGOUT_REQUEST_TIMEOUT_SECONDS = 5

HUMBUG_REPORTER_BACKEND_TOKEN = os.environ.get("HUMBUG_REPORTER_BACKEND_TOKEN")

# Default value is "" instead of None so that mypy understands that MOONSTREAM_APPLICATION_ID is a string
MOONSTREAM_APPLICATION_ID = os.environ.get("MOONSTREAM_APPLICATION_ID", "")
if MOONSTREAM_APPLICATION_ID == "":
    raise ValueError("MOONSTREAM_APPLICATION_ID environment variable must be set")

MOONSTREAM_DATA_JOURNAL_ID = os.environ.get("MOONSTREAM_DATA_JOURNAL_ID", "")
if MOONSTREAM_DATA_JOURNAL_ID == "":
    raise ValueError("MOONSTREAM_DATA_JOURNAL_ID environment variable must be set")


MOONSTREAM_QUERIES_JOURNAL_ID = os.environ.get("MOONSTREAM_QUERIES_JOURNAL_ID", "")
if MOONSTREAM_DATA_JOURNAL_ID == "":
    raise ValueError("MOONSTREAM_QUERIES_JOURNAL_ID environment variable must be set")


MOONSTREAM_ADMIN_ACCESS_TOKEN = os.environ.get("MOONSTREAM_ADMIN_ACCESS_TOKEN", "")
if MOONSTREAM_ADMIN_ACCESS_TOKEN == "":
    raise ValueError("MOONSTREAM_ADMIN_ACCESS_TOKEN environment variable must be set")

# Origin
RAW_ORIGINS = os.environ.get("MOONSTREAM_CORS_ALLOWED_ORIGINS")
if RAW_ORIGINS is None:
    raise ValueError(
        "MOONSTREAM_CORS_ALLOWED_ORIGINS environment variable must be set (comma-separated list of CORS allowed origins)"
    )
ORIGINS = RAW_ORIGINS.split(",")

# OpenAPI
DOCS_TARGET_PATH = "docs"

DEFAULT_STREAM_TIMEINTERVAL = 5 * 60

HUMBUG_TXPOOL_CLIENT_ID = os.environ.get(
    "HUMBUG_TXPOOL_CLIENT_ID", "client:ethereum-txpool-crawler-0"
)

# S3 Bucket
ETHERSCAN_SMARTCONTRACTS_BUCKET = os.environ.get("MOONSTREAM_S3_SMARTCONTRACTS_BUCKET")
if ETHERSCAN_SMARTCONTRACTS_BUCKET is None:
    raise ValueError("MOONSTREAM_S3_SMARTCONTRACTS_BUCKET is not set")

MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET = os.environ.get(
    "MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET"
)
if MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET is None:
    raise ValueError(
        "MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET environment variable must be set"
    )
MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX = os.environ.get(
    "MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX"
)
if MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX is None:
    raise ValueError(
        "MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX environment variable must be set"
    )
MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX = (
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX.rstrip("/")
)

MOONSTREAM_CRAWLERS_SERVER_URL = os.environ.get("MOONSTREAM_CRAWLERS_SERVER_URL")
if MOONSTREAM_CRAWLERS_SERVER_URL is None:
    raise ValueError("MOONSTREAM_CRAWLERS_SERVER_URL environment variable must be set")
MOONSTREAM_CRAWLERS_SERVER_URL = MOONSTREAM_CRAWLERS_SERVER_URL.rstrip("/")

MOONSTREAM_CRAWLERS_SERVER_PORT = os.environ.get("MOONSTREAM_CRAWLERS_SERVER_PORT")
if MOONSTREAM_CRAWLERS_SERVER_PORT is None:
    raise ValueError("MOONSTREAM_CRAWLERS_SERVER_PORT environment variable must be set")
MOONSTREAM_CRAWLERS_SERVER_PORT = MOONSTREAM_CRAWLERS_SERVER_PORT.rstrip("/")


MOONSTREAM_MOONWORM_TASKS_JOURNAL = os.environ.get(
    "MOONSTREAM_MOONWORM_TASKS_JOURNAL", ""
)
if MOONSTREAM_MOONWORM_TASKS_JOURNAL == "":
    raise ValueError(
        "MOONSTREAM_MOONWORM_TASKS_JOURNAL environment variable must be set"
    )

# Web3
MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI == "":
    raise ValueError(
        "MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI environment variable must be set"
    )
MOONSTREAM_POLYGON_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_POLYGON_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_POLYGON_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_POLYGON_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_AMOY_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_AMOY_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_AMOY_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_AMOY_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_XDAI_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_XDAI_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_XDAI_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_XDAI_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_WYRM_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_WYRM_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_WYRM_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_WYRM_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_ZKSYNC_ERA_TESTNET_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ZKSYNC_ERA_TESTNET_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ZKSYNC_ERA_TESTNET_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_ZKSYNC_ERA_TESTNET_WEB3_PROVIDER_URI env variable is not set"
    )

MOONSTREAM_ZKSYNC_ERA_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ZKSYNC_ERA_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ZKSYNC_ERA_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_ZKSYNC_ERA_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_ZKSYNC_ERA_SEPOLIA_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ZKSYNC_ERA_SEPOLIA_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ZKSYNC_ERA_SEPOLIA_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_ZKSYNC_ERA_SEPOLIA_WEB3_PROVIDER_URI env variable is not set"
    )


MOONSTREAM_ARBITRUM_ONE_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ARBITRUM_ONE_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ARBITRUM_ONE_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_ARBITRUM_ONE_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_ARBITRUM_NOVA_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ARBITRUM_NOVA_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ARBITRUM_NOVA_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_ARBITRUM_NOVA_WEB3_PROVIDER_URI env variable is not set"
    )

MOONSTREAM_ARBITRUM_SEPOLIA_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ARBITRUM_SEPOLIA_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ARBITRUM_SEPOLIA_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_ARBITRUM_SEPOLIA_WEB3_PROVIDER_URI env variable is not set"
    )

MOONSTREAM_XAI_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_XAI_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_XAI_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_XAI_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_XAI_SEPOLIA_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_XAI_SEPOLIA_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_XAI_SEPOLIA_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_XAI_SEPOLIA_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_AVALANCHE_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_AVALANCHE_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_AVALANCHE_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_AVALANCHE_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_AVALANCHE_FUJI_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_AVALANCHE_FUJI_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_AVALANCHE_FUJI_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_AVALANCHE_FUJI_WEB3_PROVIDER_URI env variable is not set"
    )

MOONSTREAM_BLAST_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_BLAST_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_BLAST_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_BLAST_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_BLAST_SEPOLIA_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_BLAST_SEPOLIA_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_BLAST_SEPOLIA_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_BLAST_SEPOLIA_WEB3_PROVIDER_URI env variable is not set"
    )

MOONSTREAM_PROOFOFPLAY_APEX_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_PROOFOFPLAY_APEX_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_PROOFOFPLAY_APEX_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_PROOFOFPLAY_APEX_WEB3_PROVIDER_URI env variable is not set"
    )
MOONSTREAM_MANTLE_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_MANTLE_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_MANTLE_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_MANTLE_WEB3_PROVIDER_URI env variable is not set")

MOONSTREAM_MANTLE_SEPOLIA_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_MANTLE_SEPOLIA_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_MANTLE_SEPOLIA_WEB3_PROVIDER_URI == "":
    raise Exception(
        "MOONSTREAM_MANTLE_SEPOLIA_WEB3_PROVIDER_URI env variable is not set"
    )

## QueryAPI

MOONSTREAM_S3_QUERIES_BUCKET = os.environ.get("MOONSTREAM_S3_QUERIES_BUCKET", "")
if MOONSTREAM_S3_QUERIES_BUCKET == "":
    raise ValueError("MOONSTREAM_S3_QUERIES_BUCKET environment variable must be set")

MOONSTREAM_S3_QUERIES_BUCKET_PREFIX = os.environ.get(
    "MOONSTREAM_S3_QUERIES_BUCKET_PREFIX", ""
)
if MOONSTREAM_S3_QUERIES_BUCKET_PREFIX == "":
    raise ValueError(
        "MOONSTREAM_S3_QUERIES_BUCKET_PREFIX environment variable must be set"
    )

# Entities reserved tags
MOONSTREAM_ENTITIES_RESERVED_TAGS = [
    "type",
    "subscription_type_id",
    "color",
    "label",
    "user_id",
    "address",
    "blockchain",
]

## Moonstream resources types

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"
BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION = "entity_subscription"
BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"
MOONSTREAM_QUERY_TEMPLATE_CONTEXT_TYPE = "moonstream_query_template"


# Node balancer
NB_ACCESS_ID_HEADER = os.environ.get("NB_ACCESS_ID_HEADER", "x-node-balancer-access-id")
NB_DATA_SOURCE_HEADER = os.environ.get(
    "NB_DATA_SOURCE_HEADER", "x-node-balancer-data-source"
)
NB_DATA_SOURCE_HEADER_VALUE = os.environ.get(
    "NB_DATA_SOURCE_HEADER_VALUE", "blockchain"
)


# Thread timeout

THREAD_TIMEOUT_SECONDS = 10

multicall_contracts: Dict[AvailableBlockchainType, str] = {
    AvailableBlockchainType.POLYGON: "0xc8E51042792d7405184DfCa245F2d27B94D013b6",
    AvailableBlockchainType.MUMBAI: "0xe9939e7Ea7D7fb619Ac57f648Da7B1D425832631",
    AvailableBlockchainType.AMOY: "0xcA11bde05977b3631167028862bE2a173976CA11",
    AvailableBlockchainType.ETHEREUM: "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
    AvailableBlockchainType.ARBITRUM_ONE: "0xcA11bde05977b3631167028862bE2a173976CA11",
    AvailableBlockchainType.ARBITRUM_NOVA: "0xcA11bde05977b3631167028862bE2a173976CA11",
    AvailableBlockchainType.ARBITRUM_SEPOLIA: "0xcA11bde05977b3631167028862bE2a173976CA11",
    AvailableBlockchainType.XAI: "0xcA11bde05977b3631167028862bE2a173976CA11",
    AvailableBlockchainType.XDAI: "0xcA11bde05977b3631167028862bE2a173976CA11",
    AvailableBlockchainType.ZKSYNC_ERA: "0xF9cda624FBC7e059355ce98a31693d299FACd963",
    AvailableBlockchainType.ZKSYNC_ERA_TESTNET: "0xF9cda624FBC7e059355ce98a31693d299FACd963",
}


multicall_contract_abi = [
    {
        "inputs": [
            {"internalType": "bool", "name": "requireSuccess", "type": "bool"},
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "target",
                        "type": "address",
                    },
                    {
                        "internalType": "bytes",
                        "name": "callData",
                        "type": "bytes",
                    },
                ],
                "internalType": "struct Multicall2.Call[]",
                "name": "calls",
                "type": "tuple[]",
            },
        ],
        "name": "tryAggregate",
        "outputs": [
            {
                "components": [
                    {"internalType": "bool", "name": "success", "type": "bool"},
                    {
                        "internalType": "bytes",
                        "name": "returnData",
                        "type": "bytes",
                    },
                ],
                "internalType": "struct Multicall2.Result[]",
                "name": "returnData",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes", "name": "data", "type": "bytes"}],
        "name": "aggregate",
        "outputs": [
            {"internalType": "bool", "name": "success", "type": "bool"},
            {"internalType": "bytes", "name": "result", "type": "bytes"},
        ],
        "stateMutability": "payable",
        "type": "function",
    },
]


supportsInterface_abi = [
    {
        "inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}],
        "name": "supportsInterface",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    }
]

MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS_RAW = os.environ.get(
    "MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS"
)
MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS = 10
try:
    if MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS_RAW is not None:
        MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS = int(
            MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS_RAW
        )
except:
    raise Exception(
        f"Could not parse MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS as int: {MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS_RAW}"
    )

MOONSTREAM_PUBLIC_QUERIES_DATA_ACCESS_TOKEN = os.environ.get(
    "MOONSTREAM_PUBLIC_QUERIES_DATA_ACCESS_TOKEN", ""
)
if MOONSTREAM_PUBLIC_QUERIES_DATA_ACCESS_TOKEN == "":
    raise ValueError(
        "MOONSTREAM_PUBLIC_QUERIES_DATA_ACCESS_TOKEN environment variable must be set"
    )


MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID = os.environ.get(
    "MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID", ""
)
if MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID == "":
    raise ValueError(
        "MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID environment variable must be set"
    )


MOONSTREAM_USAGE_REPORTS_JOURNAL_ID = os.environ.get(
    "MOONSTREAM_USAGE_REPORTS_JOURNAL_ID"
)
