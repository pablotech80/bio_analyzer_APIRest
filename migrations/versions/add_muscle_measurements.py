"""Add muscle measurements fields

Revision ID: add_muscle_measurements
Revises: b782377526f4
Create Date: 2025-10-06 21:55:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "add_muscle_measurements"
down_revision = "b782377526f4"
branch_labels = None
depends_on = None


def upgrade():
    """Add muscle measurement fields to biometric_analyses table."""
    # Add new columns for muscle measurements
    op.add_column("biometric_analyses", sa.Column("biceps", sa.Float(), nullable=True))
    op.add_column(
        "biometric_analyses", sa.Column("cuadriceps", sa.Float(), nullable=True)
    )
    op.add_column("biometric_analyses", sa.Column("gemelos", sa.Float(), nullable=True))


def downgrade():
    """Remove muscle measurement fields from biometric_analyses table."""
    # Remove the columns
    op.drop_column("biometric_analyses", "gemelos")
    op.drop_column("biometric_analyses", "cuadriceps")
    op.drop_column("biometric_analyses", "biceps")
