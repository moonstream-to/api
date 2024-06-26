"""Arbitrum One blockchain

Revision ID: e9f640a2b45b
Revises: e9e1b43f49e1
Create Date: 2024-05-10 10:39:21.257483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e9f640a2b45b'
down_revision: Union[str, None] = 'e9e1b43f49e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('arbitrum_one_labels',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('label', sa.VARCHAR(length=256), nullable=False),
    sa.Column('transaction_hash', sa.VARCHAR(length=128), nullable=False),
    sa.Column('log_index', sa.Integer(), nullable=True),
    sa.Column('block_number', sa.BigInteger(), nullable=False),
    sa.Column('block_hash', sa.VARCHAR(length=256), nullable=False),
    sa.Column('block_timestamp', sa.BigInteger(), nullable=False),
    sa.Column('caller_address', sa.VARCHAR(length=64), nullable=True),
    sa.Column('origin_address', sa.VARCHAR(length=64), nullable=True),
    sa.Column('address', sa.VARCHAR(length=64), nullable=True),
    sa.Column('label_name', sa.Text(), nullable=True),
    sa.Column('label_type', sa.VARCHAR(length=64), nullable=True),
    sa.Column('label_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_arbitrum_one_labels')),
    sa.UniqueConstraint('id', name=op.f('uq_arbitrum_one_labels_id'))
    )
    op.create_index('ix_arbitrum_one_labels_addr_block_num', 'arbitrum_one_labels', ['address', 'block_number'], unique=False)
    op.create_index('ix_arbitrum_one_labels_addr_block_ts', 'arbitrum_one_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_address'), 'arbitrum_one_labels', ['address'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_block_number'), 'arbitrum_one_labels', ['block_number'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_caller_address'), 'arbitrum_one_labels', ['caller_address'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_label'), 'arbitrum_one_labels', ['label'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_label_name'), 'arbitrum_one_labels', ['label_name'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_label_type'), 'arbitrum_one_labels', ['label_type'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_origin_address'), 'arbitrum_one_labels', ['origin_address'], unique=False)
    op.create_index(op.f('ix_arbitrum_one_labels_transaction_hash'), 'arbitrum_one_labels', ['transaction_hash'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_arbitrum_one_labels_transaction_hash'), table_name='arbitrum_one_labels')
    op.drop_index(op.f('ix_arbitrum_one_labels_origin_address'), table_name='arbitrum_one_labels')
    op.drop_index(op.f('ix_arbitrum_one_labels_label_type'), table_name='arbitrum_one_labels')
    op.drop_index(op.f('ix_arbitrum_one_labels_label_name'), table_name='arbitrum_one_labels')
    op.drop_index(op.f('ix_arbitrum_one_labels_label'), table_name='arbitrum_one_labels')
    op.drop_index(op.f('ix_arbitrum_one_labels_caller_address'), table_name='arbitrum_one_labels')
    op.drop_index(op.f('ix_arbitrum_one_labels_block_number'), table_name='arbitrum_one_labels')
    op.drop_index(op.f('ix_arbitrum_one_labels_address'), table_name='arbitrum_one_labels')
    op.drop_index('ix_arbitrum_one_labels_addr_block_ts', table_name='arbitrum_one_labels')
    op.drop_index('ix_arbitrum_one_labels_addr_block_num', table_name='arbitrum_one_labels')
    op.drop_table('arbitrum_one_labels')
    # ### end Alembic commands ###
