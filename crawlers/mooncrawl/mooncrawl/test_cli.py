import unittest

from . import crawler


class TestYieldBlockNumbersLists(unittest.TestCase):
    def test_yield_descending_10_6_step_4(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "10-6", block_step=4
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8, 7], [6]])

    def test_yield_descending_10_6_step_3(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "10-6", block_step=3
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8], [7, 6]])

    def test_yield_descending_10_6_descending_step_3(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "10-6", crawler.ProcessingOrder.DESCENDING, 3
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8], [7, 6]])

    def test_yield_descending_10_6_descending_step_10(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "10-6", crawler.ProcessingOrder.DESCENDING, 10
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8, 7, 6]])

    def test_yield_descending_6_10_step_4(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "6-10", block_step=4
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8, 7], [6]])

    def test_yield_descending_6_10_step_3(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "6-10", block_step=3
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8], [7, 6]])

    def test_yield_descending_6_10_descending_step_3(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "6-10", crawler.ProcessingOrder.DESCENDING, 3
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8], [7, 6]])

    def test_yield_descending_6_10_descending_step_10(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "6-10", crawler.ProcessingOrder.DESCENDING, 10
            )
        ]
        self.assertListEqual(partition, [[10, 9, 8, 7, 6]])

    def test_yield_ascending_10_6_ascending_step_3(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "10-6", crawler.ProcessingOrder.ASCENDING, 3
            )
        ]
        self.assertListEqual(partition, [[6, 7, 8], [9, 10]])

    def test_yield_ascending_10_6_ascending_step_10(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "10-6", crawler.ProcessingOrder.ASCENDING, 10
            )
        ]
        self.assertListEqual(partition, [[6, 7, 8, 9, 10]])

    def test_yield_ascending_6_10_ascending_step_4(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "6-10", crawler.ProcessingOrder.ASCENDING, 4
            )
        ]
        self.assertListEqual(partition, [[6, 7, 8, 9], [10]])

    def test_yield_ascending_6_10_ascending_step_10(self):
        partition = [
            block_numbers_list
            for block_numbers_list in crawler.yield_blocks_numbers_lists(
                "6-10", crawler.ProcessingOrder.ASCENDING, 10
            )
        ]
        self.assertListEqual(partition, [[6, 7, 8, 9, 10]])


if __name__ == "__main__":
    unittest.main()
