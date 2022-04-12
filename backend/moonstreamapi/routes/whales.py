"""
Moonstream's /whales endpoints.

These endpoints provide public access to whale watch summaries. No authentication required.
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from moonstreamdb import db

from .. import data
from ..providers.bugout import ethereum_whalewatch_provider
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
    bugout_client,
)
from ..stream_queries import StreamQuery

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/whales")


@router.get("/", tags=["whales"], response_model=data.GetEventsResponse)
async def stream_handler(
    start_time: int = Query(0),
    end_time: Optional[int] = Query(None),
    include_start: bool = Query(False),
    include_end: bool = Query(False),
    db_session: Session = Depends(db.yield_db_session),
) -> data.GetEventsResponse:
    """
    Retrieves the list of whales spotted over given stream boundary

    - **start_time**: Timestamp. Must be provided otherwise this request will hang
    - **end_time**: Timestamp. Optional.
    - **include_start** (string): is start_time inclusive or not
    - **include_end** (string): is end_time inclusive or not
    """
    stream_boundary = data.StreamBoundary(
        start_time=start_time,
        end_time=end_time,
        include_start=include_start,
        include_end=include_end,
    )

    result = ethereum_whalewatch_provider.get_events(
        db_session=db_session,
        bugout_client=bugout_client,
        data_journal_id=MOONSTREAM_DATA_JOURNAL_ID,
        data_access_token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        stream_boundary=stream_boundary,
        user_subscriptions={ethereum_whalewatch_provider.event_type: []},
        query=StreamQuery(subscription_types=[ethereum_whalewatch_provider.event_type]),
    )

    if result is None:
        return data.GetEventsResponse(stream_boundary=stream_boundary, events=[])

    provider_stream_boundary, events = result
    return data.GetEventsResponse(
        stream_boundary=provider_stream_boundary, events=events
    )
