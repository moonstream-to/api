"""Add deploy block

Revision ID: 6807bdf6f417
Revises: 48d2562504d1
Create Date: 2024-08-23 16:51:47.147758

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6807bdf6f417"
down_revision: Union[str, None] = "25b339f55f8f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "abi_jobs",
        sa.Column("deployment_block_number", sa.BigInteger(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("abi_jobs", "deployment_block_number")
    # ### end Alembic commands ###
