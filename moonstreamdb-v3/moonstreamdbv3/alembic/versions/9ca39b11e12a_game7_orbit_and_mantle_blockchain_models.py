"""Game7 Orbit and Mantle blockchain models

Revision ID: 9ca39b11e12a
Revises: d2ceff33be47
Create Date: 2024-05-29 13:17:07.194421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9ca39b11e12a'
down_revision: Union[str, None] = 'd2ceff33be47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game7_orbit_arbitrum_sepolia_labels',
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
    sa.PrimaryKeyConstraint('id', name=op.f('pk_game7_orbit_arbitrum_sepolia_labels')),
    sa.UniqueConstraint('id', name=op.f('uq_game7_orbit_arbitrum_sepolia_labels_id'))
    )
    op.create_index('ix_g7o_arbitrum_sepolia_labels_addr_block_num', 'game7_orbit_arbitrum_sepolia_labels', ['address', 'block_number'], unique=False)
    op.create_index('ix_g7o_arbitrum_sepolia_labels_addr_block_ts', 'game7_orbit_arbitrum_sepolia_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_address'), 'game7_orbit_arbitrum_sepolia_labels', ['address'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_block_number'), 'game7_orbit_arbitrum_sepolia_labels', ['block_number'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_caller_address'), 'game7_orbit_arbitrum_sepolia_labels', ['caller_address'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_label'), 'game7_orbit_arbitrum_sepolia_labels', ['label'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_label_name'), 'game7_orbit_arbitrum_sepolia_labels', ['label_name'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_label_type'), 'game7_orbit_arbitrum_sepolia_labels', ['label_type'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_origin_address'), 'game7_orbit_arbitrum_sepolia_labels', ['origin_address'], unique=False)
    op.create_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_transaction_hash'), 'game7_orbit_arbitrum_sepolia_labels', ['transaction_hash'], unique=False)
    op.create_index('uk_g7o_arbitrum_sepolia_labels_tx_hash_log_idx_evt', 'game7_orbit_arbitrum_sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_g7o_arbitrum_sepolia_labels_tx_hash_tx_call', 'game7_orbit_arbitrum_sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_table('mantle_labels',
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
    sa.PrimaryKeyConstraint('id', name=op.f('pk_mantle_labels')),
    sa.UniqueConstraint('id', name=op.f('uq_mantle_labels_id'))
    )
    op.create_index('ix_mantle_labels_addr_block_num', 'mantle_labels', ['address', 'block_number'], unique=False)
    op.create_index('ix_mantle_labels_addr_block_ts', 'mantle_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index(op.f('ix_mantle_labels_address'), 'mantle_labels', ['address'], unique=False)
    op.create_index(op.f('ix_mantle_labels_block_number'), 'mantle_labels', ['block_number'], unique=False)
    op.create_index(op.f('ix_mantle_labels_caller_address'), 'mantle_labels', ['caller_address'], unique=False)
    op.create_index(op.f('ix_mantle_labels_label'), 'mantle_labels', ['label'], unique=False)
    op.create_index(op.f('ix_mantle_labels_label_name'), 'mantle_labels', ['label_name'], unique=False)
    op.create_index(op.f('ix_mantle_labels_label_type'), 'mantle_labels', ['label_type'], unique=False)
    op.create_index(op.f('ix_mantle_labels_origin_address'), 'mantle_labels', ['origin_address'], unique=False)
    op.create_index(op.f('ix_mantle_labels_transaction_hash'), 'mantle_labels', ['transaction_hash'], unique=False)
    op.create_index('uk_mantle_labels_tx_hash_log_idx_evt', 'mantle_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_mantle_labels_tx_hash_tx_call', 'mantle_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_table('mantle_sepolia_labels',
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
    sa.PrimaryKeyConstraint('id', name=op.f('pk_mantle_sepolia_labels')),
    sa.UniqueConstraint('id', name=op.f('uq_mantle_sepolia_labels_id'))
    )
    op.create_index('ix_mantle_sepolia_labels_addr_block_num', 'mantle_sepolia_labels', ['address', 'block_number'], unique=False)
    op.create_index('ix_mantle_sepolia_labels_addr_block_ts', 'mantle_sepolia_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_address'), 'mantle_sepolia_labels', ['address'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_block_number'), 'mantle_sepolia_labels', ['block_number'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_caller_address'), 'mantle_sepolia_labels', ['caller_address'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_label'), 'mantle_sepolia_labels', ['label'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_label_name'), 'mantle_sepolia_labels', ['label_name'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_label_type'), 'mantle_sepolia_labels', ['label_type'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_origin_address'), 'mantle_sepolia_labels', ['origin_address'], unique=False)
    op.create_index(op.f('ix_mantle_sepolia_labels_transaction_hash'), 'mantle_sepolia_labels', ['transaction_hash'], unique=False)
    op.create_index('uk_mantle_sepolia_labels_tx_hash_log_idx_evt', 'mantle_sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_mantle_sepolia_labels_tx_hash_tx_call', 'mantle_sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('uk_mantle_sepolia_labels_tx_hash_tx_call', table_name='mantle_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_mantle_sepolia_labels_tx_hash_log_idx_evt', table_name='mantle_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index(op.f('ix_mantle_sepolia_labels_transaction_hash'), table_name='mantle_sepolia_labels')
    op.drop_index(op.f('ix_mantle_sepolia_labels_origin_address'), table_name='mantle_sepolia_labels')
    op.drop_index(op.f('ix_mantle_sepolia_labels_label_type'), table_name='mantle_sepolia_labels')
    op.drop_index(op.f('ix_mantle_sepolia_labels_label_name'), table_name='mantle_sepolia_labels')
    op.drop_index(op.f('ix_mantle_sepolia_labels_label'), table_name='mantle_sepolia_labels')
    op.drop_index(op.f('ix_mantle_sepolia_labels_caller_address'), table_name='mantle_sepolia_labels')
    op.drop_index(op.f('ix_mantle_sepolia_labels_block_number'), table_name='mantle_sepolia_labels')
    op.drop_index(op.f('ix_mantle_sepolia_labels_address'), table_name='mantle_sepolia_labels')
    op.drop_index('ix_mantle_sepolia_labels_addr_block_ts', table_name='mantle_sepolia_labels')
    op.drop_index('ix_mantle_sepolia_labels_addr_block_num', table_name='mantle_sepolia_labels')
    op.drop_table('mantle_sepolia_labels')
    op.drop_index('uk_mantle_labels_tx_hash_tx_call', table_name='mantle_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_mantle_labels_tx_hash_log_idx_evt', table_name='mantle_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index(op.f('ix_mantle_labels_transaction_hash'), table_name='mantle_labels')
    op.drop_index(op.f('ix_mantle_labels_origin_address'), table_name='mantle_labels')
    op.drop_index(op.f('ix_mantle_labels_label_type'), table_name='mantle_labels')
    op.drop_index(op.f('ix_mantle_labels_label_name'), table_name='mantle_labels')
    op.drop_index(op.f('ix_mantle_labels_label'), table_name='mantle_labels')
    op.drop_index(op.f('ix_mantle_labels_caller_address'), table_name='mantle_labels')
    op.drop_index(op.f('ix_mantle_labels_block_number'), table_name='mantle_labels')
    op.drop_index(op.f('ix_mantle_labels_address'), table_name='mantle_labels')
    op.drop_index('ix_mantle_labels_addr_block_ts', table_name='mantle_labels')
    op.drop_index('ix_mantle_labels_addr_block_num', table_name='mantle_labels')
    op.drop_table('mantle_labels')
    op.drop_index('uk_g7o_arbitrum_sepolia_labels_tx_hash_tx_call', table_name='game7_orbit_arbitrum_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_g7o_arbitrum_sepolia_labels_tx_hash_log_idx_evt', table_name='game7_orbit_arbitrum_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_transaction_hash'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_origin_address'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_label_type'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_label_name'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_label'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_caller_address'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_block_number'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index(op.f('ix_game7_orbit_arbitrum_sepolia_labels_address'), table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index('ix_g7o_arbitrum_sepolia_labels_addr_block_ts', table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_index('ix_g7o_arbitrum_sepolia_labels_addr_block_num', table_name='game7_orbit_arbitrum_sepolia_labels')
    op.drop_table('game7_orbit_arbitrum_sepolia_labels')
    # ### end Alembic commands ###
