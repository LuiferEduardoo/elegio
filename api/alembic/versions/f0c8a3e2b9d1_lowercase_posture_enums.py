"""normalize posture enums to lowercase

Revision ID: f0c8a3e2b9d1
Revises: e91f4c5a72b0
Create Date: 2026-05-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f0c8a3e2b9d1'
down_revision: Union[str, None] = 'e91f4c5a72b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE postures SET confidence = LOWER(confidence)")
    op.execute("UPDATE postures SET coder_type = LOWER(coder_type)")
    op.execute(
        "ALTER TABLE postures MODIFY confidence "
        "ENUM('high','medium','low') "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL"
    )
    op.execute(
        "ALTER TABLE postures MODIFY coder_type "
        "ENUM('llm','human') "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL"
    )


def downgrade() -> None:
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
