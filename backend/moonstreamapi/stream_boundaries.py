"""
Utilities to work with stream boundaries.
"""
import time
from typing import Tuple

from .data import StreamBoundary


class InvalidStreamBoundary(Exception):
    """
    Raised if a StreamBoundary object does not satisfy required constraints.
    """


def validate_stream_boundary(
    stream_boundary: StreamBoundary,
    time_difference_seconds: int,
    raise_when_invalid: bool = False,
) -> Tuple[bool, StreamBoundary]:
    """
    This function can be used by event providers to check if a stream boundary is valid according to their
    requirements.
    """
    start_time = stream_boundary.start_time
    max_end_time = start_time + time_difference_seconds
    end_time = stream_boundary.end_time
    if end_time is None:
        end_time = int(time.time())

    if end_time > max_end_time:
        if raise_when_invalid:
            raise InvalidStreamBoundary(
                f"Stream boundary start and end times must not differ by more than {time_difference_seconds} seconds:\n{stream_boundary.json()}"
            )
        else:
            return False, stream_boundary

    # If required reversed time stream of events
    if start_time > end_time:
        include_start = stream_boundary.include_start
        include_end = stream_boundary.include_end
        stream_boundary.start_time = end_time
        stream_boundary.end_time = start_time
        stream_boundary.include_start = include_end
        stream_boundary.include_end = include_start
        stream_boundary.reversed_time = True

    return True, stream_boundary
