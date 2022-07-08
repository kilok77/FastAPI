"""create posts table

Revision ID: 2734ed11daf6
Revises: 
Create Date: 2022-07-08 14:54:33.558659

"""
from re import T
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2734ed11daf6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable=False,primary_key=True), sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table('posts')
    pass
