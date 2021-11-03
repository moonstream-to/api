"""
The Moonstream subscriptions HTTP API
"""
import logging
import json
from typing import List, Optional, Dict, Any, Union

import boto3  # ignore
from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Request, Form

from ..admin import subscription_types
from .. import data
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
    MOONSTREAM_SMARTCONTRACTS_ABI_BUCKET,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
)

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
    abi: Optional[str] = Form(None),
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
        "abi": None,
        "bucket": None,
        "s3_path": None,
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

    if abi:

        # ABI validation

        try:
            json.loads(abi)
        except:
            raise MoonstreamHTTPException(status_code=400, detail="ABI is incorret")

        s3_client = boto3.client("s3")

        bucket = MOONSTREAM_SMARTCONTRACTS_ABI_BUCKET

        result_bytes = abi.encode("utf-8")
        result_key = (
            f"abi/v1/{resource.resource_data['address']}/{resource.id}/abi.json"
        )

        s3_client.put_object(
            Body=result_bytes,
            Bucket=bucket,
            Key=result_key,
            ContentType="application/json",
            Metadata={"Moonstream": "Abi data"},
        )

        update_resource = {}

        update_resource["abi"] = True

        update_resource["bucket"] = MOONSTREAM_SMARTCONTRACTS_ABI_BUCKET
        update_resource[
            "s3_path"
        ] = f"abi/v1/{resource.resource_data['address']}/{resource.id}/abi.json"

        try:
            updated_resource: BugoutResource = bc.update_resource(
                token=token,
                resource_id=resource.id,
                resource_data=data.SubscriptionUpdate(
                    update=update_resource,
                ).dict(),
            )
            resource = updated_resource
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
        abi=resource.resource_data.get("abi"),
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
        abi=deleted_resource.resource_data.get("abi"),
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
                abi=resource.resource_data.get("abi"),
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
    abi: Optional[str] = Form(None),
) -> data.SubscriptionResourceData:
    """
    Get user's subscriptions.
    """
    token = request.state.token

    update: Dict[str, Any] = {}

    if color:
        update["color"] = color

    if label:
        update["label"] = label

    if abi:

        # ABI validation

        try:
            json.loads(abi)
        except:
            raise MoonstreamHTTPException(status_code=400, detail="ABI is incorret")

        try:
            subscription: BugoutResource = bc.get_resource(
                token=token,
                resource_id=subscription_id,
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
        except BugoutResponseException as e:
            raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            logger.error(f"Error getting user subscriptions: {str(e)}")
            raise MoonstreamHTTPException(status_code=500, internal_error=e)

        if subscription.resource_data["abi"] is not None:
            raise MoonstreamHTTPException(
                status_code=403, detail="ABI can't be updated"
            )

        s3_client = boto3.client("s3")

        bucket = MOONSTREAM_SMARTCONTRACTS_ABI_BUCKET

        result_bytes = abi.encode("utf-8")
        result_key = (
            f"abi/v1/{subscription.resource_data['address']}/{subscription_id}/abi.json"
        )

        s3_client.put_object(
            Body=result_bytes,
            Bucket=bucket,
            Key=result_key,
            ContentType="application/json",
            Metadata={"Moonstream": "Abi data"},
        )

        update["abi"] = True

        update["bucket"] = MOONSTREAM_SMARTCONTRACTS_ABI_BUCKET
        update[
            "s3_path"
        ] = f"abi/v1/{subscription.resource_data['address']}/{subscription_id}/abi.json"

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
        abi=resource.resource_data.get("abi"),
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
