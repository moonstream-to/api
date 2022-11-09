import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException

from .reporter import reporter

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
        internal_error: Optional[Exception] = None,
    ):
        super().__init__(status_code, detail, headers)
        if internal_error is not None:
            reporter.error_report(internal_error)
