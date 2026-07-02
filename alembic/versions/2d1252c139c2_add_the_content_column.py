""" add the content column

Revision ID: 2d1252c139c2
Revises: 8b43a482be3c
Create Date: 2026-07-02 00:25:46.696169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d1252c139c2'
down_revision: Union[str, Sequence[str], None] = '8b43a482be3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
