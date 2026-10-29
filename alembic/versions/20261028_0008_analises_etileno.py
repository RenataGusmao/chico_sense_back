"""Immutable session ethylene analyses; no legacy data rewrite or backfill."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision='20261028_0008_analises_etileno'
down_revision='20261028_0007_historico_iot'
branch_labels=None
depends_on=None


def upgrade():
    op.create_table('analises_etileno',
        sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True,nullable=False),
        sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.Column('sessao_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('usuario_id',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('chave_idempotencia',postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('assinatura_requisicao',sa.String(64),nullable=False),
        sa.Column('executada_em',sa.DateTime(timezone=True),nullable=False),
        sa.Column('inicio',sa.DateTime(timezone=True),nullable=False),
        sa.Column('fim',sa.DateTime(timezone=True),nullable=False),
        sa.Column('corte_aquisicao',sa.DateTime(timezone=True),nullable=False),
        sa.Column('revisao_aquisicao',sa.Integer(),nullable=False),
        sa.Column('massa_kg',sa.Numeric(12,4),nullable=True),
        sa.Column('maturacao',sa.String(30),nullable=False),
        sa.Column('modo',sa.String(30),nullable=False),
        sa.Column('intervalo_maximo_s',sa.Numeric(12,3),nullable=True),
        sa.Column('versao_modelo',sa.String(80),nullable=False),
        sa.Column('status_calculo',sa.String(40),nullable=False),
        sa.Column('classificacao_risco_etileno',sa.String(20),nullable=False),
        sa.Column('hash_entrada',sa.String(64),nullable=False),
        sa.Column('hash_resultado',sa.String(64),nullable=False),
        sa.Column('entrada_snapshot',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.Column('resultado',sa.JSON().with_variant(postgresql.JSONB(),'postgresql'),nullable=False),
        sa.ForeignKeyConstraint(['sessao_id'],['sessoes_monitoramento.id']),
        sa.ForeignKeyConstraint(['usuario_id'],['usuarios.id']),
        sa.UniqueConstraint('sessao_id','chave_idempotencia',name='uq_analise_sessao_chave'),
        sa.CheckConstraint('fim > inicio AND corte_aquisicao >= fim AND executada_em >= corte_aquisicao',name='ck_analise_janela'),
        sa.CheckConstraint('revisao_aquisicao >= 0',name='ck_analise_revisao'),
        sa.CheckConstraint("classificacao_risco_etileno = 'NAO_AVALIADO'",name='ck_analise_risco'),
        sa.CheckConstraint("status_calculo IN ('ENTRADA_INVALIDA','CONFIGURACAO_INCOMPLETA','SEM_ESTIMATIVA','PARCIAL','COMPLETO_NO_MODELO')",name='ck_analise_status'),
    )
    op.create_index('ix_analise_sessao_execucao','analises_etileno',['sessao_id','executada_em','id'])


def downgrade():
    op.drop_index('ix_analise_sessao_execucao',table_name='analises_etileno')
    op.drop_table('analises_etileno')
