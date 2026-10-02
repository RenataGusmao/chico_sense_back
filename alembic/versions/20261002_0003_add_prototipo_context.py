"""add prototype measurement context

Revision ID: 20261002_0003
Revises: 20261002_0002
Create Date: 2026-10-02 00:00:00
"""

from typing import Sequence, Union

from alembic import op

revision: str = "20261002_0003"
down_revision: Union[str, None] = "20261002_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE contexto_medicao ADD VALUE IF NOT EXISTS 'PROTOTIPO'")
    op.alter_column("medicoes", "viagem_id", nullable=True)
    op.alter_column("medicoes", "carga_id", nullable=True)


def downgrade() -> None:
    op.alter_column("medicoes", "carga_id", nullable=False)
    op.alter_column("medicoes", "viagem_id", nullable=False)

