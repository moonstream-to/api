"""
The Moonstream queries HTTP API
"""
import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID

import boto3  # type: ignore
from bugout.data import BugoutResources, BugoutJournalEntryContent, BugoutJournalEntry
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Body, Request
import requests
from slugify import slugify


from .. import data
from ..actions import get_query_by_name
from ..middleware import MoonstreamHTTPException
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_CRAWLERS_SERVER_URL,
    MOONSTREAM_CRAWLERS_SERVER_PORT,
    MOONSTREAM_QUERIES_BUCKET,
    MOONSTREAM_QUERIES_JOURNAL_ID,
    BUGOUT_RESOURCE_QUERY_RESOLVER,
)
from ..settings import bugout_client as bc


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/queries",)


BUGOUT_RESOURCE_QUERY_RESOLVER = "query_name_resolver"


@router.get("/list", tags=["queries"])
async def get_list_of_queries_handler(request: Request) -> Dict[str, Any]:

    token = request.state.token

    # Check already existed queries

    params = {
        "type": BUGOUT_RESOURCE_QUERY_RESOLVER,
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    users_queries: List[Dict[str, Any]] = [
        resource.resource_data for resource in resources.resources
    ]
    return users_queries


@router.post("/", tags=["queries"])
async def create_query_handler(
    request: Request, query_name: str, query_applied: data.PreapprovedQuery = Body(...)
) -> BugoutJournalEntry:
    """
    Create query in bugout journal
    """

    token = request.state.token

    user = request.state.user

    # Check already existed queries

    params = {
        "type": BUGOUT_RESOURCE_QUERY_RESOLVER,
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    used_queries: List[str] = [
        resource.resource_data["name"] for resource in resources.resources
    ]

    query_name = slugify(query_applied.name)

    if query_name in used_queries:

        raise MoonstreamHTTPException(
            status_code=404,
            detail=f"Provided query name already use. Please remove it or use PUT /{query_name}",
        )

    try:
        # Put query to journal
        entry = bc.create_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            title=f"Query:{query_name}",
            tags=["type:query"],
            content=query_applied.query,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating query entry: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    try:
        # create resource query_name_resolver
        bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data={
                "type": BUGOUT_RESOURCE_QUERY_RESOLVER,
                "user_id": str(user.id),
                "user": str(user.username),
                "name": query_name,
                "entry_id": str(entry.id),
            },
        )
    except BugoutResponseException as e:
        logger.error(f"Error creating name resolving resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating name resolving resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    try:

        bc.update_tags(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            entry_id=entry.id,
            tags=[f"query_id:{entry.id}", f"preapprove"],
        )

    except BugoutResponseException as e:
        logger.error(f"Error in applind tags to query entry: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error in applind tags to query entry: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return entry


@router.get("/{query_name}/query", tags=["queries"])
async def get_query_handler(request: Request, query_name: str) -> BugoutJournalEntry:

    token = request.state.token

    query_id = get_query_by_name(query_name, token)

    try:

        entry = bc.get_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            entry_id=query_id,
        )

    except BugoutResponseException as e:
        logger.error(f"Error in updating query: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logger.error(f"Error in updating query: {e}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return entry


@router.put("/{query_name}", tags=["queries"])
async def update_query_handler(
    request: Request,
    query_name: str,
    request_update: data.UpdateQueryRequest = Body(...),
) -> BugoutJournalEntryContent:

    token = request.state.token

    query_id = get_query_by_name(query_name, token)

    try:

        entry = bc.update_entry_content(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            entry_id=query_id,
            title=query_name,
            content=request_update.query,
            tags=["preapprove"],
        )

    except BugoutResponseException as e:
        logger.error(f"Error in updating query: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logger.error(f"Error in updating query: {e}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return entry


@router.post("/{query_name}/update_data", tags=["queries"])
async def update_query_data_handler(
    request: Request,
    query_name: str,
    request_update: data.UpdateDataRequest = Body(...),
) -> Optional[Dict[str, Any]]:
    """
    Request update data on S3 bucket
    """

    token = request.state.token

    query_id = get_query_by_name(query_name, token)

    try:
        entries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=f"#approved ! #query_id:{query_id}",
            limit=1,
            timeout=5,
        )

        if entries.results and entries.results[0].content:
            content = entries.results[0].content

            tags = entries.results[0].tags

            file_type = "json"

            if "ext:csv" in tags:
                file_type = "csv"

            responce = requests.post(
                f"{MOONSTREAM_CRAWLERS_SERVER_URL}:{MOONSTREAM_CRAWLERS_SERVER_PORT}/jobs/{query_id}/query_update",
                json={
                    "query": content,
                    "params": request_update.params,
                    "file_type": file_type,
                },
                timeout=5,
            )

            if responce.status_code != 200:
                raise MoonstreamHTTPException(
                    status_code=responce.status_code,
                    detail="Task for start generate stats failed.",
                )

            return responce.json()
    except Exception as e:
        logger.error(f"Error in send generate query data task: {e}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    raise MoonstreamHTTPException(status_code=403, detail="Query not approved yet.")


@router.get("/{query_name}", tags=["queries"])
async def get_access_link_handler(request: Request, query_name: str,) -> str:
    """
    Request update data on S3 bucket
    """

    # get real connect to query_id

    token = request.state.token

    query_id = get_query_by_name(query_name, token)

    s3 = boto3.client("s3")

    try:
        entries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=f"#approved #query_id:{query_id}",
            limit=1,
            timeout=5,
        )

        if entries.results and entries.results[0].content:

            tags = entries.results[0].tags

            file_type = "json"

            if "ext:csv" in tags:
                file_type = "csv"

            stats_presigned_url = s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": MOONSTREAM_QUERIES_BUCKET,
                    "Key": f"queries/{query_id}/data.{file_type}",
                },
                ExpiresIn=300000,
                HttpMethod="GET",
            )
            return stats_presigned_url
    except Exception as e:
        logger.error(f"Error in send generate query data task: {e}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    raise MoonstreamHTTPException(status_code=403, detail="Query not approved yet.")


@router.delete("/{query_name}", tags=["queries"])
async def remove_query_handler(
    request: Request, query_name: str,
) -> BugoutJournalEntry:
    """
    Request update data on S3 bucket
    """
    token = request.state.token

    """
        def delete_resource(
        self,
        token: Union[str, uuid.UUID],
        resource_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT
    """

    params = {"type": BUGOUT_RESOURCE_QUERY_RESOLVER, "name": query_name}
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error get query, error: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    query_ids: Dict[str, Tuple[UUID, Union[UUID, str]]] = {
        resource.resource_data["name"]: (
            resource.id,
            resource.resource_data["entry_id"],
        )
        for resource in resources.resources
    }
    if len(query_ids) == 0:
        raise MoonstreamHTTPException(status_code=404, detail="Query does not existю")

    try:
        bc.remove_resources(token=token, resource_id=query_ids[query_name][0])
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error get query, error: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    try:
        entry = bc.delete_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            entry_id=query_ids[query_name][1],
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error get query, error: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return entry

