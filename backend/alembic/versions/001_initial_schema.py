"""Initial schema - SQLite compatible

Revision ID: 001
Revises: 
Create Date: 2026-01-21 00:50:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('auth_provider_id', sa.String(), nullable=True),
        sa.Column('subscription_tier', sa.String(), nullable=True, server_default='free'),
        sa.Column('subscription_status', sa.String(), nullable=True, server_default='active'),
        sa.Column('tasks_used_this_month', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('billing_period_start', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create user_integrations table
    op.create_table('user_integrations',
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('access_token', sa.String(), nullable=True),
        sa.Column('refresh_token', sa.String(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'provider')
    )

    # Create tasks table
    op.create_table('tasks',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('priority', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='pending'),
        sa.Column('points_value', sa.Integer(), nullable=True, server_default='10'),
        sa.Column('context_notes', sa.Text(), nullable=True),
        sa.Column('estimated_duration_minutes', sa.Integer(), nullable=True),
        sa.Column('ai_reasoning', sa.Text(), nullable=True),
        sa.Column('parent_task_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['parent_task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tasks_status', 'tasks', ['user_id', 'status'])

    # Create calendar_events table
    op.create_table('calendar_events',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('task_id', sa.String(36), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_fixed', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('source', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_calendar_range', 'calendar_events', ['user_id', 'start_time', 'end_time'])


def downgrade() -> None:
    op.drop_index('idx_calendar_range', table_name='calendar_events')
    op.drop_table('calendar_events')
    op.drop_index('idx_tasks_status', table_name='tasks')
    op.drop_table('tasks')
    op.drop_table('user_integrations')
    op.drop_table('users')
