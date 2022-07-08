"""add user table

Revision ID: 0d2d9b4c9a62
Revises: 7e4b554b5171
Create Date: 2022-07-08 15:05:04.289545

"""
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d2d9b4c9a62'
down_revision = '7e4b554b5171'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
    sa.Column('id',sa.Integer(),nullable=False),
    sa.Column('email',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')
    pass
