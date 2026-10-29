"""Independent, deterministic ethylene reference engine (no integration side effects)."""
from .motor import converter_massa, converter_temperatura, estimar_etileno
from .tipos import (
    EntradaEstimativa, EstagioMaturacao, IntervaloEstimativa, LeituraTemperatura,
    ModoCalculo, Motivo, ObservacaoNormalizada, ResultadoEstimativa, StatusCalculo,
)

__all__ = [
    "EntradaEstimativa", "EstagioMaturacao", "IntervaloEstimativa", "LeituraTemperatura",
    "ModoCalculo", "Motivo", "ObservacaoNormalizada", "ResultadoEstimativa", "StatusCalculo",
    "converter_massa", "converter_temperatura", "estimar_etileno",
]
