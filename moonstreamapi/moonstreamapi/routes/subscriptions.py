"""
The Moonstream subscriptions HTTP API
"""
import hashlib
import json
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Union, cast

from bugout.data import BugoutSearchResult, BugoutSearchResultAsEntity
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, BackgroundTasks, Depends, Form, Path, Query, Request
from moonstreamdb.blockchain import AvailableBlockchainType
from web3 import Web3

from .. import data
from ..actions import (
    AddressNotSmartContractException,
    EntityJournalNotFoundException,
    apply_moonworm_tasks,
    check_if_smart_contract,
    get_entity_subscription_journal_id,
    get_list_of_support_interfaces,
    validate_abi_json,
)
from ..admin import subscription_types
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_ENTITIES_RESERVED_TAGS,
    THREAD_TIMEOUT_SECONDS,
)
from ..settings import bugout_client as bc
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
    web3: Web3 = Depends(yield_web3_provider),
) -> data.SubscriptionResourceData:
    """
    Add subscription to blockchain stream data for user.
    """
    token = request.state.token

    form = await request.form()

    try:
        form_data = data.CreateSubscriptionRequest(**form)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=400, detail=str(e))

    address = form_data.address
    color = form_data.color
    label = form_data.label
    abi = form_data.abi
    description = form_data.description
    tags = form_data.tags
    subscription_type_id = form_data.subscription_type_id

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

    if description:
        content["description"] = description

    allowed_required_fields: List[Any] = []
    if tags:
        allowed_required_fields = [
            item
            for item in tags
            if not any(key in item for key in MOONSTREAM_ENTITIES_RESERVED_TAGS)
        ]

    required_fields: List[Dict[str, Union[str, bool, int, List[Any]]]] = [
        {"type": "subscription"},
        {"subscription_type_id": f"{subscription_type_id}"},
        {"color": f"{color}"},
        {"label": f"{label}"},
        {"user_id": f"{user.id}"},
    ]

    if allowed_required_fields:
        required_fields.extend(allowed_required_fields)

    try:
        journal_id = get_entity_subscription_journal_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            user_id=user.id,
            create_if_not_exist=True,
        )
        blockchain = subscription_types.CANONICAL_SUBSCRIPTION_TYPES[
            subscription_type_id
        ].blockchain
        entity = bc.create_entity(
            token=token,
            journal_id=journal_id,
            address=address,
            blockchain=blockchain if blockchain is not None else "",
            title=label,
            required_fields=required_fields,
            secondary_fields=content,
        )
    except EntityJournalNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions journal not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Failed to get journal id")
        raise MoonstreamHTTPException(
            status_code=500,
            internal_error=e,
            detail="Currently unable to get journal id",
        )
    entity_required_fields = (
        entity.required_fields if entity.required_fields is not None else []
    )
    entity_secondary_fields = (
        entity.secondary_fields if entity.secondary_fields is not None else {}
    )
    normalized_entity_tags = [
        f"{key}:{value}"
        for tag in entity_required_fields
        for key, value in tag.items()
        if key not in MOONSTREAM_ENTITIES_RESERVED_TAGS
    ]

    return data.SubscriptionResourceData(
        id=str(entity.id),
        user_id=str(user.id),
        address=address,
        color=color,
        label=label,
        abi=entity_secondary_fields.get("abi"),
        description=entity_secondary_fields.get("description"),
        tags=normalized_entity_tags,
        subscription_type_id=subscription_type_id,
        updated_at=entity.updated_at,
        created_at=entity.created_at,
    )


@router.delete(
    "/{subscription_id}",
    tags=["subscriptions"],
    response_model=data.SubscriptionResourceData,
)
async def delete_subscription_handler(
    request: Request, subscription_id: str = Path(...)
):
    """
    Delete subscriptions.
    """
    token = request.state.token
    user = request.state.user
    try:
        journal_id = get_entity_subscription_journal_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            user_id=user.id,
        )
        deleted_entity = bc.delete_entity(
            token=token,
            journal_id=journal_id,
            entity_id=subscription_id,
        )
    except EntityJournalNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions journal not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Failed to delete subscription")
        raise MoonstreamHTTPException(
            status_code=500,
            detail="Internal error",
        )

    tags_raw = (
        deleted_entity.required_fields
        if deleted_entity.required_fields is not None
        else {}
    )

    subscription_type_id = None
    color = None
    label = None
    abi = None
    description = None

    for tag in tags_raw:
        if "subscription_type_id" in tag:
            subscription_type_id = tag["subscription_type_id"]
        if "color" in tag:
            color = tag["color"]
        if "label" in tag:
            label = tag["label"]

    normalized_entity_tags = [
        f"{key}:{value}"
        for tag in tags_raw
        for key, value in tag.items()
        if key not in MOONSTREAM_ENTITIES_RESERVED_TAGS
    ]

    if deleted_entity.secondary_fields is not None:
        abi = deleted_entity.secondary_fields.get("abi")
        description = deleted_entity.secondary_fields.get("description")

    return data.SubscriptionResourceData(
        id=str(deleted_entity.id),
        user_id=str(user.id),
        address=deleted_entity.address,
        color=color,
        label=label,
        abi=abi,
        description=description,
        tags=normalized_entity_tags,
        subscription_type_id=subscription_type_id,
        updated_at=deleted_entity.updated_at,
        created_at=deleted_entity.created_at,
    )


@router.get("/", tags=["subscriptions"], response_model=data.SubscriptionsListResponse)
async def get_subscriptions_handler(
    request: Request,
    limit: int = Query(10),
    offset: int = Query(0),
) -> data.SubscriptionsListResponse:
    """
    Get user's subscriptions.
    """
    token = request.state.token
    user = request.state.user
    try:
        journal_id = get_entity_subscription_journal_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            user_id=user.id,
            create_if_not_exist=True,
        )
        subscriptions_list: Any = bc.search(
            token=token,
            journal_id=journal_id,
            query="tag:type:subscription",
            limit=limit,
            offset=offset,
            representation="entity",
        )

    except EntityJournalNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions journal not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({user.id}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    subscriptions = []

    user_subscriptions_results = cast(
        List[BugoutSearchResultAsEntity], subscriptions_list.results
    )

    for subscription in user_subscriptions_results:
        tags = subscription.required_fields

        label, color, subscription_type_id = None, None, None

        for tag in tags:
            if "subscription_type_id" in tag:
                subscription_type_id = tag["subscription_type_id"]

            if "color" in tag:
                color = tag["color"]

            if "label" in tag:
                label = tag["label"]

        normalized_entity_tags = [
            f"{key}:{value}"
            for tag in tags
            for key, value in tag.items()
            if key not in MOONSTREAM_ENTITIES_RESERVED_TAGS
        ]

        subscriptions.append(
            data.SubscriptionResourceData(
                id=str(subscription.entity_url.split("/")[-1]),
                user_id=str(user.id),
                address=subscription.address,
                color=color,
                label=label,
                abi="True"
                if subscription.secondary_fields.get("abi", None)
                else "False",  ### TODO(ANDREY): remove this hack when frontend is updated
                description=subscription.secondary_fields.get("description"),
                tags=normalized_entity_tags,
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
    background_tasks: BackgroundTasks,
    subscription_id: str = Path(...),
) -> data.SubscriptionResourceData:
    """
    Get user's subscriptions.
    """
    token = request.state.token

    user = request.state.user

    form = await request.form()
    try:
        form_data = data.UpdateSubscriptionRequest(**form)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=400, detail=str(e))

    color = form_data.color
    label = form_data.label
    abi = form_data.abi
    description = form_data.description
    tags = form_data.tags

    try:
        journal_id = get_entity_subscription_journal_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            user_id=user.id,
        )

        # get subscription entity
        subscription_entity = bc.get_entity(
            token=token,
            journal_id=journal_id,
            entity_id=subscription_id,
        )

        update_required_fields = []
        if subscription_entity.required_fields is not None:
            update_required_fields = [
                field
                for field in subscription_entity.required_fields
                if any(key in field for key in MOONSTREAM_ENTITIES_RESERVED_TAGS)
            ]

        update_secondary_fields = (
            subscription_entity.secondary_fields
            if subscription_entity.secondary_fields is not None
            else {}
        )

        subscription_type_id = None
        for field in update_required_fields:
            if "subscription_type_id" in field:
                subscription_type_id = field["subscription_type_id"]

        if not subscription_type_id:
            logger.error(
                f"Subscription entity {subscription_id} in journal (collection) {journal_id} has no subscription_type_id malformed subscription entity"
            )
            raise MoonstreamHTTPException(
                status_code=409,
                detail="Not valid subscription entity",
            )

    except EntityJournalNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions journal not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Error get subscriptions for user ({user.id}), error: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    for field in update_required_fields:
        if "color" in field:
            if color is not None:
                field["color"] = color
            else:
                color = field["color"]

        if "label" in field:
            if label is not None:
                field["label"] = label
            else:
                label = field["label"]

    if abi is not None:
        try:
            json_abi = json.loads(abi)
        except json.JSONDecodeError:
            raise MoonstreamHTTPException(status_code=400, detail="Malformed abi body.")

        validate_abi_json(json_abi)

        abi_string = json.dumps(json_abi, sort_keys=True, indent=2)

        update_secondary_fields["abi"] = abi_string
        hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

        update_secondary_fields["abi_hash"] = hash

    if description is not None:
        update_secondary_fields["description"] = description

    if tags:
        allowed_required_fields = [
            item
            for item in tags
            if not any(key in item for key in MOONSTREAM_ENTITIES_RESERVED_TAGS)
        ]

        if allowed_required_fields:
            update_required_fields.extend(allowed_required_fields)

    address = subscription_entity.address
    if address is None:
        logger.error(f"Lost address at entity {subscription_id} for subscription")
        raise MoonstreamHTTPException(status_code=500)

    try:
        subscription = bc.update_entity(
            token=token,
            journal_id=journal_id,
            entity_id=subscription_id,
            title=subscription_entity.title
            if subscription_entity.title is not None
            else "",
            address=address,
            blockchain=subscription_entity.blockchain
            if subscription_entity.blockchain is not None
            else "",
            required_fields=update_required_fields,
            secondary_fields=update_secondary_fields,
        )
    except Exception as e:
        logger.error(f"Error update user subscriptions: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if abi:
        background_tasks.add_task(
            apply_moonworm_tasks,
            subscription_type_id,
            json_abi,
            address,
        )
    subscription_required_fields = (
        subscription.required_fields if subscription.required_fields is not None else {}
    )
    subscription_secondary_fields = (
        subscription.secondary_fields
        if subscription.secondary_fields is not None
        else {}
    )

    normalized_entity_tags = [
        f"{key}:{value}"
        for tag in subscription_required_fields
        for key, value in tag.items()
        if key not in MOONSTREAM_ENTITIES_RESERVED_TAGS
    ]

    return data.SubscriptionResourceData(
        id=str(subscription.id),
        user_id=str(user.id),
        address=subscription.address,
        color=color,
        label=label,
        abi=subscription_secondary_fields.get("abi"),
        description=subscription_secondary_fields.get("description"),
        tags=normalized_entity_tags,
        subscription_type_id=subscription_type_id,
        updated_at=subscription_entity.updated_at,
        created_at=subscription_entity.created_at,
    )


@router.get(
    "/{subscription_id}/abi",
    tags=["subscriptions"],
    response_model=data.SubscriptionsAbiResponse,
)
async def get_subscription_abi_handler(
    request: Request,
    subscription_id: str = Path(...),
) -> data.SubscriptionsAbiResponse:
    token = request.state.token
    user = request.state.user

    try:
        journal_id = get_entity_subscription_journal_id(
            resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            user_id=user.id,
        )

        # get subscription entity
        subscription_resource = bc.get_entity(
            token=token,
            journal_id=journal_id,
            entity_id=subscription_id,
        )

    except EntityJournalNotFoundException as e:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="User subscriptions journal not found",
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Error get subscriptions for user ({user}), error: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if subscription_resource.secondary_fields is None:
        raise MoonstreamHTTPException(
            status_code=500, detail=f"Malformed subscription entity {subscription_id}"
        )
    if "abi" not in subscription_resource.secondary_fields.keys():
        raise MoonstreamHTTPException(status_code=404, detail="Abi not found")

    return data.SubscriptionsAbiResponse(
        abi=subscription_resource.secondary_fields["abi"]
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
        response = subscription_types.list_subscription_types(active_only=True)
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


@router.get(
    "/is_contract",
    tags=["subscriptions"],
    response_model=data.ContractInfoResponse,
)
async def address_info(request: Request, address: str = Query(...)):
    """
    Looking if address is contract
    """

    user_token = request.state.token

    try:
        Web3.toChecksumAddress(address)
    except ValueError as e:
        raise MoonstreamHTTPException(
            status_code=400,
            detail=str(e),
            internal_error=e,
        )

    contract_info = {}

    for blockchain_type in AvailableBlockchainType:
        try:
            # connnect to blockchain

            futures = []

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures.append(
                    executor.submit(
                        check_if_smart_contract,
                        address=address,
                        blockchain_type=blockchain_type,
                        user_token=user_token,
                    )
                )

                for future in as_completed(futures):
                    blockchain_type, address, is_contract = future.result(
                        timeout=THREAD_TIMEOUT_SECONDS
                    )

                    if is_contract:
                        contract_info[blockchain_type.value] = is_contract

        except Exception as e:
            logger.error(f"Error reading contract info from web3: {str(e)}")
            raise MoonstreamHTTPException(status_code=500, internal_error=e)
    if len(contract_info) == 0:
        raise MoonstreamHTTPException(
            status_code=404,
            detail="Not found contract on chains. EOA address or not used valid address.",
        )

    return data.ContractInfoResponse(
        contract_info=contract_info,
    )


@router.get(
    "/supported_interfaces",
    tags=["subscriptions"],
    response_model=data.ContractInterfacesResponse,
)
def get_contract_interfaces(
    request: Request,
    address: str = Query(...),
    blockchain: str = Query(...),
):
    """
    Request contract interfaces from web3
    """

    user_token = request.state.token

    try:
        Web3.toChecksumAddress(address)
    except ValueError as e:
        raise MoonstreamHTTPException(
            status_code=400,
            detail=str(e),
            internal_error=e,
        )

    try:
        blockchain_type = AvailableBlockchainType(blockchain)
    except ValueError as e:
        raise MoonstreamHTTPException(
            status_code=400,
            detail=str(e),
            internal_error=e,
        )

    try:
        interfaces = get_list_of_support_interfaces(
            blockchain_type=blockchain_type,
            address=address,
            user_token=user_token,
        )
    except AddressNotSmartContractException as e:
        raise MoonstreamHTTPException(
            status_code=409,
            detail=str(e),
            internal_error=e,
        )

    except Exception as e:
        logger.error(f"Error reading contract info from web3: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return data.ContractInterfacesResponse(
        interfaces=interfaces,
    )
