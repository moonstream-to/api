import os
from typing import Dict, Optional
from uuid import UUID

from bugout.app import Bugout
from moonstreamdb.blockchain import AvailableBlockchainType

# Bugout
BUGOUT_BROOD_URL = os.environ.get("BUGOUT_BROOD_URL", "https://auth.bugout.dev")
BUGOUT_SPIRE_URL = os.environ.get("BUGOUT_SPIRE_URL", "https://spire.bugout.dev")

bugout_client = Bugout(brood_api_url=BUGOUT_BROOD_URL, spire_api_url=BUGOUT_SPIRE_URL)


MOONSTREAM_API_URL = os.environ.get("MOONSTREAM_API_URL", "https://api.moonstream.to")
MOONSTREAM_ENGINE_URL = os.environ.get(
    "MOONSTREAM_ENGINE_URL", "https://engineapi.moonstream.to"
)


BUGOUT_REQUEST_TIMEOUT_SECONDS_RAW = os.environ.get(
    "MOONSTREAM_BUGOUT_TIMEOUT_SECONDS", 30
)
try:
    BUGOUT_REQUEST_TIMEOUT_SECONDS = int(BUGOUT_REQUEST_TIMEOUT_SECONDS_RAW)
except:
    raise Exception(
        f"Could not parse MOONSTREAM_BUGOUT_TIMEOUT_SECONDS_RAW as int: {BUGOUT_REQUEST_TIMEOUT_SECONDS_RAW}"
    )


HUMBUG_REPORTER_CRAWLERS_TOKEN = os.environ.get("HUMBUG_REPORTER_CRAWLERS_TOKEN")

# Origin
RAW_ORIGINS = os.environ.get("MOONSTREAM_CORS_ALLOWED_ORIGINS")
if RAW_ORIGINS is None:
    raise ValueError(
        "MOONSTREAM_CORS_ALLOWED_ORIGINS environment variable must be set (comma-separated list of CORS allowed origins)"
    )
ORIGINS = RAW_ORIGINS.split(",")

# OpenAPI
DOCS_TARGET_PATH = "docs"


# Crawler label
CRAWLER_LABEL = "moonworm-alpha"
VIEW_STATE_CRAWLER_LABEL = "view-state-alpha"
METADATA_CRAWLER_LABEL = "metadata-crawler"

MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS = 30000
MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS_RAW = os.environ.get(
    "MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS"
)
try:
    if MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS_RAW is not None:
        MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS = int(
            MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS_RAW
        )
except:
    raise Exception(
        f"Could not parse MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS as int: {MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS_RAW}"
    )


MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS = 100000
MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS_RAW = os.environ.get(
    "MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS"
)
try:
    if MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS_RAW is not None:
        MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS = int(
            MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS_RAW
        )
except:
    raise Exception(
        f"Could not parse MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS as int: {MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS_RAW}"
    )

# Geth connection address
MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI = os.environ.get(
    "MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI", ""
)
if MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI == "":
    raise Exception("MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI env variable is not set")

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

MOONSTREAM_CRAWL_WORKERS = 4
MOONSTREAM_CRAWL_WORKERS_RAW = os.environ.get("MOONSTREAM_CRAWL_WORKERS")
try:
    if MOONSTREAM_CRAWL_WORKERS_RAW is not None:
        MOONSTREAM_CRAWL_WORKERS = int(MOONSTREAM_CRAWL_WORKERS_RAW)
except:
    raise Exception(
        f"Could not parse MOONSTREAM_CRAWL_WORKERS as int: {MOONSTREAM_CRAWL_WORKERS_RAW}"
    )

# Etherscan
MOONSTREAM_ETHERSCAN_TOKEN = os.environ.get("MOONSTREAM_ETHERSCAN_TOKEN")

# NFT crawler
NFT_HUMBUG_TOKEN = os.environ.get("NFT_HUMBUG_TOKEN", "")
if NFT_HUMBUG_TOKEN == "":
    raise ValueError("NFT_HUMBUG_TOKEN env variable is not set")

MOONSTREAM_ADMIN_ACCESS_TOKEN = os.environ.get("MOONSTREAM_ADMIN_ACCESS_TOKEN", "")
if MOONSTREAM_ADMIN_ACCESS_TOKEN == "":
    raise ValueError("MOONSTREAM_ADMIN_ACCESS_TOKEN env variable is not set")

MOONSTREAM_DATA_JOURNAL_ID = os.environ.get("MOONSTREAM_DATA_JOURNAL_ID", "")
if MOONSTREAM_DATA_JOURNAL_ID == "":
    raise ValueError("MOONSTREAM_DATA_JOURNAL_ID env variable is not set")


MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX = os.environ.get(
    "MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX"
)
if MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX is None:
    raise ValueError(
        "MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX environment variable must be set"
    )

MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET = os.environ.get(
    "MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET"
)
if MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET is None:
    raise ValueError(
        "MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET environment variable must be set"
    )

MOONSTREAM_MOONWORM_TASKS_JOURNAL = os.environ.get(
    "MOONSTREAM_MOONWORM_TASKS_JOURNAL", ""
)
if MOONSTREAM_MOONWORM_TASKS_JOURNAL == "":
    raise ValueError(
        "MOONSTREAM_MOONWORM_TASKS_JOURNAL environment variable must be set"
    )

# queries


LINKS_EXPIRATION_TIME = 60 * 60 * 12  # 12 hours

MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS = 30000
MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS_RAW = os.environ.get(
    "MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS"
)
try:
    if MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS_RAW is not None:
        MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS = int(
            MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS_RAW
        )
except:
    raise Exception(
        f"Could not parse MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS as int: {MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS_RAW}"
    )


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

# Node balancer
NB_ACCESS_ID_HEADER = os.environ.get("NB_ACCESS_ID_HEADER", "x-node-balancer-access-id")
NB_DATA_SOURCE_HEADER = os.environ.get(
    "NB_DATA_SOURCE_HEADER", "x-node-balancer-data-source"
)

NB_CONTROLLER_ACCESS_ID: Optional[UUID] = None
NB_CONTROLLER_ACCESS_ID_RAW = os.environ.get("NB_CONTROLLER_ACCESS_ID", "")
try:
    NB_CONTROLLER_ACCESS_ID = UUID(NB_CONTROLLER_ACCESS_ID_RAW)
except:
    pass


# HTTPProvider for web3 client

WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS = 600
WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS_RAW = os.environ.get(
    "WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS"
)
try:
    if WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS_RAW is not None:
        WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS = int(
            WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS_RAW
        )
except:
    raise Exception(
        f"Could not parse WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS as int: {WEB3_CLIENT_REQUEST_TIMEOUT_SECONDS_RAW}"
    )


multicall_contracts: Dict[AvailableBlockchainType, str] = {
    AvailableBlockchainType.POLYGON: "0xc8E51042792d7405184DfCa245F2d27B94D013b6",
    AvailableBlockchainType.MUMBAI: "0xe9939e7Ea7D7fb619Ac57f648Da7B1D425832631",
    AvailableBlockchainType.ETHEREUM: "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
}


# Custom Crawler

MOONSTREAM_S3_PUBLIC_DATA_BUCKET = os.environ.get(
    "MOONSTREAM_S3_PUBLIC_DATA_BUCKET", ""
)  # S3 bucket for storing custom crawler data

if MOONSTREAM_S3_PUBLIC_DATA_BUCKET == "":
    raise ValueError(
        "MOONSTREAM_S3_PUBLIC_DATA_BUCKET environment variable must be set"
    )


MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX = os.environ.get(
    "MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX", "dev"
)


# infura config


INFURA_PROJECT_ID = os.environ.get("INFURA_PROJECT_ID")

infura_networks = {
    AvailableBlockchainType.ETHEREUM: {
        "name": "mainnet",
        "url": f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
    },
    AvailableBlockchainType.POLYGON: {
        "name": "polygon",
        "url": f"https://polygon-mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
    },
    AvailableBlockchainType.MUMBAI: {
        "name": "mumbai",
        "url": f"https://polygon-mumbai.infura.io/v3/{INFURA_PROJECT_ID}",
    },
}


## Moonstream resources types

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"
BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION = "entity_subscription"
BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"


# Historical crawler status config

HISTORICAL_CRAWLER_STATUSES = {
    "pending": "pending",
    "running": "running",
    "finished": "finished",
}

# Historical crawler moonworm status config

HISTORICAL_CRAWLER_MOONWORM_STATUSES = {
    "pickedup": True,
}

# Statuses tags prefixes

HISTORICAL_CRAWLER_STATUS_TAG_PREFIXES = {
    "moonworm_status": "moonworm_task_pickedup",
    "historical_crawl_status": "historical_crawl_status",
    "progress_status": "progress",
}


# Leaderboard generator

MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID = os.environ.get(
    "MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID", ""
)
if MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID == "":
    raise ValueError(
        "MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID environment variable must be set"
    )
