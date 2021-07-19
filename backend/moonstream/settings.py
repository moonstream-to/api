import os

# Origin
RAW_ORIGIN = os.environ.get("MOONSTREAM_CORS_ALLOWED_ORIGINS")
if RAW_ORIGIN is None:
    raise ValueError(
        "MOONSTREAM_CORS_ALLOWED_ORIGINS environment variable must be set (comma-separated list of CORS allowed origins"
    )
ORIGINS = RAW_ORIGIN.split(",")

# OpenAPI
DOCS_TARGET_PATH = "docs"
MOONSTREAM_OPENAPI_LIST = []
MOONSTREAM_OPENAPI_LIST_RAW = os.environ.get("MOONSTREAM_OPENAPI_LIST")
if MOONSTREAM_OPENAPI_LIST_RAW is not None:
    MOONSTREAM_OPENAPI_LIST = MOONSTREAM_OPENAPI_LIST_RAW.split(",")
