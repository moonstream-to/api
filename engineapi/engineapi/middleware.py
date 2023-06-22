import base64
import json
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence, Set

from bugout.data import BugoutResources, BugoutUser
from bugout.exceptions import BugoutResponseException
from fastapi import HTTPException, Request, Response
from pydantic import AnyHttpUrl, parse_obj_as
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from web3 import Web3

from .auth import (
    MoonstreamAuthorizationExpired,
    MoonstreamAuthorizationVerificationError,
    verify,
)
from .rc import REDIS_CONFIG_CORS_KEY, rc_client
from .settings import (
    ALLOW_ORIGINS,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_ADMIN_USER,
    MOONSTREAM_APPLICATION_ID,
)
from .settings import bugout_client as bc

logger = logging.getLogger(__name__)


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

        authorization_header = request.headers.get("authorization")
        if authorization_header is None:
            return Response(
                status_code=403, content="No authorization header passed with request"
            )
        user_token_list = authorization_header.split()
        if len(user_token_list) != 2:
            return Response(status_code=403, content="Wrong authorization header")
        user_token: str = user_token_list[-1]

        try:
            user: BugoutUser = bc.get_user(user_token)
            if not user.verified:
                logger.info(
                    f"Attempted journal access by unverified Brood account: {user.id}"
                )
                return Response(
                    status_code=403,
                    content="Only verified accounts can access journals",
                )
            if str(user.application_id) != str(MOONSTREAM_APPLICATION_ID):
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

            json_payload = json.loads(json_payload_str)
            verified = verify(json_payload)
            address = json_payload.get("address")
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


def parse_origins_from_resources(origins: List[str]) -> Set[str]:
    """
    Parse list of CORS origins with HTTP validation and remove duplications.
    """
    resource_origins_set = set()
    for resource in origins:
        origins = resource.resource_data.get("origins", [])
        for o in origins:
            try:
                parse_obj_as(AnyHttpUrl, o)
                resource_origins_set.add(o)
            except Exception:
                logger.info(f"Unable to parse origin: {o} as URL")
                continue

    return resource_origins_set


def check_default_origins(origins: Set[str]) -> Set[str]:
    """
    To prevent default origins loss.
    """
    for o in ALLOW_ORIGINS:
        if o not in origins:
            origins.add(o)
    return origins


def fetch_application_settings_cors_origins(token: str) -> Set[str]:
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
        return ALLOW_ORIGINS

    # If there are no resources with CORS origins configuration, create new one
    # with default list of origins from environment variable
    if len(resources.resources) == 0:
        try:
            resource = bc.create_resource(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                application_id=MOONSTREAM_APPLICATION_ID,
                resource_data={
                    "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                    "setting": "cors",
                    "user_id": str(MOONSTREAM_ADMIN_USER.id),
                    "origins": ALLOW_ORIGINS,
                },
            )
            resources.resources.append(resource)
            logger.info(
                "Created resource with default CORS origins setting by moonstream admin user"
            )
        except Exception as err:
            logger.error(
                f"Unable to write default CORS origins to resources: {str(err)}"
            )
            return ALLOW_ORIGINS

    resource_origins_set: Set[str] = parse_origins_from_resources(resources.resources)
    resource_origins_set = check_default_origins(resource_origins_set)

    return list(resource_origins_set)


def set_cors_origins_cache(allow_origins: Set[str]) -> None:
    try:
        rc_client.sadd(REDIS_CONFIG_CORS_KEY, *allow_origins)
    except Exception:
        logger.warning("Unable to set CORS origins at Redis cache")
    finally:
        rc_client.close()


def fetch_and_set_cors_origins_cache():
    allow_origins = fetch_application_settings_cors_origins(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN
    )
    set_cors_origins_cache(allow_origins)

    return list(allow_origins)


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
        application_configs_allowed_origins = fetch_and_set_cors_origins_cache()

        super().__init__(
            app=app,
            allow_origins=application_configs_allowed_origins,
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
