import unittest
from urllib import parse

from .stream_queries import parse_query_string


class TestParseQueryString(unittest.TestCase):
    def test_single_subscription_type(self):
        q = "type:ethereum_blockchain"
        query = parse_query_string(q)
        self.assertListEqual(query.subscription_types, ["ethereum_blockchain"])
        self.assertListEqual(query.subscriptions, [])

    def test_multiple_subscription_types(self):
        q = "type:ethereum_blockchain type:ethereum_whalewatch"
        query = parse_query_string(q)
        self.assertListEqual(
            query.subscription_types, ["ethereum_blockchain", "ethereum_whalewatch"]
        )
        self.assertListEqual(query.subscriptions, [])

    def test_single_subscription(self):
        q = "sub:ethereum_blockchain:0xbb2569ca55552fb4c1d73ec536e06a620c3d3d66"
        query = parse_query_string(q)
        self.assertListEqual(query.subscription_types, [])
        self.assertListEqual(
            query.subscriptions,
            [("ethereum_blockchain", "0xbb2569ca55552fb4c1d73ec536e06a620c3d3d66")],
        )

    def test_multiple_subscriptions(self):
        q = "sub:ethereum_blockchain:from:0xbb2569ca55552fb4c1d73ec536e06a620c3d3d66 sub:ethereum_blockchain:to:0x2819c144d5946404c0516b6f817a960db37d4929 sub:ethereum_txpool:0x2819c144d5946404c0516b6f817a960db37d4929"
        query = parse_query_string(q)
        self.assertListEqual(query.subscription_types, [])
        self.assertListEqual(
            query.subscriptions,
            [
                (
                    "ethereum_blockchain",
                    "from:0xbb2569ca55552fb4c1d73ec536e06a620c3d3d66",
                ),
                (
                    "ethereum_blockchain",
                    "to:0x2819c144d5946404c0516b6f817a960db37d4929",
                ),
                ("ethereum_txpool", "0x2819c144d5946404c0516b6f817a960db37d4929"),
            ],
        )

    def test_multiple_subscription_types_and_subscriptions(self):
        q = "type:ethereum_whalewatch type:solana_blockchain sub:ethereum_blockchain:from:0xbb2569ca55552fb4c1d73ec536e06a620c3d3d66 sub:ethereum_blockchain:to:0x2819c144d5946404c0516b6f817a960db37d4929 sub:ethereum_txpool:0x2819c144d5946404c0516b6f817a960db37d4929"
        query = parse_query_string(q)
        self.assertListEqual(
            query.subscription_types, ["ethereum_whalewatch", "solana_blockchain"]
        )
        self.assertListEqual(
            query.subscriptions,
            [
                (
                    "ethereum_blockchain",
                    "from:0xbb2569ca55552fb4c1d73ec536e06a620c3d3d66",
                ),
                (
                    "ethereum_blockchain",
                    "to:0x2819c144d5946404c0516b6f817a960db37d4929",
                ),
                ("ethereum_txpool", "0x2819c144d5946404c0516b6f817a960db37d4929"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
