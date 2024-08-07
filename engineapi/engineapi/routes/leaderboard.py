"""
Leaderboard API.
"""

import logging
from typing import Any, Dict, List, Optional, Any, Union
from uuid import UUID

from bugout.exceptions import BugoutResponseException
from fastapi import Body, Depends, FastAPI, Header, Path, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from web3 import Web3

from .. import actions, data, db
from ..middleware import (
    BugoutCORSMiddleware,
    EngineHTTPException,
    ExtractBearerTokenMiddleware,
)
from ..settings import ALLOW_ORIGINS, DOCS_TARGET_PATH
from ..settings import bugout_client as bc
from ..version import VERSION

logger = logging.getLogger(__name__)


tags_metadata = [
    {
        "name": "Public Endpoints",
        "description": "Endpoints under this tag can be accessed without any authentication. They are open to all and do not require any specific headers or tokens to be passed. Suitable for general access and non-sensitive operations.",
    },
    {
        "name": "Authorized Endpoints",
        "description": """
Endpoints under this tag require authentication. To access these endpoints, a valid `moonstream token` must be included in the request header as:

```
Authorization: Bearer <moonstream token>
```

Failure to provide a valid token will result in unauthorized access errors. These endpoints are suitable for operations that involve sensitive data or actions that only authenticated users are allowed to perform.""",
    },
]

AuthHeader = Header(
    ..., description="The expected format is 'Bearer YOUR_MOONSTREAM_ACCESS_TOKEN'."
)


leaderboard_whitelist = {
    f"/leaderboard/{DOCS_TARGET_PATH}": "GET",
    "/leaderboard/openapi.json": "GET",
    "/leaderboard/info": "GET",
    "/leaderboard/scores/changes": "GET",
    "/leaderboard/quartiles": "GET",
    "/leaderboard/count/addresses": "GET",
    "/leaderboard/position": "GET",
    "/leaderboard": "GET",
    "/leaderboard/": "GET",
    "/leaderboard/rank": "GET",
    "/leaderboard/ranks": "GET",
    "/leaderboard/scores": "GET",
    "/scores/changes": "GET",
    "/leaderboard/docs": "GET",
    "/leaderboard/openapi.json": "GET",
}

app = FastAPI(
    title=f"Moonstream Engine leaderboard API",
    description="Moonstream Engine leaderboard API endpoints.",
    version=VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)


app.add_middleware(ExtractBearerTokenMiddleware, whitelist=leaderboard_whitelist)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(ALLOW_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def points_data_dependency(request: Request):
    # Extract all query parameters as a dictionary
    query_params = dict(request.query_params)
    # Filter parameters that start with 'points_data.'
    points_data_params = {
        key[len("points_data.") :]: value
        for key, value in query_params.items()
        if key.startswith("points_data.")
    }

    return points_data_params


@app.get(
    "",
    response_model=List[data.LeaderboardPosition],
    tags=["Public Endpoints"],
)
@app.get(
    "/",
    response_model=List[data.LeaderboardPosition],
    tags=["Public Endpoints"],
)
async def leaderboard(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    limit: int = Query(10),
    offset: int = Query(0),
    db_session: Session = Depends(db.yield_db_read_only_session),
    version: Optional[str] = Query(None, description="Version of the leaderboard."),
    points_data: Dict[str, str] = Depends(points_data_dependency),
) -> List[data.LeaderboardPosition]:
    """
    Returns the leaderboard positions.
    """

    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    leaderboard_positions = actions.get_leaderboard_positions(
        db_session, leaderboard.id, limit, offset, points_data, version
    )

    result = [
        data.LeaderboardPosition(
            address=position.address,
            score=position.score,
            rank=position.rank,
            points_data=position.points_data,
        )
        for position in leaderboard_positions
    ]

    return result


@app.post(
    "",
    response_model=data.LeaderboardCreatedResponse,
    tags=["Authorized Endpoints"],
    include_in_schema=False,
)
@app.post(
    "/", response_model=data.LeaderboardCreatedResponse, tags=["Authorized Endpoints"]
)
async def create_leaderboard(
    request: Request,
    leaderboard: data.LeaderboardCreateRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardCreatedResponse:
    """
    Create leaderboard.
    """

    token = request.state.token

    try:
        created_leaderboard = actions.create_leaderboard(
            db_session,
            title=leaderboard.title,
            description=leaderboard.description,
            token=token,
            wallet_connect=leaderboard.wallet_connect,
            blockchain_ids=leaderboard.blockchain_ids,
            columns_names=leaderboard.columns_names,
        )
    except actions.LeaderboardCreateError as e:
        logger.error(f"Error while creating leaderboard: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail="Leaderboard creation failed. Please try again.",
        )

    except Exception as e:
        logger.error(f"Error while creating leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    # Add resource to the leaderboard

    return data.LeaderboardCreatedResponse(
        id=created_leaderboard.id,
        title=created_leaderboard.title,
        description=created_leaderboard.description,
        resource_id=created_leaderboard.resource_id,
        wallet_connect=created_leaderboard.wallet_connect,
        blockchain_ids=created_leaderboard.blockchain_ids,
        columns_names=created_leaderboard.columns_names,
        created_at=created_leaderboard.created_at,
        updated_at=created_leaderboard.updated_at,
    )


@app.put(
    "/{leaderboard_id}",
    response_model=data.LeaderboardUpdatedResponse,
    tags=["Authorized Endpoints"],
)
async def update_leaderboard(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    leaderboard: data.LeaderboardUpdateRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardUpdatedResponse:
    """
    Update leaderboard.
    """

    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if access != True:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        updated_leaderboard = actions.update_leaderboard(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            title=leaderboard.title,
            description=leaderboard.description,
            wallet_connect=leaderboard.wallet_connect,
            blockchain_ids=leaderboard.blockchain_ids,
            columns_names=leaderboard.columns_names,
        )
    except actions.LeaderboardUpdateError as e:
        logger.error(f"Error while updating leaderboard: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail="Leaderboard update failed. Please try again.",
        )

    except Exception as e:
        logger.error(f"Error while updating leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardUpdatedResponse(
        id=updated_leaderboard.id,
        title=updated_leaderboard.title,
        description=updated_leaderboard.description,
        resource_id=updated_leaderboard.resource_id,
        wallet_connect=updated_leaderboard.wallet_connect,
        blockchain_ids=updated_leaderboard.blockchain_ids,
        columns_names=updated_leaderboard.columns_names,
        created_at=updated_leaderboard.created_at,
        updated_at=updated_leaderboard.updated_at,
    )


@app.delete(
    "/{leaderboard_id}",
    response_model=data.LeaderboardDeletedResponse,
    tags=["Authorized Endpoints"],
)
async def delete_leaderboard(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardDeletedResponse:
    """
    Delete leaderboard.
    """

    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if access != True:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        deleted_leaderboard = actions.delete_leaderboard(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except actions.LeaderboardDeleteError as e:
        logger.error(f"Error while deleting leaderboard: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail="Leaderboard deletion failed. Please try again.",
        )

    except Exception as e:
        logger.error(f"Error while deleting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardDeletedResponse(
        id=deleted_leaderboard.id,
        title=deleted_leaderboard.title,
        description=deleted_leaderboard.description,
        resource_id=deleted_leaderboard.resource_id,
        wallet_connect=deleted_leaderboard.wallet_connect,
        blockchain_ids=deleted_leaderboard.blockchain_ids,
        columns_names=deleted_leaderboard.columns_names,
        created_at=deleted_leaderboard.created_at,
        updated_at=deleted_leaderboard.updated_at,
    )


@app.get(
    "/leaderboards",
    response_model=List[data.Leaderboard],
    tags=["Authorized Endpoints"],
)
async def get_leaderboards(
    request: Request,
    db_session: Session = Depends(db.yield_db_read_only_session),
    Authorization: str = AuthHeader,
) -> List[data.Leaderboard]:
    """
    Returns leaderboard list to which user has access.
    """

    token = request.state.token

    try:
        leaderboards = actions.get_leaderboards(db_session, token)
    except actions.LeaderboardsResourcesNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboards not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboards: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    results = [
        data.Leaderboard(
            id=leaderboard.id,
            title=leaderboard.title,
            description=leaderboard.description,
            resource_id=leaderboard.resource_id,
            wallet_connect=leaderboard.wallet_connect,
            blockchain_ids=leaderboard.blockchain_ids,
            columns_names=leaderboard.columns_names,
            created_at=leaderboard.created_at,
            updated_at=leaderboard.updated_at,
        )
        for leaderboard in leaderboards
    ]

    return results


@app.get(
    "/count/addresses",
    response_model=data.CountAddressesResponse,
    tags=["Public Endpoints"],
)
async def count_addresses(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    version: Optional[int] = Query(None, description="Version of the leaderboard."),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> data.CountAddressesResponse:
    """
    Returns the number of addresses in the leaderboard.
    """

    ### Check if leaderboard exists
    try:
        actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    count = actions.get_leaderboard_total_count(db_session, leaderboard_id, version)

    return data.CountAddressesResponse(count=count)


@app.get(
    "/info", response_model=data.LeaderboardInfoResponse, tags=["Public Endpoints"]
)
async def leadeboard_info(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_read_only_session),
    version: Optional[int] = Query(None, description="Version of the leaderboard."),
) -> data.LeaderboardInfoResponse:
    """
    Returns leaderboard info.
    """
    try:
        leaderboard = actions.get_leaderboard_info(db_session, leaderboard_id, version)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardInfoResponse(
        id=leaderboard.id,
        title=leaderboard.title,
        description=leaderboard.description,
        users_count=leaderboard.users_count,
        last_updated_at=leaderboard.last_update,
    )


@app.get(
    "/scores/changes",
    response_model=List[data.LeaderboardScoresChangesResponse],
    tags=["Public Endpoints"],
)
async def get_scores_changes(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.LeaderboardScoresChangesResponse]:
    """
    Returns the score history for the given address.
    """

    try:
        scores = actions.get_leaderboard_scores_changes(db_session, leaderboard_id)
    except actions.LeaderboardIsEmpty:
        raise EngineHTTPException(status_code=204, detail="Leaderboard is empty.")

    except Exception as e:
        logger.error(f"Error while getting scores: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return [
        data.LeaderboardScoresChangesResponse(
            players_count=score.players_count,
            date=score.date,
        )
        for score in scores
    ]


@app.get("/quartiles", response_model=data.QuartilesResponse, tags=["Public Endpoints"])
async def quartiles(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_read_only_session),
    version: Optional[int] = Query(None, description="Version of the leaderboard."),
) -> data.QuartilesResponse:
    """
    Returns the quartiles of the leaderboard.
    """
    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    try:
        q1, q2, q3 = actions.get_qurtiles(db_session, leaderboard_id, version)

    except actions.LeaderboardIsEmpty:
        raise EngineHTTPException(status_code=204, detail="Leaderboard is empty.")
    except Exception as e:
        logger.error(f"Error while getting quartiles: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    result = data.QuartilesResponse(
        percentile_25={"address": q1.address, "rank": q1.rank, "score": q1.score},
        percentile_50={"address": q2.address, "rank": q2.rank, "score": q2.score},
        percentile_75={"address": q3.address, "rank": q3.rank, "score": q3.score},
    )

    return result


@app.get(
    "/position",
    response_model=List[data.LeaderboardPosition],
    tags=["Public Endpoints"],
)
async def position(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    address: str = Query(..., description="Address to get position for."),
    window_size: int = Query(1, description="Amount of positions up and down."),
    limit: int = Query(10),
    offset: int = Query(0),
    normalize_addresses: bool = Query(
        True, description="Normalize addresses to checksum."
    ),
    version: Optional[int] = Query(None, description="Version of the leaderboard."),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.LeaderboardPosition]:
    """
    Returns the leaderboard posotion for the given address.
    With given window size.
    """

    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    if normalize_addresses:
        address = Web3.toChecksumAddress(address)

    positions = actions.get_position(
        db_session,
        leaderboard_id,
        address,
        window_size,
        limit,
        offset,
        version,
    )

    results = [
        data.LeaderboardPosition(
            address=position.address,
            score=position.score,
            rank=position.rank,
            points_data=position.points_data,
        )
        for position in positions
    ]

    return results


@app.get(
    "/rank",
    response_model=List[data.LeaderboardPosition],
    tags=["Public Endpoints"],
)
async def rank(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    rank: int = Query(1, description="Rank to get."),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
    version: Optional[int] = Query(None, description="Version of the leaderboard."),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.LeaderboardPosition]:
    """
    Returns the leaderboard scores for the given rank.
    """

    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    leaderboard_rank = actions.get_rank(
        db_session,
        leaderboard_id,
        rank,
        limit=limit,
        offset=offset,
        version_number=version,
    )

    results = [
        data.LeaderboardPosition(
            address=position.address,
            score=position.score,
            rank=position.rank,
            points_data=position.points_data,
        )
        for position in leaderboard_rank
    ]
    return results


@app.get("/ranks", response_model=List[data.RanksResponse], tags=["Public Endpoints"])
async def ranks(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    version: Optional[int] = Query(None, description="Version of the leaderboard."),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> List[data.RanksResponse]:
    """
    Returns the leaderboard rank buckets overview with score and size of bucket.
    """

    ### Check if leaderboard exists
    try:
        actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    ranks = actions.get_ranks(db_session, leaderboard_id, version)
    results = [
        data.RanksResponse(
            score=rank.score,
            rank=rank.rank,
            size=rank.size,
        )
        for rank in ranks
    ]
    return results


@app.get(
    "/scores",
    response_model=data.LeaderboardScore,
    tags=["Public Endpoints"],
)
async def leaderboard_score(
    address: str = Query(..., description="Address to get position for."),
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    version: Optional[int] = Query(None, description="Version of the leaderboard."),
    normalize_addresses: bool = Query(
        True, description="Normalize addresses to checksum."
    ),
    db_session: Session = Depends(db.yield_db_read_only_session),
) -> data.LeaderboardScore:
    """
    Returns the leaderboard posotion for the given address.
    """

    ### Check if leaderboard exists
    try:
        actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    if normalize_addresses:
        address = Web3.toChecksumAddress(address)

    score = actions.get_leaderboard_score(
        db_session,
        leaderboard_id,
        address,
        version,
    )

    if score is None:
        raise EngineHTTPException(status_code=204, detail="Score not found.")

    return data.LeaderboardScore(
        leaderboard_id=score.leaderboard_id,
        address=score.address,
        score=score.score,
        points_data=score.points_data,
    )


@app.put(
    "/{leaderboard_id}/scores",
    response_model=List[data.LeaderboardScore],
    tags=["Authorized Endpoints"],
)
async def leaderboard_push_scores(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    scores: List[data.Score] = Body(
        ..., description="Scores to put to the leaderboard."
    ),
    normalize_addresses: bool = Query(
        True, description="Normalize addresses to checksum."
    ),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> List[data.LeaderboardScore]:
    """
    Put the leaderboard to the database.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        new_version = actions.create_leaderboard_version(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
        )
    except Exception as e:
        logger.error(f"Error while creating leaderboard version: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    try:
        leaderboard_points = actions.add_scores(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            scores=scores,
            normalize_addresses=normalize_addresses,
            version_number=new_version.version_number,
        )
    except actions.DuplicateLeaderboardAddressError as e:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Duplicates in push to database is disallowed.\n List of duplicates:{e.duplicates}.\n Please handle duplicates manualy.",
        )
    except actions.LeaderboardNormalizeScoresError as e:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Normalize scores failed for addresses: {e.normilize_errors}.",
        )
    except actions.LeaderboardPushScoreError as e:
        raise EngineHTTPException(
            status_code=500,
            detail=f"Write scores to database failed",
        )
    except Exception as e:
        logger.error(f"Score update failed with error: {e}")
        raise EngineHTTPException(status_code=500, detail="Score update failed.")

    try:
        actions.change_publish_leaderboard_version_status(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=new_version.version_number,
            published=True,
        )
    except Exception as e:
        logger.error(f"Error while updating leaderboard version: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    try:
        actions.delete_previous_versions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            threshold_version_number=new_version.version_number,
        )
    except Exception as e:
        logger.error(f"Error while deleting leaderboard versions: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    result = [
        data.LeaderboardScore(
            leaderboard_id=score["leaderboard_id"],
            address=score["address"],
            score=score["score"],
            points_data=score["points_data"],
        )
        for score in leaderboard_points
    ]

    return result


@app.get(
    "/{leaderboard_id}/config",
    response_model=data.LeaderboardConfig,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_read_only_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardConfig:
    """
    Get leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        leaderboard_config = actions.get_leaderboard_config(
            leaderboard_id=leaderboard_id,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardConfig(**leaderboard_config)


@app.put(
    "/{leaderboard_id}/config",
    response_model=data.LeaderboardConfig,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config_update(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    config: data.LeaderboardConfigUpdate = Body(..., description="Leaderboard config."),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardConfig:
    """
    Update leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        leaderboard_config = actions.update_leaderboard_config(
            leaderboard_id=leaderboard_id,
            config=config,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except Exception as e:
        logger.error(f"Error while updating leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardConfig(**leaderboard_config)


@app.post(
    "/{leaderboard_id}/config/activate",
    response_model=bool,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config_activate(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> bool:
    """
    Activate leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        actions.activate_leaderboard_config(
            leaderboard_id=leaderboard_id,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except actions.LeaderboardConfigAlreadyActive as e:
        raise EngineHTTPException(
            status_code=409,
            detail="Leaderboard config is already active.",
        )
    except Exception as e:
        logger.error(f"Error while activating leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return True


@app.post(
    "/{leaderboard_id}/config/deactivate",
    response_model=bool,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config_deactivate(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> bool:
    """
    Deactivate leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        actions.deactivate_leaderboard_config(
            leaderboard_id=leaderboard_id,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except actions.LeaderboardConfigAlreadyInactive as e:
        raise EngineHTTPException(
            status_code=409,
            detail="Leaderboard config is already inactive.",
        )
    except Exception as e:
        logger.error(f"Error while deactivating leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return True


@app.get(
    "/{leaderboard_id}/versions",
    response_model=List[data.LeaderboardVersion],
    tags=["Authorized Endpoints"],
)
async def leaderboard_versions_list(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_read_only_session),
    Authorization: str = AuthHeader,
) -> List[data.LeaderboardVersion]:
    """
    Get leaderboard versions list.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard version."
        )

    try:
        leaderboard_versions = actions.get_leaderboard_versions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard versions list: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    result = [
        data.LeaderboardVersion(
            leaderboard_id=version.leaderboard_id,
            version=version.version_number,
            published=version.published,
            created_at=version.created_at,
            updated_at=version.updated_at,
        )
        for version in leaderboard_versions
    ]

    return result


@app.get(
    "/{leaderboard_id}/versions/{version}",
    response_model=data.LeaderboardVersion,
    tags=["Authorized Endpoints"],
)
async def leaderboard_version_handler(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    version: int = Path(..., description="Version of the leaderboard."),
    db_session: Session = Depends(db.yield_db_read_only_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardVersion:
    """
    Get leaderboard version.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        leaderboard_version = actions.get_leaderboard_version(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard version: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardVersion(
        leaderboard_id=leaderboard_version.leaderboard_id,
        version=leaderboard_version.version_number,
        published=leaderboard_version.published,
        created_at=leaderboard_version.created_at,
        updated_at=leaderboard_version.updated_at,
    )


@app.post(
    "/{leaderboard_id}/versions",
    response_model=data.LeaderboardVersion,
    tags=["Authorized Endpoints"],
)
async def create_leaderboard_version(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    request_body: data.LeaderboardVersionRequest = Body(
        ...,
        description="JSON object specifying whether to publish or unpublish version.",
    ),
    Authorization: str = AuthHeader,
) -> data.LeaderboardVersion:
    """
    Create leaderboard version.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        new_version = actions.create_leaderboard_version(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            publish=request_body.publish,
        )
    except Exception as e:
        logger.error(f"Error while creating leaderboard version: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardVersion(
        leaderboard_id=new_version.leaderboard_id,
        version=new_version.version_number,
        published=new_version.published,
        created_at=new_version.created_at,
        updated_at=new_version.updated_at,
    )


@app.put(
    "/{leaderboard_id}/versions/{version}",
    response_model=data.LeaderboardVersion,
    tags=["Authorized Endpoints"],
)
async def update_leaderboard_version_handler(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    version: int = Path(..., description="Version of the leaderboard."),
    request_body: data.LeaderboardVersionRequest = Body(
        ...,
        description="JSON object specifying whether to publish or unpublish version.",
    ),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardVersion:
    """
    Update leaderboard version.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard version."
        )

    try:
        leaderboard_version = actions.change_publish_leaderboard_version_status(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version,
            published=request_body.publish,
        )
    except Exception as e:
        logger.error(f"Error while updating leaderboard version: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardVersion(
        leaderboard_id=leaderboard_version.leaderboard_id,
        version=leaderboard_version.version_number,
        published=leaderboard_version.published,
        created_at=leaderboard_version.created_at,
        updated_at=leaderboard_version.updated_at,
    )


@app.delete(
    "/{leaderboard_id}/versions/{version}",
    response_model=data.LeaderboardVersion,
    tags=["Authorized Endpoints"],
)
async def delete_leaderboard_version_handler(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    version: int = Path(..., description="Version of the leaderboard."),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardVersion:
    """
    Delete leaderboard version.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session, leaderboard_id=leaderboard_id, token=token
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard version."
        )

    try:
        leaderboard_version = actions.delete_leaderboard_version(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )
    except Exception as e:
        logger.error(f"Error while deleting leaderboard version: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardVersion(
        leaderboard_id=leaderboard_version.leaderboard_id,
        version=leaderboard_version.version_number,
        published=leaderboard_version.published,
        created_at=leaderboard_version.created_at,
        updated_at=leaderboard_version.updated_at,
    )


@app.get(
    "/{leaderboard_id}/versions/{version}/scores",
    response_model=List[data.LeaderboardPosition],
    tags=["Authorized Endpoints"],
)
async def leaderboard_version_scores_handler(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    version: int = Path(..., description="Version of the leaderboard."),
    limit: int = Query(10),
    offset: int = Query(0),
    db_session: Session = Depends(db.yield_db_read_only_session),
    Authorization: str = AuthHeader,
) -> List[data.LeaderboardPosition]:
    """
    Get leaderboard version scores.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session, leaderboard_id=leaderboard_id, token=token
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard version."
        )

    try:
        leaderboard_version_scores = actions.get_leaderboard_version_scores(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard version scores: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    result = [
        data.LeaderboardPosition(
            address=score.address,
            score=score.score,
            rank=score.rank,
            points_data=score.points_data,
        )
        for score in leaderboard_version_scores
    ]

    return result


@app.put(
    "/{leaderboard_id}/versions/{version}/scores",
    response_model=List[data.LeaderboardScore],
    tags=["Authorized Endpoints"],
)
async def leaderboard_version_push_scores_handler(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    version: int = Path(..., description="Version of the leaderboard."),
    scores: List[data.Score] = Body(
        ..., description="Scores to put to the leaderboard version."
    ),
    normalize_addresses: bool = Query(
        True, description="Normalize addresses to checksum."
    ),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> List[data.LeaderboardScore]:
    """
    Put the leaderboard version to the database.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session, leaderboard_id=leaderboard_id, token=token
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard version."
        )

    try:
        leaderboard_version = actions.get_leaderboard_version(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard version not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard version: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    try:
        leaderboard_points = actions.add_scores(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            scores=scores,
            normalize_addresses=normalize_addresses,
            version_number=leaderboard_version.version_number,
        )
    except actions.DuplicateLeaderboardAddressError as e:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Duplicates in push to database is disallowed.\n List of duplicates:{e.duplicates}.\n Please handle duplicates manualy.",
        )
    except actions.LeaderboardNormalizeScoresError as e:
        raise EngineHTTPException(
            status_code=400,
            detail=f"Normalize scores failed for addresses: {e.normilize_errors}.",
        )
    except actions.LeaderboardPushScoreError as e:
        raise EngineHTTPException(
            status_code=500,
            detail=f"Write scores to database failed",
        )
    except Exception as e:
        logger.error(f"Score update failed with error: {e}")
        raise EngineHTTPException(status_code=500, detail="Score update failed.")

    result = [
        data.LeaderboardScore(
            leaderboard_id=score["leaderboard_id"],
            address=score["address"],
            score=score["score"],
            points_data=score["points_data"],
        )
        for score in leaderboard_points
    ]

    return result
