"""merge media files migration

Revision ID: c9f6829d4b64
Revises: 089feeece422, create_media_files
Create Date: 2025-10-31 23:20:52.750154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9f6829d4b64'
down_revision = ('089feeece422', 'create_media_files')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
