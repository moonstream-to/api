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


from .. import data
from ..middleware import BroodAuthMiddleware
from ..providers import ethereum_blockchain
from ..settings import (
    DOCS_TARGET_PATH,
    ORIGINS,
    DOCS_PATHS,
    bugout_client as bc,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
)
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

    # TODO(kompotkot, zomglings): PAGINATION!!!
    user_subscriptions: Dict[str, List[Dict[str, Any]]] = {}
    for subscription in response.resources:
        subscription_type = subscription.get("subscription_type_id")
        if subscription_type is None:
            continue
        if user_subscriptions.get(subscription_type) is None:
            user_subscriptions[subscription_type] = []
        user_subscriptions[subscription_type].append(subscription)

    return user_subscriptions


@app.get("/", tags=["streams"])
async def search_transactions(
    request: Request,
    q: str = Query(""),
    start_time: Optional[int] = Query(0),
    end_time: Optional[int] = Query(0),
    include_start: Optional[bool] = Query(False),
    include_end: Optional[bool] = Query(False),
    db_session: Session = Depends(db.yield_db_session),
):
    # get user subscriptions
    token = request.state.token
    params = {"user_id": str(request.state.user.id)}
    try:
        # TODO(andrey, kompotkot): This query should filter resources of type "subscription". We may
        # create other resources for users. When we do, I think this code will break.
        # See how we apply this filter for "type": "subscription_type" in the /subscriptions route.
        user_subscriptions_resources: BugoutResources = bc.list_resources(
            token=token, params=params
        )
    except BugoutResponseException as e:
        if e.detail == "Resources not found":
            return data.EthereumTransactionResponse(stream=[])
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)

    # TODO(andrey, kompotkot): Pagination over resources!!
    # Issue: https://github.com/bugout-dev/brood/issues/14
    address_to_subscriptions = {
        resource.resource_data["address"]: resource.resource_data
        for resource in user_subscriptions_resources.resources
    }

    boundaries = data.PageBoundary(
        start_time=start_time,
        end_time=end_time,
        next_event_time=0,
        previous_event_time=0,
        include_start=include_start,
        include_end=include_end,
    )

    if address_to_subscriptions:
        response = await ethereum_blockchain.get_transaction_in_blocks(
            db_session=db_session,
            query=q,
            user_subscriptions_resources_by_address=address_to_subscriptions,
            boundaries=boundaries,
        )
        return response
    else:
        return data.EthereumTransactionResponse(stream=[], boundaries=boundaries)
