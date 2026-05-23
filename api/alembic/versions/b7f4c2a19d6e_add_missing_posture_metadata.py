"""add missing posture metadata

Revision ID: b7f4c2a19d6e
Revises: d4e711e3dfd9
Create Date: 2026-05-22 15:20:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7f4c2a19d6e"
down_revision: Union[str, None] = "d4e711e3dfd9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "postures",
        sa.Column(
            "confidence",
            sa.Enum("high", "medium", "low", name="confidence_level"),
            nullable=False,
        ),
    )
    op.add_column("postures", sa.Column("reasoning", sa.Text(), nullable=True))
    op.add_column("postures", sa.Column("ambiguities", sa.Text(), nullable=True))
    op.add_column(
        "postures",
        sa.Column(
            "coder_type",
            sa.Enum("llm", "human", name="coder_type"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("postures", "coder_type")
    op.drop_column("postures", "ambiguities")
    op.drop_column("postures", "reasoning")
    op.drop_column("postures", "confidence")
