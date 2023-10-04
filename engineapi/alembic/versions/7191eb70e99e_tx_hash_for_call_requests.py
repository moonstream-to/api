"""Tx hash for call requests

Revision ID: 7191eb70e99e
Revises: 4f05d212ea49
Create Date: 2023-10-04 11:23:12.516797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7191eb70e99e'
down_revision = '4f05d212ea49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('call_requests', sa.Column('tx_hash', sa.VARCHAR(length=256), nullable=True))
    op.create_unique_constraint(op.f('uq_call_requests_tx_hash'), 'call_requests', ['tx_hash'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_call_requests_tx_hash'), 'call_requests', type_='unique')
    op.drop_column('call_requests', 'tx_hash')
    # ### end Alembic commands ###
