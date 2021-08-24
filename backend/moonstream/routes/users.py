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
whitelist_paths.update(
    {
        "/users": "POST",
        "/users/token": "POST",
        "/users/password/reset_initiate": "POST",
        "/users/password/reset_complete": "POST",
    }
)
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)


@app.post("/", tags=["users"], response_model=BugoutUser)
async def create_user_handler(
    username: str = Form(...), email: str = Form(...), password: str = Form(...)
) -> BugoutUser:
    try:
        user: BugoutUser = bc.create_user(
            username=username,
            email=email,
            password=password,
            application_id=MOONSTREAM_APPLICATION_ID,
        )
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return user


@app.get("/", tags=["users"], response_model=BugoutUser)
async def get_user_handler(request: Request) -> BugoutUser:
    user: BugoutUser = request.state.user
    return user


@app.post("/password/reset_initiate", tags=["users"], response_model=Dict[str, Any])
async def restore_password_handler(email: str = Form(...)) -> Dict[str, Any]:
    try:
        response = bc.restore_password(email=email)
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return response


@app.post("/password/reset_complete", tags=["users"], response_model=BugoutUser)
async def reset_password_handler(
    reset_id: str = Form(...), new_password: str = Form(...)
) -> BugoutUser:
    try:
        response = bc.reset_password(reset_id=reset_id, new_password=new_password)
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return response


@app.post("/password/change", tags=["users"], response_model=BugoutUser)
async def change_password_handler(
    request: Request, current_password: str = Form(...), new_password: str = Form(...)
) -> BugoutUser:
    token = request.state.token
    try:
        user = bc.change_password(
            token=token, current_password=current_password, new_password=new_password
        )
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return user


@app.delete("/", tags=["users"], response_model=BugoutUser)
async def delete_user_handler(
    request: Request, password: str = Form(...)
) -> BugoutUser:
    user = request.state.user
    token = request.state.token
    try:
        user = bc.delete_user(token=token, user_id=user.id, password=password)
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return user


@app.post("/token", tags=["tokens"], response_model=BugoutToken)
async def login_handler(
    username: str = Form(...), password: str = Form(...)
) -> BugoutToken:
    try:
        token: BugoutToken = bc.create_token(
            username=username,
            password=password,
            application_id=MOONSTREAM_APPLICATION_ID,
        )
    except BugoutResponseException as e:
        raise HTTPException(
            status_code=e.status_code, detail=f"Error from Brood API: {e.detail}"
        )
    except Exception as e:
        raise HTTPException(status_code=500)
    return token


@app.delete("/token", tags=["tokens"], response_model=uuid.UUID)
async def logout_handler(request: Request) -> uuid.UUID:
    token = request.state.token
    try:
        token_id: uuid.UUID = bc.revoke_token(token=token)
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)
    return token_id
