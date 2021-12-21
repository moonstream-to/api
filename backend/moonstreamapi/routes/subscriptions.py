"""
The Moonstream subscriptions HTTP API
"""
import hashlib
import json
import logging
from typing import Any, Dict, List, Optional

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Depends, Request, Form, BackgroundTasks
from web3 import Web3

from ..actions import validate_abi_json, upload_abi_to_s3, apply_moonworm_tasks
from ..admin import subscription_types
from .. import data
from ..actions import upload_abi_to_s3, validate_abi_json
from ..admin import subscription_types
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
)
from ..settings import bugout_client as bc
from ..web3_provider import yield_web3_provider

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/subscriptions",
)

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"


@router.post("/", tags=["subscriptions"], response_model=data.SubscriptionResourceData)
async def add_subscription_handler(
    request: Request,  # subscription_data: data.CreateSubscriptionRequest = Body(...)
    background_tasks: BackgroundTasks,
    address: str = Form(...),
    color: str = Form(...),
    label: str = Form(...),
    subscription_type_id: str = Form(...),
    abi: Optional[str] = Form(None),
    web3: Web3 = Depends(yield_web3_provider),
) -> data.SubscriptionResourceData:
    """
    Add subscription to blockchain stream data for user.
    """
    token = request.state.token

    if subscription_type_id != "ethereum_whalewatch":
        try:
            address = web3.toChecksumAddress(address)
        except ValueError as e:
            raise MoonstreamHTTPException(
                status_code=400,
                detail=str(e),
                internal_error=e,
            )
        except Exception as e:
            logger.error(f"Failed to convert address to checksum address")
            raise MoonstreamHTTPException(
                status_code=500,
                internal_error=e,
                detail="Currently unable to convert address to checksum address",
            )

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

        try:
            json_abi = json.loads(abi)
        except json.JSONDecodeError:
            raise MoonstreamHTTPException(status_code=400, detail="Malformed abi body.")

        validate_abi_json(json_abi)

        update_resource = upload_abi_to_s3(resource=resource, abi=abi, update={})

        abi_string = json.dumps(json_abi, sort_keys=True, indent=2)

        hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

        update_resource["abi_hash"] = hash

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

        background_tasks.add_task(
            apply_moonworm_tasks,
            subscription_type_id,
            json_abi,
            address,
        )

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
    background_tasks: BackgroundTasks,
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

        try:
            json_abi = json.loads(abi)
        except json.JSONDecodeError:
            raise MoonstreamHTTPException(status_code=400, detail="Malformed abi body.")

        validate_abi_json(json_abi)

        abi_string = json.dumps(json_abi, sort_keys=True, indent=2)

        hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

        try:
            subscription_resource: BugoutResource = bc.get_resource(
                token=token,
                resource_id=subscription_id,
            )
        except BugoutResponseException as e:
            raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            logger.error(f"Error creating subscription resource: {str(e)}")
            raise MoonstreamHTTPException(status_code=500, internal_error=e)

        if subscription_resource.resource_data["abi"] is not None:
            raise MoonstreamHTTPException(
                status_code=400,
                detail="Subscription already have ABI. For add a new ABI create new subscription.",
            )

        update = upload_abi_to_s3(
            resource=subscription_resource, abi=abi, update=update
        )

        update["abi_hash"] = hash

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

    if abi:
        background_tasks.add_task(
            apply_moonworm_tasks,
            subscription_resource.resource_data["subscription_type_id"],
            json_abi,
            subscription_resource.resource_data["address"],
        )

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
    "/{subscription_id}/abi",
    tags=["subscriptions"],
    response_model=data.SubdcriptionsAbiResponse,
)
async def get_subscription_abi_handler(
    request: Request,
    subscription_id: str,
) -> data.SubdcriptionsAbiResponse:

    token = request.state.token

    try:
        subscription_resource: BugoutResource = bc.get_resource(
            token=token,
            resource_id=subscription_id,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating subscription resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if subscription_resource.resource_data["abi"] is None:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="Subscription abi not exists.",
        )

    s3_client = boto3.client("s3")

    result_key = f"{subscription_resource.resource_data['s3_path']}"
    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": subscription_resource.resource_data["bucket"],
            "Key": result_key,
        },
        ExpiresIn=300,
        HttpMethod="GET",
    )

    return data.SubdcriptionsAbiResponse(url=presigned_url)


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
