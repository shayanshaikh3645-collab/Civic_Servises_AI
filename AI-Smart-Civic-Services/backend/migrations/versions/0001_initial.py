"""Initial schema for AI Smart Civic Services

Revision ID: 0001_initial
Revises: 
Create Date: 2026-08-08 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='citizen'),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'complaints',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('citizen_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=False),
        sa.Column('priority_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='Submitted'),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('assigned_department_id', sa.Integer(), sa.ForeignKey('departments.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('assigned_staff_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('title', 'citizen_id', name='uq_complaint_title_citizen'),
    )
    op.create_index('ix_complaint_status_priority', 'complaints', ['status', 'priority'])

    op.create_table(
        'complaint_images',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('complaint_id', sa.Integer(), sa.ForeignKey('complaints.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=1024), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'complaint_status_history',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('complaint_id', sa.Integer(), sa.ForeignKey('complaints.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('changed_by_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'ai_analyses',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('complaint_id', sa.Integer(), sa.ForeignKey('complaints.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=False),
        sa.Column('priority_score', sa.Float(), nullable=False),
        sa.Column('raw_input', sa.Text(), nullable=True),
        sa.Column('raw_output', sa.Text(), nullable=True),
        sa.Column('model_name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_table('ai_analyses')
    op.drop_table('complaint_status_history')
    op.drop_table('complaint_images')
    op.drop_index('ix_complaint_status_priority', table_name='complaints')
    op.drop_table('complaints')
    op.drop_table('departments')
    op.drop_table('users')
