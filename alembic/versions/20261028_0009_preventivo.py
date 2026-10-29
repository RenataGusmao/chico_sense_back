"""Versioned operational evaluation and links to existing alerts/occurrences."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261028_0009_preventivo'
down_revision='20261028_0008_analises_etileno'
branch_labels=None
depends_on=None

def upgrade():
    op.create_table('configuracoes_ambientais',
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('usuario_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('chave_idempotencia',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('assinatura',sa.String(64),nullable=False),
        sa.Column('versao',sa.Integer(),nullable=False),
        sa.Column('registrada_em',sa.DateTime(timezone=True),nullable=False),
        sa.Column('parametros',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.Column('id',postgresql.UUID(as_uuid=True),nullable=False,primary_key=True),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['usuario_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id'],name=None),
        sa.CheckConstraint('versao > 0',name='ck_config_ambiental_versao'),
        sa.UniqueConstraint('sessao_id','chave_idempotencia',name='uq_config_ambiental_chave'),
        sa.UniqueConstraint('id','sessao_id',name='uq_config_ambiental_id_sessao'),
        sa.UniqueConstraint('sessao_id','versao',name='uq_config_ambiental_versao'),
    )
    op.create_table('avaliacoes_preventivas',
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('usuario_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('configuracao_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('anterior_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('analise_etileno_id',postgresql.UUID(as_uuid=True),nullable=True),
        sa.Column('chave_idempotencia',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('assinatura',sa.String(64),nullable=False),
        sa.Column('executada_em',sa.DateTime(timezone=True),nullable=False),
        sa.Column('inicio',sa.DateTime(timezone=True),nullable=False),
        sa.Column('fim',sa.DateTime(timezone=True),nullable=False),
        sa.Column('corte_aquisicao',sa.DateTime(timezone=True),nullable=False),
        sa.Column('revisao',sa.Integer(),nullable=False),
        sa.Column('hash_entrada',sa.String(64),nullable=False),
        sa.Column('hash_resultado',sa.String(64),nullable=False),
        sa.Column('entrada_snapshot',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.Column('resultado',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.Column('id',postgresql.UUID(as_uuid=True),nullable=False,primary_key=True),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['analise_etileno_id'],['analises_etileno.id'],name=None),
        sa.ForeignKeyConstraint(['usuario_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id'],name=None),
        sa.CheckConstraint('fim > inicio AND corte_aquisicao >= fim AND executada_em >= corte_aquisicao AND revisao >= 0',name='ck_avaliacao_preventiva_janela'),
        sa.ForeignKeyConstraint(['anterior_id', 'sessao_id'],['avaliacoes_preventivas.id', 'avaliacoes_preventivas.sessao_id'],name='fk_avaliacao_anterior_sessao'),
        sa.ForeignKeyConstraint(['configuracao_id', 'sessao_id'],['configuracoes_ambientais.id', 'configuracoes_ambientais.sessao_id'],name='fk_avaliacao_config_sessao'),
        sa.UniqueConstraint('sessao_id','chave_idempotencia',name='uq_avaliacao_preventiva_chave'),
        sa.UniqueConstraint('id','sessao_id',name='uq_avaliacao_preventiva_id_sessao'),
    )
    op.create_index('ix_avaliacao_preventiva_sessao','avaliacoes_preventivas',['sessao_id', 'executada_em', 'id'])
    op.create_table('alertas_sessao',
        sa.Column('alerta_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('identidade',sa.String(64),nullable=False),
        sa.Column('regra',sa.String(120),nullable=False),
        sa.Column('id',postgresql.UUID(as_uuid=True),nullable=False,primary_key=True),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['alerta_id'],['alertas.id'],name=None),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id'],name=None),
        sa.UniqueConstraint('alerta_id',name='uq_alerta_sessao_alerta'),
        sa.UniqueConstraint('alerta_id','sessao_id',name='uq_alerta_sessao_id_sessao'),
        sa.UniqueConstraint('sessao_id','identidade',name='uq_alerta_sessao_identidade'),
    )
    op.create_table('evidencias_preventivas',
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('avaliacao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('alerta_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('identidade',sa.String(64),nullable=False),
        sa.Column('evidencia',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.Column('id',postgresql.UUID(as_uuid=True),nullable=False,primary_key=True),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id'],name=None),
        sa.ForeignKeyConstraint(['alerta_id', 'sessao_id'],['alertas_sessao.alerta_id', 'alertas_sessao.sessao_id'],name='fk_evidencia_alerta_sessao'),
        sa.ForeignKeyConstraint(['avaliacao_id', 'sessao_id'],['avaliacoes_preventivas.id', 'avaliacoes_preventivas.sessao_id'],name='fk_evidencia_avaliacao_sessao'),
        sa.UniqueConstraint('avaliacao_id','alerta_id',name='uq_evidencia_preventiva_avaliacao_alerta'),
    )
    op.create_index('ix_evidencia_preventiva_identidade','evidencias_preventivas',['sessao_id','identidade'])
    op.create_table('decisoes_alerta',
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('alerta_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('ocorrencia_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('usuario_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('chave_idempotencia',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('assinatura',sa.String(64),nullable=False),
        sa.Column('acao',sa.String(30),nullable=False),
        sa.Column('estado_anterior',sa.String(30),nullable=True),
        sa.Column('estado_posterior',sa.String(30),nullable=False),
        sa.Column('registrada_em',sa.DateTime(timezone=True),nullable=False),
        sa.Column('id',postgresql.UUID(as_uuid=True),nullable=False,primary_key=True),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['ocorrencia_id'],['ocorrencias.id'],name=None),
        sa.ForeignKeyConstraint(['usuario_id'],['usuarios.id'],name=None),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id'],name=None),
        sa.CheckConstraint("acao IN ('CRIAR','RECONHECER','OBSERVAR','RESOLVER','DESCARTAR')",name='ck_decisao_alerta_acao'),
        sa.ForeignKeyConstraint(['alerta_id', 'sessao_id'],['alertas_sessao.alerta_id', 'alertas_sessao.sessao_id'],name='fk_decisao_alerta_sessao'),
        sa.UniqueConstraint('alerta_id','chave_idempotencia',name='uq_decisao_alerta_chave'),
        sa.UniqueConstraint('ocorrencia_id',name='uq_decisao_alerta_ocorrencia'),
    )
    op.create_index('ix_decisao_alerta_historico','decisoes_alerta',['alerta_id', 'registrada_em', 'id'])

def downgrade():
    op.drop_index('ix_decisao_alerta_historico',table_name='decisoes_alerta')
    op.drop_table('decisoes_alerta')
    op.drop_index('ix_evidencia_preventiva_identidade',table_name='evidencias_preventivas')
    op.drop_table('evidencias_preventivas')
    op.drop_table('alertas_sessao')
    op.drop_index('ix_avaliacao_preventiva_sessao',table_name='avaliacoes_preventivas')
    op.drop_table('avaliacoes_preventivas')
    op.drop_table('configuracoes_ambientais')
