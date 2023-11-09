"""leaderboard metadata

Revision ID: e86bb1230bca
Revises: 040f2dfde5a5
Create Date: 2023-11-09 16:43:21.553490

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e86bb1230bca"
down_revision = "040f2dfde5a5"
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
        sa.Column("show_connect", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "leaderboards",
        sa.Column("public", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "leaderboards",
        sa.Column(
            "columns_names",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default="{}",
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("leaderboards", "columns_names")
    op.drop_column("leaderboards", "public")
    op.drop_column("leaderboards", "show_connect")
    op.drop_column("leaderboards", "blockchain_ids")
    # ### end Alembic commands ###
