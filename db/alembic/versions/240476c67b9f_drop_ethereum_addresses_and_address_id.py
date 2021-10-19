"""Drop ethereum_addresses and address_id column

Revision ID: 240476c67b9f
Revises: f1e8cf50a3ff
Create Date: 2021-10-19 14:49:07.905565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "240476c67b9f"
down_revision = "f1e8cf50a3ff"
branch_labels = None
depends_on = None


def upgrade():

    op.execute(
        """
            LOCK TABLE ethereum_labels IN ACCESS EXCLUSIVE MODE;

            INSERT INTO
                ethereum_labels_v2 (
                    id,
                    label,
                    label_data,
                    created_at,
                    transaction_hash,
                    address
                )
            SELECT
                ethereum_labels.id as id,
                ethereum_labels.label as label,
                ethereum_labels.label_data as label_data,
                ethereum_labels.created_at as created_at,
                ethereum_labels.transaction_hash as transaction_hash,
                ethereum_addresses.address as address
            FROM
                (
                    SELECT
                        Row_Number() over (
                            order by
                                id
                        ) AS RowIndex,
                        *
                    from
                        ethereum_labels
                ) AS ethereum_labels
                INNER JOIN ethereum_addresses ON RowIndex > (select count(*) from ethereum_labels_v2 ) and ethereum_labels.address_id = ethereum_addresses.id;

    """
    )

    op.execute(
        "ALTER TABLE IF EXISTS ethereum_labels DROP CONSTRAINT IF EXISTS fk_ethereum_labels_address_id_ethereum_addresses;"
    )

    op.execute(
        "ALTER TABLE IF EXISTS ethereum_addresses DROP CONSTRAINT IF EXISTS fk_ethereum_smart_contracts_transaction_hash_ethereum_t_f928;"
    )

    op.execute(
        """
        /* Rename tabels */
        ALTER TABLE
            ethereum_labels RENAME TO ethereum_labels_v1;

        ALTER TABLE
            ethereum_labels_v2 RENAME TO ethereum_labels;
    """
    )

    op.execute(
        """
        ALTER INDEX pk_ethereum_labels RENAME TO pk_ethereum_labels_v1;
        ALTER INDEX idx_ethereum_labels_opensea_nft_name RENAME TO idx_ethereum_labels_opensea_nft_name_v1;
        ALTER INDEX ix_ethereum_labels_label RENAME TO ix_ethereum_labels_label_v1;
        ALTER INDEX ix_ethereum_labels_transaction_hash RENAME TO ix_ethereum_labels_transaction_hash_v1;
        ALTER INDEX uq_ethereum_labels_id RENAME TO uq_ethereum_labels_id_v1;
    """
    )

    op.execute(
        """

            ALTER TABLE
                ONLY ethereum_labels
            ADD
                CONSTRAINT pk_ethereum_labels PRIMARY KEY (id);

            ALTER TABLE
                ONLY ethereum_labels
            ADD
                CONSTRAINT uq_ethereum_labels_id UNIQUE (id);

            /* Create indexes must be unique cross database */
            CREATE INDEX idx_ethereum_labels_opensea_nft_name ON ethereum_labels USING btree (((label_data ->> 'name' :: text)))
            WHERE
                ((label) :: text = 'opensea_nft' :: text);

            CREATE INDEX ix_ethereum_labels_address ON ethereum_labels USING btree (address);

            CREATE INDEX ix_ethereum_labels_block_number ON ethereum_labels USING btree (block_number);

            CREATE INDEX ix_ethereum_labels_label ON ethereum_labels USING btree (label);

            CREATE INDEX ix_ethereum_labels_transaction_hash ON ethereum_labels USING btree (transaction_hash);

            CREATE INDEX ix_ethereum_labels_block_timestamp ON ethereum_labels USING btree (block_timestamp);

    """
    )

    op.execute(
        """
        DROP TABLE ethereum_addresses;
        """
    )


def downgrade():

    op.execute(
        """
        CREATE TABLE ethereum_addresses (
            id integer PRIMARY KEY,
            transaction_hash character varying(256),
            address character varying(256) NOT NULL,
            created_at timestamp with time zone DEFAULT timezone('utc'::text, statement_timestamp()) NOT NULL
        );



        CREATE UNIQUE INDEX ix_ethereum_addresses_address ON ethereum_addresses USING btree (address);

        CREATE INDEX ix_ethereum_addresses_transaction_hash ON ethereum_addresses USING btree (transaction_hash);

        """
    )

    op.execute(
        "ALTER TABLE IF EXISTS ethereum_labels DROP CONSTRAINT IF EXISTS pk_ethereum_labels;"
    )

    op.execute(
        "ALTER TABLE IF EXISTS ethereum_labels DROP CONSTRAINT IF EXISTS uq_ethereum_labels_id;"
    )

    op.execute(
        """
        DROP INDEX IF EXISTS pk_ethereum_labels;
        DROP INDEX IF EXISTS idx_ethereum_labels_opensea_nft_name;
        DROP INDEX IF EXISTS ix_ethereum_labels_address;
        DROP INDEX IF EXISTS ix_ethereum_labels_label;
        DROP INDEX IF EXISTS ix_ethereum_labels_transaction_hash;
        DROP INDEX IF EXISTS ix_ethereum_labels_block_number;
        DROP INDEX IF EXISTS ix_ethereum_labels_block_timestamp;
        DROP INDEX IF EXISTS uq_ethereum_labels_id;
    """
    )

    op.execute(
        """
        ALTER TABLE ethereum_labels RENAME TO ethereum_labels_v2;

        ALTER TABLE ethereum_labels_v1 RENAME TO ethereum_labels;
    """
    )

    op.execute(
        """
        ALTER INDEX pk_ethereum_labels_v1 RENAME TO pk_ethereum_labels;
        ALTER INDEX idx_ethereum_labels_opensea_nft_name_v1 RENAME TO idx_ethereum_labels_opensea_nft_name;
        ALTER INDEX ix_ethereum_labels_label_v1 RENAME TO ix_ethereum_labels_label;
        ALTER INDEX ix_ethereum_labels_transaction_hash_v1 RENAME TO ix_ethereum_labels_transaction_hash;
        ALTER INDEX uq_ethereum_labels_id_v1 RENAME TO uq_ethereum_labels_id;
    """
    )
