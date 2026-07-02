"""add users table

Revision ID: 88ec644ac1bb
Revises: 2d1252c139c2
Create Date: 2026-07-02 00:31:20.381785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88ec644ac1bb'
down_revision: Union[str, Sequence[str], None] = '2d1252c139c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
    sa.Column('email', sa.String(), nullable=False,unique=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.text('now()')),
        
    )

    pass


def downgrade():
    op.drop_table('users')
    pass
