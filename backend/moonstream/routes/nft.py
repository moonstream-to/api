"""
Moonstream's /nft endpoints.

These endpoints provide public access to NFT market summaries. No authentication required.
"""
import logging
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from . import data
from ..settings import DOCS_TARGET_PATH, ORIGINS
from ..version import MOONSTREAM_VERSION

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "nft", "description": "NFT market summaries"},
]

app = FastAPI(
    title=f"Moonstream /nft API",
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


@app.get("/", tags=["streams"], response_model=data.GetEventsResponse)
async def stream_handler(
    start_time: int = Query(0),
    end_time: Optional[int] = Query(None),
    include_start: bool = Query(False),
    include_end: bool = Query(False),
) -> data.GetEventsResponse:
    pass
