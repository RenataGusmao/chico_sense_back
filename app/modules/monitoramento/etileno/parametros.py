"""General mango reference parameters, not a Tommy Atkins calibration."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PontoReferencia:
    temperatura_c: Decimal
    minimo_ul_kg_h: Decimal
    maximo_ul_kg_h: Decimal


VERSAO_MODELO = "chicosense-etileno-1.0.0"
FONTE = "https://postharvest.ucdavis.edu/produce-facts-sheets/mango"
REFERENCIA = "Kader, A. A. Mango. UC Davis PREC. Atualizacao: fevereiro de 1997."
DATA_CONSULTA = "2026-10-23"
TAXAS = tuple(
    PontoReferencia(Decimal(t), Decimal(lo), Decimal(hi))
    for t, lo, hi in (
        ("10", "0.1", "0.5"), ("13", "0.2", "1.0"),
        ("15", "0.3", "4.0"), ("20", "0.5", "8.0"),
    )
)
LIMITACOES_GERAIS = (
    "Referencias gerais de manga, sem validacao especifica para Tommy Atkins.",
    "Extremos nao sao limites fisicos garantidos nem intervalo de confianca.",
    "Temperatura do ar pode diferir da polpa; representatividade depende do sensor.",
    "Retencao da temperatura inicial nao revela variacoes entre amostras.",
    "Massa constante; maturacao, atmosfera e tratamentos nao sao modelados.",
    "Volume potencial nao e concentracao, dano, vida util ou remocao por exaustao.",
)
