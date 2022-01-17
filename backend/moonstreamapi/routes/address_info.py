import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from web3 import Web3

from moonstreamdb.db import yield_db_session

from .. import actions, data
from ..middleware import MoonstreamHTTPException
from ..web3_provider import yield_web3_provider

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/address_info",
)


@router.get(
    "/ethereum",
    tags=["addressinfo"],
    response_model=data.EthereumAddressInfo,
)
async def addressinfo_handler(
    address: str,
    db_session: Session = Depends(yield_db_session),
    web3: Web3 = Depends(yield_web3_provider),
) -> Optional[data.EthereumAddressInfo]:
    try:
        response = actions.get_ethereum_address_info(db_session, web3, address)
    except ValueError as e:
        raise MoonstreamHTTPException(status_code=400, detail=str(e), internal_error=e)
    except Exception as e:
        logger.error(f"Unable to get info about Ethereum address {e}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return response


@router.get(
    "/ethereum/ens_name",
    tags=["ens_name"],
    response_model=str,
)
async def ens_name_handler(
    address: str,
    web3: Web3 = Depends(yield_web3_provider),
) -> Optional[str]:
    try:
        response = actions.get_ens_name(web3, address)
    except ValueError as e:
        raise MoonstreamHTTPException(
            status_code=400,
            detail=str(e),
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Failed to get ens name: {e}")
        raise MoonstreamHTTPException(
            status_code=500,
            internal_error=e,
            detail="Currently unable to get ens name",
        )
    return response


@router.get(
    "/ethereum/ens_address",
    tags=["ens_address"],
    response_model=str,
)
async def ens_address_handler(
    name: str,
    web3: Web3 = Depends(yield_web3_provider),
) -> Optional[str]:
    try:
        response = actions.get_ens_address(web3, name)
    except ValueError as e:
        raise MoonstreamHTTPException(
            status_code=400,
            detail=str(e),
            internal_error=e,
        )
    except Exception as e:
        logger.error(f"Failed to get ens address: {e}")
        raise MoonstreamHTTPException(
            status_code=500,
            internal_error=e,
            detail="Currently unable to get ens address",
        )
    return response


@router.get(
    "/labels/ethereum",
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
