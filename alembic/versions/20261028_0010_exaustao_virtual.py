"""Supervised virtual exhaust; no hardware configuration or legacy rewrites."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261028_0010_exaustao_virtual'
down_revision='20261028_0009_preventivo'
branch_labels=None
depends_on=None

def upgrade():
    op.create_table('intervencoes_simuladas',
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('viagem_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('carga_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('veiculo_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('alerta_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('avaliacao_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('analise_etileno_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('solicitante_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('decidida_por_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('iniciada_por_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('finalizada_por_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('modalidade',sa.String(20),nullable=False),
        sa.Column('estado',sa.String(30),nullable=False),
        sa.Column('chave_idempotencia',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('assinatura',sa.String(64),nullable=False),
        sa.Column('justificativa_solicitacao',sa.Text(),nullable=False),
        sa.Column('motivo_fim',sa.Text(),nullable=True),
        sa.Column('solicitada_em',sa.DateTime(timezone=True),nullable=False),
        sa.Column('decidida_em',sa.DateTime(timezone=True),nullable=True),
        sa.Column('iniciada_em',sa.DateTime(timezone=True),nullable=True),
        sa.Column('prazo_planejado_em',sa.DateTime(timezone=True),nullable=True),
        sa.Column('finalizada_em',sa.DateTime(timezone=True),nullable=True),
        sa.Column('duracao_planejada_s',sa.Numeric(12,3),nullable=False),
        sa.Column('duracao_registrada_s',sa.Numeric(20,6),nullable=True),
        sa.Column('referencias_snapshot',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.Column('hash_referencias',sa.String(64),nullable=False),
        sa.Column('id',postgresql.UUID(as_uuid=True),nullable=False,primary_key=True),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['analise_etileno_id'],['analises_etileno.id'],name=None),
        sa.ForeignKeyConstraint(['solicitante_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['decidida_por_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['iniciada_por_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['finalizada_por_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id'],name=None),
        sa.ForeignKeyConstraint(['veiculo_id'],['veiculos.id'],name=None),
        sa.ForeignKeyConstraint(['viagem_id'],['viagens.id'],name=None),
        sa.CheckConstraint("((estado IN ('SOLICITADA','AUTORIZADA','RECUSADA')) AND iniciada_em IS NULL AND finalizada_em IS NULL AND duracao_registrada_s IS NULL) OR (estado = 'EM_EXECUCAO' AND iniciada_em IS NOT NULL AND finalizada_em IS NULL AND duracao_registrada_s IS NULL) OR (estado IN ('CONCLUIDA','FALHA_SIMULACAO') AND iniciada_em IS NOT NULL AND finalizada_em IS NOT NULL AND duracao_registrada_s IS NOT NULL) OR (estado = 'CANCELADA' AND finalizada_em IS NOT NULL AND ((iniciada_em IS NULL AND duracao_registrada_s IS NULL) OR (iniciada_em IS NOT NULL AND duracao_registrada_s IS NOT NULL)))",name='ck_intervencao_ciclo'),
        sa.CheckConstraint("(estado = 'SOLICITADA' AND decidida_em IS NULL AND decidida_por_id IS NULL) OR (estado IN ('AUTORIZADA','RECUSADA','EM_EXECUCAO','CONCLUIDA','FALHA_SIMULACAO') AND decidida_em IS NOT NULL AND decidida_por_id IS NOT NULL) OR estado = 'CANCELADA'",name='ck_intervencao_decisao'),
        sa.CheckConstraint('duracao_planejada_s > 0 AND duracao_planejada_s <= 86400 AND (duracao_registrada_s IS NULL OR duracao_registrada_s >= 0)',name='ck_intervencao_duracoes'),
        sa.CheckConstraint("estado IN ('SOLICITADA','AUTORIZADA','RECUSADA','EM_EXECUCAO','CONCLUIDA','CANCELADA','FALHA_SIMULACAO')",name='ck_intervencao_estado'),
        sa.CheckConstraint('(finalizada_em IS NULL AND finalizada_por_id IS NULL AND motivo_fim IS NULL) OR (finalizada_em IS NOT NULL AND finalizada_por_id IS NOT NULL AND motivo_fim IS NOT NULL)',name='ck_intervencao_finalizacao'),
        sa.CheckConstraint('(decidida_em IS NULL OR decidida_em >= solicitada_em) AND (iniciada_em IS NULL OR iniciada_em >= decidida_em) AND (prazo_planejado_em IS NULL OR prazo_planejado_em > iniciada_em) AND (finalizada_em IS NULL OR finalizada_em >= solicitada_em) AND (iniciada_em IS NULL OR finalizada_em IS NULL OR finalizada_em >= iniciada_em)',name='ck_intervencao_horarios'),
        sa.CheckConstraint('(iniciada_em IS NULL AND iniciada_por_id IS NULL AND prazo_planejado_em IS NULL) OR (iniciada_em IS NOT NULL AND iniciada_por_id IS NOT NULL AND prazo_planejado_em IS NOT NULL)',name='ck_intervencao_inicio'),
        sa.CheckConstraint("modalidade = 'SIMULADA'",name='ck_intervencao_virtual'),
        sa.ForeignKeyConstraint(['alerta_id', 'sessao_id'],['alertas_sessao.alerta_id', 'alertas_sessao.sessao_id'],name='fk_intervencao_alerta_sessao'),
        sa.ForeignKeyConstraint(['avaliacao_id', 'sessao_id'],['avaliacoes_preventivas.id', 'avaliacoes_preventivas.sessao_id'],name='fk_intervencao_avaliacao_sessao'),
        sa.ForeignKeyConstraint(['carga_id', 'viagem_id'],['cargas.id', 'cargas.viagem_id'],name='fk_intervencao_carga_viagem'),
        sa.UniqueConstraint('id','sessao_id',name='uq_intervencao_id_sessao'),
        sa.UniqueConstraint('sessao_id','chave_idempotencia',name='uq_intervencao_sessao_chave'),
    )
    op.create_index('ix_intervencao_sessao_solicitada','intervencoes_simuladas',['sessao_id', 'solicitada_em', 'id'])
    op.create_index('uq_exaustor_virtual_executando','intervencoes_simuladas',['veiculo_id'],unique=True,postgresql_where=sa.text("estado = 'EM_EXECUCAO'"),sqlite_where=sa.text("estado = 'EM_EXECUCAO'"))
    op.create_table('acoes_intervencao',
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('intervencao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('ocorrencia_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('usuario_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('chave_idempotencia',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('assinatura',sa.String(64),nullable=False),
        sa.Column('numero',sa.Integer(),nullable=False),
        sa.Column('acao',sa.String(30),nullable=False),
        sa.Column('estado_anterior',sa.String(30),nullable=True),
        sa.Column('estado_posterior',sa.String(30),nullable=False),
        sa.Column('registrada_em',sa.DateTime(timezone=True),nullable=False),
        sa.Column('contexto_snapshot',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.Column('id',postgresql.UUID(as_uuid=True),nullable=False,primary_key=True),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['usuario_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id'],name=None),
        sa.ForeignKeyConstraint(['ocorrencia_id'],['ocorrencias.id'],name=None),
        sa.CheckConstraint("acao IN ('SOLICITAR','AUTORIZAR','RECUSAR','INICIAR','ENCERRAR','CANCELAR','REGISTRAR_FALHA')",name='ck_acao_intervencao_acao'),
        sa.CheckConstraint('numero > 0',name='ck_acao_intervencao_numero'),
        sa.ForeignKeyConstraint(['intervencao_id', 'sessao_id'],['intervencoes_simuladas.id', 'intervencoes_simuladas.sessao_id'],name='fk_acao_intervencao_sessao'),
        sa.UniqueConstraint('intervencao_id','chave_idempotencia',name='uq_acao_intervencao_chave'),
        sa.UniqueConstraint('intervencao_id','numero',name='uq_acao_intervencao_numero'),
        sa.UniqueConstraint('ocorrencia_id',name='uq_acao_intervencao_ocorrencia'),
    )
    op.create_index('ix_acao_intervencao_historico','acoes_intervencao',['intervencao_id', 'numero'])

def downgrade():
    op.drop_index('ix_acao_intervencao_historico',table_name='acoes_intervencao')
    op.drop_table('acoes_intervencao')
    op.drop_index('ix_intervencao_sessao_solicitada',table_name='intervencoes_simuladas')
    op.drop_index('uq_exaustor_virtual_executando',table_name='intervencoes_simuladas')
    op.drop_table('intervencoes_simuladas')
