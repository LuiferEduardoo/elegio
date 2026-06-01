"""add is_in_the_second_round to candidates

Revision ID: b5d1f2c83a40
Revises: f0c8a3e2b9d1
Create Date: 2026-05-31 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5d1f2c83a40'
down_revision: Union[str, None] = 'f0c8a3e2b9d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'candidates',
        sa.Column(
            'is_in_the_second_round',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('0'),
        ),
    )


def downgrade() -> None:
    op.drop_column('candidates', 'is_in_the_second_round')
