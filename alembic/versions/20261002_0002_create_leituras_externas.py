"""create external readings tracking table

Revision ID: 20261002_0002
Revises: 20260930_0001
Create Date: 2026-10-02 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20261002_0002"
down_revision: Union[str, None] = "20260930_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "leituras_externas",
        sa.Column("origem", sa.String(length=80), nullable=False),
        sa.Column("channel_id", sa.String(length=80), nullable=False),
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("field_name", sa.String(length=40), nullable=False),
        sa.Column("medicao_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["medicao_id"], ["medicoes.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "origem",
            "channel_id",
            "entry_id",
            "field_name",
            name="uq_leitura_externa_origem_channel_entry_field",
        ),
    )
    op.create_index("ix_leituras_externas_medicao_id", "leituras_externas", ["medicao_id"], unique=False)
    op.create_index(
        "ix_leituras_externas_origem_channel",
        "leituras_externas",
        ["origem", "channel_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_leituras_externas_origem_channel", table_name="leituras_externas")
    op.drop_index("ix_leituras_externas_medicao_id", table_name="leituras_externas")
    op.drop_table("leituras_externas")

