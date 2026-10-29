"""Authenticated analysis contracts. Decimal values are serialized as JSON strings."""
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator
from app.schemas.operacional import Input, Response
from app.modules.monitoramento.service import utc
from app.modules.monitoramento.etileno import ModoCalculo, StatusCalculo


class AnaliseCreate(Input):
    chave_idempotencia: UUID
    modo: ModoCalculo = ModoCalculo.MODO_RESTRITO
    intervalo_maximo_s: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=3,
        description='G operacional explicito. Ausencia persiste CONFIGURACAO_INCOMPLETA, sem volumes.')
    inicio: AwareDatetime | None = None
    fim: AwareDatetime | None = None
    corte_aquisicao: AwareDatetime | None = Field(default=None,
        description='Obrigatorio para sessao ativa; inclui apenas revisoes consolidadas ate este instante. Nunca futuro.')
    revisao_aquisicao: int | None = Field(default=None, ge=0,
        description='Revisao consolidada; 0 representa ausencia de aquisicao. Omissao fixa a ultima elegivel no corte.')


class IntervaloResponse(Input):
    inicio: datetime
    fim: datetime
    duracao_s: Decimal
    temperatura_inicio_c: Decimal | None
    taxa_min_ul_kg_h: Decimal | None
    taxa_max_ul_kg_h: Decimal | None
    volume_min_ul: Decimal | None
    volume_max_ul: Decimal | None
    motivos: list[str]


class ResultadoResponse(BaseModel):
    model_config=ConfigDict(extra='allow')
    status_calculo: StatusCalculo
    volume_coberto_min_ul: Decimal | None
    volume_coberto_max_ul: Decimal | None
    volume_janela_min_ul: Decimal | None
    volume_janela_max_ul: Decimal | None
    duracao_coberta_s: Decimal | None
    duracao_nao_coberta_s: Decimal | None
    percentual_cobertura: Decimal | None
    unidade_volume: str
    motivos: list[str]
    limitacoes: list[str]
    classificacao_risco_etileno: Literal['NAO_AVALIADO']
    motivo_risco: Literal['SEM_LIMIAR_VALIDADO']
    versao_modelo: str
    intervalos: list[IntervaloResponse]
    massa_kg: Decimal | None
    inicio: datetime | None
    fim: datetime | None
    modo: ModoCalculo | None
    maturacao: str | None
    intervalo_maximo_s: Decimal | None
    corte_aquisicao: datetime | None
    sensor_id: str
    sessao_id: str
    tabela_referencia: list[dict]
    cobertura: Decimal | None
    duracao_janela_s: Decimal | None
    duplicatas_descartadas: int
    interpolacao_utilizada: bool
    perfil: str | None
    metodologia: str
    fonte: str
    referencia: str
    data_consulta: str
    aplicabilidade: str


class AnaliseResponse(Response):
    sessao_id: UUID
    usuario_id: UUID
    chave_idempotencia: UUID
    executada_em: datetime
    inicio: datetime
    fim: datetime
    corte_aquisicao: datetime
    revisao_aquisicao: int
    massa_kg: Decimal | None
    maturacao: str
    modo: ModoCalculo
    intervalo_maximo_s: Decimal | None
    versao_modelo: str
    status_calculo: StatusCalculo
    classificacao_risco_etileno: Literal['NAO_AVALIADO']
    hash_entrada: str
    hash_resultado: str
    entrada_snapshot: dict
    resultado: ResultadoResponse

    @field_validator("executada_em", "inicio", "fim", "corte_aquisicao", "created_at", "updated_at")
    @classmethod
    def horarios_utc(cls, value):
        return utc(value)


class AnaliseLista(Input):
    sessao_id: UUID
    total: int
    limit: int
    offset: int
    analises: list[AnaliseResponse]
