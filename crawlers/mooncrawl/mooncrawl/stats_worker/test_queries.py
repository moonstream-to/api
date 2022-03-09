import unittest

from . import queries


class TestQueries(unittest.TestCase):
    def test_query_validation(self):
        q = "SELECT * FROM ethereum_blocks"
        self.assertEqual(queries.query_validation(q), q)

        q = "select count(*), tx_dublicates from ( select count(*) as tx_dublicates from polygon_labels where address = '0x123' and label_data->>'name' = 'Transfer' group by transaction_hash, log_index order by tx_dublicates desc) as dublicates group by dublicates.tx_dublicates"
        self.assertEqual(queries.query_validation(q), q)

        q = """
        Select difference.address,
            difference.transfers_in - difference.transfers_out as count
        from (
                SELECT total.address,
                    sum(total.transfer_out) as transfers_out,
                    sum(total.transfer_in) as transfers_in
                from (
                        SELECT label_data->'args'->>'from' as address,
                            (label_data->'args'->'values'->>0)::int as transfer_out,
                            0 as transfer_in
                        from polygon_labels
                        where address = '0x123'
                            and label = 'moonworm'
                            and label_data->>'name' = 'TransferBatch'
                            and (label_data->'args'->'ids'->>0)::int in (2, 3, 4)
                        UNION ALL
                        SELECT label_data->'args'->>'from' as address,
                            (label_data->'args'->'value')::int as transfer_out,
                            0 as transfer_in
                        from polygon_labels
                        where address = '0x123'
                            and label = 'moonworm'
                            and label_data->>'name' = 'TransferSingle'
                            and (label_data->'args'->>'id')::int in (2, 3, 4)
                    ) as total
                group by address
            ) difference
        order by count desc
        """
        self.assertEqual(queries.query_validation(q), q)

        with self.assertRaises(queries.QueryNotValid):
            queries.query_validation("SELECT hash FROM ethereum_transaction;")

        with self.assertRaises(queries.QueryNotValid):
            queries.query_validation("%20UNION")

        with self.assertRaises(queries.QueryNotValid):
            queries.query_validation("?id=1")

        with self.assertRaises(queries.QueryNotValid):
            queries.query_validation("FROM`")

        with self.assertRaises(queries.QueryNotValid):
            queries.query_validation("WHERE login='[USER]'")

        with self.assertRaises(queries.QueryNotValid):
            queries.query_validation("OR(1=1)#")

        with self.assertRaises(queries.QueryNotValid):
            queries.query_validation("/etc/hosts")
