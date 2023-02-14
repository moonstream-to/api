"""
The Moonstream subscriptions HTTP API
"""
import hashlib
import json
import logging
from pprint import pprint
from typing import Any, Dict, List, Optional

from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from entity.exceptions import EntityUnexpectedResponse
from fastapi import APIRouter, Depends, Request, Form, BackgroundTasks
from web3 import Web3

from ..actions import (
    validate_abi_json,
    apply_moonworm_tasks,
    get_entity_subscription_collection_id,
    EntityCollectionNotFoundException,
)
from ..admin import subscription_types
from .. import data
from ..admin import subscription_types
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import bugout_client as bc, entity_client as ec
from ..web3_provider import yield_web3_provider


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/subscriptions",
)

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"
BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION = "entity_subscription"


@router.post("/", tags=["subscriptions"], response_model=data.SubscriptionResourceData)
async def add_subscription_handler(
    request: Request,
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
    else:
        raise MoonstreamHTTPException(
            status_code=400,
            detail="Currently ethereum_whalewatch not supported",
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

    content: Dict[str, Any] = {}

    if abi:

        try:
            json_abi = json.loads(abi)
        except json.JSONDecodeError:
            raise MoonstreamHTTPException(status_code=400, detail="Malformed abi body.")

        validate_abi_json(json_abi)

        abi_string = json.dumps(json_abi, sort_keys=True, indent=2)

        hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

        content["abi"] = abi
        content["abi_hash"] = hash

        background_tasks.add_task(
            apply_moonworm_tasks,
            subscription_type_id,
            json_abi,
            address,
        )

    try:

        collection_id = get_entity_subscription_collection_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=token,
            user_id=user.id,
            create_if_not_exist=True,
        )

        entity = ec.add_entity(
            token=token,
            collection_id=collection_id,
            address=address,
            blockchain=subscription_types.CANONICAL_SUBSCRIPTION_TYPES[
                subscription_type_id
            ].blockchain,
            name=label,
            required_fields=[
                {"type": "subscription"},
                {"subscription_type_id": f"{subscription_type_id}"},
                {"color": f"{color}"},
                {"label": f"{label}"},
                {"user_id": f"{user.id}"},
            ],
            secondary_fields=content,
        )
    except EntityCollectionNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions collection not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Failed to get collection id")
        raise MoonstreamHTTPException(
            status_code=500,
            internal_error=e,
            detail="Currently unable to get collection id",
        )

    return data.SubscriptionResourceData(
        id=str(entity.entity_id),
        user_id=str(user.id),
        address=address,
        color=color,
        label=label,
        abi=entity.secondary_fields.get("abi"),
        subscription_type_id=subscription_type_id,
        updated_at=entity.updated_at,
        created_at=entity.created_at,
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
    user = request.state.user
    try:

        collection_id = get_entity_subscription_collection_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=token,
            user_id=user.id,
        )

        deleted_entity = ec.delete_entity(
            token=token,
            collection_id=collection_id,
            entity_id=subscription_id,
        )
    except EntityCollectionNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions collection not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Failed to delete subscription")
        raise MoonstreamHTTPException(
            status_code=500,
            detail="Internal error",
        )

    tags = deleted_entity.required_fields

    subscription_type_id = None
    color = None
    label = None
    abi = None

    if tags is not None:
        for tag in tags:

            if "subscription_type_id" in tag:
                subscription_type_id = tag["subscription_type_id"]

            if "color" in tag:
                color = tag["color"]

            if "label" in tag:
                label = tag["label"]

    if deleted_entity.secondary_fields is not None:
        abi = deleted_entity.secondary_fields.get("abi")

    return data.SubscriptionResourceData(
        id=str(deleted_entity.entity_id),
        user_id=str(user.id),
        address=deleted_entity.address,
        color=color,
        label=label,
        abi=abi,
        subscription_type_id=subscription_type_id,
        updated_at=deleted_entity.updated_at,
        created_at=deleted_entity.created_at,
    )


@router.get("/", tags=["subscriptions"], response_model=data.SubscriptionsListResponse)
async def get_subscriptions_handler(request: Request) -> data.SubscriptionsListResponse:
    """
    Get user's subscriptions.
    """
    token = request.state.token
    user = request.state.user
    try:
        collection_id = get_entity_subscription_collection_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=token,
            user_id=user.id,
        )

        subscriprions_list = ec.search_entities(
            token=token,
            collection_id=collection_id,
            required_field=[f"type:subscription"],
            limit=1000,
        )

        # resources: BugoutResources = bc.list_resources(token=token, params=params)
    except EntityCollectionNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions collection not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({user.id}) with token ({token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    subscriptions = []

    for subscription in subscriprions_list.entities:

        tags = subscription.required_fields

        label, color, subscription_type_id = None, None, None

        for tag in tags:

            if "subscription_type_id" in tag:
                subscription_type_id = tag["subscription_type_id"]

            if "color" in tag:
                color = tag["color"]

            if "label" in tag:
                label = tag["label"]

        subscriptions.append(
=======
=======
>>>>>>> Stashed changes
    pprint(resources.resources)

    return data.SubscriptionsListResponse(
        subscriptions=[
>>>>>>> Stashed changes
            data.SubscriptionResourceData(
                id=str(subscription.entity_id),
                user_id=str(user.id),
                address=subscription.address,
                color=color,
                label=label,
                abi=subscription.secondary_fields.get("abi"),
                subscription_type_id=subscription_type_id,
                updated_at=subscription.updated_at,
                created_at=subscription.created_at,
            )
        )

    return data.SubscriptionsListResponse(subscriptions=subscriptions)


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

    user = request.state.user

    update_required_fields = []

    update_secondary_fields = {}

    try:

        collection_id = get_entity_subscription_collection_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=token,
            user_id=user.id,
        )

        # get subscription entity
        subscription_entity = ec.get_entity(
            token=token,
            collection_id=collection_id,
            entity_id=subscription_id,
        )

        subscription_type_id = None

        update_required_fields = subscription_entity.required_fields

        print(update_required_fields)

        for field in update_required_fields:
            if "subscription_type_id" in field:
                subscription_type_id = field["subscription_type_id"]

        if not subscription_type_id:
            logger.error(
                f"Subscription entity {subscription_id} in collection {collection_id} has no subscription_type_id malformed subscription entity"
            )
            raise MoonstreamHTTPException(
                status_code=404,
                detail="Not valid subscription entity",
            )

    except EntityCollectionNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions collection not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(
            f"Error get subscriptions for user ({user.id}) with token ({token}), error: {str(e)}"
        )
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    for field in update_required_fields:
        if "color" in field and color is not None:
            field["color"] = color

        if "label" in field and label is not None:
            field["label"] = label

    if abi:

        try:
            json_abi = json.loads(abi)
        except json.JSONDecodeError:
            raise MoonstreamHTTPException(status_code=400, detail="Malformed abi body.")

        validate_abi_json(json_abi)

        abi_string = json.dumps(json_abi, sort_keys=True, indent=2)

        update_secondary_fields["abi"] = abi_string
        hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

        update_secondary_fields["abi_hash"] = hash
    else:
        update_secondary_fields = subscription_entity.secondary_fields

    try:

        subscription = ec.update_entity(
            token=token,
            collection_id=collection_id,
            entity_id=subscription_id,
            address=subscription_entity.address,
            blockchain=subscription_entity.blockchain,
            name=subscription_entity.name,
            required_fields=update_required_fields,
            secondary_fields=update_secondary_fields,
        )

    except Exception as e:
        logger.error(f"Error getting user subscriptions: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if abi:
        background_tasks.add_task(
            apply_moonworm_tasks,
            subscription_type_id,
            json_abi,
            subscription.address,
        )

    return data.SubscriptionResourceData(
        id=str(subscription.entity_id),
        user_id=str(user.id),
        address=subscription.address,
        color=color,
        label=label,
        abi=subscription.secondary_fields.get("abi"),
        subscription_type_id=subscription_type_id,
        updated_at=subscription_entity.updated_at,
        created_at=subscription_entity.created_at,
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
    user = request.state.user

    try:

        collection_id = get_entity_subscription_collection_id(
            resource_type=BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
            token=token,
            user_id=user.id,
        )

        # get subscription entity
        subscription_resource = ec.get_entity(
            token=token,
            collection_id=collection_id,
            entity_id=subscription_id,
        )

    except EntityCollectionNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions collection not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(
            f"Error get subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if "abi" not in subscription_resource.secondary_fields.keys():
        raise MoonstreamHTTPException(status_code=404, detail="Abi not found")

    return data.SubdcriptionsAbiResponse(
        abi=subscription_resource.secondary_fields["abi"]
    )


@router.get(
    "/types", tags=["subscriptions"], response_model=data.SubscriptionTypesListResponse
)
async def list_subscription_types() -> data.SubscriptionTypesListResponse:
    """
    Get availables subscription types.
    """
    print("list_subscription_types")
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
