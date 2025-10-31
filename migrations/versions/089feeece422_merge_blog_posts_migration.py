"""merge blog posts migration

Revision ID: 089feeece422
Revises: 581cd9ed2c74, create_blog_posts
Create Date: 2025-10-31 23:10:57.010064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '089feeece422'
down_revision = ('581cd9ed2c74', 'create_blog_posts')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
