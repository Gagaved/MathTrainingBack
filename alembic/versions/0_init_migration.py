from alembic import op
import sqlalchemy as sa

"""
Revision ID: 0_init_migration
Revises:
Create Date: 2023-07-04 10:00:00
"""
revision = '0_init_migration'
down_revision = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String),
        sa.Column('email', sa.String)
    )

def downgrade():
    op.drop_table('users')