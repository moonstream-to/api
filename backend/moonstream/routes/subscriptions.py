"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Dict, List

from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import Body, FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware

from .. import data
from ..middleware import BroodAuthMiddleware
from ..settings import (
    DOCS_TARGET_PATH,
    DOCS_PATHS,
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    ORIGINS,
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
whitelist_paths.update(
    {
        "/subscriptions/types": "GET"
    }
)
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)


@app.post("/", tags=["subscriptions"], response_model=data.SubscriptionResourceData)
async def add_subscription_handler(
    request: Request,  # subscription_data: data.CreateSubscriptionRequest = Body(...)
    address: str = Form(...),
    color: str = Form(...),
    label: str = Form(...),
    subscription_type_id: str = Form(...),
) -> data.SubscriptionResourceData:
    """
    Add subscription to blockchain stream data for user.
    """
    subscription_data = data.CreateSubscriptionRequest(
        address=address,
        color=color,
        label=label,
        subscription_type_id=subscription_type_id,
    )

    token = request.state.token

    params = {"type": "subscription_type"}

    # request availble subscriptions
    try:
        subscription_resources: BugoutResources = bc.list_resources(
            token=token, params=params
        )
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)

    # allowed subscriptions
    subscription_ids_list = [
        resource.resource_data["id"] for resource in subscription_resources.resources
    ]

    if subscription_data.subscription_type_id not in subscription_ids_list:
        raise HTTPException(
            status_code=403, detail="Subscription type is not avilable."
        )

    user = request.state.user

    # chek if that contract not already setted up

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

    return data.SubscriptionResourceData(
        id=str(resource.id),
        user_id=resource.resource_data["user_id"],
        address=resource.resource_data["address"],
        color=resource.resource_data["color"],
        label=resource.resource_data["label"],
        subscription_type_id=resource.resource_data["subscription_type_id"],
    )


@app.delete(
    "/{subscription_id}",
    tags=["subscriptions"],
    response_model=data.SubscriptionResourceData,
)
async def delete_subscription_handler(request: Request, subscription_id: str):
    """
    Delete subscriptions.
    """

    token = request.state.token
    try:
        deleted_resource = bc.delete_resource(token=token, resource_id=subscription_id)
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)

    return data.SubscriptionResourceData(
        id=str(deleted_resource.id),
        user_id=deleted_resource.resource_data["user_id"],
        address=deleted_resource.resource_data["address"],
        color=deleted_resource.resource_data["color"],
        label=deleted_resource.resource_data["label"],
        subscription_type_id=deleted_resource.resource_data["subscription_type_id"],
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
        if e.detail == "Resources not found":
            return data.SubscriptionsListResponse(subscriptions=[])
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)

    return data.SubscriptionsListResponse(
        subscriptions=[
            data.SubscriptionResourceData(
                id=str(resource.id),
                user_id=resource.resource_data["user_id"],
                address=resource.resource_data["address"],
                color=resource.resource_data["color"],
                label=resource.resource_data["label"],
                subscription_type_id=resource.resource_data["subscription_type_id"],
            )
            for resource in resources.resources
        ]
    )


@app.get(
    "/types", tags=["subscriptions"], response_model=data.SubscriptionTypesListResponce
)
async def get_available_subscriptions_type(
    request: Request,
) -> data.SubscriptionTypesListResponce:

    """
    Get available's subscriptions types.
    """
    params = {"type": "subscription_type"}
    try:
        resources: BugoutResources = bc.list_resources(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN, params=params
        )
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return data.SubscriptionTypesListResponce(
        subscriptions=[
            data.SubscriptionTypeResourceData.validate(resource.resource_data)
            for resource in resources.resources
        ]
    )
