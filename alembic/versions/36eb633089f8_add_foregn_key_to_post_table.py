"""add foregn key to post table 

Revision ID: 36eb633089f8
Revises: 594e67eff846
Create Date: 2026-07-02 23:49:30.813461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36eb633089f8'
down_revision: Union[str, Sequence[str], None] = '594e67eff846'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() :
   op.drop_constraint('post_users_fk', table_name='posts')
   op.drop_column('posts', 'owner_id')
   pass
