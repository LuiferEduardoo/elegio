"""expand rhetorical_weight range to 5

Revision ID: d7a2b4f01e8c
Revises: c3e8f1a2b9d4
Create Date: 2026-05-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd7a2b4f01e8c'
down_revision: Union[str, None] = 'c3e8f1a2b9d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        'ck_rhetorical_weights_value_range', 'rhetorical_weights', type_='check'
    )
    op.create_check_constraint(
        'ck_rhetorical_weights_value_range',
        'rhetorical_weights',
        'value >= 0.0 AND value <= 5.0',
    )


def downgrade() -> None:
    op.drop_constraint(
        'ck_rhetorical_weights_value_range', 'rhetorical_weights', type_='check'
    )
    op.create_check_constraint(
        'ck_rhetorical_weights_value_range',
        'rhetorical_weights',
        'value >= 0.0 AND value <= 2.0',
    )
