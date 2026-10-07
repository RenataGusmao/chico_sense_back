"""Enforce normalized email identity without changing existing user records.

Revision ID: 20261005_0004_auth_email
Revises: 20261002_0003
"""
from alembic import op
import sqlalchemy as sa

revision = "20261005_0004_auth_email"
down_revision = "20261002_0003"
branch_labels = None
depends_on = None


def upgrade():
    # Existing case-insensitive duplicates cause a failure requiring manual review.
    op.create_index("uq_usuarios_email_normalizado", "usuarios",
                    [sa.text("lower(trim(email))")], unique=True)


def downgrade():
    op.drop_index("uq_usuarios_email_normalizado", table_name="usuarios")
