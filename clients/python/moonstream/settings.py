import os

MOONSTREAM_API_URL = os.environ.get("MOONSTREAM_API_URL", "https://api.moonstream.to")

MOONSTREAM_REQUEST_TIMEOUT = 10
MOONSTREAM_REQUEST_TIMEOUT_RAW = os.environ.get("MOONSTREAM_REQUEST_TIMEOUT")
try:
    if MOONSTREAM_REQUEST_TIMEOUT_RAW is not None:
        MOONSTREAM_REQUEST_TIMEOUT = int(MOONSTREAM_REQUEST_TIMEOUT_RAW)
except:
    raise Exception(
        f"Could not parse MOONSTREAM_REQUEST_TIMEOUT environment variable as int: {MOONSTREAM_REQUEST_TIMEOUT_RAW}"
    )
