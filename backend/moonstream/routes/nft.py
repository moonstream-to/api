"""
Moonstream's /nft endpoints.

These endpoints provide public access to NFT market summaries. No authentication required.
"""
from datetime import datetime
import logging
from typing import Optional

from fastapi import Depends, FastAPI, Query
from moonstreamdb import db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .. import data
from ..providers.bugout import nft_summary_provider
from ..settings import (
    bugout_client,
    DOCS_TARGET_PATH,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
    ORIGINS,
)
from ..stream_queries import StreamQuery
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
    db_session: Session = Depends(db.yield_db_session),
) -> data.GetEventsResponse:
    stream_boundary = data.StreamBoundary(
        start_time=start_time,
        end_time=end_time,
        include_start=include_start,
        include_end=include_end,
    )

    result = nft_summary_provider.get_events(
        db_session=db_session,
        bugout_client=bugout_client,
        data_journal_id=MOONSTREAM_DATA_JOURNAL_ID,
        data_access_token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        stream_boundary=stream_boundary,
        user_subscriptions={},
        query=StreamQuery(subscription_types=[nft_summary_provider.event_type]),
    )

    if result is None:
        return data.GetEventsResponse(stream_boundary=stream_boundary, events=[])

    provider_stream_boundary, events = result
    return data.GetEventsResponse(
        stream_boundary=provider_stream_boundary, events=events
    )
