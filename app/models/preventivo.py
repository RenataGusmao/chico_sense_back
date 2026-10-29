"""Session links and immutable evidence around the existing Alerta/Ocorrencia models."""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Integer, JSON, String, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
from app.models.base import ModelBase


class ConfiguracaoAmbiental(ModelBase,Base):
    __tablename__='configuracoes_ambientais'
    __table_args__=(UniqueConstraint('sessao_id','versao',name='uq_config_ambiental_versao'),
        UniqueConstraint('sessao_id','chave_idempotencia',name='uq_config_ambiental_chave'),
        UniqueConstraint('id','sessao_id',name='uq_config_ambiental_id_sessao'),
        CheckConstraint('versao > 0',name='ck_config_ambiental_versao'))
    sessao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('sessoes_monitoramento.id'),nullable=False)
    usuario_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'),nullable=False)
    chave_idempotencia:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    assinatura:Mapped[str]=mapped_column(String(64),nullable=False)
    versao:Mapped[int]=mapped_column(Integer,nullable=False)
    registrada_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    parametros:Mapped[dict]=mapped_column(JSON().with_variant(JSONB(),'postgresql'),nullable=False)


class AvaliacaoPreventiva(ModelBase,Base):
    __tablename__='avaliacoes_preventivas'
    __table_args__=(UniqueConstraint('sessao_id','chave_idempotencia',name='uq_avaliacao_preventiva_chave'),
        UniqueConstraint('id','sessao_id',name='uq_avaliacao_preventiva_id_sessao'),
        ForeignKeyConstraint(['configuracao_id','sessao_id'],['configuracoes_ambientais.id','configuracoes_ambientais.sessao_id'],name='fk_avaliacao_config_sessao'),
        ForeignKeyConstraint(['anterior_id','sessao_id'],['avaliacoes_preventivas.id','avaliacoes_preventivas.sessao_id'],name='fk_avaliacao_anterior_sessao'),
        CheckConstraint('fim > inicio AND corte_aquisicao >= fim AND executada_em >= corte_aquisicao AND revisao >= 0',name='ck_avaliacao_preventiva_janela'),
        Index('ix_avaliacao_preventiva_sessao','sessao_id','executada_em','id'))
    sessao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('sessoes_monitoramento.id'),nullable=False)
    usuario_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'),nullable=False)
    configuracao_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True))
    anterior_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True))
    analise_etileno_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),ForeignKey('analises_etileno.id'))
    chave_idempotencia:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    assinatura:Mapped[str]=mapped_column(String(64),nullable=False)
    executada_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    inicio:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    fim:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    corte_aquisicao:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    revisao:Mapped[int]=mapped_column(Integer,nullable=False)
    hash_entrada:Mapped[str]=mapped_column(String(64),nullable=False)
    hash_resultado:Mapped[str]=mapped_column(String(64),nullable=False)
    entrada_snapshot:Mapped[dict]=mapped_column(JSON().with_variant(JSONB(),'postgresql'),nullable=False)
    resultado:Mapped[dict]=mapped_column(JSON().with_variant(JSONB(),'postgresql'),nullable=False)


class AlertaSessao(ModelBase,Base):
    __tablename__='alertas_sessao'
    __table_args__=(UniqueConstraint('alerta_id',name='uq_alerta_sessao_alerta'),
        UniqueConstraint('sessao_id','identidade',name='uq_alerta_sessao_identidade'),
        UniqueConstraint('alerta_id','sessao_id',name='uq_alerta_sessao_id_sessao'))
    alerta_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('alertas.id'),nullable=False)
    sessao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('sessoes_monitoramento.id'),nullable=False)
    identidade:Mapped[str]=mapped_column(String(64),nullable=False)
    regra:Mapped[str]=mapped_column(String(120),nullable=False)


class EvidenciaPreventiva(ModelBase,Base):
    __tablename__='evidencias_preventivas'
    __table_args__=(UniqueConstraint('avaliacao_id','alerta_id',name='uq_evidencia_preventiva_avaliacao_alerta'),
        Index('ix_evidencia_preventiva_identidade','sessao_id','identidade'),
        ForeignKeyConstraint(['avaliacao_id','sessao_id'],['avaliacoes_preventivas.id','avaliacoes_preventivas.sessao_id'],name='fk_evidencia_avaliacao_sessao'),
        ForeignKeyConstraint(['alerta_id','sessao_id'],['alertas_sessao.alerta_id','alertas_sessao.sessao_id'],name='fk_evidencia_alerta_sessao'))
    sessao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('sessoes_monitoramento.id'),nullable=False)
    avaliacao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    alerta_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    identidade:Mapped[str]=mapped_column(String(64),nullable=False)
    evidencia:Mapped[dict]=mapped_column(JSON().with_variant(JSONB(),'postgresql'),nullable=False)


class DecisaoAlerta(ModelBase,Base):
    __tablename__='decisoes_alerta'
    __table_args__=(UniqueConstraint('alerta_id','chave_idempotencia',name='uq_decisao_alerta_chave'),
        UniqueConstraint('ocorrencia_id',name='uq_decisao_alerta_ocorrencia'),
        ForeignKeyConstraint(['alerta_id','sessao_id'],['alertas_sessao.alerta_id','alertas_sessao.sessao_id'],name='fk_decisao_alerta_sessao'),
        CheckConstraint("acao IN ('CRIAR','RECONHECER','OBSERVAR','RESOLVER','DESCARTAR')",name='ck_decisao_alerta_acao'),
        Index('ix_decisao_alerta_historico','alerta_id','registrada_em','id'))
    sessao_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('sessoes_monitoramento.id'),nullable=False)
    alerta_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    ocorrencia_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('ocorrencias.id'),nullable=False)
    usuario_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('usuarios.id'),nullable=False)
    chave_idempotencia:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),nullable=False)
    assinatura:Mapped[str]=mapped_column(String(64),nullable=False)
    acao:Mapped[str]=mapped_column(String(30),nullable=False)
    estado_anterior:Mapped[str|None]=mapped_column(String(30))
    estado_posterior:Mapped[str]=mapped_column(String(30),nullable=False)
    registrada_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
