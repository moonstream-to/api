import os

from bugout.app import Bugout

# Bugout
BUGOUT_BROOD_URL = os.environ.get("BUGOUT_BROOD_URL", "https://auth.bugout.dev")
BUGOUT_SPIRE_URL = os.environ.get("BUGOUT_SPIRE_URL", "https://spire.bugout.dev")
bugout_client = Bugout(brood_api_url=BUGOUT_BROOD_URL, spire_api_url=BUGOUT_SPIRE_URL)

# Default value is "" instead of None so that mypy understands that MOONSTREAM_APPLICATION_ID is a string
MOONSTREAM_APPLICATION_ID = os.environ.get("MOONSTREAM_APPLICATION_ID", "")
if MOONSTREAM_APPLICATION_ID == "":
    raise ValueError("MOONSTREAM_APPLICATION_ID environment variable must be set")

MOONSTREAM_DATA_JOURNAL_ID = os.environ.get("MOONSTREAM_DATA_JOURNAL_ID")
if MOONSTREAM_DATA_JOURNAL_ID is None:
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
MOONSTREAM_OPENAPI_LIST = []
MOONSTREAM_OPENAPI_LIST_RAW = os.environ.get("MOONSTREAM_OPENAPI_LIST")
if MOONSTREAM_OPENAPI_LIST_RAW is not None:
    MOONSTREAM_OPENAPI_LIST = MOONSTREAM_OPENAPI_LIST_RAW.split(",")

DOCS_PATHS = {}
for path in MOONSTREAM_OPENAPI_LIST:
    DOCS_PATHS[f"/{path}/{DOCS_TARGET_PATH}"] = "GET"
    DOCS_PATHS[f"/{path}/{DOCS_TARGET_PATH}/openapi.json"] = "GET"

DEFAULT_STREAM_TIMEINTERVAL = 5 * 60
