"""
The Mooncrawl HTTP API
"""
import logging
import time
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import data
from .middleware import MoonstreamHTTPException
from .settings import DOCS_TARGET_PATH, ORIGINS
from .version import MOONCRAWL_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


tags_metadata = [
    {"name": "jobs", "description": "Trigger crawler jobs."},
    {"name": "time", "description": "Server timestamp endpoints."},
]

app = FastAPI(
    title=f"Mooncrawl HTTP API",
    description="Mooncrawl API endpoints.",
    version=MOONCRAWL_VERSION,
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
    return data.VersionResponse(version=MOONCRAWL_VERSION)


@app.get("/now", tags=["time"])
async def now_handler() -> data.NowResponse:
    """
    Get server current time.
    """
    return data.NowResponse(epoch_time=time.time())


@app.get("/jobs/stats_update", tags=["jobs"])
async def status_handler():
    """
    Find latest crawlers records with creation timestamp:
    - ethereum_txpool
    - ethereum_trending
    """
    try:
        pass
    except Exception as e:
        logger.error(f"Unhandled status exception, error: {e}")
        raise MoonstreamHTTPException(status_code=500)

    return
