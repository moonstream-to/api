import logging
from typing import Any, Dict

from bugout.data import BugoutSearchResults
from bugout.exceptions import BugoutResponseException
from bugout.journal import SearchOrder
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .. import data
from ..middleware import MoonstreamHTTPException
from ..settings import (
    bugout_client as bc,
    DOCS_TARGET_PATH,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
    ORIGINS,
)
from ..version import MOONSTREAM_VERSION

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "status", "description": "Status of Moonstream API services."}
]
app = FastAPI(
    title=f"Moonstream users API.",
    description="User, token and password handlers.",
    version=MOONSTREAM_VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["status"], response_model=data.StatusResponse)
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
