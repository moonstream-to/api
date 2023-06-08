import base64
import json
import logging
from typing import Any, Awaitable, Callable, Dict, Optional

from bugout.data import BugoutUser
from bugout.exceptions import BugoutResponseException
from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from web3 import Web3

from .auth import (
    MoonstreamAuthorizationExpired,
    MoonstreamAuthorizationVerificationError,
    verify,
)
from .settings import bugout_client as bc, MOONSTREAM_APPLICATION_ID

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
