import json
import logging
from typing import Any, Dict, List, Optional, Union, cast
from uuid import UUID

import boto3  # type: ignore
import requests  # type: ignore
from bugout.data import BugoutResource, BugoutResources, BugoutSearchResultAsEntity
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Body, Path, Query, Request

from .. import actions, data
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_CRAWLERS_SERVER_PORT,
    MOONSTREAM_CRAWLERS_SERVER_URL,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
)
from ..settings import bugout_client as bc

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/dashboards",
)

BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"


@router.post("/", tags=["dashboards"], response_model=BugoutResource)
async def add_dashboard_handler(
    request: Request,
    dashboard: data.DashboardCreate = Body(...),
) -> BugoutResource:
    """
    Add subscription to blockchain stream data for user.
    """

    token = request.state.token

    user = request.state.user

    subscription_settings = dashboard.subscription_settings

    # Get user journal (collection) id

    journal_id = actions.get_entity_subscription_journal_id(
        resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
        user_id=user.id,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
    )

    subscriptions_list = bc.search(
        token=token,
        journal_id=journal_id,
        query="tag:type:subscription",
        limit=1000,
        representation="entity",
    )

    # process existing subscriptions with supplied ids
    available_subscriptions_ids: Dict[Union[UUID, str], BugoutSearchResultAsEntity]
    for result in subscriptions_list.results:
        entity = cast(BugoutSearchResultAsEntity, result)
        entity_url_list = entity.entity_url.split("/")
        subscription_id = entity_url_list[len(entity_url_list) - 1]
        available_subscriptions_ids[subscription_id] = entity

    for dashboard_subscription in subscription_settings:
        if dashboard_subscription.subscription_id in available_subscriptions_ids.keys():
            if (
                available_subscriptions_ids[
                    dashboard_subscription.subscription_id
                ].secondary_fields.get("abi")
                is None
            ):
                logger.error(
                    f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi"
                )
                raise MoonstreamHTTPException(
                    status_code=404,
                    detail=f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi",
                )

            abi = json.loads(
                available_subscriptions_ids[
                    dashboard_subscription.subscription_id
                ].secondary_fields["abi"]
            )

            actions.dashboards_abi_validation(
                dashboard_subscription,
                abi,
            )

        else:
            logger.error(
                f"Error subscription_id: {str(dashboard_subscription.subscription_id)} not exists."
            )
            raise MoonstreamHTTPException(status_code=404)

    dashboard_resource = data.DashboardResource(
        type=BUGOUT_RESOURCE_TYPE_DASHBOARD,
        user_id=str(user.id),
        name=dashboard.name,
        subscription_settings=subscription_settings,
    )

    try:
        # json.loads(dashboard_resource.json())
        # Necessary because the UUIDs inside dashboard_resources do not get serialized into string if we directly convert to ".dict()"
        resource: BugoutResource = bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data=json.loads(dashboard_resource.json()),
        )
    except BugoutResponseException as e:
        logger.error(f"Error creating dashboard resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating dashboard resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resource


@router.delete(
    "/{dashboard_id}",
    tags=["subscriptions"],
    response_model=BugoutResource,
)
async def delete_subscription_handler(request: Request, dashboard_id: str = Path(...)):
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


@router.get("/", tags=["dashboards"], response_model=BugoutResources)
async def get_dashboards_handler(
    request: Request,
    limit: int = Query(10),
    offset: int = Query(0),
) -> BugoutResources:
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
            f"Error listing subscriptions for user ({request.user.id}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resources


@router.get("/{dashboard_id}", tags=["dashboards"], response_model=BugoutResource)
async def get_dashboard_handler(
    request: Request, dashboard_id: UUID = Path(...)
) -> BugoutResource:
    """
    Get user's subscriptions.
    """
    token = request.state.token

    try:
        resource: BugoutResource = bc.get_resource(
            token=token,
            resource_id=dashboard_id,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resource


@router.put("/{dashboard_id}", tags=["dashboards"], response_model=BugoutResource)
async def update_dashboard_handler(
    request: Request,
    dashboard_id: str = Path(...),
    dashboard: data.DashboardUpdate = Body(...),
) -> BugoutResource:
    """
    Update dashboards mainly fully overwrite name and subscription metadata
    """

    token = request.state.token

    user = request.state.user

    subscription_settings = dashboard.subscription_settings

    # Get user journal (collection) id

    journal_id = actions.get_entity_subscription_journal_id(
        resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
        user_id=user.id,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
    )

    subscriptions_list = bc.search(
        token=token,
        journal_id=journal_id,
        query="tag:type:subscription",
        limit=1000,
        representation="entity",
    )

    available_subscriptions_ids: Dict[Union[UUID, str], BugoutSearchResultAsEntity]
    for result in subscriptions_list.results:
        entity = cast(BugoutSearchResultAsEntity, result)
        entity_url_list = entity.entity_url.split("/")
        subscription_id = entity_url_list[len(entity_url_list) - 1]
        available_subscriptions_ids[subscription_id] = entity

    for dashboard_subscription in subscription_settings:
        if dashboard_subscription.subscription_id in available_subscriptions_ids:
            if (
                available_subscriptions_ids[
                    dashboard_subscription.subscription_id
                ].secondary_fields.get("abi")
                is None
            ):
                logger.error(
                    f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi"
                )
                raise MoonstreamHTTPException(
                    status_code=404,
                    detail=f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi",
                )
            abi_raw = available_subscriptions_ids[
                dashboard_subscription.subscription_id
            ].secondary_fields.get("abi")
            abi = json.loads(abi_raw if abi_raw is not None else "")

            actions.dashboards_abi_validation(dashboard_subscription, abi)

        else:
            logger.error(
                f"Error subscription_id: {dashboard_subscription.subscription_id} not exists."
            )
            raise MoonstreamHTTPException(status_code=404)

    dashboard_resource: Dict[str, Any] = {}

    if subscription_settings:
        dashboard_resource["subscription_settings"] = json.loads(dashboard.json())[
            "subscription_settings"
        ]

    if dashboard.name is not None:
        dashboard_resource["name"] = dashboard.name

    try:
        resource: BugoutResource = bc.update_resource(
            token=token,
            resource_id=dashboard_id,
            resource_data=data.SubscriptionUpdate(update=dashboard_resource).dict(),
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error updating subscription resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resource


@router.get("/{dashboard_id}/stats", tags=["dashboards"])
async def get_dashboard_data_links_handler(
    request: Request, dashboard_id: str = Path(...)
) -> Dict[Union[UUID, str], Any]:
    """
    Get s3 presign urls for dashboard grafics
    """

    token = request.state.token

    user = request.state.user

    try:
        dashboard_resource: BugoutResource = bc.get_resource(
            token=token, resource_id=dashboard_id
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    s3_client = boto3.client("s3")

    # get subscriptions

    journal_id = actions.get_entity_subscription_journal_id(
        resource_type=BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
        user_id=user.id,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
    )

    subscriptions_list = bc.search(
        token=token,
        journal_id=journal_id,
        query="tag:type:subscription",
        limit=1000,
        representation="entity",
    )

    # filter out dashboards

    subscriptions_ids = [
        subscription_meta["subscription_id"]
        for subscription_meta in dashboard_resource.resource_data[
            "subscription_settings"
        ]
    ]

    dashboard_subscriptions: Dict[Union[UUID, str], BugoutSearchResultAsEntity]
    for result in subscriptions_list.results:
        entity = cast(BugoutSearchResultAsEntity, result)
        entity_url_list = entity.entity_url.split("/")
        subscription_id = entity_url_list[len(entity_url_list) - 1]
        if str(subscription_id) in subscriptions_ids:
            dashboard_subscriptions[subscription_id] = entity

    # generate s3 links

    s3_client = boto3.client("s3")

    stats: Dict[Union[str, UUID], Dict[str, Any]] = {}

    for id, subscription in dashboard_subscriptions.items():
        available_timescales = [timescale.value for timescale in data.TimeScale]
        stats[id] = {}

        for fields in subscription.required_fields:
            if "subscription_type_id" in fields:
                subscription_type_id = fields["subscription_type_id"]

        for timescale in available_timescales:
            try:
                result_key = f"{MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX}/{actions.blockchain_by_subscription_id[subscription_type_id]}/contracts_data/{subscription.address}/{dashboard_id}/v1/{timescale}.json"
                stats_presigned_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
                        "Key": result_key,
                    },
                    ExpiresIn=300,
                    HttpMethod="GET",
                )
                stats[id][timescale] = {"url": stats_presigned_url}
            except Exception as err:
                logger.warning(
                    f"Can't generate S3 presigned url in stats endpoint for Bucket:{MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET},  get error:{err}"
                )

    return stats


@router.post("/{dashboard_id}/stats_update", tags=["dashboards"])
async def update_dashbord_data_handler(
    request: Request,
    dashboard_id: str = Path(...),
    updatestats: data.UpdateStats = Body(...),
) -> Dict[str, Any]:
    """
    Return journal statistics
    journal.read permission required.
    """

    token = request.state.token
    user = request.state.user

    responce = requests.post(
        f"{MOONSTREAM_CRAWLERS_SERVER_URL}:{MOONSTREAM_CRAWLERS_SERVER_PORT}/jobs/stats_update",
        json={
            "dashboard_id": dashboard_id,
            "timescales": updatestats.timescales,
            "token": token,
            "user_id": str(user.id),
        },
    )
    if responce.status_code != 200:
        raise MoonstreamHTTPException(
            status_code=responce.status_code,
            detail="Task for start generate stats failed.",
        )
    return responce.json()
