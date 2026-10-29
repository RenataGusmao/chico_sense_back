"""Cargo declarations, monitoring sessions and lifecycle audit.

Revision ID: 20261028_0006_monitoramento
Revises: 20261007_0005_logistica
No existing cargo receives inferred mass, maturity or lot information.
"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision = "20261028_0006_monitoramento"
down_revision = "20261007_0005_logistica"
branch_labels = None
depends_on = None


def base_columns():
    return [
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    ]


def cargo_columns():
    return [
        sa.Column("produto_identificado", sa.String(40), nullable=False),
        sa.Column("massa_kg", sa.Numeric(12, 4), nullable=False),
        sa.Column("maturacao", sa.String(30), nullable=False),
        sa.Column("lote_codigo", sa.String(120), nullable=False),
        sa.Column("lote_hipotetico", sa.Boolean(), nullable=False),
        sa.Column("rastreabilidade", sa.Text(), nullable=False),
    ]


MATURACAO = "maturacao IN ('VERDE_MADURA','EM_AMADURECIMENTO','MADURA','MISTA','DESCONHECIDA')"


def upgrade():
    op.create_index("uq_cargas_id_viagem_monitoramento", "cargas", ["id", "viagem_id"], unique=True)
    op.create_table(
        "cargas_monitoramento", *base_columns(), *cargo_columns(),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cargas.id"), nullable=False),
        sa.Column("versao", sa.Integer(), nullable=False),
        sa.Column("atualizado_por_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.UniqueConstraint("carga_id", name="uq_config_monitoramento_carga"),
        sa.UniqueConstraint("id", "carga_id", name="uq_config_monitoramento_id_carga"),
        sa.CheckConstraint("massa_kg > 0 AND massa_kg < 100000000", name="ck_config_monitoramento_massa"),
        sa.CheckConstraint(MATURACAO, name="ck_config_monitoramento_maturacao"),
        sa.CheckConstraint("produto_identificado = 'MANGA_TOMMY_ATKINS'", name="ck_config_monitoramento_produto"),
        sa.CheckConstraint("versao > 0", name="ck_config_monitoramento_versao"),
    )
    op.create_table(
        "sessoes_monitoramento", *base_columns(), *cargo_columns(),
        sa.Column("carga_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("viagem_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("viagens.id"), nullable=False),
        sa.Column("configuracao_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fim", sa.DateTime(timezone=True), nullable=True),
        sa.Column("estado", sa.String(20), nullable=False),
        sa.Column("sensor_temperatura_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sensores.id"), nullable=False),
        sa.Column("sensor_umidade_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sensores.id"), nullable=True),
        sa.Column("ambiente_aquisicao", sa.String(30), nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("configuracao_versao", sa.Integer(), nullable=False),
        sa.Column("origem_sensor", sa.JSON().with_variant(postgresql.JSONB(), "postgresql"), nullable=False),
        sa.Column("criada_por_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("finalizada_por_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("usuarios.id"), nullable=True),
        sa.Column("motivo_fim", sa.Text(), nullable=True),
        sa.Column("chave_idempotencia", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("assinatura_requisicao", sa.String(64), nullable=False),
        sa.ForeignKeyConstraint(["carga_id", "viagem_id"], ["cargas.id", "cargas.viagem_id"], name="fk_sessao_carga_viagem"),
        sa.ForeignKeyConstraint(["configuracao_id", "carga_id"], ["cargas_monitoramento.id", "cargas_monitoramento.carga_id"], name="fk_sessao_config_carga"),
        sa.UniqueConstraint("criada_por_id", "chave_idempotencia", name="uq_sessao_autor_idempotencia"),
        sa.CheckConstraint("estado IN ('ATIVA','ENCERRADA','CANCELADA')", name="ck_sessao_estado"),
        sa.CheckConstraint("(estado = 'ATIVA' AND fim IS NULL AND finalizada_por_id IS NULL AND motivo_fim IS NULL) OR (estado <> 'ATIVA' AND fim IS NOT NULL AND fim > inicio AND finalizada_por_id IS NOT NULL AND motivo_fim IS NOT NULL)", name="ck_sessao_ciclo"),
        sa.CheckConstraint("sensor_umidade_id IS NULL OR sensor_umidade_id <> sensor_temperatura_id", name="ck_sessao_sensores_distintos"),
        sa.CheckConstraint("massa_kg > 0 AND massa_kg < 100000000", name="ck_sessao_massa"),
        sa.CheckConstraint(MATURACAO, name="ck_sessao_maturacao"),
        sa.CheckConstraint("ambiente_aquisicao IN ('LABORATORIO','TRANSPORTE_REFRIGERADO')", name="ck_sessao_ambiente"),
    )
    op.create_index("ix_sessoes_viagem_inicio", "sessoes_monitoramento", ["viagem_id", "inicio"])
    op.create_index("ix_sessoes_carga_inicio", "sessoes_monitoramento", ["carga_id", "inicio"])
    for name, column in (("uq_sessao_ativa_carga", "carga_id"), ("uq_sessao_ativa_temperatura", "sensor_temperatura_id"), ("uq_sessao_ativa_umidade", "sensor_umidade_id")):
        op.create_index(name, "sessoes_monitoramento", [column], unique=True,
                        postgresql_where=sa.text("estado = 'ATIVA'"), sqlite_where=sa.text("estado = 'ATIVA'"))
    op.create_table(
        "eventos_monitoramento", *base_columns(),
        sa.Column("configuracao_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cargas_monitoramento.id"), nullable=False),
        sa.Column("sessao_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sessoes_monitoramento.id"), nullable=True),
        sa.Column("usuario_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("tipo", sa.String(40), nullable=False),
        sa.Column("registrado_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dados", sa.JSON().with_variant(postgresql.JSONB(), "postgresql"), nullable=False),
    )
    op.create_index("ix_eventos_monitoramento_configuracao_id", "eventos_monitoramento", ["configuracao_id"])
    op.create_index("ix_eventos_monitoramento_sessao_id", "eventos_monitoramento", ["sessao_id"])


def downgrade():
    # Explicit rollback removes only the new feature data and its supporting index.
    op.drop_table("eventos_monitoramento")
    op.drop_table("sessoes_monitoramento")
    op.drop_table("cargas_monitoramento")
    op.drop_index("uq_cargas_id_viagem_monitoramento", table_name="cargas")
