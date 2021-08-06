"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Any, cast, Dict, List, Optional, Set, Union
from pydantic.utils import to_camel

from datetime import datetime, timedelta

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import FastAPI, HTTPException, Request, Form, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from moonstreamdb import db
from sqlalchemy.orm import Session


from .. import actions
from .. import data
from ..middleware import BroodAuthMiddleware
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
    DEFAULT_PAGE_SIZE,
    DOCS_TARGET_PATH,
    ORIGINS,
    DOCS_PATHS,
    bugout_client as bc,
)
from ..version import MOONSTREAM_VERSION

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "streams", "description": "Operations with data stream and filters."},
]

app = FastAPI(
    title=f"Moonstream streams API.",
    description="Streams endpoints.",
    version=MOONSTREAM_VERSION,
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

whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(DOCS_PATHS)
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)


@app.get("/", tags=["streams"])
async def search_transactions(
    request: Request,
    q: str = Query(""),
    start_time: Optional[int] = Query(0),  # Optional[int] = Query(0),  #
    end_time: Optional[int] = Query(0),  # Optional[int] = Query(0),  #
    db_session: Session = Depends(db.yield_db_session),
):

    # get user subscriptions

    token = request.state.token
    params = {"user_id": str(request.state.user.id)}
    try:
        user_subscriptions_resources: BugoutResources = bc.list_resources(
            token=token, params=params
        )
    except BugoutResponseException as e:
        if e.detail == "Resources not found":
            return data.EthereumTransactionResponse(stream=[])
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)

    address_to_subscriptions = {
        resource.resource_data["address"]: resource.resource_data
        for resource in user_subscriptions_resources.resources
    }

    transactions: List[Any] = []

    if address_to_subscriptions:
        print("address_to_subscriptions")
        (
            transactions_in_blocks,
            first_item_time,
            last_item_time,
        ) = await actions.get_transaction_in_blocks(
            db_session=db_session,
            query=q,
            user_subscriptions_resources_by_address=address_to_subscriptions,
            start_time=start_time,
            end_time=end_time,
        )

        transactions.extend(transactions_in_blocks)

    return data.EthereumTransactionResponse(
        stream=transactions, start_time=first_item_time, end_time=last_item_time
    )
