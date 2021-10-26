"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import List, Optional

from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Form, Request

from .. import data
from ..admin import subscription_types
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import MOONSTREAM_APPLICATION_ID
from ..settings import bugout_client as bc

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/subscriptions",
)

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"


@router.post("/", tags=["subscriptions"], response_model=data.SubscriptionResourceData)
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
    token = request.state.token

    active_subscription_types_response = subscription_types.list_subscription_types(
        active_only=True
    )
    available_subscription_type_ids = [
        subscription_type.resource_data.get("id")
        for subscription_type in active_subscription_types_response.resources
        if subscription_type.resource_data.get("id") is not None
    ]

    if subscription_type_id not in available_subscription_type_ids:
        raise MoonstreamHTTPException(
            status_code=404,
            detail=f"Invalid subscription type: {subscription_type_id}.",
        )

    user = request.state.user

    resource_data = {
        "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
        "user_id": str(user.id),
        "subscription_type_id": subscription_type_id,
        "address": address,
        "color": color,
        "label": label,
    }

    try:
        resource: BugoutResource = bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data=resource_data,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating subscription resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return data.SubscriptionResourceData(
        id=str(resource.id),
        user_id=resource.resource_data["user_id"],
        address=resource.resource_data["address"],
        color=resource.resource_data["color"],
        label=resource.resource_data["label"],
        subscription_type_id=resource.resource_data["subscription_type_id"],
        updated_at=resource.updated_at,
        created_at=resource.created_at,
    )


@router.delete(
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
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error deleting subscription: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return data.SubscriptionResourceData(
        id=str(deleted_resource.id),
        user_id=deleted_resource.resource_data["user_id"],
        address=deleted_resource.resource_data["address"],
        color=deleted_resource.resource_data["color"],
        label=deleted_resource.resource_data["label"],
        subscription_type_id=deleted_resource.resource_data["subscription_type_id"],
        updated_at=deleted_resource.updated_at,
        created_at=deleted_resource.created_at,
    )


@router.get("/", tags=["subscriptions"], response_model=data.SubscriptionsListResponse)
async def get_subscriptions_handler(request: Request) -> data.SubscriptionsListResponse:
    """
    Get user's subscriptions.
    """
    token = request.state.token
    params = {
        "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
        "user_id": str(request.state.user.id),
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return data.SubscriptionsListResponse(
        subscriptions=[
            data.SubscriptionResourceData(
                id=str(resource.id),
                user_id=resource.resource_data["user_id"],
                address=resource.resource_data["address"],
                color=resource.resource_data["color"],
                label=resource.resource_data["label"],
                subscription_type_id=resource.resource_data["subscription_type_id"],
                updated_at=resource.updated_at,
                created_at=resource.created_at,
            )
            for resource in resources.resources
        ]
    )


@router.put(
    "/{subscription_id}",
    tags=["subscriptions"],
    response_model=data.SubscriptionResourceData,
)
async def update_subscriptions_handler(
    request: Request,
    subscription_id: str,
    color: Optional[str] = Form(None),
    label: Optional[str] = Form(None),
) -> data.SubscriptionResourceData:
    """
    Get user's subscriptions.
    """
    token = request.state.token

    update = {}

    if color:
        update["color"] = color

    if label:
        update["label"] = label

    try:
        resource: BugoutResource = bc.update_resource(
            token=token,
            resource_id=subscription_id,
            resource_data=data.SubscriptionUpdate(
                update=update,
            ).dict(),
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error getting user subscriptions: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return data.SubscriptionResourceData(
        id=str(resource.id),
        user_id=resource.resource_data["user_id"],
        address=resource.resource_data["address"],
        color=resource.resource_data["color"],
        label=resource.resource_data["label"],
        subscription_type_id=resource.resource_data["subscription_type_id"],
        updated_at=resource.updated_at,
        created_at=resource.created_at,
    )


@router.get(
    "/types", tags=["subscriptions"], response_model=data.SubscriptionTypesListResponse
)
async def list_subscription_types() -> data.SubscriptionTypesListResponse:
    """
    Get availables subscription types.
    """
    results: List[data.SubscriptionTypeResourceData] = []
    try:
        response = subscription_types.list_subscription_types()
        results = [
            data.SubscriptionTypeResourceData.validate(resource.resource_data)
            for resource in response.resources
        ]
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error reading subscription types from Brood API: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return data.SubscriptionTypesListResponse(subscription_types=results)
