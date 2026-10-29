"""Human-supervised virtual exhaust only; no device command or scientific effect."""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Integer, JSON, Numeric, String, Text, UniqueConstraint, CheckConstraint, Index, text
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
from app.models.base import ModelBase


class IntervencaoSimulada(ModelBase,Base):
    __tablename__='intervencoes_simuladas'
    __table_args__=(
        UniqueConstraint('sessao_id','chave_idempotencia',name='uq_intervencao_sessao_chave'),
        UniqueConstraint('id','sessao_id',name='uq_intervencao_id_sessao'),
        ForeignKeyConstraint(['alerta_id','sessao_id'],['alertas_sessao.alerta_id','alertas_sessao.sessao_id'],name='fk_intervencao_alerta_sessao'),
        ForeignKeyConstraint(['avaliacao_id','sessao_id'],['avaliacoes_preventivas.id','avaliacoes_preventivas.sessao_id'],name='fk_intervencao_avaliacao_sessao'),
        ForeignKeyConstraint(['carga_id','viagem_id'],['cargas.id','cargas.viagem_id'],name='fk_intervencao_carga_viagem'),
        CheckConstraint("modalidade = 'SIMULADA'",name='ck_intervencao_virtual'),
        CheckConstraint("estado IN ('SOLICITADA','AUTORIZADA','RECUSADA','EM_EXECUCAO','CONCLUIDA','CANCELADA','FALHA_SIMULACAO')",name='ck_intervencao_estado'),
        CheckConstraint('duracao_planejada_s > 0 AND duracao_planejada_s <= 86400 AND (duracao_registrada_s IS NULL OR duracao_registrada_s >= 0)',name='ck_intervencao_duracoes'),
        CheckConstraint("((estado IN ('SOLICITADA','AUTORIZADA','RECUSADA')) AND iniciada_em IS NULL AND finalizada_em IS NULL AND duracao_registrada_s IS NULL) OR (estado = 'EM_EXECUCAO' AND iniciada_em IS NOT NULL AND finalizada_em IS NULL AND duracao_registrada_s IS NULL) OR (estado IN ('CONCLUIDA','FALHA_SIMULACAO') AND iniciada_em IS NOT NULL AND finalizada_em IS NOT NULL AND duracao_registrada_s IS NOT NULL) OR (estado = 'CANCELADA' AND finalizada_em IS NOT NULL AND ((iniciada_em IS NULL AND duracao_registrada_s IS NULL) OR (iniciada_em IS NOT NULL AND duracao_registrada_s IS NOT NULL)))",name='ck_intervencao_ciclo'),
        CheckConstraint("(estado = 'SOLICITADA' AND decidida_em IS NULL AND decidida_por_id IS NULL) OR (estado IN ('AUTORIZADA','RECUSADA','EM_EXECUCAO','CONCLUIDA','FALHA_SIMULACAO') AND decidida_em IS NOT NULL AND decidida_por_id IS NOT NULL) OR estado = 'CANCELADA'",name='ck_intervencao_decisao'),
        CheckConstraint('(iniciada_em IS NULL AND iniciada_por_id IS NULL AND prazo_planejado_em IS NULL) OR (iniciada_em IS NOT NULL AND iniciada_por_id IS NOT NULL AND prazo_planejado_em IS NOT NULL)',name='ck_intervencao_inicio'),
        CheckConstraint('(finalizada_em IS NULL AND finalizada_por_id IS NULL AND motivo_fim IS NULL) OR (finalizada_em IS NOT NULL AND finalizada_por_id IS NOT NULL AND motivo_fim IS NOT NULL)',name='ck_intervencao_finalizacao'),
        CheckConstraint('(decidida_em IS NULL OR decidida_em >= solicitada_em) AND (iniciada_em IS NULL OR iniciada_em >= decidida_em) AND (prazo_planejado_em IS NULL OR prazo_planejado_em > iniciada_em) AND (finalizada_em IS NULL OR finalizada_em >= solicitada_em) AND (iniciada_em IS NULL OR finalizada_em IS NULL OR finalizada_em >= iniciada_em)',name='ck_intervencao_horarios'),
        Index('uq_exaustor_virtual_executando','veiculo_id',unique=True,postgresql_where=text("estado = 'EM_EXECUCAO'"),sqlite_where=text("estado = 'EM_EXECUCAO'")),
        Index('ix_intervencao_sessao_solicitada','sessao_id','solicitada_em','id'),
    )
    sessao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('sessoes_monitoramento.id'),nullable=False)
    viagem_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('viagens.id'),nullable=False)
    carga_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    veiculo_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('veiculos.id'),nullable=False)
    alerta_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True))
    avaliacao_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True))
    analise_etileno_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),ForeignKey('analises_etileno.id'))
    solicitante_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'),nullable=False)
    decidida_por_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'))
    iniciada_por_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'))
    finalizada_por_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'))
    modalidade:Mapped[str]=mapped_column(String(20),nullable=False)
    estado:Mapped[str]=mapped_column(String(30),nullable=False)
    chave_idempotencia:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    assinatura:Mapped[str]=mapped_column(String(64),nullable=False)
    justificativa_solicitacao:Mapped[str]=mapped_column(Text,nullable=False)
    motivo_fim:Mapped[str|None]=mapped_column(Text)
    solicitada_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    decidida_em:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    iniciada_em:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    prazo_planejado_em:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    finalizada_em:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    duracao_planejada_s:Mapped[Decimal]=mapped_column(Numeric(12,3),nullable=False)
    duracao_registrada_s:Mapped[Decimal|None]=mapped_column(Numeric(20,6))
    referencias_snapshot:Mapped[dict]=mapped_column(JSON().with_variant(JSONB(),'postgresql'),nullable=False)
    hash_referencias:Mapped[str]=mapped_column(String(64),nullable=False)


class AcaoIntervencao(ModelBase,Base):
    __tablename__='acoes_intervencao'
    __table_args__=(
        UniqueConstraint('intervencao_id','chave_idempotencia',name='uq_acao_intervencao_chave'),
        UniqueConstraint('intervencao_id','numero',name='uq_acao_intervencao_numero'),
        UniqueConstraint('ocorrencia_id',name='uq_acao_intervencao_ocorrencia'),
        ForeignKeyConstraint(['intervencao_id','sessao_id'],['intervencoes_simuladas.id','intervencoes_simuladas.sessao_id'],name='fk_acao_intervencao_sessao'),
        CheckConstraint('numero > 0',name='ck_acao_intervencao_numero'),
        CheckConstraint("acao IN ('SOLICITAR','AUTORIZAR','RECUSAR','INICIAR','ENCERRAR','CANCELAR','REGISTRAR_FALHA')",name='ck_acao_intervencao_acao'),
        Index('ix_acao_intervencao_historico','intervencao_id','numero'),
    )
    sessao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('sessoes_monitoramento.id'),nullable=False)
    intervencao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    ocorrencia_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('ocorrencias.id'),nullable=False)
    usuario_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'),nullable=False)
    chave_idempotencia:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    assinatura:Mapped[str]=mapped_column(String(64),nullable=False)
    numero:Mapped[int]=mapped_column(Integer,nullable=False)
    acao:Mapped[str]=mapped_column(String(30),nullable=False)
    estado_anterior:Mapped[str|None]=mapped_column(String(30))
    estado_posterior:Mapped[str]=mapped_column(String(30),nullable=False)
    registrada_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    contexto_snapshot:Mapped[dict]=mapped_column(JSON().with_variant(JSONB(),'postgresql'),nullable=False)
