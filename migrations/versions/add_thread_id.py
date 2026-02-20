"""add openai_thread_id to user_telegram_links

Revision ID: add_thread_id
Revises: 0aafee66b26c
Create Date: 2026-02-20 22:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_thread_id'
down_revision = '0aafee66b26c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user_telegram_links',
        sa.Column('openai_thread_id', sa.String(length=100), nullable=True)
    )


def downgrade():
    op.drop_column('user_telegram_links', 'openai_thread_id')
