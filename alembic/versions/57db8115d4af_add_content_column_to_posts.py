"""add content column to posts

Revision ID: 57db8115d4af
Revises: de05214c0eef
Create Date: 2023-03-16 11:34:08.990271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57db8115d4af'
down_revision = 'de05214c0eef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('Posts', 'content')
