"""create notification table

Revision ID: create_notifications
Revises: c9f6829d4b64
Create Date: 2025-01-09 14:23:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_notifications'
down_revision = 'c9f6829d4b64'
branch_label = None
depends_on = None


def upgrade():
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False, comment='Título de la notificación'),
    sa.Column('message', sa.Text(), nullable=False, comment='Mensaje de la notificación'),
    sa.Column('notification_type', sa.String(length=50), nullable=False, comment='Tipo: info, success, warning, danger'),
    sa.Column('is_read', sa.Boolean(), nullable=False, comment='Si fue leída'),
    sa.Column('read_at', sa.DateTime(), nullable=True, comment='Fecha de lectura'),
    sa.Column('nutrition_plan_id', sa.Integer(), nullable=True),
    sa.Column('training_plan_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['nutrition_plan_id'], ['nutrition_plans.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['training_plan_id'], ['training_plans.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)
    op.create_index(op.f('ix_notifications_is_read'), 'notifications', ['is_read'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_notifications_is_read'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_table('notifications')
