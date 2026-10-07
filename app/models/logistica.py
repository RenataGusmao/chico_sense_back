from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase
from app.models.enums import StatusCarga, StatusCaixa, StatusViagem

if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.integracoes import DadoExterno
    from app.models.inteligencia import RecomendacaoIA
    from app.models.iot import Dispositivo, Medicao
    from app.models.monitoramento import Alerta, Ocorrencia
    from app.models.produto import Produto


class Veiculo(ModelBase, Base):
    __tablename__ = "veiculos"
    __table_args__ = (UniqueConstraint("empresa_id", "identificador", name="uq_veiculo_empresa_identificador"),)

    empresa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id"),
        nullable=False,
    )
    identificador: Mapped[str] = mapped_column(String(80), nullable=False)
    placa: Mapped[str | None] = mapped_column(String(20), unique=True)
    modelo: Mapped[str | None] = mapped_column(String(120))
    descricao: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)

    empresa: Mapped[Empresa] = relationship(back_populates="veiculos")
    viagens: Mapped[list[Viagem]] = relationship(back_populates="veiculo")
    dispositivos: Mapped[list[Dispositivo]] = relationship(back_populates="veiculo")


class Motorista(ModelBase, Base):
    __tablename__ = "motoristas"

    empresa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id"),
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    documento: Mapped[str | None] = mapped_column(String(40), unique=True)
    telefone: Mapped[str | None] = mapped_column(String(40))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)

    empresa: Mapped[Empresa] = relationship(back_populates="motoristas")
    viagens: Mapped[list[Viagem]] = relationship(back_populates="motorista")


class Viagem(ModelBase, Base):
    __tablename__ = "viagens"

    transportadora_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id"),
        nullable=False,
    )
    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("veiculos.id"),
        nullable=False,
    )
    motorista_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("motoristas.id"),
        nullable=False,
    )
    origem: Mapped[str] = mapped_column(String(255), nullable=False)
    destino: Mapped[str] = mapped_column(String(255), nullable=False)
    saida_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    previsao_chegada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    chegada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    inicio_real: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    observacoes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[StatusViagem] = mapped_column(
        Enum(StatusViagem, name="status_viagem"),
        default=StatusViagem.PLANEJADA,
        nullable=False,
    )

    transportadora: Mapped[Empresa] = relationship(
        back_populates="viagens_transportadora",
        foreign_keys=[transportadora_id],
    )
    veiculo: Mapped[Veiculo] = relationship(back_populates="viagens")
    motorista: Mapped[Motorista] = relationship(back_populates="viagens")
    cargas: Mapped[list[Carga]] = relationship(back_populates="viagem")
    dispositivos: Mapped[list[Dispositivo]] = relationship(back_populates="viagem")
    medicoes: Mapped[list[Medicao]] = relationship(back_populates="viagem")
    alertas: Mapped[list[Alerta]] = relationship(back_populates="viagem")
    ocorrencias: Mapped[list[Ocorrencia]] = relationship(back_populates="viagem")
    recomendacoes_ia: Mapped[list[RecomendacaoIA]] = relationship(back_populates="viagem")
    dados_externos: Mapped[list[DadoExterno]] = relationship(back_populates="viagem")


class Carga(ModelBase, Base):
    __tablename__ = "cargas"
    __table_args__ = (UniqueConstraint("viagem_id", "identificacao", name="uq_carga_viagem_identificacao"),)

    viagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("viagens.id"),
        nullable=False,
    )
    produto_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id"),
        nullable=False,
    )
    produtor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id"),
        nullable=False,
    )
    cliente_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id"),
    )
    identificacao: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    quantidade_caixas: Mapped[int | None] = mapped_column(Integer)
    quantidade: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    unidade: Mapped[str | None] = mapped_column(String(30))
    origem_produto: Mapped[str | None] = mapped_column(String(255))
    observacoes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[StatusCarga] = mapped_column(
        Enum(StatusCarga, name="status_carga"),
        default=StatusCarga.PLANEJADA,
        nullable=False,
    )

    viagem: Mapped[Viagem] = relationship(back_populates="cargas")
    produto: Mapped[Produto] = relationship(back_populates="cargas")
    produtor: Mapped[Empresa] = relationship(
        back_populates="cargas_produtor",
        foreign_keys=[produtor_id],
    )
    cliente: Mapped[Empresa | None] = relationship(
        back_populates="cargas_cliente",
        foreign_keys=[cliente_id],
    )
    caixas: Mapped[list[Caixa]] = relationship(back_populates="carga")
    dispositivos: Mapped[list[Dispositivo]] = relationship(back_populates="carga")
    medicoes: Mapped[list[Medicao]] = relationship(back_populates="carga")
    alertas: Mapped[list[Alerta]] = relationship(back_populates="carga")
    ocorrencias: Mapped[list[Ocorrencia]] = relationship(back_populates="carga")
    recomendacoes_ia: Mapped[list[RecomendacaoIA]] = relationship(back_populates="carga")
    dados_externos: Mapped[list[DadoExterno]] = relationship(back_populates="carga")


class Caixa(ModelBase, Base):
    __tablename__ = "caixas"
    __table_args__ = (UniqueConstraint("carga_id", "identificacao", name="uq_caixa_carga_identificacao"),)

    carga_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cargas.id"),
        nullable=False,
    )
    identificacao: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    codigo_externo: Mapped[str | None] = mapped_column(String(120))
    peso: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    status: Mapped[StatusCaixa] = mapped_column(
        Enum(StatusCaixa, name="status_caixa"),
        default=StatusCaixa.REGISTRADA,
        nullable=False,
    )
    observacoes: Mapped[str | None] = mapped_column(Text)

    carga: Mapped[Carga] = relationship(back_populates="caixas")
    medicoes: Mapped[list[Medicao]] = relationship(back_populates="caixa")
    alertas: Mapped[list[Alerta]] = relationship(back_populates="caixa")
    ocorrencias: Mapped[list[Ocorrencia]] = relationship(back_populates="caixa")
    recomendacoes_ia: Mapped[list[RecomendacaoIA]] = relationship(back_populates="caixa")
    dados_externos: Mapped[list[DadoExterno]] = relationship(back_populates="caixa")
