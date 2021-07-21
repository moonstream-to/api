"""
The Moonstream users HTTP API
"""
import logging
from typing import Any, Dict
import uuid

from bugout.data import BugoutToken, BugoutUser
from bugout.exceptions import BugoutResponseException
from fastapi import (
    FastAPI,
    Form,
    HTTPException,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware

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
    {"name": "users", "description": "Operations with users."},
    {"name": "tokens", "description": "Operations with user tokens."},
]

app = FastAPI(
    title=f"Moonstream API.",
    description="The Bugout blockchain inspector API.",
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
whitelist_paths.update({"/users": "POST", "/users/tokens": "POST"})
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)


@app.post("/", tags=["users"], response_model=BugoutUser)
async def create_user_handler(
    username: str = Form(...), email: str = Form(...), password: str = Form(...)
) -> BugoutUser:
    try:
        user: BugoutUser = bc.create_user(
            username, email, password, MOONSTREAM_APPLICATION_ID
        )
    except BugoutResponseException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        return HTTPException(status_code=500)
    return user


@app.get("/", tags=["users"], response_model=BugoutUser)
async def get_user_handler(request: Request) -> BugoutUser:
    user: BugoutUser = request.state.user
    if str(user.application_id) != str(MOONSTREAM_APPLICATION_ID):
        raise HTTPException(
            status_code=403, detail="User does not belong to this application"
        )
    return user


@app.post("/tokens", tags=["tokens"], response_model=BugoutToken)
async def login_handler(
    username: str = Form(...), password: str = Form(...)
) -> BugoutToken:
    try:
        token: BugoutToken = bc.create_token(
            username, password, MOONSTREAM_APPLICATION_ID
        )
    except BugoutResponseException as e:
        return HTTPException(status_code=e.status_code)
    except Exception as e:
        return HTTPException(status_code=500)
    return token


@app.delete("/tokens", tags=["tokens"], response_model=uuid.UUID)
async def logout_handler(request: Request) -> uuid.UUID:
    token = request.state.token
    try:
        token_id: uuid.UUID = bc.revoke_token(token)
    except BugoutResponseException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        return HTTPException(status_code=500)
    return token_id
