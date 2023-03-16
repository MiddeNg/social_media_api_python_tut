"""add foreign-key to posts table

Revision ID: 3015d510d560
Revises: 2ca1a9a5d888
Create Date: 2023-03-16 11:48:12.215388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3015d510d560'
down_revision = '2ca1a9a5d888'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column(('owner_id'), sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', "Posts", "Users", ["owner_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("post_users_fk", "Posts")
    op.drop_column("Posts", "owner_id")
