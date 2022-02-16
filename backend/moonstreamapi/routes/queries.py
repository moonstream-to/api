"""
The Moonstream queries HTTP API
"""
import logging
from typing import Any, Dict, Optional


from fastapi import APIRouter, Body
import requests

from .. import data
from ..middleware import MoonstreamHTTPException
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_QUERIES_JOURNAL_ID,
    MOONSTREAM_CRAWLERS_SERVER_URL,
    MOONSTREAM_CRAWLERS_SERVER_PORT,
)
from ..settings import bugout_client as bc


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/queries",
)


@router.post("/{query_id}/update", tags=["queries"])
async def update_query_data_handler(
    query_id: str, request_update: data.UpdateDataRequest = Body(...)
) -> Optional[Dict[str, Any]]:
    """
    Request update data on S3 bucket
    """

    try:
        entries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=f"#approved #query:{query_id}",
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
    return None
