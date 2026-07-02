"""add last few columns

Revision ID: f3bff9c26c4d
Revises: 36eb633089f8
Create Date: 2026-07-02 23:57:34.020728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3bff9c26c4d'
down_revision: Union[str, Sequence[str], None] = '36eb633089f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() :
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    
    pass
