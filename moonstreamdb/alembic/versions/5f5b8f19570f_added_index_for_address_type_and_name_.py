"""Added index for address type and name of event

Revision ID: 5f5b8f19570f
Revises: f991fc7493c8
Create Date: 2022-05-04 11:32:42.309322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5f5b8f19570f"
down_revision = "f991fc7493c8"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE INDEX ix_polygon_labels_address_label_label_data_type_and_name ON polygon_labels USING BTREE (address,label,(label_data->>'type'),(label_data->>'name'));
        """
    )


def downgrade():
    op.execute(
        """
        DROP INDEX ix_polygon_labels_address_label_label_data_type_and_name;
        """
    )
