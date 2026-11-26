from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class MedicaoIA(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        allow_inf_nan=False,
    )

    data_hora: datetime

    temperatura: float = Field(
        description="Temperatura em graus Celsius"
    )

    umidade: float = Field(
        description="Umidade relativa em percentual"
    )


class AnaliseIARequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    medicoes: list[MedicaoIA] = Field(
        max_length=1000,
        description=(
            "Sequencia de medicoes ambientais "
            "para analise de anomalias"
        ),
    )


class AnaliseIAResponse(BaseModel):

    status: Literal[
        "ANOMALIA_DETECTADA",
        "NAO_SINALIZADO",
        "DADOS_INSUFICIENTES",
        "DADOS_INVALIDOS",
    ]

    anomalia: bool | None

    score: float | None

    limite: float | None

    algoritmo: str

    versao: str

    origem: str

    data_hora: datetime | None = None

    fatores_considerados: dict[str, float] | None

    recomendacao: str

    limitacao: str


class StatusIAResponse(BaseModel):

    disponivel: bool

    algoritmo: str

    versao: str

    quantidade_features: int

    features: list[str]

    modo: str

    limitacao: str


class HistoricoIAResponse(BaseModel):

    origem: str

    monitoramento_tempo_real: bool

    resultado: dict[str, Any]

    limitacao: str