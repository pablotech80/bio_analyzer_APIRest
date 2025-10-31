"""create media_files table

Revision ID: create_media_files
Revises: 
Create Date: 2025-10-31 23:20:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_media_files'
down_revision = None  # Se actualizará automáticamente
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'media_files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('alt_text', sa.String(length=200), nullable=True),
        sa.Column('caption', sa.String(length=500), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('uploaded_by', sa.Integer(), nullable=False),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_media_files_file_path'), 'media_files', ['file_path'], unique=True)
    op.create_index(op.f('ix_media_files_uploaded_at'), 'media_files', ['uploaded_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_media_files_uploaded_at'), table_name='media_files')
    op.drop_index(op.f('ix_media_files_file_path'), table_name='media_files')
    op.drop_table('media_files')
