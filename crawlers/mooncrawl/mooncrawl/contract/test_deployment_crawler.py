from typing import Optional
from unittest import TestCase

from web3.main import Web3

from .deployment_crawler import get_batch_block_range


class TestDeploymentCrawler(TestCase):
    def test_get_batch_block_range(self):
        from_block = 0
        to_block = 101
        batch_size = 10
        result = get_batch_block_range(from_block, to_block, batch_size)

        last_end: Optional[int] = None  # type: ignore
        for batch_start, batch_end in result:
            if last_end is not None:
                self.assertEqual(batch_start, last_end + 1)
            self.assertTrue(batch_start <= batch_end)
            self.assertTrue(batch_start <= to_block)
            self.assertTrue(batch_end <= to_block)
            last_end = batch_end

        self.assertEqual(last_end, to_block)

    def test_get_batch_block_range_with_from_block_gt_to_block(self):
        from_block = 101
        to_block = 0
        batch_size = 10
        result = get_batch_block_range(from_block, to_block, batch_size)

        last_end: Optional[int] = None  # type: ignore
        for batch_start, batch_end in result:
            if last_end is not None:
                self.assertEqual(batch_start, last_end - 1)

            last_end = batch_end
            self.assertTrue(batch_start >= batch_end)
            self.assertTrue(batch_start >= to_block)
            self.assertTrue(batch_end >= to_block)

        self.assertEqual(last_end, to_block)
