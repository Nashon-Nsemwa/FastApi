"""create post table

Revision ID: 8b43a482be3c
Revises: 
Create Date: 2026-07-02 00:12:52.542490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b43a482be3c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
    sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade() :
    op.drop_table('posts')
    
    pass
