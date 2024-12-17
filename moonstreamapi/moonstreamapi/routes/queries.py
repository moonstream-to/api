"""
The Moonstream queries HTTP API
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from uuid import UUID

import requests  # type: ignore
from bugout.data import (
    BugoutJournalEntry,
    BugoutJournalEntryContent,
    BugoutResources,
    BugoutSearchResult,
)
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Body, Path, Query, Request
from moonstreamtypes.blockchain import AvailableBlockchainType
from sqlalchemy import text

from .. import data
from ..actions import (
    NameNormalizationException,
    create_resource_for_user,
    generate_s3_access_links,
    get_query_by_name,
    name_normalization,
    query_parameter_hash,
    check_user_resource_access,
)
from ..middleware import MoonstreamHTTPException
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_CRAWLERS_SERVER_PORT,
    MOONSTREAM_CRAWLERS_SERVER_URL,
    MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_QUERIES_JOURNAL_ID,
    MOONSTREAM_QUERY_TEMPLATE_CONTEXT_TYPE,
    MOONSTREAM_S3_QUERIES_BUCKET,
    MOONSTREAM_S3_QUERIES_BUCKET_PREFIX,
)
from ..settings import bugout_client as bc

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/queries",
)


@router.get("/list", tags=["queries"])
async def get_list_of_queries_handler(request: Request) -> List[Dict[str, Any]]:
    """
    Return list of queries which user own
    """

    token = request.state.token

    # Check already existed queries

    params = {
        "type": data.BUGOUT_RESOURCE_QUERY_RESOLVER,
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    users_queries: List[Dict[str, Any]] = [
        resource.resource_data for resource in resources.resources
    ]
    return users_queries


@router.post("/", tags=["queries"])
async def create_query_handler(
    request: Request, query_applied: data.PreapprovedQuery = Body(...)
) -> BugoutJournalEntry:
    """
    Create query in bugout journal with preapprove status required approval from moonstream team
    """

    token = request.state.token

    user = request.state.user

    # Check already existed queries

    params = {
        "type": data.BUGOUT_RESOURCE_QUERY_RESOLVER,
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    used_queries: List[str] = [
        resource.resource_data["name"] for resource in resources.resources
    ]
    try:
        query_name = name_normalization(query_applied.name)
    except NameNormalizationException:
        raise MoonstreamHTTPException(
            status_code=403,
            detail=f"Provided query name can't be normalize please select different.",
        )

    if query_name in used_queries:
        raise MoonstreamHTTPException(
            status_code=404,
            detail=f"Provided query name already use. Please remove it or use PUT /{query_name} for update query",
        )

    try:
        # Put query to journal
        entry = bc.create_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            title=f"Query:{query_name}",
            tags=["type:query"],
            content=query_applied.query,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS * 2,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    create_resource_for_user(
        user_id=user.id,
        resource_data={
            "type": data.BUGOUT_RESOURCE_QUERY_RESOLVER,
            "user_id": str(user.id),
            "user": str(user.username),
            "name": query_name,
            "entry_id": str(entry.id),
        },
    )

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
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return entry


@router.get("/templates", tags=["queries"])
def get_suggested_queries(
    supported_interfaces: Optional[List[str]] = Query(
        None, description="Supported interfaces in format: d73f4e3a erc1155"
    ),
    address: Optional[str] = Query(
        None,
        description="Query address for search if template applied to particular address",
    ),
    title: Optional[str] = Query(None, description="Query title for search"),
    limit: int = Query(10),
) -> data.SuggestedQueriesResponse:
    """
    Return set of suggested queries for user
    """

    filters = ["tag:approved", "tag:query_template"]

    if supported_interfaces:
        filters.extend(
            [f"?#interface:{interface}" for interface in supported_interfaces]
        )

    if address:
        filters.append(f"?#address:{address}")

    if title:
        filters.append(title)

    query = " ".join(filters)

    try:
        queries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=query,
            limit=limit,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
    except BugoutResponseException as e:
        logger.error(f"Error in get suggested queries templates: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    # make split by interfaces

    interfaces: Dict[str, Any] = {}

    queries_results = cast(List[BugoutSearchResult], queries.results)

    for entry in queries_results:
        for tag in entry.tags:
            if tag.startswith("interface:"):
                interface = tag.split(":")[1]

                if interface not in interfaces:
                    interfaces[interface] = []

                interfaces[interface].append(entry)

    return data.SuggestedQueriesResponse(
        queries=queries_results,
        interfaces=interfaces,
    )


@router.get("/{query_name}/query", tags=["queries"])
async def get_query_handler(
    request: Request, query_name: str = Path(..., description="Query name")
) -> data.QueryInfoResponse:
    token = request.state.token

    # normalize query name

    try:
        query_name_normalized = name_normalization(query_name)
    except NameNormalizationException:
        raise MoonstreamHTTPException(
            status_code=403,
            detail=f"Provided query name can't be normalize please select different.",
        )

    # check in templates
    try:
        entries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=f"tag:query_template tag:query_url:{query_name_normalized}",
            filters=[
                f"context_type:{MOONSTREAM_QUERY_TEMPLATE_CONTEXT_TYPE}",
            ],
            limit=1,
        )
    except BugoutResponseException as e:
        logger.error(f"Error in search template: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if len(entries.results) == 0:
        try:
            query_id = get_query_by_name(query_name, token)
        except NameNormalizationException:
            raise MoonstreamHTTPException(
                status_code=403,
                detail=f"Provided query name can't be normalize please select different.",
            )

        try:
            entry = bc.get_entry(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
                entry_id=query_id,
            )
        except BugoutResponseException as e:
            logger.error(f"Error in get query: {str(e)}")
            raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise MoonstreamHTTPException(status_code=500, internal_error=e)

    else:
        entries_results = cast(List[BugoutSearchResult], entries.results)
        query_id = entries_results[0].entry_url.split("/")[-1]
        entry = entries_results[0]

    content = entry.content
    tags = entry.tags
    created_at = entry.created_at
    updated_at = entry.updated_at

    if content is None:
        raise MoonstreamHTTPException(
            status_code=403, detail=f"Query is empty. Please update it."
        )

    try:
        query = text(content)
    except Exception as e:
        raise MoonstreamHTTPException(
            status_code=500, internal_error=e, detail="Error in query parsing"
        )

    query_parameters_names = list(query._bindparams.keys())

    tags_dict = {
        tag.split(":")[0]: (tag.split(":")[1] if ":" in tag else True) for tag in tags
    }

    query_parameters: Dict[str, Any] = {}

    for param in query_parameters_names:
        if param in tags_dict:
            query_parameters[param] = tags_dict[param]
        else:
            query_parameters[param] = None

    return data.QueryInfoResponse(
        query=content,
        query_id=str(query_id),
        preapprove="preapprove" in tags_dict,
        approved="approved" in tags_dict,
        parameters=query_parameters,
        created_at=created_at,  # type: ignore
        updated_at=updated_at,  # type: ignore
    )


@router.put("/{query_name}", tags=["queries"])
async def update_query_handler(
    request: Request,
    query_name: str = Path(..., description="Query name"),
    request_update: data.UpdateQueryRequest = Body(...),
) -> BugoutJournalEntryContent:
    token = request.state.token

    try:
        query_id = get_query_by_name(query_name, token)
    except NameNormalizationException:
        raise MoonstreamHTTPException(
            status_code=403,
            detail=f"Provided query name can't be normalize please select different.",
        )

    try:
        entry = bc.update_entry_content(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            entry_id=query_id,
            title=f"Query:{query_name}",
            content=request_update.query,
            tags=["preapprove"],
        )

    except BugoutResponseException as e:
        logger.error(f"Error in updating query: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return entry


@router.post(
    "/{query_name}/update_data",
    tags=["queries"],
)
async def update_query_data_handler(
    request: Request,
    query_name: str = Path(..., description="Query name"),
    request_update: data.UpdateDataRequest = Body(...),
    customer_id: Optional[str] = Query(None),
    instance_id: Optional[str] = Query(None),
) -> data.QueryPresignUrl:
    """
    Request update data on S3 bucket
    """

    token = request.state.token

    if request_update.blockchain:
        try:
            AvailableBlockchainType(request_update.blockchain)
        except ValueError:
            raise MoonstreamHTTPException(
                status_code=400,
                detail=f"Provided blockchain is not supported.",
            )

    json_payload = {}

    is_customer_database = customer_id is not None and instance_id is not None

    if is_customer_database:

        results = check_user_resource_access(
            customer_id=customer_id,
            user_token=token,
        )

        if results is None:
            raise MoonstreamHTTPException(
                status_code=404,
                detail="Not found customer",
            )

        json_payload["customer_id"] = customer_id
        json_payload["instance_id"] = instance_id

    # normalize query name

    try:
        query_name_normalized = name_normalization(query_name)
    except NameNormalizationException:
        raise MoonstreamHTTPException(
            status_code=403,
            detail=f"Provided query name can't be normalize please select different.",
        )

    # check in templates
    try:
        entries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=f"tag:query_template tag:query_url:{query_name_normalized}",
            filters=[
                f"context_type:{MOONSTREAM_QUERY_TEMPLATE_CONTEXT_TYPE}",
            ],
            limit=1,
        )
    except BugoutResponseException as e:
        logger.error(f"Error in search template: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if len(entries.results) == 0:
        try:
            query_id = get_query_by_name(query_name, token)
        except NameNormalizationException:
            raise MoonstreamHTTPException(
                status_code=403,
                detail=f"Provided query name can't be normalize please select different.",
            )

        try:
            entry = bc.get_entry(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
                entry_id=query_id,
            )

        except BugoutResponseException as e:
            logger.error(f"Error in get query: {str(e)}")
            raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise MoonstreamHTTPException(status_code=500, internal_error=e)

        ### check tags
        if (
            "preapprove" in entry.tags or "approved" not in entry.tags
        ) and not is_customer_database:
            raise MoonstreamHTTPException(
                status_code=403, detail="Query not approved yet."
            )

        content = entry.content
        tags = entry.tags

    else:
        entries_results = cast(List[BugoutSearchResult], entries.results)
        query_id = entries_results[0].entry_url.split("/")[-1]
        content = entries_results[0].content
        tags = entries_results[0].tags

    if content:
        file_type = "json"

        if "ext:csv" in tags:
            file_type = "csv"

        json_payload["query"] = content
        json_payload["params"] = request_update.params
        json_payload["file_type"] = file_type
        json_payload["blockchain"] = request_update.blockchain

        try:
            responce = requests.post(
                f"{MOONSTREAM_CRAWLERS_SERVER_URL}:{MOONSTREAM_CRAWLERS_SERVER_PORT}/jobs/{query_id}/query_update",
                json=json_payload,
                timeout=MOONSTREAM_INTERNAL_REQUEST_TIMEOUT_SECONDS,
            )
        except Exception as e:
            logger.error(f"Error interaction with crawlers: {str(e)}")
            raise MoonstreamHTTPException(status_code=500, internal_error=e)

        if responce.status_code != 200:
            raise MoonstreamHTTPException(
                status_code=responce.status_code,
                detail=responce.text,
            )

        s3_response = data.QueryPresignUrl(**responce.json())
    else:
        raise MoonstreamHTTPException(
            status_code=403, detail=f"Query is empty. Please update it."
        )

    return s3_response


@router.post("/{query_name}", tags=["queries"])
async def get_access_link_handler(
    request: Request,
    query_name: str = Path(..., description="Query name"),
    request_update: data.UpdateDataRequest = Body(...),
) -> Optional[data.QueryPresignUrl]:
    """
    Request S3 presign url
    """

    # get real connect to query_id

    token = request.state.token

    # normalize query name
    try:
        query_name_normalized = name_normalization(query_name)
    except NameNormalizationException:
        raise MoonstreamHTTPException(
            status_code=403,
            detail=f"Provided query name can't be normalize please select different.",
        )

    # check in templattes
    try:
        entries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=f"tag:query_template tag:query_url:{query_name_normalized}",
            filters=[f"context_type:{MOONSTREAM_QUERY_TEMPLATE_CONTEXT_TYPE}"],
            limit=1,
        )
    except BugoutResponseException as e:
        logger.error(f"Error in search template: {str(e)}")
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    if len(entries.results) == 0:
        try:
            query_id = get_query_by_name(query_name, token)
        except NameNormalizationException:
            raise MoonstreamHTTPException(
                status_code=403,
                detail=f"Provided query name can't be normalize please select different.",
            )

        try:
            entry = bc.get_entry(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
                entry_id=query_id,
            )
        except BugoutResponseException as e:
            logger.error(f"Error in get query: {str(e)}")
            raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise MoonstreamHTTPException(status_code=500, internal_error=e)

    else:
        entry = cast(BugoutJournalEntry, entries.results[0])

    content = entry.content
    tags = entry.tags

    if not content:
        raise MoonstreamHTTPException(
            status_code=403, detail=f"Query is empty. Please update it."
        )
    try:
        passed_params = dict(request_update.params)

        file_type = "json"

        if "ext:csv" in tags:
            file_type = "csv"

        params_hash = query_parameter_hash(passed_params)

        bucket = MOONSTREAM_S3_QUERIES_BUCKET
        key = f"{MOONSTREAM_S3_QUERIES_BUCKET_PREFIX}/queries/{query_id}/{params_hash}/data.{file_type}"

        stats_presigned_url = generate_s3_access_links(
            method_name="get_object",
            bucket=bucket,
            key=key,
            expiration=300000,
            http_method="GET",
        )
        s3_response = data.QueryPresignUrl(url=stats_presigned_url)
    except Exception as e:
        logger.error(f"Error in get access link: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return s3_response


@router.delete("/{query_name}", tags=["queries"])
async def remove_query_handler(
    request: Request, query_name: str = Path(..., description="Query name")
) -> BugoutJournalEntry:
    """
    Request delete query from journal
    """
    token = request.state.token

    params = {"type": data.BUGOUT_RESOURCE_QUERY_RESOLVER, "name": query_name}
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    query_ids: Dict[str, Tuple[UUID, Union[UUID, str]]] = {
        resource.resource_data["name"]: (
            resource.id,
            resource.resource_data["entry_id"],
        )
        for resource in resources.resources
    }
    if len(query_ids) == 0:
        raise MoonstreamHTTPException(status_code=404, detail="Query does not exists")

    try:
        bc.delete_resource(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN, resource_id=query_ids[query_name][0]
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
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
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return entry
