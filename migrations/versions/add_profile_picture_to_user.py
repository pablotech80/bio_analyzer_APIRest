"""
Revision ID: add_profile_picture_to_user
Revises: d8a613f94370
Create Date: 2025-10-05
"""

# Alembic identifiers
revision = 'add_profile_picture_to_user'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('profile_picture', sa.String(length=255)))

def downgrade():
    op.drop_column('users', 'profile_picture')
