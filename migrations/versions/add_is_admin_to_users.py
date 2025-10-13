"""add is_admin to users

Revision ID: add_is_admin_field
Revises: 425d964eee8d
Create Date: 2025-10-07 18:30:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "add_is_admin_field"
down_revision = "425d964eee8d"
branch_labels = None
depends_on = None


def upgrade():
    # Agregar columna is_admin a tabla users
    op.add_column(
        "users", sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="0")
    )


def downgrade():
    # Eliminar columna is_admin de tabla users
    op.drop_column("users", "is_admin")
