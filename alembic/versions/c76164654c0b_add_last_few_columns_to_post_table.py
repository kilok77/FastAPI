"""add last few columns to post table

Revision ID: c76164654c0b
Revises: 20530296bed5
Create Date: 2022-07-08 20:48:34.740856

"""
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c76164654c0b'
down_revision = '20530296bed5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))




def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
