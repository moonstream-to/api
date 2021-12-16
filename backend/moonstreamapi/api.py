"""
The Moonstream HTTP API
"""
import logging
import time
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import actions, data
from .middleware import BroodAuthMiddleware, MoonstreamHTTPException
from .routes.address_info import router as addressinfo_router
from .routes.dashboards import router as dashboards_router
from .routes.streams import router as streams_router
from .routes.subscriptions import router as subscriptions_router
from .routes.txinfo import router as txinfo_router
from .routes.users import router as users_router
from .routes.whales import router as whales_router
from .settings import DOCS_TARGET_PATH, ORIGINS
from .version import MOONSTREAMAPI_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


tags_metadata = [
    {"name": "addressinfo", "description": "Blockchain addresses public information."},
    {
        "name": "labels",
        "description": "Labels for transactions, addresses with additional information.",
    },
    {"name": "streams", "description": "Operations with data streams and filters."},
    {"name": "subscriptions", "description": "Operations with user subscriptions."},
    {"name": "time", "description": "Server timestamp endpoints."},
    {"name": "tokens", "description": "Operations with user tokens."},
    {"name": "txinfo", "description": "Ethereum transactions info."},
    {"name": "users", "description": "Operations with users."},
    {"name": "whales", "description": "Whales summaries"},
]

app = FastAPI(
    title=f"Moonstream API",
    description="Moonstream API endpoints.",
    version=MOONSTREAMAPI_VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)

whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(
    {
        "/ping": "GET",
        "/version": "GET",
        "/now": "GET",
        "/docs": "GET",
        "/openapi.json": "GET",
        "/streams/info": "GET",
        "/subscriptions/types": "GET",
        "/users": "POST",
        "/users/token": "POST",
        "/users/password/reset_initiate": "POST",
        "/users/password/reset_complete": "POST",
    }
)
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", response_model=data.PingResponse)
async def ping_handler() -> data.PingResponse:
    """
    Check server status.
    """
    return data.PingResponse(status="ok")


@app.get("/version", response_model=data.VersionResponse)
async def version_handler() -> data.VersionResponse:
    """
    Get server version.
    """
    return data.VersionResponse(version=MOONSTREAMAPI_VERSION)


@app.get("/now", tags=["time"])
async def now_handler() -> data.NowResponse:
    """
    Get server current time.
    """
    return data.NowResponse(epoch_time=time.time())


@app.get("/status", response_model=data.StatusResponse)
async def status_handler() -> data.StatusResponse:
    """
    Find latest crawlers records with creation timestamp:
    - ethereum_txpool
    - ethereum_trending
    """
    try:
        crawl_types_timestamp = actions.check_api_status()
    except actions.StatusAPIException:
        raise MoonstreamHTTPException(status_code=500)
    except Exception as e:
        logger.error(f"Unhandled status exception, error: {e}")
        raise MoonstreamHTTPException(status_code=500)

    return data.StatusResponse(
        ethereum_txpool_timestamp=crawl_types_timestamp["ethereum_txpool"],
        ethereum_trending_timestamp=crawl_types_timestamp["ethereum_trending"],
    )


app.include_router(addressinfo_router)
app.include_router(streams_router)
app.include_router(subscriptions_router)
app.include_router(txinfo_router)
app.include_router(users_router)
app.include_router(whales_router)
app.include_router(dashboards_router)
