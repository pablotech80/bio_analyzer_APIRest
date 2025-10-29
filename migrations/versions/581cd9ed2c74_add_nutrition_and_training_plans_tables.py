"""add_nutrition_and_training_plans_tables

Revision ID: 581cd9ed2c74
Revises: c18eb18a660c
Create Date: 2025-10-29 11:34:49.613235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '581cd9ed2c74'
down_revision = 'c18eb18a660c'
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla nutrition_plans
    op.create_table('nutrition_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('analysis_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('goal', sa.String(length=100), nullable=True),
    sa.Column('daily_calories', sa.Integer(), nullable=True),
    sa.Column('protein_grams', sa.Integer(), nullable=True),
    sa.Column('carbs_grams', sa.Integer(), nullable=True),
    sa.Column('fats_grams', sa.Integer(), nullable=True),
    sa.Column('meals', sa.JSON(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('supplements', sa.Text(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['analysis_id'], ['biometric_analyses.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nutrition_plans_analysis_id'), 'nutrition_plans', ['analysis_id'], unique=False)
    op.create_index(op.f('ix_nutrition_plans_user_id'), 'nutrition_plans', ['user_id'], unique=False)

    # Crear tabla training_plans
    op.create_table('training_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('analysis_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('goal', sa.String(length=100), nullable=True),
    sa.Column('frequency', sa.String(length=100), nullable=True),
    sa.Column('routine_type', sa.String(length=100), nullable=True),
    sa.Column('duration_weeks', sa.Integer(), nullable=True),
    sa.Column('workouts', sa.JSON(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('warm_up', sa.Text(), nullable=True),
    sa.Column('cool_down', sa.Text(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['analysis_id'], ['biometric_analyses.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_plans_analysis_id'), 'training_plans', ['analysis_id'], unique=False)
    op.create_index(op.f('ix_training_plans_user_id'), 'training_plans', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_training_plans_user_id'), table_name='training_plans')
    op.drop_index(op.f('ix_training_plans_analysis_id'), table_name='training_plans')
    op.drop_table('training_plans')
    op.drop_index(op.f('ix_nutrition_plans_user_id'), table_name='nutrition_plans')
    op.drop_index(op.f('ix_nutrition_plans_analysis_id'), table_name='nutrition_plans')
    op.drop_table('nutrition_plans')
