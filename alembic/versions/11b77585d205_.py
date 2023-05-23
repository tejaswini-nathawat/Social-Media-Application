"""empty message

Revision ID: 11b77585d205
Revises: 5251e9f4177e
Create Date: 2023-05-23 12:03:41.046599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11b77585d205'
down_revision = '5251e9f4177e'
branch_labels = None
depends_on = None


def upgrade() :
 
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))

    pass


def downgrade():
    op.drop_column('posts','content')
    pass
