import os

from bugout.app import Bugout

# Bugout
BUGOUT_BROOD_URL = os.environ.get("BUGOUT_BROOD_URL", "https://auth.bugout.dev")
BUGOUT_SPIRE_URL = os.environ.get("BUGOUT_SPIRE_URL", "https://spire.bugout.dev")


bugout_client = Bugout(brood_api_url=BUGOUT_BROOD_URL, spire_api_url=BUGOUT_SPIRE_URL)

BUGOUT_REQUEST_TIMEOUT_SECONDS = 5

HUMBUG_REPORTER_BACKEND_TOKEN = os.environ.get("HUMBUG_REPORTER_BACKEND_TOKEN")

# Default value is "" instead of None so that mypy understands that MOONSTREAM_APPLICATION_ID is a string
MOONSTREAM_APPLICATION_ID = os.environ.get("MOONSTREAM_APPLICATION_ID", "")
if MOONSTREAM_APPLICATION_ID == "":
    raise ValueError("MOONSTREAM_APPLICATION_ID environment variable must be set")

MOONSTREAM_DATA_JOURNAL_ID = os.environ.get("MOONSTREAM_DATA_JOURNAL_ID", "")
if MOONSTREAM_DATA_JOURNAL_ID == "":
    raise ValueError("MOONSTREAM_DATA_JOURNAL_ID environment variable must be set")

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
