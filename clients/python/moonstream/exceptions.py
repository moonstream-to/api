from typing import Any, Optional


class MoonstreamResponseException(Exception):
    """
    Raised when Moonstream server response with error.
    """

    def __init__(
        self,
        message,
        status_code: int,
        detail: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        if detail is not None:
            self.detail = detail


class MoonstreamUnexpectedResponse(Exception):
    """
    Raised when Moonstream server response is unexpected (e.g. unparseable).
    """
