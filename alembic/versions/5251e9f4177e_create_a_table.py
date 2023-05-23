"""create a table

Revision ID: 5251e9f4177e
Revises: 
Create Date: 2023-05-23 11:46:51.763864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5251e9f4177e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",sa.Column('id',sa.Integer,nullable=False,primary_key=True),
    sa.Column('title',sa.String,nullable=False),
   
   
   )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
