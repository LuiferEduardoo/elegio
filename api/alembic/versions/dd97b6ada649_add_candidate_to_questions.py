"""add candidate to questions

Revision ID: dd97b6ada649
Revises: 76446176c32f
Create Date: 2026-06-15 19:51:55.338138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd97b6ada649'
down_revision: Union[str, None] = '76446176c32f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('questions', sa.Column('candidate_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_questions_candidate_id',
        'questions',
        'candidates',
        ['candidate_id'],
        ['id'],
        ondelete='SET NULL',
    )


def downgrade() -> None:
    op.drop_constraint('fk_questions_candidate_id', 'questions', type_='foreignkey')
    op.drop_column('questions', 'candidate_id')
