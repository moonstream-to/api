"""
The Mooncrawl HTTP API
"""
import logging
import time
from cgi import test
from datetime import timedelta
from collections import OrderedDict
import hashlib
import json
from typing import Any, Dict, List
from uuid import UUID

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

from .actions import generate_s3_access_links
from . import data
from .middleware import MoonstreamHTTPException
from .settings import (
    BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
    DOCS_TARGET_PATH,
    MOONSTREAM_S3_QUERIES_BUCKET,
    MOONSTREAM_S3_QUERIES_BUCKET_PREFIX,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
    NB_CONTROLLER_ACCESS_ID,
    ORIGINS,
    LINKS_EXPIRATION_TIME,
)
from .settings import bugout_client as bc
from .stats_worker import dashboard, queries
from .version import MOONCRAWL_VERSION

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
            access_id=NB_CONTROLLER_ACCESS_ID,
        )

    except Exception as e:
        logger.error(
            f"Unhandled /jobs/stats_update start background task exception, error: {e}"
        )
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


@app.post("/jobs/{query_id}/query_update", tags=["jobs"])
async def queries_data_update_handler(
    query_id: str,
    request_data: data.QueryDataUpdate,
    background_tasks: BackgroundTasks,
) -> Dict[str, Any]:

    # Check if query is valid
    try:
        queries.query_validation(request_data.query)
    except queries.QueryNotValid:
        logger.error(f"Query not pass validation check query id: {query_id}")
        raise MoonstreamHTTPException(
            status_code=401,
            detail="Incorrect query is not valid with current restrictions",
        )
    except Exception as e:
        logger.error(f"Unhandled query execute exception, error: {e}")
        raise MoonstreamHTTPException(status_code=500)

    # Check if it can transform to TextClause
    try:
        query = text(request_data.query)
    except Exception as e:
        logger.error(
            f"Can't parse query {query_id} to TextClause in drones /query_update endpoint, error: {e}"
        )
        raise MoonstreamHTTPException(status_code=500, detail="Can't parse query")

    # Get requried keys for query
    expected_query_parameters = query._bindparams.keys()

    # request.params validations
    passed_params = {
        key: queries.from_json_types(value)
        for key, value in request_data.params.items()
        if key in expected_query_parameters
    }

    if len(passed_params) != len(expected_query_parameters):
        logger.error(
            f"Unmatched amount of applying query parameters: {passed_params}, query_id:{query_id}."
        )
        raise MoonstreamHTTPException(
            status_code=500, detail="Unmatched amount of applying query parameters"
        )

    params_hash = hashlib.md5(
        json.dumps(OrderedDict(passed_params)).encode("utf-8")
    ).hexdigest()

    bucket = MOONSTREAM_S3_QUERIES_BUCKET
    key = f"{MOONSTREAM_S3_QUERIES_BUCKET_PREFIX}/queries/{query_id}/{params_hash}/data.{request_data.file_type}"

    try:

        background_tasks.add_task(
            queries.data_generate,
            query_id=f"{query_id}",
            file_type=request_data.file_type,
            bucket=bucket,
            key=key,
            query=query,
            params=passed_params,
            params_hash=params_hash,
        )

    except Exception as e:
        logger.error(f"Unhandled query execute exception, error: {e}")
        raise MoonstreamHTTPException(status_code=500)

    stats_presigned_url = generate_s3_access_links(
        method_name="get_object",
        bucket=bucket,
        key=key,
        expiration=LINKS_EXPIRATION_TIME,
        http_method="GET",
    )

    return {"url": stats_presigned_url}
