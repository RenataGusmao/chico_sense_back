"""create initial domain tables

Revision ID: 20260930_0001
Revises:
Create Date: 2026-09-30 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260930_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ENUMS = {
    "tipo_empresa": ("PRODUTOR", "TRANSPORTADORA", "CLIENTE"),
    "status_viagem": ("PLANEJADA", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"),
    "status_carga": ("PLANEJADA", "EM_TRANSITO", "ENTREGUE", "CANCELADA"),
    "status_caixa": ("REGISTRADA", "EM_TRANSITO", "ENTREGUE", "AVARIADA"),
    "status_dispositivo": ("ATIVO", "INATIVO", "MANUTENCAO"),
    "tipo_sensor": ("TEMPERATURA", "UMIDADE"),
    "contexto_medicao": ("AMBIENTE", "PRODUTO", "CAIXA"),
    "status_sensor": ("ATIVO", "INATIVO", "MANUTENCAO"),
    "nivel_alerta": ("INFORMATIVO", "ATENCAO", "CRITICO"),
    "status_alerta": ("ABERTO", "EM_ANALISE", "RESOLVIDO", "DESCARTADO"),
}


def enum_type(name: str) -> postgresql.ENUM:
    return postgresql.ENUM(*ENUMS[name], name=name, create_type=False)


def id_column() -> sa.Column:
    return sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False)


def timestamp_columns() -> tuple[sa.Column, sa.Column]:
    return (
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )


def create_enum_types() -> None:
    bind = op.get_bind()
    for name, values in ENUMS.items():
        postgresql.ENUM(*values, name=name).create(bind, checkfirst=True)


def drop_enum_types() -> None:
    bind = op.get_bind()
    for name, values in reversed(ENUMS.items()):
        postgresql.ENUM(*values, name=name).drop(bind, checkfirst=True)


def upgrade() -> None:
    create_enum_types()

    op.create_table(
        "perfis",
        id_column(),
        sa.Column("nome", sa.String(length=80), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        *timestamp_columns(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_table(
        "empresas",
        id_column(),
        sa.Column("nome", sa.String(length=180), nullable=False),
        sa.Column("documento", sa.String(length=40), nullable=True),
        sa.Column("tipo", enum_type("tipo_empresa"), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        *timestamp_columns(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("documento"),
    )
    op.create_index(op.f("ix_empresas_nome"), "empresas", ["nome"], unique=False)

    op.create_table(
        "produtos",
        id_column(),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        *timestamp_columns(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_table(
        "usuarios",
        id_column(),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.Column("perfil_id", postgresql.UUID(as_uuid=True), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["perfil_id"], ["perfis.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=False)

    op.create_table(
        "parametros_produto",
        id_column(),
        sa.Column("produto_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome_parametro", sa.String(length=120), nullable=False),
        sa.Column("unidade", sa.String(length=30), nullable=True),
        sa.Column("valor_minimo", sa.Numeric(12, 4), nullable=True),
        sa.Column("valor_maximo", sa.Numeric(12, 4), nullable=True),
        sa.Column("observacao", sa.Text(), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["produto_id"], ["produtos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "veiculos",
        id_column(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("identificador", sa.String(length=80), nullable=False),
        sa.Column("placa", sa.String(length=20), nullable=True),
        sa.Column("modelo", sa.String(length=120), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("placa"),
    )
    op.create_table(
        "motoristas",
        id_column(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("documento", sa.String(length=40), nullable=True),
        sa.Column("telefone", sa.String(length=40), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("documento"),
    )
    op.create_table(
        "viagens",
        id_column(),
        sa.Column("transportadora_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("veiculo_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("motorista_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("origem", sa.String(length=255), nullable=False),
        sa.Column("destino", sa.String(length=255), nullable=False),
        sa.Column("saida_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("previsao_chegada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("chegada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", enum_type("status_viagem"), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["motorista_id"], ["motoristas.id"]),
        sa.ForeignKeyConstraint(["transportadora_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["veiculo_id"], ["veiculos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "empresas_usuarios",
        id_column(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("usuario_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cargo", sa.String(length=120), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("empresa_id", "usuario_id", name="uq_empresa_usuario"),
    )
    op.create_table(
        "cargas",
        id_column(),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("produto_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("produtor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cliente_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("identificacao", sa.String(length=120), nullable=False),
        sa.Column("quantidade_caixas", sa.Integer(), nullable=True),
        sa.Column("status", enum_type("status_carga"), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["cliente_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["produtor_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["produto_id"], ["produtos.id"]),
        sa.ForeignKeyConstraint(["viagem_id"], ["viagens.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cargas_identificacao"), "cargas", ["identificacao"], unique=False)

    op.create_table(
        "caixas",
        id_column(),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("identificacao", sa.String(length=120), nullable=False),
        sa.Column("status", enum_type("status_caixa"), nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["carga_id"], ["cargas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_caixas_identificacao"), "caixas", ["identificacao"], unique=False)

    op.create_table(
        "dispositivos",
        id_column(),
        sa.Column("identificador", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.String(length=255), nullable=True),
        sa.Column("status", enum_type("status_dispositivo"), nullable=False),
        sa.Column("veiculo_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["carga_id"], ["cargas.id"]),
        sa.ForeignKeyConstraint(["veiculo_id"], ["veiculos.id"]),
        sa.ForeignKeyConstraint(["viagem_id"], ["viagens.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("identificador"),
    )
    op.create_table(
        "sensores",
        id_column(),
        sa.Column("dispositivo_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("identificador", sa.String(length=120), nullable=False),
        sa.Column("tipo", enum_type("tipo_sensor"), nullable=False),
        sa.Column("contexto", enum_type("contexto_medicao"), nullable=False),
        sa.Column("unidade", sa.String(length=30), nullable=False),
        sa.Column("status", enum_type("status_sensor"), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["dispositivo_id"], ["dispositivos.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dispositivo_id", "identificador", name="uq_sensor_dispositivo_identificador"),
    )
    op.create_table(
        "medicoes",
        id_column(),
        sa.Column("sensor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("caixa_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("medida_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("contexto", enum_type("contexto_medicao"), nullable=False),
        sa.Column("valor", sa.Numeric(12, 4), nullable=False),
        sa.Column("unidade", sa.String(length=30), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["caixa_id"], ["caixas.id"]),
        sa.ForeignKeyConstraint(["carga_id"], ["cargas.id"]),
        sa.ForeignKeyConstraint(["sensor_id"], ["sensores.id"]),
        sa.ForeignKeyConstraint(["viagem_id"], ["viagens.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_medicoes_caixa_id", "medicoes", ["caixa_id"], unique=False)
    op.create_index("ix_medicoes_carga_id", "medicoes", ["carga_id"], unique=False)
    op.create_index("ix_medicoes_medida_em", "medicoes", ["medida_em"], unique=False)
    op.create_index("ix_medicoes_sensor_id", "medicoes", ["sensor_id"], unique=False)
    op.create_index("ix_medicoes_sensor_medida_em", "medicoes", ["sensor_id", "medida_em"], unique=False)
    op.create_index("ix_medicoes_viagem_id", "medicoes", ["viagem_id"], unique=False)

    op.create_table(
        "alertas",
        id_column(),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("caixa_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("medicao_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tipo", sa.String(length=120), nullable=False),
        sa.Column("nivel", enum_type("nivel_alerta"), nullable=False),
        sa.Column("status", enum_type("status_alerta"), nullable=False),
        sa.Column("limite_considerado", sa.Numeric(12, 4), nullable=True),
        sa.Column("valor_registrado", sa.Numeric(12, 4), nullable=True),
        sa.Column("unidade", sa.String(length=30), nullable=True),
        sa.Column("iniciado_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finalizado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duracao_segundos", sa.Integer(), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["caixa_id"], ["caixas.id"]),
        sa.ForeignKeyConstraint(["carga_id"], ["cargas.id"]),
        sa.ForeignKeyConstraint(["medicao_id"], ["medicoes.id"]),
        sa.ForeignKeyConstraint(["viagem_id"], ["viagens.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ocorrencias",
        id_column(),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("caixa_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tipo", sa.String(length=120), nullable=False),
        sa.Column("titulo", sa.String(length=180), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("registrada_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=True),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["caixa_id"], ["caixas.id"]),
        sa.ForeignKeyConstraint(["carga_id"], ["cargas.id"]),
        sa.ForeignKeyConstraint(["viagem_id"], ["viagens.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "recomendacoes_ia",
        id_column(),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("caixa_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.Column("nivel_risco", sa.String(length=80), nullable=True),
        sa.Column("justificativa", sa.Text(), nullable=True),
        sa.Column("fatores_considerados", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("gerada_em", sa.DateTime(timezone=True), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["caixa_id"], ["caixas.id"]),
        sa.ForeignKeyConstraint(["carga_id"], ["cargas.id"]),
        sa.ForeignKeyConstraint(["viagem_id"], ["viagens.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dados_externos",
        id_column(),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("caixa_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("fonte", sa.String(length=120), nullable=False),
        sa.Column("tipo", sa.String(length=120), nullable=False),
        sa.Column("dados", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("coletado_em", sa.DateTime(timezone=True), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(["caixa_id"], ["caixas.id"]),
        sa.ForeignKeyConstraint(["carga_id"], ["cargas.id"]),
        sa.ForeignKeyConstraint(["viagem_id"], ["viagens.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("dados_externos")
    op.drop_table("recomendacoes_ia")
    op.drop_table("ocorrencias")
    op.drop_table("alertas")
    op.drop_index("ix_medicoes_viagem_id", table_name="medicoes")
    op.drop_index("ix_medicoes_sensor_medida_em", table_name="medicoes")
    op.drop_index("ix_medicoes_sensor_id", table_name="medicoes")
    op.drop_index("ix_medicoes_medida_em", table_name="medicoes")
    op.drop_index("ix_medicoes_carga_id", table_name="medicoes")
    op.drop_index("ix_medicoes_caixa_id", table_name="medicoes")
    op.drop_table("medicoes")
    op.drop_table("sensores")
    op.drop_table("dispositivos")
    op.drop_index(op.f("ix_caixas_identificacao"), table_name="caixas")
    op.drop_table("caixas")
    op.drop_index(op.f("ix_cargas_identificacao"), table_name="cargas")
    op.drop_table("cargas")
    op.drop_table("empresas_usuarios")
    op.drop_table("viagens")
    op.drop_table("motoristas")
    op.drop_table("veiculos")
    op.drop_table("parametros_produto")
    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_table("usuarios")
    op.drop_table("produtos")
    op.drop_index(op.f("ix_empresas_nome"), table_name="empresas")
    op.drop_table("empresas")
    op.drop_table("perfis")
    drop_enum_types()

