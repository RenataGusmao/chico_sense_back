"""Operational logistics fields and scoped identifiers.

Revision ID: 20261007_0005_logistica
Revises: 20261005_0004_auth_email
"""
import sqlalchemy as sa
from alembic import op

revision = "20261007_0005_logistica"
down_revision = "20261005_0004_auth_email"
branch_labels = None
depends_on = None


def added_columns():
    return {
        "veiculos": [
            sa.Column("descricao", sa.Text(), nullable=True),
            sa.Column("ativo", sa.Boolean(), server_default=sa.true(), nullable=False),
        ],
        "motoristas": [sa.Column("ativo", sa.Boolean(), server_default=sa.true(), nullable=False)],
        "viagens": [
            sa.Column("inicio_real", sa.DateTime(timezone=True), nullable=True),
            sa.Column("observacoes", sa.Text(), nullable=True),
        ],
        "cargas": [
            sa.Column("quantidade", sa.Numeric(12, 4), nullable=True),
            sa.Column("unidade", sa.String(30), nullable=True),
            sa.Column("origem_produto", sa.String(255), nullable=True),
            sa.Column("observacoes", sa.Text(), nullable=True),
        ],
        "caixas": [
            sa.Column("codigo_externo", sa.String(120), nullable=True),
            sa.Column("peso", sa.Numeric(12, 4), nullable=True),
        ],
    }


CONSTRAINTS = [
    ("uq_veiculo_empresa_identificador", "veiculos", ["empresa_id", "identificador"]),
    ("uq_carga_viagem_identificacao", "cargas", ["viagem_id", "identificacao"]),
    ("uq_caixa_carga_identificacao", "caixas", ["carga_id", "identificacao"]),
    ("uq_parametro_produto_nome", "parametros_produto", ["produto_id", "nome_parametro"]),
]


def upgrade():
    for table, columns in added_columns().items():
        for column in columns:
            op.add_column(table, column)
    # Existing duplicates require manual review; do not remove historical records.
    for name, table, columns in CONSTRAINTS:
        op.create_unique_constraint(name, table, columns)


def downgrade():
    for name, table, columns in reversed(CONSTRAINTS):
        op.drop_constraint(name, table, type_="unique")
    for table, columns in reversed(list(added_columns().items())):
        for column in reversed(columns):
            op.drop_column(table, column.name)
