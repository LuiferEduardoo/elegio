"""accept both upper and lower case posture enums

Revision ID: e91f4c5a72b0
Revises: d7a2b4f01e8c
Create Date: 2026-05-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e91f4c5a72b0'
down_revision: Union[str, None] = 'd7a2b4f01e8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE postures MODIFY confidence "
        "ENUM('high','medium','low','HIGH','MEDIUM','LOW') "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL"
    )
    op.execute(
        "ALTER TABLE postures MODIFY coder_type "
        "ENUM('llm','human','LLM','HUMAN') "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE postures MODIFY confidence "
        "ENUM('HIGH','MEDIUM','LOW') NOT NULL"
    )
    op.execute(
        "ALTER TABLE postures MODIFY coder_type "
        "ENUM('LLM','HUMAN') NOT NULL"
    )
