from dataclasses import FrozenInstanceError
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


class TestMoonstreamEndpoints(unittest.TestCase):
    def setUp(self):
        self.url = "https://api.moonstream.to"
        self.normalized_url = "https://api.moonstream.to"

    def test_moonstream_endpoints(self):
        endpoints = client.moonstream_endpoints(self.url)
        self.assertDictEqual(
            endpoints,
            {
                "/ping": f"{self.normalized_url}/ping",
                "/version": f"{self.normalized_url}/version",
                "/now": f"{self.normalized_url}/now",
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
