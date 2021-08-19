"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Any, Dict, List, Optional

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import FastAPI, HTTPException, Request, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from moonstreamdb import db
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user


from .. import data
from ..middleware import BroodAuthMiddleware
from ..providers import ethereum_blockchain
from ..settings import (
    DOCS_TARGET_PATH,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
    ORIGINS,
    DOCS_PATHS,
    bugout_client as bc,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
)
from .. import stream_queries
from .subscriptions import BUGOUT_RESOURCE_TYPE_SUBSCRIPTION
from ..version import MOONSTREAM_VERSION

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "streams", "description": "Operations with data stream and filters."},
]

app = FastAPI(
    title=f"Moonstream streams API.",
    description="Streams endpoints.",
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

whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(DOCS_PATHS)
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)


def get_user_subscriptions(token: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Returns the given user's subscriptions grouped by subscription type.
    """
    response = bc.list_resources(
        token=token,
        params={
            "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
        },
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    # TODO(andrey, kompotkot, zomglings): PAGINATION!!!
    user_subscriptions: Dict[str, List[Dict[str, Any]]] = {}
    for subscription in response.resources:
        subscription_type = subscription.resource_data.get("subscription_type_id")
        if subscription_type is None:
            continue
        if user_subscriptions.get(subscription_type) is None:
            user_subscriptions[subscription_type] = []
        user_subscriptions[subscription_type].append(subscription)

    return user_subscriptions


EVENT_PROVIDERS: Dict[str, Any] = {ethereum_blockchain.event_type: ethereum_blockchain}


@app.get("/", tags=["streams"], response_model=data.GetEventsResponse)
async def search_transactions(
    request: Request,
    q: str = Query(""),
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

    user_subscriptions = get_user_subscriptions(request.state.token)
    query = stream_queries.StreamQuery(
        subscription_types=[subtype for subtype in EVENT_PROVIDERS], subscriptions=[]
    )
    if q.strip() != "":
        query = stream_queries.parse_query_string(q)

    results = {
        event_type: provider.get_events(
            db_session,
            bc,
            MOONSTREAM_DATA_JOURNAL_ID,
            MOONSTREAM_ADMIN_ACCESS_TOKEN,
            stream_boundary,
            query,
            user_subscriptions,
        )
        for event_type, provider in EVENT_PROVIDERS.items()
    }
    events = [
        event
        for _, event_list in results.values()
        if event_list is not None
        for event in event_list
    ]
    events.sort(key=lambda event: event.event_timestamp, reverse=True)
    response = data.GetEventsResponse(stream_boundary=stream_boundary, events=events)
    return response
