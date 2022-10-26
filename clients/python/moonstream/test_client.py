import os
import unittest

from . import client


class TestMoonstreamCalls(unittest.TestCase):
    def setUp(self):
        url = os.environ.get("MOONSTREAM_API_URL", "https://api.moonstream.to")
        self.token = os.environ.get("MOONSTREAM_ACCESS_TOKEN")
        if self.token is None:
            raise Exception("MOONSTREAM_ACCESS_TOKEN should be specified")
        self.m = client.Moonstream(moonstream_api_url=url)

        queries = self.m.list_queries(self.token)
        for query in queries.queries:
            if query.name.startswith("test_query_name"):
                self.m.delete_query(self.token, query.name)

    def test_ping(self):
        response = self.m.ping()
        self.assertEqual(response["status"], "ok")

    def test_create_query(self):
        query = "SELECT count(*) FROM polygon_blocks"
        name = "test-query-name-1"
        response = self.m.create_query(self.token, query, name)
        self.assertEqual(f"Query:{name.replace('-', '_')}", response.name)

    def test_list_queries(self):
        query = (
            "SELECT hash,block_number FROM polygon_blocks WHERE block_number = 21175765"
        )
        name = "test-query-name-2"
        response_1 = self.m.create_query(self.token, query, name)
        self.assertEqual(f"Query:{name.replace('-', '_')}", response_1.name)

        response_2 = self.m.list_queries(self.token)
        self.assertGreaterEqual(len(response_2.queries), 1)

    def test_delete_query(self):
        query = "SELECT 1"
        name = "test-query-name-0"
        response_1 = self.m.create_query(self.token, query, name)
        self.assertEqual(f"Query:{name.replace('-', '_')}", response_1.name)

        response_2 = self.m.delete_query(self.token, name.replace("-", "_"))
        self.assertEqual(response_1.id, response_2)

    def tearDown(self) -> None:
        queries = self.m.list_queries(self.token)
        for query in queries.queries:
            if query.name.startswith("test_query_name"):
                self.m.delete_query(self.token, query.name)
