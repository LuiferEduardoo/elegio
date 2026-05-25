"""create rhetorical_weights table

Revision ID: c3e8f1a2b9d4
Revises: b7f4c2a19d6e
Create Date: 2026-05-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3e8f1a2b9d4'
down_revision: Union[str, None] = 'b7f4c2a19d6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'rhetorical_weights',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('candidate_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('editorial_justification', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.CheckConstraint('value >= 0.0 AND value <= 2.0', name='ck_rhetorical_weights_value_range'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('rhetorical_weights')
