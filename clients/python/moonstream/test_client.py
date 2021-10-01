from dataclasses import FrozenInstanceError
import os
import unittest

from . import client


class TestMoonstreamClient(unittest.TestCase):
    def test_client_init(self):
        m = client.Moonstream()
        self.assertEqual(m.api.url, "https://api.moonstream.to")
        self.assertIsNone(m.timeout)
        self.assertGreater(len(m.api.endpoints), 0)

    def test_client_init_with_timeout(self):
        timeout = 7
        m = client.Moonstream(timeout=timeout)
        self.assertEqual(m.api.url, "https://api.moonstream.to")
        self.assertEqual(m.timeout, timeout)
        self.assertGreater(len(m.api.endpoints), 0)

    def test_client_with_custom_url_and_timeout(self):
        timeout = 9
        url = "https://my.custom.api.url"
        m = client.Moonstream(url=url, timeout=timeout)
        self.assertEqual(m.api.url, url)
        self.assertEqual(m.timeout, timeout)
        self.assertGreater(len(m.api.endpoints), 0)

    def test_client_with_custom_messy_url_and_timeout(self):
        timeout = 3.5
        url = "https://my.custom.api.url/"
        m = client.Moonstream(url=url, timeout=timeout)
        self.assertEqual(m.api.url, url)
        self.assertEqual(m.timeout, timeout)
        self.assertGreater(len(m.api.endpoints), 0)

    def test_client_with_custom_messy_url_no_protocol_and_timeout(self):
        timeout = 5.5
        url = "my.custom.api.url/"
        m = client.Moonstream(url=url, timeout=timeout)
        self.assertEqual(m.api.url, url)
        self.assertEqual(m.timeout, timeout)
        self.assertGreater(len(m.api.endpoints), 0)

    def test_immutable_api_url(self):
        m = client.Moonstream()
        with self.assertRaises(FrozenInstanceError):
            m.api.url = "lol"

    def test_immutable_api_endpoints(self):
        m = client.Moonstream()
        with self.assertRaises(FrozenInstanceError):
            m.api.endpoints = {}

    def test_mutable_timeout(self):
        original_timeout = 5.0
        updated_timeout = 10.5
        m = client.Moonstream(timeout=original_timeout)
        self.assertEqual(m.timeout, original_timeout)
        m.timeout = updated_timeout
        self.assertEqual(m.timeout, updated_timeout)


class TestMoonstreamClientFromEnv(unittest.TestCase):
    def setUp(self):
        self.old_moonstream_api_url = os.environ.get("MOONSTREAM_API_URL")
        self.old_moonstream_timeout_seconds = os.environ.get(
            "MOONSTREAM_TIMEOUT_SECONDS"
        )
        self.old_moonstream_access_token = os.environ.get("MOONSTREAM_ACCESS_TOKEN")

        self.moonstream_api_url = "https://custom.example.com"
        self.moonstream_timeout_seconds = 15.333333
        self.moonstream_access_token = "1d431ca4-af9b-4c3a-b7b9-3cc79f3b0900"

        os.environ["MOONSTREAM_API_URL"] = self.moonstream_api_url
        os.environ["MOONSTREAM_TIMEOUT_SECONDS"] = str(self.moonstream_timeout_seconds)
        os.environ["MOONSTREAM_ACCESS_TOKEN"] = self.moonstream_access_token

    def tearDown(self) -> None:
        del os.environ["MOONSTREAM_API_URL"]
        del os.environ["MOONSTREAM_TIMEOUT_SECONDS"]
        del os.environ["MOONSTREAM_ACCESS_TOKEN"]

        if self.old_moonstream_api_url is not None:
            os.environ["MOONSTREAM_API_URL"] = self.old_moonstream_api_url
        if self.old_moonstream_timeout_seconds is not None:
            os.environ[
                "MOONSTREAM_TIMEOUT_SECONDS"
            ] = self.old_moonstream_timeout_seconds
        if self.old_moonstream_access_token is not None:
            os.environ["MOONSTREAM_ACCESS_TOKEN"] = self.old_moonstream_access_token

    def test_client_from_env(self):
        m = client.client_from_env()
        self.assertEqual(m.api.url, self.moonstream_api_url)
        self.assertEqual(m.timeout, self.moonstream_timeout_seconds)
        self.assertIsNone(m.requires_authorization())

        authorization_header = m._session.headers["Authorization"]
        self.assertEqual(authorization_header, f"Bearer {self.moonstream_access_token}")


class TestMoonstreamEndpoints(unittest.TestCase):
    def setUp(self):
        self.url = "https://api.moonstream.to"
        self.normalized_url = "https://api.moonstream.to"

    def test_moonstream_endpoints(self):
        endpoints = client.moonstream_endpoints(self.url)
        self.assertDictEqual(
            endpoints,
            {
                client.ENDPOINT_PING: f"{self.normalized_url}{client.ENDPOINT_PING}",
                client.ENDPOINT_VERSION: f"{self.normalized_url}{client.ENDPOINT_VERSION}",
                client.ENDPOINT_NOW: f"{self.normalized_url}{client.ENDPOINT_NOW}",
                client.ENDPOINT_TOKEN: f"{self.normalized_url}{client.ENDPOINT_TOKEN}",
                client.ENDPOINT_SUBSCRIPTION_TYPES: f"{self.normalized_url}{client.ENDPOINT_SUBSCRIPTION_TYPES}",
                client.ENDPOINT_SUBSCRIPTIONS: f"{self.normalized_url}{client.ENDPOINT_SUBSCRIPTIONS}",
                client.ENDPOINT_STREAMS: f"{self.normalized_url}{client.ENDPOINT_STREAMS}",
                client.ENDPOINT_STREAMS_LATEST: f"{self.normalized_url}{client.ENDPOINT_STREAMS_LATEST}",
                client.ENDPOINT_STREAMS_NEXT: f"{self.normalized_url}{client.ENDPOINT_STREAMS_NEXT}",
                client.ENDPOINT_STREAMS_PREVIOUS: f"{self.normalized_url}{client.ENDPOINT_STREAMS_PREVIOUS}",
            },
        )


class TestMoonstreamEndpointsMessyURL(TestMoonstreamEndpoints):
    def setUp(self):
        self.url = "https://api.moonstream.to/"
        self.normalized_url = "https://api.moonstream.to"


class TestMoonstreamEndpointsMessyURLWithNoProtocol(TestMoonstreamEndpoints):
    def setUp(self):
        self.url = "api.moonstream.to/"
        self.normalized_url = "http://api.moonstream.to"
