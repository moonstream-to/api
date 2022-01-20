import logging
from typing import Any, Awaitable, Callable, Dict, Optional

from bugout.data import BugoutUser
from bugout.exceptions import BugoutResponseException
from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .reporter import reporter
from .settings import MOONSTREAM_APPLICATION_ID
from .settings import bugout_client as bc

logger = logging.getLogger(__name__)


class MoonstreamHTTPException(HTTPException):
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
            reporter.error_report(internal_error)


class BroodAuthMiddleware(BaseHTTPMiddleware):
    """
    Checks the authorization header on the request. If it represents a verified Brood user,
    create another request and get groups user belongs to, after this
    adds a brood_user attribute to the request.state. Otherwise raises a 403 error.
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
            reporter.error_report(e)
            return Response(status_code=500, content="Internal server error")

        request.state.user = user
        request.state.token = user_token
        return await call_next(request)
