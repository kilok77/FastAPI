"""add foreign-key to posts table

Revision ID: 20530296bed5
Revises: 0d2d9b4c9a62
Create Date: 2022-07-08 20:44:00.558556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20530296bed5'
down_revision = '0d2d9b4c9a62'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts",referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")



def downgrade():
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts, owner_id')
    
