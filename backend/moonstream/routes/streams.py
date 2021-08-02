"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Any, cast, Dict, List, Optional, Set, Union

from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import Body, FastAPI, HTTPException, Request, Form, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from moonstreamdb.models import (
    EthereumBlock,
    EthereumTransaction,
    EthereumPendingTransaction,
    ESDFunctionSignature,
    ESDEventSignature,
)
from moonstreamdb import db
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_


from .. import data
from ..middleware import BroodAuthMiddleware
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
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
    filters: Optional[List[str]] = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
    db_session: Session = Depends(db.yield_db_session),
):

    # get user subscriptions

    if q == "" or q == " ":
        token = request.state.token
        params = {"user_id": str(request.state.user.id)}
        try:
            user_subscriptions_resources: BugoutResources = bc.list_resources(
                token=token, params=params
            )
            print(user_subscriptions_resources)
        except BugoutResponseException as e:
            if e.detail == "Resources not found":
                return data.EthereumTransactionResponse(stream=[])
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(status_code=500)
        user_subscriptions_resources
        # search_query = search.normalized_search_query(q, filters, strict_filter_mode=False)

        filters = [
            or_(
                EthereumTransaction.to_address == resource.resource_data["address"],
                EthereumTransaction.from_address == resource.resource_data["address"],
            )
            for resource in user_subscriptions_resources.resources
        ]
        filters = or_(*filters)

    else:
        print(f"query:|{q}|")
        filters = database_search_query(q)
        if not filters:
            return data.EthereumTransactionResponse(stream=[])
        filters = and_(*filters)

    transactions = db_session.query(EthereumTransaction).filter(filters).limit(25)

    print(transactions)

    response = [
        data.EthereumTransactionItem(
            gas=transaction.gas,
            gasPrice=transaction.gas_price,
            value=transaction.value,
            from_address=transaction.from_address,
            to_address=transaction.to_address,
            hash=transaction.hash,
            input=transaction.input,
        )
        for transaction in transactions
    ]

    return data.EthereumTransactionResponse(stream=response)


def database_search_query(q: str):

    filters = q.split("+")
    constructed_filters = []
    for filter_item in filters:
        if filter_item == "":
            logger.warning("Skipping empty filter item")
            continue

        # Try Google style search filters
        components = filter_item.split(":")
        if len(components) == 2:
            filter_type = components[0]
            filter_value = components[1]
        else:
            continue

        if filter_type == "to" and filter_value:
            constructed_filters.append(EthereumTransaction.to_address == filter_value)

        if filter_type == "from" and filter_value:
            constructed_filters.append(EthereumTransaction.from_address == filter_value)

        if filter_type == "address" and filter_value:
            constructed_filters.append(
                or_(
                    EthereumTransaction.to_address == filter_value,
                    EthereumTransaction.from_address == filter_value,
                )
            )

    return constructed_filters
