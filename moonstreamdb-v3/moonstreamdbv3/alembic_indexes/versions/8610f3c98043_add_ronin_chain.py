"""add ronin chain

Revision ID: 8610f3c98043
Revises: 5ce23893771f
Create Date: 2024-11-12 12:54:26.532910

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "8610f3c98043"
down_revision: Union[str, None] = "5ce23893771f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ronin_blocks",
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("block_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("block_timestamp", sa.BigInteger(), nullable=False),
        sa.Column("parent_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("row_id", sa.BigInteger(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("transactions_indexed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("logs_indexed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "indexed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', statement_timestamp())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("block_number", name=op.f("pk_ronin_blocks")),
    )
    op.create_index(
        op.f("ix_ronin_blocks_block_number"),
        "ronin_blocks",
        ["block_number"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_blocks_block_timestamp"),
        "ronin_blocks",
        ["block_timestamp"],
        unique=False,
    )
    op.create_table(
        "ronin_reorgs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("block_hash", sa.VARCHAR(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ronin_reorgs")),
    )
    op.create_index(
        op.f("ix_ronin_reorgs_block_hash"), "ronin_reorgs", ["block_hash"], unique=False
    )
    op.create_index(
        op.f("ix_ronin_reorgs_block_number"),
        "ronin_reorgs",
        ["block_number"],
        unique=False,
    )
    op.create_table(
        "ronin_saigon_blocks",
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("block_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("block_timestamp", sa.BigInteger(), nullable=False),
        sa.Column("parent_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("row_id", sa.BigInteger(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("transactions_indexed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("logs_indexed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "indexed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', statement_timestamp())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("block_number", name=op.f("pk_ronin_saigon_blocks")),
    )
    op.create_index(
        op.f("ix_ronin_saigon_blocks_block_number"),
        "ronin_saigon_blocks",
        ["block_number"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_saigon_blocks_block_timestamp"),
        "ronin_saigon_blocks",
        ["block_timestamp"],
        unique=False,
    )
    op.create_table(
        "ronin_saigon_reorgs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("block_hash", sa.VARCHAR(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ronin_saigon_reorgs")),
    )
    op.create_index(
        op.f("ix_ronin_saigon_reorgs_block_hash"),
        "ronin_saigon_reorgs",
        ["block_hash"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_saigon_reorgs_block_number"),
        "ronin_saigon_reorgs",
        ["block_number"],
        unique=False,
    )
    op.create_table(
        "ronin_contracts",
        sa.Column("address", sa.LargeBinary(length=20), nullable=False),
        sa.Column("deployed_by", sa.LargeBinary(length=20), nullable=False),
        sa.Column("deployed_bytecode", sa.Text(), nullable=False),
        sa.Column("deployed_bytecode_hash", sa.VARCHAR(length=32), nullable=False),
        sa.Column("bytecode_storage_id", sa.UUID(), nullable=True),
        sa.Column("abi", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("deployed_at_block_number", sa.BigInteger(), nullable=False),
        sa.Column("deployed_at_block_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("deployed_at_block_timestamp", sa.BigInteger(), nullable=False),
        sa.Column("transaction_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("transaction_index", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=256), nullable=True),
        sa.Column("statistics", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "supported_standards",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', statement_timestamp())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', statement_timestamp())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["bytecode_storage_id"],
            ["bytecode_storage.id"],
            name=op.f("fk_ronin_contracts_bytecode_storage_id_bytecode_storage"),
        ),
        sa.PrimaryKeyConstraint("address", name=op.f("pk_ronin_contracts")),
    )
    op.create_index(
        op.f("ix_ronin_contracts_deployed_by"),
        "ronin_contracts",
        ["deployed_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_contracts_deployed_bytecode_hash"),
        "ronin_contracts",
        ["deployed_bytecode_hash"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_contracts_name"), "ronin_contracts", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_ronin_contracts_transaction_hash"),
        "ronin_contracts",
        ["transaction_hash"],
        unique=False,
    )
    op.create_table(
        "ronin_saigon_contracts",
        sa.Column("address", sa.LargeBinary(length=20), nullable=False),
        sa.Column("deployed_by", sa.LargeBinary(length=20), nullable=False),
        sa.Column("deployed_bytecode", sa.Text(), nullable=False),
        sa.Column("deployed_bytecode_hash", sa.VARCHAR(length=32), nullable=False),
        sa.Column("bytecode_storage_id", sa.UUID(), nullable=True),
        sa.Column("abi", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("deployed_at_block_number", sa.BigInteger(), nullable=False),
        sa.Column("deployed_at_block_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("deployed_at_block_timestamp", sa.BigInteger(), nullable=False),
        sa.Column("transaction_hash", sa.VARCHAR(length=256), nullable=False),
        sa.Column("transaction_index", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=256), nullable=True),
        sa.Column("statistics", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "supported_standards",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', statement_timestamp())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', statement_timestamp())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["bytecode_storage_id"],
            ["bytecode_storage.id"],
            name=op.f("fk_ronin_saigon_contracts_bytecode_storage_id_bytecode_storage"),
        ),
        sa.PrimaryKeyConstraint("address", name=op.f("pk_ronin_saigon_contracts")),
    )
    op.create_index(
        op.f("ix_ronin_saigon_contracts_deployed_by"),
        "ronin_saigon_contracts",
        ["deployed_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_saigon_contracts_deployed_bytecode_hash"),
        "ronin_saigon_contracts",
        ["deployed_bytecode_hash"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_saigon_contracts_name"),
        "ronin_saigon_contracts",
        ["name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ronin_saigon_contracts_transaction_hash"),
        "ronin_saigon_contracts",
        ["transaction_hash"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_ronin_saigon_contracts_transaction_hash"),
        table_name="ronin_saigon_contracts",
    )
    op.drop_index(
        op.f("ix_ronin_saigon_contracts_name"), table_name="ronin_saigon_contracts"
    )
    op.drop_index(
        op.f("ix_ronin_saigon_contracts_deployed_bytecode_hash"),
        table_name="ronin_saigon_contracts",
    )
    op.drop_index(
        op.f("ix_ronin_saigon_contracts_deployed_by"),
        table_name="ronin_saigon_contracts",
    )
    op.drop_table("ronin_saigon_contracts")
    op.drop_index(
        op.f("ix_ronin_contracts_transaction_hash"), table_name="ronin_contracts"
    )
    op.drop_index(op.f("ix_ronin_contracts_name"), table_name="ronin_contracts")
    op.drop_index(
        op.f("ix_ronin_contracts_deployed_bytecode_hash"), table_name="ronin_contracts"
    )
    op.drop_index(op.f("ix_ronin_contracts_deployed_by"), table_name="ronin_contracts")
    op.drop_table("ronin_contracts")
    op.drop_index(
        op.f("ix_ronin_saigon_reorgs_block_number"), table_name="ronin_saigon_reorgs"
    )
    op.drop_index(
        op.f("ix_ronin_saigon_reorgs_block_hash"), table_name="ronin_saigon_reorgs"
    )
    op.drop_table("ronin_saigon_reorgs")
    op.drop_index(
        op.f("ix_ronin_saigon_blocks_block_timestamp"), table_name="ronin_saigon_blocks"
    )
    op.drop_index(
        op.f("ix_ronin_saigon_blocks_block_number"), table_name="ronin_saigon_blocks"
    )
    op.drop_table("ronin_saigon_blocks")
    op.drop_index(op.f("ix_ronin_reorgs_block_number"), table_name="ronin_reorgs")
    op.drop_index(op.f("ix_ronin_reorgs_block_hash"), table_name="ronin_reorgs")
    op.drop_table("ronin_reorgs")
    op.drop_index(op.f("ix_ronin_blocks_block_timestamp"), table_name="ronin_blocks")
    op.drop_index(op.f("ix_ronin_blocks_block_number"), table_name="ronin_blocks")
    op.drop_table("ronin_blocks")
    # ### end Alembic commands ###
