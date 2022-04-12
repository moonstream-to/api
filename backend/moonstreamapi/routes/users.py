"""
The Moonstream users HTTP API
"""
import logging
import uuid
from typing import Any, Dict, Optional

from bugout.data import BugoutResource, BugoutToken, BugoutUser, BugoutUserTokens
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Body, Form, Request

from .. import data
from ..actions import create_onboarding_resource
from ..middleware import MoonstreamHTTPException
from ..settings import BUGOUT_REQUEST_TIMEOUT_SECONDS, MOONSTREAM_APPLICATION_ID
from ..settings import bugout_client as bc

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.post("/", tags=["users"], response_model=BugoutUser)
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
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return user


@router.get("/", tags=["users"], response_model=BugoutUser)
async def get_user_handler(request: Request) -> BugoutUser:
    user: BugoutUser = request.state.user
    return user


@router.post("/password/reset_initiate", tags=["users"], response_model=Dict[str, Any])
async def restore_password_handler(email: str = Form(...)) -> Dict[str, Any]:
    try:
        response = bc.restore_password(email=email)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return response


@router.post("/password/reset_complete", tags=["users"], response_model=BugoutUser)
async def reset_password_handler(
    reset_id: str = Form(...), new_password: str = Form(...)
) -> BugoutUser:
    try:
        response = bc.reset_password(reset_id=reset_id, new_password=new_password)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return response


@router.post("/password/change", tags=["users"], response_model=BugoutUser)
async def change_password_handler(
    request: Request, current_password: str = Form(...), new_password: str = Form(...)
) -> BugoutUser:
    token = request.state.token
    try:
        user = bc.change_password(
            token=token, current_password=current_password, new_password=new_password
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return user


@router.delete("/", tags=["users"], response_model=BugoutUser)
async def delete_user_handler(
    request: Request, password: str = Form(...)
) -> BugoutUser:
    user = request.state.user
    token = request.state.token
    try:
        user = bc.delete_user(token=token, user_id=user.id, password=password)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return user


@router.post("/token", tags=["tokens"], response_model=BugoutToken)
async def login_handler(
    username: str = Form(...),
    password: str = Form(...),
    token_note: Optional[str] = Form(None),
) -> BugoutToken:
    try:
        token: BugoutToken = bc.create_token(
            username=username,
            password=password,
            application_id=MOONSTREAM_APPLICATION_ID,
            token_note=token_note,
        )

    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return token


@router.get("/tokens", tags=["tokens"], response_model=BugoutUserTokens)
async def tokens_handler(request: Request) -> BugoutUserTokens:
    token = request.state.token
    try:
        response = bc.get_user_tokens(
            token, timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS, active=True
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return response


@router.put("/token", tags=["tokens"], response_model=BugoutToken)
async def token_update_handler(
    token_note: str = Form(...), access_token: str = Form(...)
) -> BugoutToken:
    try:
        response = bc.update_token(token=access_token, token_note=token_note)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return response


@router.post("/revoke/{access_token}", tags=["tokens"], response_model=uuid.UUID)
async def delete_token_by_id_handler(
    request: Request, access_token: uuid.UUID
) -> uuid.UUID:
    token = request.state.token
    try:
        response = bc.revoke_token(
            token=token,
            target_token=access_token,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return response


@router.delete("/token", tags=["tokens"], response_model=uuid.UUID)
async def logout_handler(request: Request) -> uuid.UUID:
    token = request.state.token
    try:
        token_id: uuid.UUID = bc.revoke_token(token=token)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    return token_id


@router.post("/onboarding", tags=["users"], response_model=data.OnboardingState)
async def set_onboarding_state(
    request: Request,
    onboarding_data: data.OnboardingState = Body(...),
) -> data.OnboardingState:

    token = request.state.token
    try:
        response = bc.list_resources(
            token=token,
            params={"type": data.USER_ONBOARDING_STATE},
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        resource_data = {"type": data.USER_ONBOARDING_STATE, **onboarding_data.dict()}
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
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500)

    if (
        resource.resource_data.get("is_complete") is None
        or resource.resource_data.get("steps") is None
    ):
        logger.error(
            f"Resources did not return correct onboarding object. Resource id:{resource.id}"
        )
        raise MoonstreamHTTPException(status_code=500)

    result = data.OnboardingState(
        is_complete=resource.resource_data.get("is_complete", False),
        steps=resource.resource_data.get("steps", {}),
    )
    return result


@router.get("/onboarding", tags=["users"], response_model=data.OnboardingState)
async def get_onboarding_state(request: Request) -> data.OnboardingState:
    token = request.state.token
    try:
        response = bc.list_resources(
            token=token,
            params={"type": data.USER_ONBOARDING_STATE},
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

        if response.resources:
            resource = response.resources[0]
        else:
            resource = create_onboarding_resource(token=token)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:

        raise MoonstreamHTTPException(status_code=500)

    if (
        resource.resource_data.get("is_complete") is None
        or resource.resource_data.get("steps") is None
    ):
        logger.error(
            f"Resources did not return correct onboarding object. Resource id:{resource.id}"
        )
        raise MoonstreamHTTPException(status_code=500)
    result = data.OnboardingState(
        is_complete=resource.resource_data.get("is_complete", False),
        steps=resource.resource_data.get("steps", {}),
    )
    return result


@router.delete("/onboarding", tags=["users"], response_model=data.OnboardingState)
async def delete_onboarding_state(request: Request) -> data.OnboardingState:
    token = request.state.token
    try:
        response = bc.list_resources(
            token=token,
            params={"type": data.USER_ONBOARDING_STATE},
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        if not response.resources:
            raise MoonstreamHTTPException(status_code=404, detail="not found")
        if response.resources:
            resource: BugoutResource = bc.delete_resource(
                token=token,
                resource_id=response.resources[0].id,
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )

    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise MoonstreamHTTPException(status_code=500)

    if (
        resource.resource_data.get("is_complete") is None
        or resource.resource_data.get("steps") is None
    ):
        logger.error(
            f"Resources did not return correct onboarding object. Resource id:{resource.id}"
        )
        raise MoonstreamHTTPException(status_code=500)
    result = data.OnboardingState(
        is_complete=resource.resource_data.get("is_complete", False),
        steps=resource.resource_data.get("steps", {}),
    )
    return result
