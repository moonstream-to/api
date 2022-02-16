"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Any, Dict, List, Optional

from bugout.data import BugoutResource
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from moonstreamdb import db

from .. import data, stream_queries
from ..middleware import MoonstreamHTTPException
from ..providers import (
    ReceivingEventsException,
    event_providers,
    get_events,
    latest_events,
    next_event,
    previous_event,
)
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
)
from ..settings import bugout_client as bc
from .subscriptions import BUGOUT_RESOURCE_TYPE_SUBSCRIPTION

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/streams",
)


def get_user_subscriptions(token: str) -> Dict[str, List[BugoutResource]]:
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
    user_subscriptions: Dict[str, List[BugoutResource]] = {}
    for subscription in response.resources:
        subscription_type = subscription.resource_data.get("subscription_type_id")
        if subscription_type is None:
            continue
        if user_subscriptions.get(subscription_type) is None:
            user_subscriptions[subscription_type] = []
        user_subscriptions[subscription_type].append(subscription)

    return user_subscriptions


@router.get("/info", tags=["streams"])
async def info_handler() -> Dict[str, Any]:
    info = {
        event_type: {
            "description": provider.description,
            "default_time_interval_seconds": provider.default_time_interval_seconds,
            "estimated_events_per_time_interval": provider.estimated_events_per_time_interval,
        }
        for event_type, provider in event_providers.items()
    }
    return info


@router.get("/", tags=["streams"], response_model=data.GetEventsResponse)
async def stream_handler(
    request: Request,
    q: str = Query(""),
    start_time: int = Query(0),
    end_time: Optional[int] = Query(None),
    include_start: bool = Query(False),
    include_end: bool = Query(False),
    db_session: Session = Depends(db.yield_db_session),
) -> data.GetEventsResponse:
    """
    Gets all events in the client's stream subject to the constraints defined by the following query
    parameters:
    - q: Query string which filters over subscriptions
    - start_time, end_time, include_start, include_end: These define the window of time from which
    we want to retrieve events.

    All times must be given as seconds since the Unix epoch.
    """

    stream_boundary = data.StreamBoundary(
        start_time=start_time,
        end_time=end_time,
        include_start=include_start,
        include_end=include_end,
    )

    user_subscriptions = get_user_subscriptions(request.state.token)
    query = stream_queries.StreamQuery(
        subscription_types=[subtype for subtype in event_providers], subscriptions=[]
    )
    if q.strip() != "":
        query = stream_queries.parse_query_string(q)

    try:
        _, events = get_events(
            db_session,
            bc,
            MOONSTREAM_DATA_JOURNAL_ID,
            MOONSTREAM_ADMIN_ACCESS_TOKEN,
            stream_boundary,
            query,
            user_subscriptions,
            result_timeout=10.0,
            raise_on_error=True,
        )
    except ReceivingEventsException as e:
        logger.error("Error receiving events from provider")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    except Exception as e:
        logger.error("Unable to get events")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    response = data.GetEventsResponse(stream_boundary=stream_boundary, events=events)
    return response


@router.get("/latest", tags=["streams"])
async def latest_events_handler(
    request: Request, q=Query(""), db_session: Session = Depends(db.yield_db_session)
) -> List[data.Event]:
    """
    Gets the latest events in the client's stream subject to the constraints defined by the following query
    parameters:
    - q: Query string which filters over subscriptions

    All times must be given as seconds since the Unix epoch.
    """

    user_subscriptions = get_user_subscriptions(request.state.token)
    query = stream_queries.StreamQuery(
        subscription_types=[subtype for subtype in event_providers], subscriptions=[]
    )
    if q.strip() != "":
        query = stream_queries.parse_query_string(q)

    try:
        events = latest_events(
            db_session,
            bc,
            MOONSTREAM_DATA_JOURNAL_ID,
            MOONSTREAM_ADMIN_ACCESS_TOKEN,
            query,
            1,
            user_subscriptions,
            result_timeout=6.0,
            raise_on_error=True,
            sort_events=True,
        )
    except ReceivingEventsException as e:
        logger.error("Error receiving events from provider")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    except Exception as e:
        logger.error("Unable to get latest events")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return events


@router.get("/next", tags=["stream"])
async def next_event_handler(
    request: Request,
    q: str = Query(""),
    start_time: int = Query(0),
    end_time: Optional[int] = Query(None),
    include_start: bool = Query(False),
    include_end: bool = Query(False),
    db_session: Session = Depends(db.yield_db_session),
) -> Optional[data.Event]:
    """
    Gets the next event in the client's stream subject to the constraints defined by the following query
    parameters:
    - q: Query string which filters over subscriptions
    - start_time, end_time, include_start, include_end: These define the window of time after which
    we want to retrieve the next event.

    All times must be given as seconds since the Unix epoch.
    """
    stream_boundary = data.StreamBoundary(
        start_time=start_time,
        end_time=end_time,
        include_start=include_start,
        include_end=include_end,
    )

    user_subscriptions = get_user_subscriptions(request.state.token)
    query = stream_queries.StreamQuery(
        subscription_types=[subtype for subtype in event_providers], subscriptions=[]
    )
    if q.strip() != "":
        query = stream_queries.parse_query_string(q)

    try:
        event = next_event(
            db_session,
            bc,
            MOONSTREAM_DATA_JOURNAL_ID,
            MOONSTREAM_ADMIN_ACCESS_TOKEN,
            stream_boundary,
            query,
            user_subscriptions,
            result_timeout=6.0,
            raise_on_error=True,
        )
    except ReceivingEventsException as e:
        logger.error("Error receiving events from provider")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    except Exception as e:
        logger.error("Unable to get next events")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return event


@router.get("/previous", tags=["stream"])
async def previous_event_handler(
    request: Request,
    q: str = Query(""),
    start_time: int = Query(0),
    end_time: Optional[int] = Query(None),
    include_start: bool = Query(False),
    include_end: bool = Query(False),
    db_session: Session = Depends(db.yield_db_session),
) -> Optional[data.Event]:
    """
    Gets the previous event in the client's stream subject to the constraints defined by the following query
    parameters:
    - q: Query string which filters over subscriptions
    - start_time, end_time, include_start, include_end: These define the window of time before which
    we want to retrieve the previous event.

    All times must be given as seconds since the Unix epoch.
    """
    stream_boundary = data.StreamBoundary(
        start_time=start_time,
        end_time=end_time,
        include_start=include_start,
        include_end=include_end,
    )

    user_subscriptions = get_user_subscriptions(request.state.token)
    query = stream_queries.StreamQuery(
        subscription_types=[subtype for subtype in event_providers], subscriptions=[]
    )
    if q.strip() != "":
        query = stream_queries.parse_query_string(q)

    try:
        event = previous_event(
            db_session,
            bc,
            MOONSTREAM_DATA_JOURNAL_ID,
            MOONSTREAM_ADMIN_ACCESS_TOKEN,
            stream_boundary,
            query,
            user_subscriptions,
            result_timeout=6.0,
            raise_on_error=True,
        )
    except ReceivingEventsException as e:
        logger.error("Error receiving events from provider")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    except Exception as e:
        logger.error("Unable to get previous events")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return event
