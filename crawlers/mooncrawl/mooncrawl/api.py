"""
The Mooncrawl HTTP API
"""
from datetime import datetime, timedelta
import logging
from os import times
import time
from typing import Dict, Any, List
from uuid import UUID

import boto3  # type: ignore
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from bugout.data import BugoutResource, BugoutResources

from . import data
from .middleware import MoonstreamHTTPException
from .settings import (
    DOCS_TARGET_PATH,
    ORIGINS,
    bugout_client as bc,
    BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
)
from .version import MOONCRAWL_VERSION
from .stats_worker import dashboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


tags_metadata = [
    {"name": "jobs", "description": "Trigger crawler jobs."},
    {"name": "time", "description": "Server timestamp endpoints."},
]

app = FastAPI(
    title=f"Mooncrawl HTTP API",
    description="Mooncrawl API endpoints.",
    version=MOONCRAWL_VERSION,
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


@app.get("/ping", response_model=data.PingResponse)
async def ping_handler() -> data.PingResponse:
    """
    Check server status.
    """
    return data.PingResponse(status="ok")


@app.get("/version", response_model=data.VersionResponse)
async def version_handler() -> data.VersionResponse:
    """
    Get server version.
    """
    return data.VersionResponse(version=MOONCRAWL_VERSION)


@app.get("/now", tags=["time"])
async def now_handler() -> data.NowResponse:
    """
    Get server current time.
    """
    return data.NowResponse(epoch_time=time.time())


@app.post("/jobs/stats_update", tags=["jobs"])
async def status_handler(
    stats_update: data.StatsUpdateRequest,
    background_tasks: BackgroundTasks,
):
    """
    Update dashboard endpoint create are tasks for update.
    """

    dashboard_resource: BugoutResource = bc.get_resource(
        token=stats_update.token,
        resource_id=stats_update.dashboard_id,
        timeout=10,
    )

    # get all user subscriptions

    blockchain_subscriptions: BugoutResources = bc.list_resources(
        token=stats_update.token,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION},
        timeout=10,
    )

    subscription_by_id = {
        str(blockchain_subscription.id): blockchain_subscription
        for blockchain_subscription in blockchain_subscriptions.resources
    }

    s3_client = boto3.client("s3")

    try:

        background_tasks.add_task(
            dashboard.stats_generate_api_task,
            timescales=stats_update.timescales,
            dashboard=dashboard_resource,
            subscription_by_id=subscription_by_id,
        )

    except Exception as e:
        logger.error(f"Unhandled status exception, error: {e}")
        raise MoonstreamHTTPException(status_code=500)

    presigned_urls_response: Dict[UUID, Any] = {}

    for dashboard_subscription_filters in dashboard_resource.resource_data[
        "subscription_settings"
    ]:

        subscription = subscription_by_id[
            dashboard_subscription_filters["subscription_id"]
        ]

        for timescale in stats_update.timescales:

            presigned_urls_response[subscription.id] = {}

            try:
                result_key = f'{MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX}/{dashboard.blockchain_by_subscription_id[subscription.resource_data["subscription_type_id"]]}/contracts_data/{subscription.resource_data["address"]}/{stats_update.dashboard_id}/v1/{timescale}.json'

                object = s3_client.head_object(
                    Bucket=subscription.resource_data["bucket"], Key=result_key
                )

                stats_presigned_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": subscription.resource_data["bucket"],
                        "Key": result_key,
                    },
                    ExpiresIn=300,
                    HttpMethod="GET",
                )

                presigned_urls_response[subscription.id][timescale] = {
                    "url": stats_presigned_url,
                    "headers": {
                        "If-Modified-Since": (
                            object["LastModified"] + timedelta(seconds=1)
                        ).strftime("%c")
                    },
                }
            except Exception as err:
                logger.warning(
                    f"Can't generate S3 presigned url in stats endpoint for Bucket:{subscription.resource_data['bucket']}, Key:{result_key} get error:{err}"
                )

    return presigned_urls_response
