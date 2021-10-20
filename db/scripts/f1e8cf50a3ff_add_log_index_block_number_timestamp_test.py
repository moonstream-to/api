import argparse

from moonstreamdb.db import yield_db_session_ctx


def ethereum_labels_copy_check() -> None:

    with yield_db_session_ctx() as db_session:

        # check counts in 2 tables

        count_original = db_session.execute(
            """
            select count(*) from ethereum_labels;
        """
        ).fetchall()[0][0]

        count_new_labels = db_session.execute(
            """
            select count(*) from ethereum_labels_v2;
        """
        ).fetchall()[0][0]
        if count_original == count_new_labels:
            print(f"Count check passed")
        else:
            print(f"Tables recors counts mismatch")

        print(
            f"ethereum_labels count:{count_original}, ethereum_labels_v2 count:{count_new_labels}"
        )

        # check random selected rows
        original_table_rows_select = db_session.execute(
            """
            select id from ethereum_labels TABLESAMPLE BERNOULLI (0.1) limit 1000;
        """
        ).fetchall()

        ids = [str(row[0]) for row in original_table_rows_select]

        ids_str = "', '".join(ids)

        # check

        original_table_rows_select = db_session.execute(
            """
                SELECT
                    id,
                    label,
                    label_data,
                    created_at,
                    transaction_hash,
                    address
                FROM
                    ethereum_labels_v2
                    where id IN ('{}')
                EXCEPT 
                SELECT
                    ethereum_labels.id as id,
                    ethereum_labels.label as label,
                    ethereum_labels.label_data as label_data,
                    ethereum_labels.created_at as created_at,
                    ethereum_labels.transaction_hash as transaction_hash,
                    ethereum_addresses.address as address
                FROM
                    ethereum_labels
                    left join ethereum_addresses ON ethereum_labels.address_id = ethereum_addresses.id
                    where ethereum_labels.id IN ('{}');
        """.format(
                ids_str, ids_str
            )
        ).fetchall()

        if original_table_rows_select:
            print("Error rows data from sample missmatch")
        else:
            print("Rows sample is correct")


if __name__ == "__main__":
    ethereum_labels_copy_check()
