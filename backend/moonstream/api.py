"""
The Moonstream HTTP API
"""
import logging
import time
from typing import Any, Dict

from bugout.data import BugoutSearchResults
from bugout.exceptions import BugoutResponseException
from bugout.journal import SearchOrder
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import data
from .middleware import MoonstreamHTTPException
from .routes.address_info import app as addressinfo_api
from .routes.nft import app as nft_api
from .routes.subscriptions import app as subscriptions_api
from .routes.streams import app as streams_api
from .routes.txinfo import app as txinfo_api
from .routes.users import app as users_api
from .settings import (
    bugout_client as bc,
    ORIGINS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
)
from .version import MOONSTREAM_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", response_model=data.PingResponse)
async def ping_handler() -> data.PingResponse:
    return data.PingResponse(status="ok")


@app.get("/version", response_model=data.VersionResponse)
async def version_handler() -> data.VersionResponse:
    return data.VersionResponse(version=MOONSTREAM_VERSION)


@app.get("/now", tags=["time"])
async def now_handler() -> data.NowResponse:
    return data.NowResponse(epoch_time=time.time())


@app.get("/status", tags=["streams"], response_model=data.StatusResponse)
async def status_handler() -> data.StatusResponse:
    """
    Get latest records and their creation timestamp for crawlers:
    - ethereum_txpool
    - ethereum_trending
    """
    crawl_types_timestamp: Dict[str, Any] = {
        "ethereum_txpool": None,
        "ethereum_trending": None,
    }
    for crawl_type in crawl_types_timestamp.keys():
        try:
            search_results: BugoutSearchResults = bc.search(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_DATA_JOURNAL_ID,
                query=f"tag:crawl_type:{crawl_type}",
                limit=1,
                content=False,
                timeout=10.0,
                order=SearchOrder.DESCENDING,
            )
            if len(search_results.results) == 1:
                crawl_types_timestamp[crawl_type] = search_results.results[0].created_at
        except BugoutResponseException as e:
            raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            logger.error(f"Unable to get status for crawler with type: {crawl_type}")
            raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return data.StatusResponse(
        ethereum_txpool_timestamp=crawl_types_timestamp["ethereum_txpool"],
        ethereum_trending_timestamp=crawl_types_timestamp["ethereum_trending"],
    )


app.mount("/subscriptions", subscriptions_api)
app.mount("/users", users_api)
app.mount("/streams", streams_api)
app.mount("/txinfo", txinfo_api)
app.mount("/address_info", addressinfo_api)
app.mount("/nft", nft_api)
