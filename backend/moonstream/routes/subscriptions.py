"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Dict

from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .. import data
from ..middleware import BroodAuthMiddleware
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
    DOCS_TARGET_PATH,
    ORIGINS,
    DOCS_PATHS,
    bugout_client as bc,
)
from ..version import MOONSTREAM_VERSION

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "subscriptions", "description": "Operations with subscriptions."},
]

app = FastAPI(
    title=f"Moonstream subscriptions API.",
    description="User subscriptions endpoints.",
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


@app.post("/", tags=["subscriptions"], response_model=data.SubscriptionResponse)
async def add_subscription_handler(
    request: Request, subscription_data: data.SubscriptionRequest = Body(...)
) -> data.SubscriptionResponse:
    """
    Add subscription to blockchain stream data for user.
    """
    token = request.state.token
    user = request.state.user
    resource_data = {"user_id": str(user.id)}
    resource_data.update(subscription_data)
    try:
        resource: BugoutResource = bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data=resource_data,
        )
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return data.SubscriptionResponse(
        user_id=resource.resource_data["user_id"],
        blockchain=resource.resource_data["blockchain"],
    )


@app.get("/", tags=["subscriptions"], response_model=data.SubscriptionsListResponse)
async def get_subscriptions_handler(request: Request) -> data.SubscriptionsListResponse:
    """
    Get user's subscriptions.
    """
    token = request.state.token
    params = {"user_id": str(request.state.user.id)}
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return data.SubscriptionsListResponse(
        subscriptions=[
            data.SubscriptionResponse(
                user_id=resource.resource_data["user_id"],
                blockchain=resource.resource_data["blockchain"],
            )
            for resource in resources.resources
        ]
    )
