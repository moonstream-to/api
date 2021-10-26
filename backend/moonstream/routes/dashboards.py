import logging
from typing import Any, List, Optional
from uuid import UUID

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Request, Form
from starlette.datastructures import Address

from .. import data
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
    SMARTCONTRACTS_ABI_BUCKET,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    SMARTCONTRACTS_ABI_BUCKET,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/dashboards",
)

BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"


@router.post("/", tags=["dashboards"], response_model=data.SubscriptionResourceData)
async def add_subscription_handler(
    request: Request,
    name: str = Form(...),
    subscriptions_list: List[UUID] = Form(...),
) -> BugoutResource:
    """
    Add subscription to blockchain stream data for user.
    """

    token = request.state.token

    user = request.state.user

    # Get all user subscriptions
    params = {
        "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
        "user_id": str(user.id),
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

    active_resources_ids = [
        resource.id
        for resource in resources.resources
        if resource.resource_data["active"]
    ]

    dashboard_subscriptions = [
        subscription_id
        for subscription_id in subscriptions_list
        if subscription_id in active_resources_ids
    ]

    dashboard_resource = data.DashboardResource(
        type=BUGOUT_RESOURCE_TYPE_DASHBOARD,
        user_id=user.id,
        name=name,
        dashboard_subscriptions=dashboard_subscriptions,
    )

    try:
        resource: BugoutResource = bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data=dashboard_resource.dict(),
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating subscription resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resource


@router.delete(
    "/{dashboard_id}",
    tags=["subscriptions"],
    response_model=data.SubscriptionResourceData,
)
async def delete_subscription_handler(request: Request, dashboard_id: str):
    """
    Delete subscriptions.
    """
    token = request.state.token
    try:
        deleted_resource = bc.delete_resource(token=token, resource_id=dashboard_id)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error deleting subscription: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return deleted_resource


@router.get("/", tags=["dashboards"], response_model=Any)
async def get_dashboards_handler(
    request: Request, limit: Optional[int], offset: Optional[int]
) -> Any:
    """
    Get user's subscriptions.
    """
    token = request.state.token
    params = {
        "type": BUGOUT_RESOURCE_TYPE_DASHBOARD,
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

    return resources.resources


@router.get("/{dashboarsd_id}", tags=["dashboards"], response_model=Any)
async def get_dashboard_handler(request: Request, dashboarsd_id: UUID) -> Any:
    """
    Get user's subscriptions.
    """
    token = request.state.token

    try:
        resource: BugoutResource = bc.get_resource(
            token=token,
            resource_id=dashboarsd_id,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    # if resources

    s3_client = boto3.client("s3")

    bucket = SMARTCONTRACTS_ABI_BUCKET

    abi_urls = []

    for subscription in resource.resource_data["dashboard_subscriptions"]:

        result_key = f"/v1/{subscription}/{resource.id}/abi.json"
        address_presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": result_key},
            ExpiresIn=300,
            HttpMethod="GET",
        )

        abi_urls.append(address_presigned_url)

    # dashboard response

    return abi_urls


@router.get("/{dashboard_is}/data", tags=["dashboards"], response_model=Any)
async def get_dashboard_data(request: Request) -> Any:
    """
    Get user's subscriptions.
    """

    token = request.state.token
    params = {
        "type": BUGOUT_RESOURCE_TYPE_DASHBOARD,
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

    return resources.resources
