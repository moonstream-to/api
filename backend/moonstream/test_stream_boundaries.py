"""
Tests for stream boundary utilities.
"""
import unittest

from . import stream_boundaries
from .data import StreamBoundary


class TestValidateStreamBoundary(unittest.TestCase):
    def test_valid_stream_boundary(self):
        stream_boundary = StreamBoundary(
            start_time=1, end_time=5, include_start=True, include_end=True
        )
        self.assertTrue(
            stream_boundaries.validate_stream_boundary(
                stream_boundary, 10, raise_when_invalid=False
            )
        )

    def test_invalid_stream_boundary(self):
        stream_boundary = StreamBoundary(
            start_time=1, end_time=5, include_start=True, include_end=True
        )
        self.assertFalse(
            stream_boundaries.validate_stream_boundary(
                stream_boundary, 1, raise_when_invalid=False
            )
        )

    def test_invalid_stream_boundary_error(self):
        stream_boundary = StreamBoundary(
            start_time=1, end_time=5, include_start=True, include_end=True
        )
        with self.assertRaises(stream_boundaries.InvalidStreamBoundary):
            stream_boundaries.validate_stream_boundary(
                stream_boundary, 1, raise_when_invalid=True
            )

    def test_unconstrainted_invalid_stream_boundary(self):
        stream_boundary = StreamBoundary()
        self.assertFalse(
            stream_boundaries.validate_stream_boundary(
                stream_boundary, 1, raise_when_invalid=False
            )
        )

    def test_unconstrained_invalid_stream_boundary_error(self):
        stream_boundary = StreamBoundary()
        with self.assertRaises(stream_boundaries.InvalidStreamBoundary):
            stream_boundaries.validate_stream_boundary(
                stream_boundary, 1, raise_when_invalid=True
            )


if __name__ == "__main__":
    unittest.main()
