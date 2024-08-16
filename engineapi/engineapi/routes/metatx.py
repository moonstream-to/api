"""
Contract registration API

Moonstream users can register contracts on Moonstream Engine. This allows them to use these contracts
as part of their chain-adjacent activities (like performing signature-based token distributions on the
Dropper contract).
"""

import logging
from typing import Dict, List, Optional, Set, Tuple
from uuid import UUID

from bugout.data import BugoutResourceHolder, BugoutUser
from fastapi import BackgroundTasks, Body, Depends, FastAPI, Path, Query, Request
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from web3 import Web3

from .. import contracts_actions, data, db
from ..middleware import (
    BugoutCORSMiddleware,
    EngineHTTPException,
    metatx_verify_header,
    request_none_or_user_auth,
    request_user_auth,
)
from ..settings import DOCS_TARGET_PATH
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
    {
        "name": "requesters",
        "description": "Metatx requester represented by resource for registered contracts access.",
    },
]


app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)

app.add_middleware(
    BugoutCORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/blockchains", tags=["blockchains"], response_model=data.BlockchainsResponse)
async def blockchains_route(
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> data.BlockchainsResponse:
    """
    Returns supported list of blockchains.
    """
    try:
        blockchains = contracts_actions.list_blockchains(
            db_session=db_session,
        )
    except Exception as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=500)
    return data.BlockchainsResponse(
        blockchains=[blockchain for blockchain in blockchains]
    )


@app.get(
    "/contracts",
    tags=["contracts"],
    response_model=List[data.RegisteredContractResponse],
)
async def list_registered_contracts_route(
    blockchain: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    limit: int = Query(10),
    offset: Optional[int] = Query(None),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.RegisteredContractResponse]:
    """
    Users can use this endpoint to look up the contracts they have registered against this API.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        registered_contracts_with_blockchain = (
            contracts_actions.lookup_registered_contracts(
                db_session=db_session,
                metatx_requester_ids=metatx_requester_ids,
                blockchain=blockchain,
                address=address,
                limit=limit,
                offset=offset,
            )
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return [
        contracts_actions.parse_registered_contract_response(rc)
        for rc in registered_contracts_with_blockchain
    ]


@app.get(
    "/contracts/{contract_id}",
    tags=["contracts"],
    response_model=data.RegisteredContractResponse,
)
async def get_registered_contract_route(
    contract_id: UUID = Path(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> data.RegisteredContractResponse:
    """
    Get the contract by ID.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        contract_with_blockchain = contracts_actions.get_registered_contract(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            contract_id=contract_id,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return contracts_actions.parse_registered_contract_response(
        contract_with_blockchain
    )


@app.post(
    "/contracts", tags=["contracts"], response_model=data.RegisteredContractResponse
)
async def register_contract_route(
    contract: data.RegisterContractRequest = Body(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_session),
) -> data.RegisteredContractResponse:
    """
    Allows users to register contracts.
    """
    user, _ = user_authorization

    try:
        contract_with_blockchain = contracts_actions.register_contract(
            db_session=db_session,
            user_id=user.id,
            blockchain_name=contract.blockchain,
            address=contract.address,
            title=contract.title,
            description=contract.description,
            image_uri=contract.image_uri,
        )
    except contracts_actions.UnsupportedBlockchain:
        raise EngineHTTPException(
            status_code=400, detail="Unsupported blockchain specified"
        )
    except contracts_actions.ContractAlreadyRegistered:
        raise EngineHTTPException(
            status_code=409,
            detail="Contract already registered",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return contracts_actions.parse_registered_contract_response(
        contract_with_blockchain
    )


@app.put(
    "/contracts/{contract_id}",
    tags=["contracts"],
    response_model=data.RegisteredContractResponse,
)
async def update_contract_route(
    contract_id: UUID = Path(...),
    update_info: data.UpdateContractRequest = Body(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_session),
) -> data.RegisteredContractResponse:
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        contract_with_blockchain = contracts_actions.update_registered_contract(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            contract_id=contract_id,
            title=update_info.title,
            description=update_info.description,
            image_uri=update_info.image_uri,
            ignore_nulls=update_info.ignore_nulls,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return contracts_actions.parse_registered_contract_response(
        contract_with_blockchain
    )


@app.delete(
    "/contracts/{contract_id}",
    tags=["contracts"],
    response_model=data.RegisteredContractResponse,
)
async def delete_contract_route(
    background_tasks: BackgroundTasks,
    contract_id: UUID = Path(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_session),
) -> data.RegisteredContractResponse:
    """
    Allows users to delete contracts that they have registered.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        deleted_contract_with_blockchain = contracts_actions.delete_registered_contract(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            registered_contract_id=contract_id,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    parsed_registered_contract = contracts_actions.parse_registered_contract_response(
        deleted_contract_with_blockchain
    )

    background_tasks.add_task(
        contracts_actions.clean_metatx_requester_id,
        db_session=db_session,
        metatx_requester_id=parsed_registered_contract.metatx_requester_id,
    )

    return parsed_registered_contract


@app.get(
    "/requesters",
    tags=["requesters"],
    response_model=List[data.MetatxRequestersResponse],
)
async def list_metatx_requesters_route(
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.MetatxRequestersResponse]:
    """
    Get list of metatx requesters available to user.

    Helps to track number of empty metatx requesters without registered contracts and call requests.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)
        metatx_requesters = (
            contracts_actions.count_contracts_and_requests_for_requester(
                db_session=db_session, metatx_requester_ids=metatx_requester_ids
            )
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return metatx_requesters


@app.get(
    "/contracts/{contract_id}/holders",
    tags=["contracts"],
    response_model=data.RegisteredContractWithHoldersResponse,
)
async def list_metatx_requester_holders_route(
    contract_id: UUID = Path(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    extended: bool = Query(False),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> data.RegisteredContractWithHoldersResponse:
    """
    Get the metatx requester holders.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        contract_with_blockchain = contracts_actions.get_registered_contract(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            contract_id=contract_id,
        )

        holders = contracts_actions.fetch_metatx_requester_holders(
            resource_id=contract_with_blockchain[0].metatx_requester_id,
            extended=extended,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    parser_registered_contract = contracts_actions.parse_registered_contract_response(
        contract_with_blockchain
    )

    return data.RegisteredContractWithHoldersResponse(
        **parser_registered_contract.dict(), holders=holders
    )


@app.post(
    "/contracts/{contract_id}/holders",
    tags=["contracts"],
    response_model=data.RegisteredContractWithHoldersResponse,
)
async def add_metatx_requester_holder_route(
    contract_id: UUID = Path(...),
    holder_permissions: BugoutResourceHolder = Body(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> data.RegisteredContractWithHoldersResponse:
    """
    Add the metatx requester holder.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        contract_with_blockchain = contracts_actions.get_registered_contract(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            contract_id=contract_id,
        )

        holders = contracts_actions.add_metatx_requester_holder(
            resource_id=contract_with_blockchain[0].metatx_requester_id,
            holder_permissions=holder_permissions,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    parser_registered_contract = contracts_actions.parse_registered_contract_response(
        contract_with_blockchain
    )

    return data.RegisteredContractWithHoldersResponse(
        **parser_registered_contract.dict(), holders=holders
    )


@app.delete(
    "/contracts/{contract_id}/holders",
    tags=["contracts"],
    response_model=data.RegisteredContractWithHoldersResponse,
)
async def delete_metatx_requester_holder_route(
    contract_id: UUID = Path(...),
    holder_permissions: BugoutResourceHolder = Body(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> data.RegisteredContractWithHoldersResponse:
    """
    Delete the metatx requester holder or it's permissions.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        contract_with_blockchain = contracts_actions.get_registered_contract(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            contract_id=contract_id,
        )

        holders = contracts_actions.delete_metatx_requester_holder(
            resource_id=contract_with_blockchain[0].metatx_requester_id,
            holder_permissions=holder_permissions,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Either there is not contract with that ID or you do not have access to that contract.",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    parser_registered_contract = contracts_actions.parse_registered_contract_response(
        contract_with_blockchain
    )

    return data.RegisteredContractWithHoldersResponse(
        **parser_registered_contract.dict(), holders=holders
    )


# TODO(kompotkot): route `/contracts/types` deprecated
@app.get("/contracts/types", tags=["contracts"])
@app.get(
    "/requests/types",
    tags=["requests"],
    response_model=List[data.CallRequestTypeResponse],
)
async def call_request_types_route(
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.CallRequestTypeResponse]:
    """
    Describes the call_request_types that users can register call requests as against this API.
    """
    try:
        call_request_types = contracts_actions.list_call_request_types(
            db_session=db_session,
        )
    except Exception as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=500)
    return call_request_types


@app.get(
    "/requests",
    tags=["requests"],
    response_model=List[data.CallRequestResponse],
)
async def list_requests_route(
    contract_id: Optional[UUID] = Query(None),
    contract_address: Optional[str] = Query(None),
    caller: str = Query(...),
    limit: int = Query(100),
    offset: Optional[int] = Query(None),
    show_expired: bool = Query(False),
    live_after: Optional[int] = Query(None),
    user_authorization: Optional[Tuple[BugoutUser, UUID]] = Depends(
        request_none_or_user_auth
    ),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.CallRequestResponse]:
    """
    Allows API user to see all unexpired call requests for a given caller against a given contract.

    At least one of `contract_id` or `contract_address` must be provided as query parameters.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        requests = contracts_actions.list_call_requests(
            db_session=db_session,
            contract_id=contract_id,
            contract_address=contract_address,
            caller=caller,
            limit=limit,
            offset=offset,
            show_expired=show_expired,
            live_after=live_after,
            metatx_requester_ids=metatx_requester_ids,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except ValueError as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=500)

    return [contracts_actions.parse_call_request_response(r) for r in requests]


@app.get(
    "/requests/check",
    response_model=data.CallRequestsCheck,
)
async def check_requests_route(
    request_data: data.CreateCallRequestsAPIRequest = Body(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_session),
) -> data.CallRequestsCheck:
    """
    Implemented for pre-check until list of requests to be pushed into database.
    """
    _, token = user_authorization

    try:
        incoming_requests: Set[Tuple[str, str]] = set()
        incoming_request_ids: List[str] = []
        for r in request_data.specifications:
            caller_addr = Web3.toChecksumAddress(r.caller)
            incoming_requests.add((caller_addr, r.request_id))
            incoming_request_ids.append(r.request_id)

        if len(incoming_requests) != len(incoming_request_ids):
            raise contracts_actions.CallRequestIdDuplicates(
                "There are same call_request_id's in one request"
            )

        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        existing_requests = contracts_actions.get_call_request_from_tuple(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            requests=incoming_requests,
            contract_id=request_data.contract_id,
            contract_address=request_data.contract_address,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except contracts_actions.CallRequestIdDuplicates:
        raise EngineHTTPException(
            status_code=400, detail="There are same call_request_id's in one request"
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    existing_requests_set: Set[Tuple[str, str]] = set()
    if len(existing_requests) != 0:
        existing_requests_set = {
            (er.caller, str(er.request_id)) for er in existing_requests
        }

    return data.CallRequestsCheck(
        existing_requests=existing_requests_set,
    )


@app.get(
    "/requests/{request_id}", tags=["requests"], response_model=data.CallRequestResponse
)
async def get_request(
    request_id: UUID = Path(...),
    _: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.CallRequestResponse]:
    """
    Allows API user to see call request.

    At least one of `contract_id` or `contract_address` must be provided as query parameters.
    """
    try:
        request = contracts_actions.get_call_request(
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

    return contracts_actions.parse_call_request_response(request)


@app.post("/requests", tags=["requests"], response_model=int)
async def create_requests(
    request_data: data.CreateCallRequestsAPIRequest = Body(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_session),
) -> int:
    """
    Allows API user to register call requests from given contract details, TTL, and call specifications.

    At least one of `contract_id` or `contract_address` must be provided in the request body.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        num_requests = contracts_actions.create_request_calls(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            registered_contract_id=request_data.contract_id,
            contract_address=request_data.contract_address,
            call_specs=request_data.specifications,
            ttl_days=request_data.ttl_days,
            live_at=request_data.live_at,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except contracts_actions.InvalidAddressFormat as err:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Address not passed web3checksum validation, err: {err}",
        )
    except contracts_actions.UnsupportedCallRequestType as err:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Unsupported call request type specified, err: {err}",
        )
    except contracts_actions.CallRequestMethodValueError as err:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Unacceptable call request method specified, err: {err}",
        )
    except contracts_actions.CallRequestRequiredParamsValueError as err:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Unacceptable call request required params specified, err: {err}",
        )
    except contracts_actions.CallRequestAlreadyRegistered:
        raise EngineHTTPException(
            status_code=409,
            detail="Call request with same request_id already registered",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return num_requests


@app.delete("/requests", tags=["requests"], response_model=int)
async def delete_requests(
    request_ids: List[UUID] = Body(...),
    user_authorization: Tuple[BugoutUser, UUID] = Depends(request_user_auth),
    db_session: Session = Depends(db.yield_db_session),
) -> int:
    """
    Allows users to delete requests.
    """
    _, token = user_authorization

    try:
        metatx_requester_ids = contracts_actions.fetch_metatx_requester_ids(token=token)

        deleted_requests = contracts_actions.delete_requests(
            db_session=db_session,
            metatx_requester_ids=metatx_requester_ids,
            request_ids=request_ids,
        )
    except contracts_actions.MetatxRequestersNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="Metatx requester IDs not found",
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return deleted_requests


@app.post("/requests/{request_id}/complete", tags=["requests"])
async def complete_call_request_route(
    complete_request: data.CompleteCallRequestsAPIRequest = Body(...),
    request_id: UUID = Path(...),
    message=Depends(metatx_verify_header),
    db_session: Session = Depends(db.yield_db_session),
):
    """
    Set tx hash for specified call_request by verified account.
    """
    try:
        request = contracts_actions.complete_call_request(
            db_session=db_session,
            tx_hash=complete_request.tx_hash,
            call_request_id=request_id,
            caller=message["caller"],
        )
    except contracts_actions.CallRequestNotFound:
        raise EngineHTTPException(
            status_code=404,
            detail="There is no call request with that ID.",
        )
    except Exception as e:
        logger.error(repr(e))
        raise EngineHTTPException(status_code=500)

    return contracts_actions.parse_call_request_response(request)
