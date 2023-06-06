"""
Contract registration API

Moonstream users can register contracts on Moonstream Engine. This allows them to use these contracts
as part of their chain-adjacent activities (like performing signature-based token distributions on the
Dropper contract).
"""
import logging
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import Body, Depends, FastAPI, Query, Request, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from .. import contracts_actions, data, db
from ..middleware import BroodAuthMiddleware, EngineHTTPException
from ..settings import DOCS_TARGET_PATH, ORIGINS
from ..version import VERSION

logger = logging.getLogger(__name__)


TITLE = "Moonstream Engine Contracts API"
DESCRIPTION = "Users can register contracts on the Moonstream Engine for use in chain-adjacent activities, like setting up signature-based token distributions."


tags_metadata = [
    {
        "name": "contracts",
        "description": DESCRIPTION,
    },
    {"name": "requests", "description": "Call requests for registered contracts."},
]


whitelist_paths = {
    "/metatx/openapi.json": "GET",
    f"/metatx/{DOCS_TARGET_PATH}": "GET",
    "/metatx/contracts/types": "GET",
    "/metatx/requests": "GET",
}

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)


app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/contracts/types", tags=["contracts"])
async def contract_types() -> Dict[str, str]:
    """
    Describes the contract_types that users can register contracts as against this API.
    """
    return {
        data.ContractType.raw.value: "A generic smart contract. You can ask users to submit arbitrary calldata to this contract.",
        data.ContractType.dropper.value: "A Dropper contract. You can authorize users to submit claims against this contract.",
    }


@app.get("/contracts", tags=["contracts"], response_model=List[data.RegisteredContract])
async def list_registered_contracts(
    request: Request,
    blockchain: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    contract_type: Optional[data.ContractType] = Query(None),
    limit: int = Query(10),
    offset: Optional[int] = Query(None),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.RegisteredContract]:
    """
    Users can use this endpoint to look up the contracts they have registered against this API.
    """
    try:
        contracts = contracts_actions.lookup_registered_contracts(
            db_session=db_session,
            moonstream_user_id=request.state.user.id,
            blockchain=blockchain,
            address=address,
            contract_type=contract_type,
            limit=limit,
            offset=offset,
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)
    return [contract for contract in contracts]


@app.get(
    "/contracts/{contract_id}",
    tags=["contracts"],
    response_model=data.RegisteredContract,
)
async def get_registered_contract(
    request: Request,
    contract_id: UUID = Path(...),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.RegisteredContract]:
    """
    Get the contract by ID.
    """
    try:
        contract = contracts_actions.get_registered_contract(
            db_session=db_session,
            moonstream_user_id=request.state.user.id,
            contract_id=contract_id,
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)
    return contract


@app.post("/contracts", tags=["contracts"], response_model=data.RegisteredContract)
async def register_contract(
    request: Request,
    contract: data.RegisterContractRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.RegisteredContract:
    """
    Allows users to register contracts.
    """
    try:
        registered_contract = contracts_actions.register_contract(
            db_session=db_session,
            moonstream_user_id=request.state.user.id,
            blockchain=contract.blockchain,
            address=contract.address,
            contract_type=contract.contract_type,
            title=contract.title,
            description=contract.description,
            image_uri=contract.image_uri,
        )
    except contracts_actions.ContractAlreadyRegistered:
        raise EngineHTTPException(
            status_code=409,
            detail="Contract already registered",
        )
    return registered_contract


@app.put(
    "/contracts/{contract_id}",
    tags=["contracts"],
    response_model=data.RegisteredContract,
)
async def update_contract(
    request: Request,
    contract_id: UUID = Path(...),
    update_info: data.UpdateContractRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.RegisteredContract:
    try:
        contract = contracts_actions.update_registered_contract(
            db_session,
            request.state.user.id,
            contract_id,
            update_info.title,
            update_info.description,
            update_info.image_uri,
            update_info.ignore_nulls,
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return contract


@app.delete(
    "/contracts/{contract_id}",
    tags=["contracts"],
    response_model=data.RegisteredContract,
)
async def delete_contract(
    request: Request,
    contract_id: UUID,
    db_session: Session = Depends(db.yield_db_session),
) -> data.RegisteredContract:
    """
    Allows users to delete contracts that they have registered.
    """
    try:
        deleted_contract = contracts_actions.delete_registered_contract(
            db_session=db_session,
            moonstream_user_id=request.state.user.id,
            registered_contract_id=contract_id,
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return deleted_contract


@app.get("/requests", tags=["requests"], response_model=List[data.CallRequest])
async def list_requests(
    contract_id: Optional[UUID] = Query(None),
    contract_address: Optional[str] = Query(None),
    caller: str = Query(...),
    limit: int = Query(100),
    offset: Optional[int] = Query(None),
    show_expired: Optional[bool] = Query(False),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.CallRequest]:
    """
    Allows API user to see all unexpired call requests for a given caller against a given contract.

    At least one of `contract_id` or `contract_address` must be provided as query parameters.
    """
    try:
        requests = contracts_actions.list_call_requests(
            db_session=db_session,
            contract_id=contract_id,
            contract_address=contract_address,
            caller=caller,
            limit=limit,
            offset=offset,
            show_expired=show_expired,
        )
    except ValueError as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=500)

    return requests


@app.get("/requests/{request_id}", tags=["requests"], response_model=data.CallRequest)
async def get_request(
    request_id: UUID = Path(...),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.CallRequest]:
    """
    Allows API user to see call request.

    At least one of `contract_id` or `contract_address` must be provided as query parameters.
    """
    try:
        result = contracts_actions.get_call_requests(
            db_session=db_session,
            request_id=request_id,
        )
    except contracts_actions.CallRequestNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="There is no call request with that ID.",
        )
    except Exception as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=500)

    return result


@app.post("/requests", tags=["requests"], response_model=int)
async def create_requests(
    request: Request,
    data: data.CreateCallRequestsAPIRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> int:
    """
    Allows API user to register call requests from given contract details, TTL, and call specifications.

    At least one of `contract_id` or `contract_address` must be provided in the request body.
    """
    try:
        num_requests = contracts_actions.request_calls(
            db_session=db_session,
            moonstream_user_id=request.state.user.id,
            registered_contract_id=data.contract_id,
            contract_address=data.contract_address,
            call_specs=data.specifications,
            ttl_days=data.ttl_days,
        )
    except contracts_actions.InvalidAddressFormat as err:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Address not passed web3checksum validation, err: {err}",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return num_requests


@app.delete("/requests", tags=["requests"], response_model=int)
async def delete_requests(
    request: Request,
    request_ids: List[UUID] = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> int:
    """
    Allows users to delete requests.
    """
    try:
        deleted_requests = contracts_actions.delete_requests(
            db_session=db_session,
            moonstream_user_id=request.state.user.id,
            request_ids=request_ids,
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return deleted_requests
