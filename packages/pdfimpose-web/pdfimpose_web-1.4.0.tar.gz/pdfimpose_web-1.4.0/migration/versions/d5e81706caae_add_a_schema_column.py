"""Add a 'layout' column

Revision ID: d5e81706caae
Revises:
Create Date: 2025-04-27 15:57:51.048627

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5e81706caae"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("daily_stat", sa.Column("layout", sa.String(32)))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("daily_stat", "layout")
