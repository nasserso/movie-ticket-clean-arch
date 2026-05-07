"""add unique constraint to seat

Revision ID: 1afcd93f2568
Revises: 08862d618a90
Create Date: 2026-05-07 02:17:10.795787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1afcd93f2568'
down_revision: Union[str, Sequence[str], None] = '08862d618a90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("seats", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "uq_seat_position",
            ["horizontal", "vertical", "room_id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("seats", schema=None) as batch_op:
        batch_op.drop_constraint("uq_seat_position", type_="unique")
