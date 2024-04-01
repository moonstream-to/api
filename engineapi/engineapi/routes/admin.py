"""
Moonstream Engine Admin API.
"""
import logging
from typing import Optional, Any, Dict
from uuid import UUID

from web3 import Web3
from fastapi import Body, FastAPI, Request, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from .. import actions
from .. import data
from .. import db
from ..middleware import EngineHTTPException, EngineAuthMiddleware, BugoutCORSMiddleware
from ..settings import DOCS_TARGET_PATH
from ..version import VERSION


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tags_metadata = [{"name": "admin", "description": "Moonstream Engine Admin API"}]

whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(
    {
        "/admin/docs": "GET",
        "/admin/openapi.json": "GET",
    }
)

app = FastAPI(
    title=f"Moonstream Engine Admin API",
    description="Moonstream Engine Admin API endpoints.",
    version=VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)


app.add_middleware(EngineAuthMiddleware, whitelist=whitelist_paths)

app.add_middleware(
    BugoutCORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/drops", response_model=data.DropListResponse)
async def get_drop_list_handler(
    request: Request,
    blockchain: str,
    contract_address: str,
    drop_number: Optional[int] = Query(None),
    terminus_address: Optional[str] = Query(None),
    terminus_pool_id: Optional[int] = Query(None),
    active: Optional[bool] = Query(None),
    limit: int = 20,
    offset: int = 0,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropListResponse:
    """
    Get list of drops for a given dropper contract and drop number.
    """

    contract_address = Web3.toChecksumAddress(contract_address)

    # try:
    #     actions.ensure_contract_admin_token_holder(
    #         blockchain, contract_address, request.state.address
    #     )
    # except actions.AuthorizationError as e:
    #     logger.error(e)
    #     raise EngineHTTPException(status_code=403)
    # except NoResultFound:
    #     raise EngineHTTPException(status_code=404, detail="Drop not found")

    if terminus_address:
        terminus_address = Web3.toChecksumAddress(terminus_address)

    try:
        results = actions.get_drops(
            db_session=db_session,
            dropper_contract_address=contract_address,
            blockchain=blockchain,
            drop_number=drop_number,
            terminus_address=terminus_address,
            terminus_pool_id=terminus_pool_id,
            active=active,
            limit=limit,
            offset=offset,
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="No drops found.")
    except Exception as e:
        logger.error(f"Can't get drops. Failed with error: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't get claims")

    return data.DropListResponse(
        drops=[
            data.DropsResponseItem(
                id=result.id,
                title=result.title,
                description=result.description,
                terminus_address=result.terminus_address,
                terminus_pool_id=result.terminus_pool_id,
                claim_block_deadline=result.claim_block_deadline,
                drop_number=result.drop_number,
                active=result.active,
                dropper_contract_address=result.dropper_contract_address,
            )
            for result in results
        ]
    )


@app.post("/drops", response_model=data.DropCreatedResponse)
async def create_drop(
    request: Request,
    register_request: data.DropRegisterRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropCreatedResponse:
    """
    Create a drop for a given dropper contract.
    """
    try:
        actions.ensure_dropper_contract_owner(
            db_session, register_request.dropper_contract_id, request.state.address
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Dropper contract not found")
    except Exception as e:
        logger.error(e)
        raise EngineHTTPException(status_code=500)

    if register_request.terminus_address:
        register_request.terminus_address = Web3.toChecksumAddress(
            register_request.terminus_address
        )

    try:
        claim = actions.create_claim(
            db_session=db_session,
            dropper_contract_id=register_request.dropper_contract_id,
            title=register_request.title,
            description=register_request.description,
            claim_block_deadline=register_request.claim_block_deadline,
            terminus_address=register_request.terminus_address,
            terminus_pool_id=register_request.terminus_pool_id,
            claim_id=register_request.claim_id,
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Dropper contract not found")
    except Exception as e:
        logger.error(f"Can't create claim: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't create claim")

    return data.DropCreatedResponse(
        dropper_claim_id=claim.id,
        dropper_contract_id=claim.dropper_contract_id,
        title=claim.title,
        description=claim.description,
        claim_block_deadline=claim.claim_block_deadline,
        terminus_address=claim.terminus_address,
        terminus_pool_id=claim.terminus_pool_id,
        claim_id=claim.claim_id,
    )


@app.put(
    "/drops/{dropper_claim_id}/activate",
    response_model=data.DropUpdatedResponse,
)
async def activate_drop(
    request: Request,
    dropper_claim_id: UUID,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropUpdatedResponse:
    """
    Activate a given drop by drop id.
    """
    try:
        actions.ensure_admin_token_holder(
            db_session, dropper_claim_id, request.state.address
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Drop not found")

    try:
        drop = actions.activate_drop(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Drop not found")
    except Exception as e:
        logger.error(f"Can't activate drop: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't activate drop")

    return data.DropUpdatedResponse(
        dropper_claim_id=drop.id,
        dropper_contract_id=drop.dropper_contract_id,
        title=drop.title,
        description=drop.description,
        claim_block_deadline=drop.claim_block_deadline,
        terminus_address=drop.terminus_address,
        terminus_pool_id=drop.terminus_pool_id,
        claim_id=drop.claim_id,
        active=drop.active,
    )


@app.put(
    "/drops/{dropper_claim_id}/deactivate",
    response_model=data.DropUpdatedResponse,
)
async def deactivate_drop(
    request: Request,
    dropper_claim_id: UUID,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropUpdatedResponse:
    """
    Activate a given drop by drop id.
    """
    try:
        actions.ensure_admin_token_holder(
            db_session, dropper_claim_id, request.state.address
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Drop not found")

    try:
        drop = actions.deactivate_drop(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Drop not found")
    except Exception as e:
        logger.error(f"Can't activate drop: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't activate drop")

    return data.DropUpdatedResponse(
        dropper_claim_id=drop.id,
        dropper_contract_id=drop.dropper_contract_id,
        title=drop.title,
        description=drop.description,
        claim_block_deadline=drop.claim_block_deadline,
        terminus_address=drop.terminus_address,
        terminus_pool_id=drop.terminus_pool_id,
        claim_id=drop.claim_id,
        active=drop.active,
    )


@app.patch("/drops/{dropper_claim_id}", response_model=data.DropUpdatedResponse)
async def update_drop(
    request: Request,
    dropper_claim_id: UUID,
    update_request: data.DropUpdateRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropUpdatedResponse:
    """
    Update a given drop by drop id.
    """
    try:
        actions.ensure_admin_token_holder(
            db_session, dropper_claim_id, request.state.address
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Drop not found")

    try:
        drop = actions.update_drop(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
            title=update_request.title,
            description=update_request.description,
            claim_block_deadline=update_request.claim_block_deadline,
            terminus_address=update_request.terminus_address,
            terminus_pool_id=update_request.terminus_pool_id,
            claim_id=update_request.claim_id,
            address=request.state.address,
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="Drop not found")
    except Exception as e:
        logger.error(f"Can't update drop: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't update drop")

    return data.DropUpdatedResponse(
        dropper_claim_id=drop.id,
        dropper_contract_id=drop.dropper_contract_id,
        title=drop.title,
        description=drop.description,
        claim_block_deadline=drop.claim_block_deadline,
        terminus_address=drop.terminus_address,
        terminus_pool_id=drop.terminus_pool_id,
        claim_id=drop.claim_id,
        active=drop.active,
    )


@app.get("/drops/{dropper_claim_id}/claimants", response_model=data.ClaimantsResponse)
async def get_claimants(
    request: Request,
    dropper_claim_id: UUID,
    amount: Optional[int] = None,
    added_by: Optional[str] = None,
    address: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db_session: Session = Depends(db.yield_db_session),
) -> data.ClaimantsResponse:
    """
    Get list of claimants for a given dropper contract.
    """
    if address:
        address = Web3.toChecksumAddress(address)

    try:
        actions.ensure_admin_token_holder(
            db_session, dropper_claim_id, request.state.address
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except Exception as e:
        logger.error(e)
        raise EngineHTTPException(status_code=500)

    try:
        results = actions.get_claimants(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
            amount=amount,
            added_by=added_by,
            address=address,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.info(f"Can't add claimants for claim {dropper_claim_id} with error: {e}")
        raise EngineHTTPException(status_code=500, detail=f"Error adding claimants")

    return data.ClaimantsResponse(
        claimants=[
            data.Claimant(
                address=result.address,
                amount=result.amount,
                raw_amount=result.raw_amount,
                added_by=result.added_by,
            )
            for result in results
        ]
    )


@app.post(
    "/drops/{dropper_claim_id}/claimants/batch", response_model=data.ClaimantsResponse
)
async def add_claimants(
    request: Request,
    dropper_claim_id: UUID,
    claimants_list: data.BatchAddClaimantsRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.ClaimantsResponse:
    """
    Add addresses to particular claim
    """

    try:
        actions.ensure_admin_token_holder(
            db_session, dropper_claim_id, request.state.address
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except Exception as e:
        logger.error(e)
        raise EngineHTTPException(status_code=500)

    try:
        results = actions.add_claimants(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
            claimants=claimants_list.claimants,
            added_by=request.state.address,
        )
    except actions.DublicateClaimantError:
        raise EngineHTTPException(
            status_code=400,
            detail="Dublicated claimants in request please deduplicate them",
        )
    except Exception as e:
        logger.info(f"Can't add claimants for claim {dropper_claim_id} with error: {e}")
        raise EngineHTTPException(status_code=500, detail=f"Error adding claimants")

    return data.ClaimantsResponse(claimants=results)


@app.delete(
    "/drops/{dropper_claim_id}/claimants", response_model=data.RemoveClaimantsResponse
)
async def delete_claimants(
    request: Request,
    dropper_claim_id: UUID,
    claimants_list: data.BatchRemoveClaimantsRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.RemoveClaimantsResponse:
    """
    Remove addresses to particular claim
    """

    try:
        actions.ensure_admin_token_holder(
            db_session,
            dropper_claim_id,
            request.state.address,
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except Exception as e:
        logger.error(e)
        raise EngineHTTPException(status_code=500)

    try:
        results = actions.delete_claimants(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
            addresses=claimants_list.claimants,
        )
    except Exception as e:
        logger.info(
            f"Can't remove claimants for claim {dropper_claim_id} with error: {e}"
        )
        raise EngineHTTPException(status_code=500, detail=f"Error removing claimants")

    return data.RemoveClaimantsResponse(addresses=results)


@app.get("/drops/{dropper_claim_id}/claimants/search", response_model=data.Claimant)
async def get_claimant_in_drop(
    request: Request,
    dropper_claim_id: UUID,
    address: str,
    db_session: Session = Depends(db.yield_db_session),
) -> data.Claimant:
    """
    Return claimant from drop
    """
    try:
        actions.ensure_admin_token_holder(
            db_session,
            dropper_claim_id,
            request.state.address,
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except Exception as e:
        logger.error(e)
        raise EngineHTTPException(status_code=500)

    try:
        claimant = actions.get_claimant(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
            address=address,
        )

    except NoResultFound:
        raise EngineHTTPException(
            status_code=404, detail="Address not present in that drop."
        )
    except Exception as e:
        logger.error(f"Can't get claimant: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't get claimant")

    return data.Claimant(
        address=claimant.address, amount=claimant.amount, raw_amount=claimant.raw_amount
    )


@app.post("/drop/{dropper_claim_id}/refetch")
async def refetch_drop_signatures(
    request: Request,
    dropper_claim_id: UUID,
    db_session: Session = Depends(db.yield_db_session),
) -> Any:
    """
    Refetch signatures for a drop
    """

    try:
        actions.ensure_admin_token_holder(
            db_session, dropper_claim_id, request.state.address
        )
    except actions.AuthorizationError as e:
        logger.error(e)
        raise EngineHTTPException(status_code=403)
    except Exception as e:
        logger.error(e)
        raise EngineHTTPException(status_code=500)

    try:
        signatures = actions.refetch_drop_signatures(
            db_session=db_session, dropper_claim_id=dropper_claim_id
        )
    except Exception as e:
        logger.info(
            f"Can't refetch signatures for drop {dropper_claim_id} with error: {e}"
        )
        raise EngineHTTPException(
            status_code=500, detail=f"Error refetching signatures"
        )

    return signatures
