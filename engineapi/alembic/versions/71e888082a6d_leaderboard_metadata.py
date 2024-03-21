"""leaderboard metadata

Revision ID: 71e888082a6d
Revises: cc80e886e153
Create Date: 2023-11-15 13:21:16.108399

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "71e888082a6d"
down_revision = "cc80e886e153"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "leaderboards",
        sa.Column(
            "blockchain_ids",
            sa.ARRAY(sa.Integer()),
            nullable=False,
            server_default="{}",
        ),
    )
    op.add_column(
        "leaderboards",
        sa.Column(
            "wallet_connect", sa.Boolean(), nullable=False, server_default="false"
        ),
    )
    op.add_column(
        "leaderboards",
        sa.Column(
            "columns_names", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("leaderboards", "columns_names")
    op.drop_column("leaderboards", "wallet_connect")
    op.drop_column("leaderboards", "blockchain_ids")
    # ### end Alembic commands ###