"""create foreign key

Revision ID: ea23256aa0e3
Revises: 9579c91c86f4
Create Date: 2023-05-23 12:54:48.950044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea23256aa0e3'
down_revision = '9579c91c86f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
