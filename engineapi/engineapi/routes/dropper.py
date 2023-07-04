"""
Lootbox API.
"""
import logging
from typing import List, Optional, Any, Dict
from uuid import UUID


from fastapi import FastAPI, Body, Request, Depends, Query
from hexbytes import HexBytes
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from web3 import Web3

from engineapi.models import DropperClaimant

from .. import actions
from ..contracts import Dropper_interface
from .. import data
from .. import db
from .. import signatures
from ..middleware import EngineHTTPException, EngineAuthMiddleware, BugoutCORSMiddleware
from ..settings import (
    DOCS_TARGET_PATH,
    BLOCKCHAIN_WEB3_PROVIDERS,
    UNSUPPORTED_BLOCKCHAIN_ERROR_MESSAGE,
)
from ..version import VERSION


logger = logging.getLogger(__name__)


tags_metadata = [{"name": "dropper", "description": "Moonstream Engine old drops API"}]


whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(
    {
        "/drops": "GET",
        "/drops/batch": "GET",
        "/drops/claims": "GET",
        "/drops/contracts": "GET",
        "/drops/docs": "GET",
        "/drops/terminus": "GET",
        "/drops/blockchains": "GET",
        "/drops/terminus/claims": "GET",
        "/drops/openapi.json": "GET",
    }
)

app = FastAPI(
    title=f"Moonstream Engine old drops API",
    description="Moonstream Engine old drops API endpoints.",
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


# TODO(zomglings): Take blockchain as a parameter (perhaps optional) here. Browser-based workflow is that
# user would already have selected their blockchain when connecting Metamask.
@app.get("", response_model=data.DropResponse)
@app.get("/", response_model=data.DropResponse)
async def get_drop_handler(
    dropper_claim_id: UUID,
    address: str,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropResponse:
    """
    Get signed transaction for user with the given address.
    """

    address = Web3.toChecksumAddress(address)

    try:
        claimant = actions.get_claimant(db_session, dropper_claim_id, address)
    except NoResultFound:
        raise EngineHTTPException(
            status_code=403, detail="You are not authorized to claim that reward"
        )
    except Exception as e:
        raise EngineHTTPException(status_code=500, detail="Can't get claimant")

    try:
        claimant_db_object = (
            db_session.query(DropperClaimant)
            .filter(DropperClaimant.id == claimant.dropper_claimant_id)
            .one()
        )
    except Exception as err:
        logger.error(
            f"Can't get claimant object for drop: {dropper_claim_id} and address: {address}"
        )
        raise EngineHTTPException(status_code=500, detail="Can't get claimant object.")

    if not claimant.active:
        raise EngineHTTPException(
            status_code=403, detail="Cannot claim rewards for an inactive claim"
        )

    # If block deadline has already been exceeded - the contract (or frontend) will handle it.
    if claimant.claim_block_deadline is None:
        raise EngineHTTPException(
            status_code=403,
            detail="Cannot claim rewards for a claim with no block deadline",
        )

    transformed_amount = claimant.raw_amount
    if transformed_amount is None:
        transformed_amount = actions.transform_claim_amount(
            db_session, dropper_claim_id, claimant.amount
        )

    signature = claimant.signature
    if signature is None or not claimant.is_recent_signature:
        dropper_contract = Dropper_interface.Contract(
            BLOCKCHAIN_WEB3_PROVIDERS[claimant.blockchain],
            claimant.dropper_contract_address,
        )
        message_hash_raw = dropper_contract.claimMessageHash(
            claimant.claim_id,
            claimant.address,
            claimant.claim_block_deadline,
            int(transformed_amount),
        ).call()

        message_hash = HexBytes(message_hash_raw).hex()

        try:
            signature = signatures.DROP_SIGNER.sign_message(message_hash)
            claimant_db_object.signature = signature
            db_session.commit()
        except signatures.AWSDescribeInstancesFail:
            raise EngineHTTPException(status_code=500)
        except signatures.SignWithInstanceFail:
            raise EngineHTTPException(status_code=500)
        except Exception as err:
            logger.error(f"Unexpected error in signing message process: {err}")
            raise EngineHTTPException(status_code=500)

    return data.DropResponse(
        claimant=claimant.address,
        amount=str(transformed_amount),
        claim_id=claimant.claim_id,
        block_deadline=claimant.claim_block_deadline,
        signature=signature,
        title=claimant.title,
        description=claimant.description,
    )


@app.get("/batch", response_model=List[data.DropBatchResponseItem])
async def get_drop_batch_handler(
    blockchain: str,
    address: str,
    limit: int = 10,
    offset: int = 0,
    current_block_number: Optional[int] = Query(None),
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.DropBatchResponseItem]:
    """
    Get signed transaction for all user drops.
    """
    if blockchain not in BLOCKCHAIN_WEB3_PROVIDERS:
        raise EngineHTTPException(
            status_code=404, detail=UNSUPPORTED_BLOCKCHAIN_ERROR_MESSAGE
        )

    address = Web3.toChecksumAddress(address)

    try:
        claimant_drops = actions.get_claimant_drops(
            db_session, blockchain, address, current_block_number, limit, offset
        )
    except NoResultFound:
        raise EngineHTTPException(
            status_code=403, detail="You are not authorized to claim that reward"
        )
    except Exception as e:
        logger.error(e)
        raise EngineHTTPException(status_code=500, detail="Can't get claimant")

    # get claimants
    try:
        claimants = (
            db_session.query(DropperClaimant)
            .filter(
                DropperClaimant.id.in_(
                    [item.dropper_claimant_id for item in claimant_drops]
                )
            )
            .all()
        )
    except Exception as err:
        logger.error(f"Can't get claimant objects for address: {address}")
        raise EngineHTTPException(status_code=500, detail="Can't get claimant objects.")

    claimants_dict = {item.id: item for item in claimants}

    # generate list of claims

    claims: List[data.DropBatchResponseItem] = []

    commit_required = False

    for claimant_drop in claimant_drops:
        transformed_amount = claimant_drop.raw_amount

        if transformed_amount is None:
            transformed_amount = actions.transform_claim_amount(
                db_session, claimant_drop.dropper_claim_id, claimant_drop.amount
            )

        signature = claimant_drop.signature
        if signature is None or not claimant_drop.is_recent_signature:
            dropper_contract = Dropper_interface.Contract(
                BLOCKCHAIN_WEB3_PROVIDERS[blockchain],
                claimant_drop.dropper_contract_address,
            )

            message_hash_raw = dropper_contract.claimMessageHash(
                claimant_drop.claim_id,
                claimant_drop.address,
                claimant_drop.claim_block_deadline,
                int(transformed_amount),
            ).call()

            message_hash = HexBytes(message_hash_raw).hex()

            try:
                signature = signatures.DROP_SIGNER.sign_message(message_hash)
                claimants_dict[claimant_drop.dropper_claimant_id].signature = signature
                commit_required = True
            except signatures.AWSDescribeInstancesFail:
                raise EngineHTTPException(status_code=500)
            except signatures.SignWithInstanceFail:
                raise EngineHTTPException(status_code=500)
            except Exception as err:
                logger.error(f"Unexpected error in signing message process: {err}")
                raise EngineHTTPException(status_code=500)

        claims.append(
            data.DropBatchResponseItem(
                claimant=claimant_drop.address,
                amount=int(transformed_amount),
                amount_string=str(transformed_amount),
                claim_id=claimant_drop.claim_id,
                block_deadline=claimant_drop.claim_block_deadline,
                signature=signature,
                dropper_claim_id=claimant_drop.dropper_claim_id,
                dropper_contract_address=claimant_drop.dropper_contract_address,
                blockchain=claimant_drop.blockchain,
                active=claimant_drop.active,
                title=claimant_drop.title,
                description=claimant_drop.description,
            )
        )

    if commit_required:
        db_session.commit()

    return claims


@app.get("/blockchains")
async def get_drops_blockchains_handler(
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.DropperBlockchainResponse]:
    """
    Get list of blockchains.
    """

    try:
        results = actions.list_drops_blockchains(db_session=db_session)
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="No drops found.")
    except Exception as e:
        logger.error(f"Can't get list of drops end with error: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't get drops")

    response = [
        data.DropperBlockchainResponse(
            blockchain=result.blockchain,
        )
        for result in results
    ]

    return response


@app.get("/contracts", response_model=List[data.DropperContractResponse])
async def get_dropper_contracts_handler(
    blockchain: Optional[str] = Query(None),
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.DropperContractResponse]:
    """
    Get list of drops for a given dropper contract.
    """

    try:
        results = actions.list_dropper_contracts(
            db_session=db_session, blockchain=blockchain
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="No drops found.")
    except Exception as e:
        logger.error(f"Can't get list of dropper contracts end with error: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't get contracts")

    response = [
        data.DropperContractResponse(
            id=result.id,
            blockchain=result.blockchain,
            address=result.address,
            title=result.title,
            description=result.description,
            image_uri=result.image_uri,
        )
        for result in results
    ]

    return response


@app.get("/terminus")
async def get_drops_terminus_handler(
    blockchain: str = Query(None),
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.DropperTerminusResponse]:
    """
    Return distinct terminus pools
    """

    try:
        results = actions.list_drops_terminus(
            db_session=db_session, blockchain=blockchain
        )
    except Exception as e:
        logger.error(f"Can't get list of terminus contracts end with error: {e}")
        raise EngineHTTPException(
            status_code=500, detail="Can't get terminus contracts"
        )

    response = [
        data.DropperTerminusResponse(
            terminus_address=result.terminus_address,
            terminus_pool_id=result.terminus_pool_id,
            blockchain=result.blockchain,
        )
        for result in results
    ]

    return response


@app.get("/claims", response_model=data.DropListResponse)
async def get_drop_list_handler(
    blockchain: str,
    claimant_address: str,
    dropper_contract_address: Optional[str] = Query(None),
    terminus_address: Optional[str] = Query(None),
    terminus_pool_id: Optional[int] = Query(None),
    active: Optional[bool] = Query(None),
    limit: int = 20,
    offset: int = 0,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropListResponse:
    """
    Get list of drops for a given dropper contract and claimant address.
    """

    if dropper_contract_address:
        dropper_contract_address = Web3.toChecksumAddress(dropper_contract_address)

    if claimant_address:
        claimant_address = Web3.toChecksumAddress(claimant_address)

    if terminus_address:
        terminus_address = Web3.toChecksumAddress(terminus_address)

    try:
        results = actions.get_claims(
            db_session=db_session,
            dropper_contract_address=dropper_contract_address,
            blockchain=blockchain,
            claimant_address=claimant_address,
            terminus_address=terminus_address,
            terminus_pool_id=terminus_pool_id,
            active=active,
            limit=limit,
            offset=offset,
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="No drops found.")
    except Exception as e:
        logger.error(
            f"Can't get claims for user {claimant_address} end with error: {e}"
        )
        raise EngineHTTPException(status_code=500, detail="Can't get claims")

    return data.DropListResponse(drops=[result for result in results])


@app.get("/claims/{dropper_claim_id}", response_model=data.DropperClaimResponse)
async def get_drop_handler(
    request: Request,
    dropper_claim_id: str,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropperClaimResponse:
    """
    Get list of drops for a given dropper contract and claimant address.
    """

    try:
        drop = actions.get_drop(
            db_session=db_session, dropper_claim_id=dropper_claim_id
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="No drops found.")
    except Exception as e:
        logger.error(f"Can't get drop {dropper_claim_id} end with error: {e}")
        raise EngineHTTPException(status_code=500, detail="Can't get drop")

    if drop.terminus_address is not None and drop.terminus_pool_id is not None:
        try:
            actions.ensure_admin_token_holder(
                db_session, dropper_claim_id, request.state.address
            )
        except actions.AuthorizationError as e:
            logger.error(e)
            raise EngineHTTPException(status_code=403)
        except NoResultFound:
            raise EngineHTTPException(status_code=404, detail="Drop not found")

    return data.DropperClaimResponse(
        id=drop.id,
        dropper_contract_id=drop.dropper_contract_id,
        title=drop.title,
        description=drop.description,
        active=drop.active,
        claim_block_deadline=drop.claim_block_deadline,
        terminus_address=drop.terminus_address,
        terminus_pool_id=drop.terminus_pool_id,
        claim_id=drop.claim_id,
    )


@app.get("/terminus/claims", response_model=data.DropListResponse)
async def get_drop_terminus_list_handler(
    blockchain: str,
    terminus_address: str,
    terminus_pool_id: int,
    dropper_contract_address: Optional[str] = Query(None),
    active: Optional[bool] = Query(None),
    limit: int = 20,
    offset: int = 0,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropListResponse:
    """
    Get list of drops for a given terminus address.
    """

    if dropper_contract_address:
        dropper_contract_address = Web3.toChecksumAddress(dropper_contract_address)

    terminus_address = Web3.toChecksumAddress(terminus_address)

    try:
        results = actions.get_terminus_claims(
            db_session=db_session,
            dropper_contract_address=dropper_contract_address,
            blockchain=blockchain,
            terminus_address=terminus_address,
            terminus_pool_id=terminus_pool_id,
            active=active,
            limit=limit,
            offset=offset,
        )
    except NoResultFound:
        raise EngineHTTPException(status_code=404, detail="No drops found.")
    except Exception as e:
        logger.error(
            f"Can't get Terminus claims (blockchain={blockchain}, address={terminus_address}, pool_id={terminus_pool_id}): {e}"
        )
        raise EngineHTTPException(status_code=500, detail="Can't get claims")

    return data.DropListResponse(drops=[result for result in results])


@app.post("/claims", response_model=data.DropCreatedResponse)
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
    "/claims/{dropper_claim_id}/activate",
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
    "/claims/{dropper_claim_id}/deactivate",
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


@app.put("/claims/{dropper_claim_id}", response_model=data.DropUpdatedResponse)
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


@app.get("/claimants", response_model=data.DropListResponse)
async def get_claimants(
    request: Request,
    dropper_claim_id: UUID,
    limit: int = 10,
    offset: int = 0,
    db_session: Session = Depends(db.yield_db_session),
) -> data.DropListResponse:
    """
    Get list of claimants for a given dropper contract.
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
        results = actions.get_claimants(
            db_session=db_session,
            dropper_claim_id=dropper_claim_id,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.info(f"Can't add claimants for claim {dropper_claim_id} with error: {e}")
        raise EngineHTTPException(status_code=500, detail=f"Error adding claimants")

    return data.DropListResponse(drops=list(results))


@app.post("/claimants", response_model=data.ClaimantsResponse)
async def add_claimants(
    request: Request,
    add_claimants_request: data.DropAddClaimantsRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.ClaimantsResponse:
    """
    Add addresses to particular claim
    """

    try:
        actions.ensure_admin_token_holder(
            db_session, add_claimants_request.dropper_claim_id, request.state.address
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
            dropper_claim_id=add_claimants_request.dropper_claim_id,
            claimants=add_claimants_request.claimants,
            added_by=request.state.address,
        )

    except actions.DublicateClaimantError:
        raise EngineHTTPException(
            status_code=400,
            detail="Dublicated claimants in request please deduplicate them.",
        )
    except Exception as e:
        logger.info(
            f"Can't add claimants for claim {add_claimants_request.dropper_claim_id} with error: {e}"
        )
        raise EngineHTTPException(status_code=500, detail=f"Error adding claimants")

    return data.ClaimantsResponse(claimants=results)


@app.delete("/claimants", response_model=data.RemoveClaimantsResponse)
async def delete_claimants(
    request: Request,
    remove_claimants_request: data.DropRemoveClaimantsRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
) -> data.RemoveClaimantsResponse:
    """
    Remove addresses to particular claim
    """

    try:
        actions.ensure_admin_token_holder(
            db_session,
            remove_claimants_request.dropper_claim_id,
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
            dropper_claim_id=remove_claimants_request.dropper_claim_id,
            addresses=remove_claimants_request.addresses,
        )
    except Exception as e:
        logger.info(
            f"Can't remove claimants for claim {remove_claimants_request.dropper_claim_id} with error: {e}"
        )
        raise EngineHTTPException(status_code=500, detail=f"Error removing claimants")

    return data.RemoveClaimantsResponse(addresses=results)


@app.get("/claimants/search", response_model=data.Claimant)
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

    return data.Claimant(address=claimant.address, amount=claimant.amount)


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
