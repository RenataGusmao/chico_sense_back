"""Versioned IoT session acquisition. No legacy measurement is rewritten."""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision = '20261028_0007_historico_iot'
down_revision = '20261028_0006_monitoramento'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('fontes_sessao_iot',
        sa.Column('sessao_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sensor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('origem', sa.String(20), nullable=False),
        sa.Column('channel_id', sa.String(80), nullable=False),
        sa.Column('field_name', sa.String(40), nullable=False),
        sa.Column('tipo', sa.String(20), nullable=False),
        sa.Column('contexto', sa.String(30), nullable=False),
        sa.Column('unidade', sa.String(30), nullable=False),
        sa.Column('snapshot', sa.JSON().with_variant(postgresql.JSONB(), "postgresql"), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensores.id'], name=None),
        sa.ForeignKeyConstraint(['sessao_id'], ['sessoes_monitoramento.id'], name=None),
        sa.UniqueConstraint('id', 'sessao_id', name='uq_fonte_id_sessao'),
        sa.UniqueConstraint('sessao_id', 'channel_id', 'field_name', name='uq_fonte_sessao_channel_field'),
        sa.UniqueConstraint('sessao_id', 'sensor_id', name='uq_fonte_sessao_sensor'),
    )
    op.create_table('sincronizacoes_iot',
        sa.Column('sessao_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('usuario_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('revisao', sa.Integer(), nullable=False),
        sa.Column('chave_idempotencia', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assinatura', sa.String(64), nullable=False),
        sa.Column('origem_dados', sa.String(20), nullable=False),
        sa.Column('estado', sa.String(20), nullable=False),
        sa.Column('inicio_janela', sa.DateTime(timezone=True), nullable=False),
        sa.Column('fim_janela', sa.DateTime(timezone=True), nullable=False),
        sa.Column('iniciada_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('finalizada_em', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expira_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('complementacao', sa.Boolean(), nullable=False),
        sa.Column('justificativa', sa.Text(), nullable=True),
        sa.Column('resumo', sa.JSON().with_variant(postgresql.JSONB(), "postgresql"), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("estado IN ('EM_EXECUCAO','CONCLUIDA','PARCIAL','FALHA','INTERROMPIDA')", name='ck_sync_estado'),
        sa.CheckConstraint('revisao > 0 AND fim_janela >= inicio_janela', name='ck_sync_janela_revisao'),
        sa.ForeignKeyConstraint(['sessao_id'], ['sessoes_monitoramento.id'], name=None),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], name=None),
        sa.UniqueConstraint('id', 'sessao_id', name='uq_sync_id_sessao'),
        sa.UniqueConstraint('sessao_id', 'chave_idempotencia', name='uq_sync_sessao_chave'),
        sa.UniqueConstraint('sessao_id', 'revisao', name='uq_sync_sessao_revisao'),
    )
    op.create_index('uq_sync_executando_sessao', 'sincronizacoes_iot', ['sessao_id'], unique=True, postgresql_where=sa.text("estado = 'EM_EXECUCAO'"), sqlite_where=sa.text("estado = 'EM_EXECUCAO'"))
    op.create_table('registros_sessao_iot',
        sa.Column('sessao_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('fonte_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sincronizacao_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('medicao_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('entry_id', sa.Integer(), nullable=False),
        sa.Column('medida_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('timestamp_origem', sa.String(80), nullable=False),
        sa.Column('recebida_em', sa.DateTime(timezone=True), nullable=True),
        sa.Column('processada_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('valor', sa.Numeric(12, 4), nullable=True),
        sa.Column('estado', sa.String(20), nullable=False),
        sa.Column('motivo', sa.String(80), nullable=True),
        sa.Column('assinatura', sa.String(64), nullable=False),
        sa.Column('tardia', sa.Boolean(), nullable=True),
        sa.Column('apos_encerramento', sa.Boolean(), nullable=False),
        sa.Column('fora_de_ordem', sa.Boolean(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint('entry_id > 0', name='ck_registro_entry'),
        sa.CheckConstraint("(estado = 'VALIDA' AND valor IS NOT NULL AND medicao_id IS NOT NULL) OR (estado = 'INVALIDA' AND valor IS NULL AND medicao_id IS NULL)", name='ck_registro_estado'),
        sa.ForeignKeyConstraint(['fonte_id', 'sessao_id'], ['fontes_sessao_iot.id', 'fontes_sessao_iot.sessao_id'], name='fk_registro_fonte_sessao'),
        sa.ForeignKeyConstraint(['sincronizacao_id', 'sessao_id'], ['sincronizacoes_iot.id', 'sincronizacoes_iot.sessao_id'], name='fk_registro_sync_sessao'),
        sa.ForeignKeyConstraint(['medicao_id'], ['medicoes.id'], name=None),
        sa.ForeignKeyConstraint(['sessao_id'], ['sessoes_monitoramento.id'], name=None),
        sa.UniqueConstraint('fonte_id', 'entry_id', name='uq_registro_fonte_entry'),
    )
    op.create_index('ix_registro_sessao_medida', 'registros_sessao_iot', ['sessao_id', 'medida_em', 'id'], unique=False)
    op.create_table('ocorrencias_iot',
        sa.Column('sincronizacao_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('fonte_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('entry_id', sa.Integer(), nullable=True),
        sa.Column('medida_em', sa.DateTime(timezone=True), nullable=True),
        sa.Column('codigo', sa.String(80), nullable=False),
        sa.Column('processada_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('detalhes', sa.JSON().with_variant(postgresql.JSONB(), "postgresql"), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['fonte_id'], ['fontes_sessao_iot.id'], name=None),
        sa.ForeignKeyConstraint(['sincronizacao_id'], ['sincronizacoes_iot.id'], name=None),
    )
    op.create_index('ix_ocorrencias_iot_sincronizacao_id', 'ocorrencias_iot', ['sincronizacao_id'], unique=False)


def downgrade():
    op.drop_table('ocorrencias_iot')
    op.drop_table('registros_sessao_iot')
    op.drop_table('sincronizacoes_iot')
    op.drop_table('fontes_sessao_iot')
