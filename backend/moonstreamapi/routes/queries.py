"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Any, Dict, List, Optional

from bugout.data import BugoutResource
from fastapi import APIRouter, Depends, Query, Request
import requests
from sqlalchemy.orm import Session

from moonstreamdb import db

from ..middleware import MoonstreamHTTPException
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_QUERIES_JOURNAL_ID,
    MOONSTREAM_CRAWLERS_SERVER_URL,
    MOONSTREAM_CRAWLERS_SERVER_PORT,
)
from ..settings import bugout_client as bc


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/queries",)


@router.post("/{query_id}/update", tags=["queries"])
async def update_query_data_handler(
    request: Request, query_id: str = Query(...),
) -> Optional[Dict[str, Any]]:
    """
    Request update data on S3 bucket
    """

    token = request.state.token

    try:
        entries = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            query=f"#approved #query:{query_id} #user_token:{token}",
            limit=1,
        )

        if entries.results and entries.results[0].content:
            content = entries.results[0].content

            responce = requests.post(
                f"{MOONSTREAM_CRAWLERS_SERVER_URL}:{MOONSTREAM_CRAWLERS_SERVER_PORT}/jobs/query_update",
                json=content,
            )

            if responce.status_code != 200:
                raise MoonstreamHTTPException(
                    status_code=responce.status_code,
                    detail="Task for start generate stats failed.",
                )

            return responce.json()
    except Exception as e:
        logger.error("Unable to get events")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return None
