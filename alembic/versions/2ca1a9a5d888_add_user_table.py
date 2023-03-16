"""add user table

Revision ID: 2ca1a9a5d888
Revises: 57db8115d4af
Create Date: 2023-03-16 11:40:48.068486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ca1a9a5d888'
down_revision = '57db8115d4af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('Users', 
                sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                sa.UniqueConstraint('email')
                )


def downgrade() -> None:
    op.drop_table('Users')
