"""
Leaderboard API.
"""
import logging
from uuid import UUID

from web3 import Web3
from fastapi import FastAPI, Request, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import Any, Dict, List, Optional

from .. import actions
from .. import data
from .. import db
from ..middleware import (
    ExtractBearerTokenMiddleware,
    EngineHTTPException,
    BugoutCORSMiddleware,
)
from ..settings import DOCS_TARGET_PATH, bugout_client as bc
from ..version import VERSION

logger = logging.getLogger(__name__)


tags_metadata = [
    {"name": "leaderboard", "description": "Moonstream Engine leaderboard API"}
]


leaderboad_whitelist = {
    "/leaderboard/info": "GET",
    "/leaderboard/quartiles": "GET",
    "/leaderboard/count/addresses": "GET",
    "/leaderboard/position": "GET",
    "/leaderboard": "GET",
    "/leaderboard/rank": "GET",
    "/leaderboard/ranks": "GET",
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


app.add_middleware(ExtractBearerTokenMiddleware, whitelist=leaderboad_whitelist)

app.add_middleware(
    BugoutCORSMiddleware,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/info")
async def get_leadeboard(
    leaderboard_id: UUID,
    db_session: Session = Depends(db.yield_db_session),
):
    """
    Returns leaderboard info.
    """
    try:
        leaderboard = actions.get_leaderboard(db_session, leaderboard_id)
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
    )


@app.get("/leaderboards")
async def get_leaderboards(
    request: Request, db_session: Session = Depends(db.yield_db_session)
):
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
            created_at=leaderboard.created_at,
            updated_at=leaderboard.updated_at,
        )
        for leaderboard in leaderboards
    ]

    return results


@app.get("/count/addresses")
async def count_addresses(
    leaderboard_id: UUID,
    db_session: Session = Depends(db.yield_db_session),
):
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

    count = actions.get_leaderboard_total_count(db_session, leaderboard_id)

    return data.CountAddressesResponse(count=count)


@app.get("/quartiles")
async def quartiles(
    leaderboard_id: UUID,
    db_session: Session = Depends(db.yield_db_session),
):
    """
    Returns the quartiles of the leaderboard.
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

    try:
        q1, q2, q3 = actions.get_qurtiles(db_session, leaderboard_id)

    except actions.LeaderboardIsEmpty:
        return Response(status_code=204)
    except Exception as e:
        logger.error(f"Error while getting quartiles: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.QuartilesResponse(
        percentile_25={"address": q1[0], "score": q1[1], "rank": q1[2]},
        percentile_50={"address": q2[0], "score": q2[1], "rank": q2[2]},
        percentile_75={"address": q3[0], "score": q3[1], "rank": q3[2]},
    )


@app.get("/position", response_model=List[data.LeaderboardPosition])
async def position(
    leaderboard_id: UUID,
    address: str,
    window_size: int = 1,
    limit: int = 10,
    offset: int = 0,
    normalize_addresses: bool = True,
    db_session: Session = Depends(db.yield_db_session),
):
    """
    Returns the leaderboard posotion for the given address.
    With given window size.
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

    positions = actions.get_position(
        db_session, leaderboard_id, address, window_size, limit, offset
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


@app.get("")
@app.get("/")
async def leaderboard(
    leaderboard_id: UUID,
    limit: int = 10,
    offset: int = 0,
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.LeaderboardPosition]:
    """
    Returns the leaderboard positions.
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

    leaderboard_positions = actions.get_leaderboard_positions(
        db_session, leaderboard_id, limit, offset
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


@app.get("/rank")
async def rank(
    leaderboard_id: UUID,
    rank: int = 1,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.LeaderboardPosition]:
    """
    Returns the leaderboard scores for the given rank.
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

    leaderboard_rank = actions.get_rank(
        db_session, leaderboard_id, rank, limit=limit, offset=offset
    )
    results = [
        data.LeaderboardPosition(
            address=rank_position.address,
            score=rank_position.score,
            rank=rank_position.rank,
            points_data=rank_position.points_data,
        )
        for rank_position in leaderboard_rank
    ]
    return results


@app.get("/ranks", response_model=List[data.RanksResponse])
async def ranks(
    leaderboard_id: UUID, db_session: Session = Depends(db.yield_db_session)
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

    ranks = actions.get_ranks(db_session, leaderboard_id)
    results = [
        data.RanksResponse(
            score=rank.score,
            rank=rank.rank,
            size=rank.size,
        )
        for rank in ranks
    ]
    return results


@app.put("/{leaderboard_id}/scores", response_model=List[data.LeaderboardScore])
async def leaderboard_push_scores(
    request: Request,
    leaderboard_id: UUID,
    scores: List[data.Score],
    overwrite: bool = False,
    normalize_addresses: bool = True,
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.LeaderboardScore]:
    """
    Put the leaderboard to the database.
    """

    access = actions.check_leaderboard_resource_permissions(
        db_session=db_session,
        leaderboard_id=leaderboard_id,
        token=request.state.token,
    )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

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

    try:
        leaderboard_points = actions.add_scores(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            scores=scores,
            overwrite=overwrite,
            normalize_addresses=normalize_addresses,
        )
    except actions.DuplicateLeaderboardAddressError as e:
        raise EngineHTTPException(
            status_code=409,
            detail=f"Duplicates in push to database is disallowed.\n List of duplicates:{e.duplicates}.\n Please handle duplicates manualy.",
        )
    except actions.LeaderboardDeleteScoresError as e:
        logger.error(f"Delete scores failed with error: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail=f"Delete scores failed.",
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
