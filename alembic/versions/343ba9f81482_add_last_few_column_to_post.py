"""add last few column to post

Revision ID: 343ba9f81482
Revises: 3015d510d560
Create Date: 2023-03-16 11:54:44.522474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '343ba9f81482'
down_revision = '3015d510d560'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column('Posts', sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text("NOW()")))


def downgrade() -> None:
    op.drop_column('Posts', "published")
    op.drop_column('Posts', "created_at")
