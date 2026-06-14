"""rename axis_value to programmatic_alignment_value on response_options

Revision ID: 96d545860ba6
Revises: 7b7de73dccdf
Create Date: 2026-06-14 09:58:38.224247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96d545860ba6'
down_revision: Union[str, None] = '7b7de73dccdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'response_options',
        'axis_value',
        new_column_name='programmatic_alignment_value',
        existing_type=sa.Float(),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'response_options',
        'programmatic_alignment_value',
        new_column_name='axis_value',
        existing_type=sa.Float(),
        existing_nullable=True,
    )
