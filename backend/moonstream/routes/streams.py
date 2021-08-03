"""
The Moonstream subscriptions HTTP API
"""
import logging
from typing import Any, cast, Dict, List, Optional, Set, Union
from pydantic.utils import to_camel

from sqlalchemy.engine.base import Transaction

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

    subscriptions_addresses = [
        resource.resource_data["address"]
        for resource in user_subscriptions_resources.resources
    ]

    if q == "" or q == " ":

        filters = [
            or_(
                EthereumTransaction.to_address == address,
                EthereumTransaction.from_address == address,
            )
            for address in subscriptions_addresses
        ]
        filters = or_(*filters)

    else:
        filters = database_search_query(q, allowed_addresses=subscriptions_addresses)
        if not filters:
            return data.EthereumTransactionResponse(stream=[])
        filters = and_(*filters)

    address_to_subscriptions = {
        resource.resource_data["address"]: resource.resource_data
        for resource in user_subscriptions_resources.resources
    }

    ethereum_transactions = (
        db_session.query(
            EthereumTransaction.hash,
            EthereumTransaction.block_number,
            EthereumTransaction.from_address,
            EthereumTransaction.to_address,
            EthereumTransaction.gas,
            EthereumTransaction.gas_price,
            EthereumTransaction.input,
            EthereumTransaction.nonce,
            EthereumTransaction.value,
            EthereumBlock.timestamp,
        )
        .join(EthereumBlock)
        .filter(filters)
        .limit(25)
    )

    response = []
    for (
        hash,
        block_number,
        from_address,
        to_address,
        gas,
        gas_price,
        input,
        nonce,
        value,
        timestamp,
    ) in ethereum_transactions:

        subscription_type_id = None
        from_label = None
        to_label = None
        color = None

        if from_address in subscriptions_addresses:
            from_label = address_to_subscriptions[from_address]["label"]
            subscription_type_id = address_to_subscriptions[from_address][
                "subscription_type_id"
            ]
            color = address_to_subscriptions[from_address]["color"]

        if to_address in subscriptions_addresses:
            subscription_type_id = address_to_subscriptions[to_address][
                "subscription_type_id"
            ]
            to_label = address_to_subscriptions[to_address]["label"]
            color = address_to_subscriptions[to_address]["color"]

        response.append(
            data.EthereumTransactionItem(
                color=color,
                from_label=from_label,
                to_label=to_label,
                gas=gas,
                gasPrice=gas_price,
                value=value,
                from_address=from_address,
                to_address=to_address,
                hash=hash,
                input=input,
                nonce=nonce,
                timestamp=timestamp,
                subscription_type_id="1",
            )
        )

    return data.EthereumTransactionResponse(stream=response)


def database_search_query(q: str, allowed_addresses: List[str]):

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
            if filter_value not in allowed_addresses:
                continue
            constructed_filters.append(EthereumTransaction.from_address == filter_value)

        if filter_type == "address" and filter_value:
            constructed_filters.append(
                or_(
                    EthereumTransaction.to_address == filter_value,
                    EthereumTransaction.from_address == filter_value,
                )
            )

    return constructed_filters
