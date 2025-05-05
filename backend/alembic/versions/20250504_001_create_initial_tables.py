"""create roles, users, documents, ingestions

Revision ID: 001_create_initial_tables
Revises:
Create Date: 2025-05-04

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001_create_initial_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('roles',
        sa.Column('role_id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True)
    )

    op.create_table('users',
        sa.Column('user_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100)),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.role_id')),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.current_timestamp())
    )

    op.create_table('documents',
        sa.Column('document_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(length=255)),
        sa.Column('filename', sa.String(length=255)),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id')),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.current_timestamp())
    )

    op.create_table('ingestions',
        sa.Column('ingestion_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('document_id', sa.Integer(), sa.ForeignKey('documents.document_id')),
        sa.Column('status', sa.String(length=50)),
        sa.Column('started_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('finished_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('error_message', sa.Text())
    )


def downgrade():
    op.drop_table('ingestions')
    op.drop_table('documents')
    op.drop_table('users')
    op.drop_table('roles')
