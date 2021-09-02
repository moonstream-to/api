"""
The Moonstream users HTTP API
"""
import logging
from typing import Any, Dict
import uuid

from bugout.data import BugoutToken, BugoutUser, BugoutResource
from bugout.exceptions import BugoutResponseException
from fastapi import (
    Body,
    FastAPI,
    Form,
    HTTPException,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware

from .. import data
from ..middleware import BroodAuthMiddleware
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
    DOCS_TARGET_PATH,
    ORIGINS,
    DOCS_PATHS,
    bugout_client as bc,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
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


USER_ONBOARDING_STATE = "onboarding_state"


def create_onboarding_resource(
    token,
    resource_data={
        "type": USER_ONBOARDING_STATE,
        "steps": {
            "welcome": 0,
            "subscriptions": 0,
            "stream": 0,
        },
        "is_complete": False,
    },
) -> BugoutResource:

    resource = bc.create_resource(
        token=token,
        application_id=MOONSTREAM_APPLICATION_ID,
        resource_data=resource_data,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    return resource


@app.post("/onboarding", tags=["users"], response_model=data.OnboardingState)
async def set_onboarding_state(
    request: Request,
    onboarding_data: data.OnboardingState = Body(...),
) -> data.OnboardingState:

    token = request.state.token
    response = bc.list_resources(
        token=token,
        params={"type": USER_ONBOARDING_STATE},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    resource_data = {"type": USER_ONBOARDING_STATE, **onboarding_data.dict()}
    try:
        if response.resources:
            resource = bc.update_resource(
                token=token,
                resource_id=str(response.resources[0].id),
                resource_data={"update": resource_data, "drop_keys": []},
            )
        else:
            resource = create_onboarding_resource(
                token=token, resource_data=resource_data
            )

    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)

    if (
        resource.resource_data.get("is_complete") is None
        or resource.resource_data.get("steps") is None
    ):
        logger.error(
            f"Resources did not return correct onboarding object. Resource id:{resource.id}"
        )
        raise HTTPException(status_code=500)

    result = data.OnboardingState(
        is_complete=resource.resource_data.get("is_complete", False),
        steps=resource.resource_data.get("steps", {}),
    )
    return result


@app.get("/onboarding", tags=["users"], response_model=data.OnboardingState)
async def get_onboarding_state(request: Request) -> data.OnboardingState:
    token = request.state.token
    response = bc.list_resources(
        token=token,
        params={"type": USER_ONBOARDING_STATE},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    try:

        if response.resources:
            resource = response.resources[0]
        else:
            resource = create_onboarding_resource(token=token)
    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:

        raise HTTPException(status_code=500)

    if (
        resource.resource_data.get("is_complete") is None
        or resource.resource_data.get("steps") is None
    ):
        logger.error(
            f"Resources did not return correct onboarding object. Resource id:{resource.id}"
        )
        raise HTTPException(status_code=500)
    result = data.OnboardingState(
        is_complete=resource.resource_data.get("is_complete", False),
        steps=resource.resource_data.get("steps", {}),
    )
    return result


@app.delete("/onboarding", tags=["users"], response_model=data.OnboardingState)
async def delete_onboarding_state(request: Request) -> data.OnboardingState:
    token = request.state.token
    response = bc.list_resources(
        token=token,
        params={"type": USER_ONBOARDING_STATE},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    if not response.resources:
        raise HTTPException(status_code=404, detail="not found")
    try:
        if response.resources:
            resource: BugoutResource = bc.delete_resource(
                token=token,
                resource_id=response.resources[0].id,
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )

    except BugoutResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500)

    if (
        resource.resource_data.get("is_complete") is None
        or resource.resource_data.get("steps") is None
    ):
        logger.error(
            f"Resources did not return correct onboarding object. Resource id:{resource.id}"
        )
        raise HTTPException(status_code=500)
    result = data.OnboardingState(
        is_complete=resource.resource_data.get("is_complete", False),
        steps=resource.resource_data.get("steps", {}),
    )
    return result
