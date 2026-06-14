"""add video fields to questions

Revision ID: b7d9ede2ed53
Revises: e0b6a8104499
Create Date: 2026-06-13 23:53:49.082514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7d9ede2ed53'
down_revision: Union[str, None] = 'e0b6a8104499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# MySQL stores the enum inline on the column, so a new value isn't picked up by
# autogenerate — modify the column explicitly.
NEW_ENUM = (
    "ENUM('MULTIPLE_CHOICE','BOOLEAN','ONLY_OPTION','OPEN_QUESTION',"
    "'VIDEO_EMOTION_SLIDER') NOT NULL"
)
OLD_ENUM = "ENUM('MULTIPLE_CHOICE','BOOLEAN','ONLY_OPTION','OPEN_QUESTION') NOT NULL"


def upgrade() -> None:
    op.add_column('questions', sa.Column('video_url', sa.String(length=500), nullable=True))
    op.execute(f"ALTER TABLE questions MODIFY COLUMN type_question {NEW_ENUM}")


def downgrade() -> None:
    op.execute(f"ALTER TABLE questions MODIFY COLUMN type_question {OLD_ENUM}")
    op.drop_column('questions', 'video_url')
