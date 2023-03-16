"""create post table

Revision ID: de05214c0eef
Revises: 
Create Date: 2023-03-16 11:24:31.381733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de05214c0eef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('Posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('Posts')
