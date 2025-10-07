"""create contact_messages table

Revision ID: create_contact_msgs
Revises: add_is_admin_field
Create Date: 2025-10-07 18:32:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_contact_msgs'
down_revision = 'add_is_admin_field'
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla contact_messages
    op.create_table(
        'contact_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['analysis_id'], ['biometric_analyses.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices para búsquedas rápidas
    op.create_index('idx_contact_messages_user_id', 'contact_messages', ['user_id'])
    op.create_index('idx_contact_messages_is_read', 'contact_messages', ['is_read'])


def downgrade():
    # Eliminar índices
    op.drop_index('idx_contact_messages_is_read', table_name='contact_messages')
    op.drop_index('idx_contact_messages_user_id', table_name='contact_messages')
    
    # Eliminar tabla
    op.drop_table('contact_messages')
