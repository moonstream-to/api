import unittest

from . import actions


class TestActions(unittest.TestCase):
    def test_name_normalization(self):
        names = [
            ["test", "test"],
            ["test_Name", "test_Name"],
            ["%20UNION", "20UNION"],
            ["UNION ALL", "UNION_ALL"],
            ["$_REQUEST", "REQUEST"],
            ["id=1", "id_1"],
            ["Lo" * 30, "Lo" * 25],
        ]
        for name in names:
            query_name = actions.name_normalization(name[0])
            self.assertEqual(query_name, name[1])
