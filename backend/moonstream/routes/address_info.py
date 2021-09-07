import logging
from typing import Dict, List, Optional

from sqlalchemy.sql.expression import true

from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from moonstreamdb.db import yield_db_session
from sqlalchemy.orm import Session

from .. import actions
from .. import data
from ..middleware import BroodAuthMiddleware, MoonstreamHTTPException
from ..settings import DOCS_TARGET_PATH, ORIGINS, DOCS_PATHS
from ..version import MOONSTREAM_VERSION

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "addressinfo", "description": "Address public information."},
    {"name": "labels", "description": "Addresses label information."},
]

app = FastAPI(
    title=f"Moonstream users API.",
    description="User, token and password handlers.",
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


@app.get(
    "/ethereum_blockchain",
    tags=["addressinfo"],
    response_model=data.EthereumAddressInfo,
)
async def addressinfo_handler(
    address: str,
    db_session: Session = Depends(yield_db_session),
) -> Optional[data.EthereumAddressInfo]:
    response = actions.get_ethereum_address_info(db_session, address)
    return response


@app.get(
    "/labels/ethereum_blockchain",
    tags=["labels bul"],
    response_model=data.AddressListLabelsResponse,
)
async def addresses_labels_bulk_handler(
    addresses: Optional[str] = Query(None),
    start: int = Query(0),
    limit: int = Query(100),
    db_session: Session = Depends(yield_db_session),
) -> data.AddressListLabelsResponse:
    """
    Fetch labels with additional public information
    about known addresses.
    """
    if limit > 100:
        raise MoonstreamHTTPException(
            status_code=406, detail="The limit cannot exceed 100 addresses"
        )
    try:
        addresses_response = actions.get_address_labels(
            db_session=db_session, start=start, limit=limit, addresses=addresses
        )
    except Exception as e:
        logger.error(f"Unable to get info about Ethereum addresses {e}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return addresses_response
