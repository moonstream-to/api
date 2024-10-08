import base64
import json
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence, Set, Tuple
from uuid import UUID

from bugout.data import BugoutResource, BugoutResources, BugoutUserWithGroups
from bugout.exceptions import BugoutResponseException
from eip712.messages import EIP712Message, _hash_eip191_message
from eth_account.messages import encode_defunct
from fastapi import Depends, Header, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer
from hexbytes import HexBytes
from pydantic import AnyHttpUrl, parse_obj_as
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from web3 import Web3
from web3.auto import w3 as w3_auto

from . import data
from .auth import (
    EIP712_AUTHORIZATION_TYPES,
    MoonstreamAuthorizationExpired,
    MoonstreamAuthorizationStructureError,
    MoonstreamAuthorizationVerificationError,
    verify,
)
from .rc import REDIS_CONFIG_CORS_KEY, rc_client
from .settings import (
    ALLOW_ORIGINS,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_ADMIN_ID,
    MOONSTREAM_APPLICATION_ID,
)
from .settings import bugout_client as bc

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class InvalidAuthHeaderFormat(Exception):
    """
    Raised when authorization header not pass validation.
    """


class BugoutUnverifiedAuth(Exception):
    """
    Raised when attempted access by unverified Brood account.
    """


class BugoutAuthWrongApp(Exception):
    """
    Raised when user does not belong to this application.
    """


def parse_auth_header(auth_header: str) -> Tuple[str, str]:
    """
    Returns: auth_format and user_token passed in authorization header.
    """
    auth_list = auth_header.split()
    if len(auth_list) != 2:
        raise InvalidAuthHeaderFormat("Wrong authorization header")

    return auth_list[0], auth_list[1]


def bugout_auth(token: str) -> BugoutUserWithGroups:
    """
    Extended bugout.get_user with additional checks.
    """
    user: BugoutUserWithGroups = bc.auth(token)
    if not user.verified:
        raise BugoutUnverifiedAuth("Only verified accounts can have access")
    if str(user.application_id) != str(MOONSTREAM_APPLICATION_ID):
        raise BugoutAuthWrongApp("User does not belong to this application")

    return user


def brood_auth(token: UUID) -> BugoutUserWithGroups:
    try:
        user: BugoutUserWithGroups = bugout_auth(token=token)
    except BugoutUnverifiedAuth:
        logger.info(f"Attempted access by unverified Brood account: {user.id}")
        raise EngineHTTPException(
            status_code=403,
            detail="Only verified accounts can have access",
        )
    except BugoutAuthWrongApp:
        raise EngineHTTPException(
            status_code=403,
            detail="User does not belong to this application",
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        logger.error(f"Error processing Brood response: {str(e)}")
        raise EngineHTTPException(
            status_code=500,
            detail="Internal server error",
        )

    return user


async def request_user_auth(
    token: UUID = Depends(oauth2_scheme),
) -> Tuple[BugoutUserWithGroups, UUID]:
    user = brood_auth(token=token)
    return user, token


async def request_none_or_user_auth(
    authorization: str = Header(None),
) -> Optional[Tuple[BugoutUserWithGroups, UUID]]:
    """
    Fetch Bugout user if authorization token provided.
    """
    if authorization is not None:
        token: str = ""
        try:
            _, token = parse_auth_header(auth_header=authorization)
        except InvalidAuthHeaderFormat:
            raise EngineHTTPException(
                status_code=403, detail="Wrong authorization header"
            )
        except Exception as e:
            logger.error(f"Error parsing auth header: {str(e)}")
            raise EngineHTTPException(status_code=500, detail="Internal server error")

        if token != "":
            user = brood_auth(token=token)
            return user, token

    return None


async def metatx_verify_header(
    authorization: str = Header(None),
) -> Optional[Dict[str, Any]]:
    message: Optional[Dict[str, Any]] = None
    if authorization is not None:
        try:
            auth_format, user_token = parse_auth_header(auth_header=authorization)
        except InvalidAuthHeaderFormat:
            raise EngineHTTPException(
                status_code=403, detail="Wrong authorization header"
            )
        except Exception as e:
            logger.error(f"Error parsing auth header: {str(e)}")
            raise EngineHTTPException(status_code=500, detail="Internal server error")

        if auth_format != "metatx":
            raise EngineHTTPException(
                status_code=403,
                detail=f"Wrong authorization header format: {auth_format}",
            )

        try:
            json_payload_str = base64.b64decode(user_token).decode("utf-8")
            payload = json.loads(json_payload_str)
            verify(
                authorization_type=EIP712_AUTHORIZATION_TYPES["MetaTXAuthorization"],
                authorization_payload=payload,
                signature_name_input="signature",
            )
            message = {
                "caller": Web3.toChecksumAddress(payload.get("caller")),
                "expires_at": payload.get("expires_at"),
            }
        except MoonstreamAuthorizationVerificationError as e:
            logger.info("MetaTX authorization verification error: %s", e)
            raise EngineHTTPException(status_code=403, detail="Invalid signer")
        except MoonstreamAuthorizationExpired as e:
            logger.info("MetaTX authorization expired: %s", e)
            raise EngineHTTPException(status_code=403, detail="Authorization expired")
        except MoonstreamAuthorizationStructureError as e:
            logger.info("MetaTX authorization incorrect structure error: %s", e)
            raise EngineHTTPException(
                status_code=403, detail="Incorrect signature structure"
            )
        except Exception as e:
            logger.error("Unexpected exception: %s", e)
            raise EngineHTTPException(status_code=500, detail="Internal server error")

        return message


class BroodAuthMiddleware(BaseHTTPMiddleware):
    """
    Checks the authorization header on the request. If it represents a verified Brood user,
    create another request and get groups user belongs to, after this
    adds a brood_user attribute to the request.state. Otherwise raises a 403 error.

    Taken almost verbatim from the Moonstream repo:
    https://github.com/bugout-dev/moonstream/blob/99504a431acdd903259d1c4014a2808ce5a104c1/backend/moonstreamapi/middleware.py
    """

    def __init__(self, app, whitelist: Optional[Dict[str, str]] = None):
        self.whitelist: Dict[str, str] = {}
        if whitelist is not None:
            self.whitelist = whitelist
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        # Filter out endpoints with proper method to work without Bearer token (as create_user, login, etc)
        path = request.url.path.rstrip("/")
        method = request.method
        if path in self.whitelist.keys() and self.whitelist[path] == method:
            return await call_next(request)

        authorization = request.headers.get("authorization")
        if authorization is None:
            return Response(
                status_code=403,
                content="No authorization header passed with request",
            )

        try:
            _, user_token = parse_auth_header(auth_header=authorization)
        except InvalidAuthHeaderFormat:
            return Response(status_code=403, content="Wrong authorization header")
        except Exception as e:
            logger.error(f"Error parsing auth header: {str(e)}")
            return Response(status_code=500, content="Internal server error")

        try:
            user: BugoutUserWithGroups = bugout_auth(token=user_token)
        except BugoutUnverifiedAuth:
            logger.info(f"Attempted access by unverified Brood account: {user.id}")
            return Response(
                status_code=403,
                content="Only verified accounts can have access",
            )
        except BugoutAuthWrongApp:
            return Response(
                status_code=403, content="User does not belong to this application"
            )
        except BugoutResponseException as e:
            return Response(status_code=e.status_code, content=e.detail)
        except Exception as e:
            logger.error(f"Error processing Brood response: {str(e)}")
            return Response(status_code=500, content="Internal server error")

        request.state.user = user
        request.state.token = user_token
        return await call_next(request)


class EngineAuthMiddleware(BaseHTTPMiddleware):
    """
    Checks the authorization header on the request. It it represents
    a correctly signer message, adds address and deadline attributes to the request.state.
    Otherwise raises a 403 error.
    """

    def __init__(self, app, whitelist: Optional[Dict[str, str]] = None):
        self.whitelist: Dict[str, str] = {}
        if whitelist is not None:
            self.whitelist = whitelist
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        # Filter out whitelisted endpoints without web3 authorization
        path = request.url.path.rstrip("/")
        method = request.method

        if path in self.whitelist.keys() and self.whitelist[path] == method:
            return await call_next(request)

        raw_authorization_header = request.headers.get("authorization")

        if raw_authorization_header is None:
            return Response(
                status_code=403, content="No authorization header passed with request"
            )

        authorization_header_components = raw_authorization_header.split()
        if (
            len(authorization_header_components) != 2
            or authorization_header_components[0].lower() != "moonstream"
        ):
            return Response(
                status_code=403,
                content="Incorrect format for authorization header. Expected 'Authorization: moonstream <base64_encoded_json_payload>'",
            )

        try:
            json_payload_str = base64.b64decode(
                authorization_header_components[-1]
            ).decode("utf-8")

            payload = json.loads(json_payload_str)
            verified = verify(
                authorization_type=EIP712_AUTHORIZATION_TYPES[
                    "MoonstreamAuthorization"
                ],
                authorization_payload=payload,
                signature_name_input="signed_message",
            )
            address = payload.get("address")
            if address is not None:
                address = Web3.toChecksumAddress(address)
            else:
                raise Exception("Address in payload is None")
        except MoonstreamAuthorizationVerificationError as e:
            logger.info("Moonstream authorization verification error: %s", e)
            return Response(status_code=403, content="Invalid authorization header")
        except MoonstreamAuthorizationExpired as e:
            logger.info("Moonstream authorization expired: %s", e)
            return Response(status_code=403, content="Authorization expired")
        except Exception as e:
            logger.error("Unexpected exception: %s", e)
            return Response(status_code=500, content="Internal server error")

        request.state.address = address
        request.state.verified = verified

        return await call_next(request)


class EngineHTTPException(HTTPException):
    """
    Extended HTTPException to handle 500 Internal server errors
    and send crash reports.
    """

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        internal_error: Exception = None,
    ):
        super().__init__(status_code, detail, headers)
        if internal_error is not None:
            print(internal_error)
            # reporter.error_report(internal_error)


class ExtractBearerTokenMiddleware(BaseHTTPMiddleware):
    """
    Checks the authorization header on the request and extract token.
    """

    def __init__(self, app, whitelist: Optional[Dict[str, str]] = None):
        self.whitelist: Dict[str, str] = {}
        if whitelist is not None:
            self.whitelist = whitelist
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        # Filter out endpoints with proper method to work without Bearer token (as create_user, login, etc)
        path = request.url.path.rstrip("/")
        method = request.method
        if path in self.whitelist.keys() and self.whitelist[path] == method:
            return await call_next(request)

        authorization_header = request.headers.get("authorization")
        if authorization_header is None:
            return Response(
                status_code=403, content="No authorization header passed with request"
            )
        authorization_header_components = authorization_header.split()
        if len(authorization_header_components) != 2:
            return Response(status_code=403, content="Wrong authorization header")
        user_token: str = authorization_header_components[-1]

        request.state.token = user_token

        return await call_next(request)


def parse_origins_from_resources(
    resources: List[BugoutResources],
) -> data.CORSOrigins:
    """
    Parse list of CORS origins with HTTP validation and remove duplications.
    """
    cors_origins = data.CORSOrigins(origins_set=set())
    for resource in resources:
        origin = resource.resource_data.get("origin", "")
        try:
            parse_obj_as(AnyHttpUrl, origin)
            cors_origins.origins_set.add(origin)
            cors_origins.resources.append(resource)
        except Exception:
            logger.warning(
                f"Unable to parse origin: {origin} as URL from resource {resource.id}"
            )
            continue

    return cors_origins


def check_default_origins(cors_origins: data.CORSOrigins) -> data.CORSOrigins:
    """
    To prevent default origins loss.
    """
    for o in ALLOW_ORIGINS:
        if o not in cors_origins.origins_set:
            cors_origins.origins_set.add(o)
    return cors_origins


def create_application_settings_cors_origin(
    token: str, user_id: Tuple[str, UUID], username: str, origin: str
) -> Optional[BugoutResource]:
    resource: Optional[BugoutResource] = None
    try:
        resource = bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data={
                "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                "setting": "cors",
                "user_id": str(user_id),
                "username": username,
                "origin": origin,
            },
        )
        if token != MOONSTREAM_ADMIN_ACCESS_TOKEN:
            bc.add_resource_holder_permissions(
                token=token,
                resource_id=resource.id,
                holder_permissions={
                    "holder_id": str(MOONSTREAM_ADMIN_ID),
                    "holder_type": "user",
                    "permissions": ["admin", "create", "read", "update", "delete"],
                },
            )
    except Exception as err:
        logger.error(
            f"Unable to write default CORS origin {origin} to Brood resource: {str(err)}"
        )

    return resource


def fetch_application_settings_cors_origins(token: str) -> data.CORSOrigins:
    """
    Fetch application config resources with CORS origins setting.
    If there are no such resources create new one with default origins from environment variable.

    Should return in any case some list of origins, by default it will be ALLOW_ORIGINS.
    """

    # Fetch CORS origins configs from resources for specified application
    resources: BugoutResources
    try:
        resources = bc.list_resources(
            token=token,
            params={
                "application_id": MOONSTREAM_APPLICATION_ID,
                "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                "setting": "cors",
            },
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

    except Exception as err:
        logger.error(f"Error fetching bugout resources with CORS origins: {str(err)}")
        return data.CORSOrigins(origins_set=ALLOW_ORIGINS)

    if len(resources.resources) == 0:
        logger.warning(
            "There are no resources with configuration CORS origins, create in manually, "
            "using default from environment variable"
        )
        return data.CORSOrigins(origins_set=ALLOW_ORIGINS)

    cors_origins: data.CORSOrigins = parse_origins_from_resources(resources.resources)
    cors_origins = check_default_origins(cors_origins)

    return cors_origins


def set_cors_origins_cache(origins_set: Set[str]) -> None:
    try:
        rc_client.sadd(REDIS_CONFIG_CORS_KEY, *origins_set)
    except Exception:
        logger.warning("Unable to set CORS origins at Redis cache")
    finally:
        rc_client.close()


def fetch_and_set_cors_origins_cache() -> data.CORSOrigins:
    cors_origins = fetch_application_settings_cors_origins(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN
    )
    set_cors_origins_cache(cors_origins.origins_set)

    return cors_origins


class BugoutCORSMiddleware(CORSMiddleware):
    """
    Modified CORSMiddleware from starlette.middleware.cors.py to work with Redis cache
    and store application configuration for each user in Brood resources.
    """

    def __init__(
        self,
        app: ASGIApp,
        allow_methods: Sequence[str] = ("GET",),
        allow_headers: Sequence[str] = (),
        allow_credentials: bool = False,
        expose_headers: Sequence[str] = (),
        max_age: int = 600,
    ):
        application_configs_allowed_origins: data.CORSOrigins = (
            fetch_and_set_cors_origins_cache()
        )

        super().__init__(
            app=app,
            allow_origins=list(application_configs_allowed_origins.origins_set),
            allow_methods=allow_methods,
            allow_headers=allow_headers,
            allow_credentials=allow_credentials,
            allow_origin_regex=None,
            expose_headers=expose_headers,
            max_age=max_age,
        )

    def is_allowed_origin(self, origin: str) -> bool:
        if self.allow_all_origins:
            return True

        if self.allow_origin_regex is not None and self.allow_origin_regex.fullmatch(
            origin
        ):
            return True

        try:
            is_allowed_origin = rc_client.sismember(REDIS_CONFIG_CORS_KEY, origin)
            return is_allowed_origin
        except Exception as err:
            logger.warning(
                f"Unable to fetch CORS origins from Redis cache, err: {str(err)}"
            )
        finally:
            rc_client.close()

        return origin in self.allow_origins
