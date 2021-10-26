import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query
from moonstreamdb.db import yield_db_session
from sqlalchemy.orm import Session

from .. import actions, data
from ..middleware import MoonstreamHTTPException

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/address_info",
)


@router.get(
    "/ethereum_blockchain",
    tags=["addressinfo"],
    response_model=data.EthereumAddressInfo,
)
async def addressinfo_handler(
    address: str,
    db_session: Session = Depends(yield_db_session),
) -> Optional[data.EthereumAddressInfo]:
    try:
        response = actions.get_ethereum_address_info(db_session, address)
    except Exception as e:
        logger.error(f"Unable to get info about Ethereum address {e}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return response


@router.get(
    "/labels/ethereum_blockchain",
    tags=["labels"],
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
