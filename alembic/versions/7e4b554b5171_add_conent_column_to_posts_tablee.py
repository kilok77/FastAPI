"""add conent column to posts tablee

Revision ID: 7e4b554b5171
Revises: 2734ed11daf6
Create Date: 2022-07-08 15:01:56.220313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e4b554b5171'
down_revision = '2734ed11daf6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
