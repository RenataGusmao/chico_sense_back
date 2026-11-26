import json
import math

from functools import lru_cache

import joblib
import pandas as pd

from app.modules.inteligencia.preparacao_dados import (
    FEATURES,
    PASTA_DADOS,
    identificar_sessoes,
    criar_features,
)


PASTA_MODELOS = PASTA_DADOS / "modelos"
PASTA_RESULTADOS = PASTA_DADOS / "resultados"

ARQUIVO_MODELO = (
    PASTA_MODELOS / "isolation_forest.joblib"
)

ARQUIVO_METADADOS = (
    PASTA_MODELOS / "metadados.json"
)

VERSAO = "1.0.0"

LIMITACAO = (
    "Modelo experimental de deteccao de anomalias. "
    "Nao comprova risco de deterioracao da carga, "
    "presenca de etileno ou necessidade de exaustao."
)


class ModeloIndisponivelError(Exception):
    pass


@lru_cache(maxsize=1)
def carregar_modelo():

    if not ARQUIVO_MODELO.is_file():
        raise ModeloIndisponivelError(
            "Modelo treinado nao encontrado."
        )

    pacote = joblib.load(ARQUIVO_MODELO)

    if pacote["features"] != FEATURES:
        raise ModeloIndisponivelError(
            "Features incompativeis com o modelo."
        )

    return pacote


def obter_status():

    disponivel = ARQUIVO_MODELO.is_file()

    return {
        "disponivel": disponivel,
        "algoritmo": "Isolation Forest",
        "versao": VERSAO,
        "quantidade_features": len(FEATURES),
        "features": FEATURES,
        "modo": "EXPERIMENTAL",
        "limitacao": LIMITACAO,
    }


def obter_metadados():

    if not ARQUIVO_METADADOS.is_file():
        raise ModeloIndisponivelError(
            "Metadados do modelo nao encontrados."
        )

    with open(
        ARQUIVO_METADADOS,
        encoding="utf-8",
    ) as arquivo:

        return json.load(arquivo)


def resposta_sem_analise(status, mensagem):

    return {
        "status": status,
        "anomalia": None,
        "score": None,
        "limite": None,
        "algoritmo": "Isolation Forest",
        "versao": VERSAO,
        "origem": "MEDICOES_FORNECIDAS",
        "fatores_considerados": None,
        "recomendacao": mensagem,
        "limitacao": LIMITACAO,
    }


def analisar_medicoes(medicoes):

    if not medicoes:

        return resposta_sem_analise(
            "DADOS_INSUFICIENTES",
            "Nenhuma medicao fornecida.",
        )

    try:

        dados = pd.DataFrame(medicoes)

        colunas = [
            "data_hora",
            "temperatura",
            "umidade",
        ]

        if not all(
            coluna in dados.columns
            for coluna in colunas
        ):
            raise ValueError("Campos obrigatorios ausentes.")

        dados = dados[colunas].copy()

        dados["data_hora"] = pd.to_datetime(
            dados["data_hora"],
            utc=True,
            errors="coerce",
        )

        for coluna in ["temperatura", "umidade"]:

            dados[coluna] = pd.to_numeric(
                dados[coluna],
                errors="coerce",
            )

        if dados.isna().any().any():
            raise ValueError("Valores ausentes ou invalidos.")

        for coluna in ["temperatura", "umidade"]:

            if not dados[coluna].map(math.isfinite).all():
                raise ValueError("Valores nao finitos.")

        if (dados["temperatura"] < -273.15).any():
            raise ValueError("Temperatura invalida.")

        if not dados["umidade"].between(0, 100).all():
            raise ValueError("Umidade invalida.")

        if dados["data_hora"].duplicated().any():
            raise ValueError("Horarios duplicados.")

    except (ValueError, TypeError, KeyError):

        return resposta_sem_analise(
            "DADOS_INVALIDOS",
            "Verifique os valores e horarios das medicoes.",
        )

    dados = dados.sort_values(
        "data_hora"
    ).reset_index(drop=True)

    dados["entry_id"] = range(1, len(dados) + 1)

    ultima_medicao = dados["entry_id"].iloc[-1]

    dados = identificar_sessoes(dados)

    dados = criar_features(dados)

    ultima = dados[
        dados["entry_id"] == ultima_medicao
    ]

    if ultima.empty:

        return resposta_sem_analise(
            "DADOS_INSUFICIENTES",
            "Sao necessarias pelo menos cinco medicoes "
            "consecutivas, sem interrupcoes superiores "
            "a 60 segundos.",
        )

    pacote = carregar_modelo()

    modelo = pacote["modelo"]

    limite = float(pacote["limite"])

    score = float(
        -modelo.score_samples(
            ultima[FEATURES]
        )[0]
    )

    anomalia = bool(score > limite)

    fatores = {
        feature: round(
            float(ultima.iloc[0][feature]),
            4,
        )
        for feature in FEATURES
    }

    if anomalia:

        status = "ANOMALIA_DETECTADA"

        recomendacao = (
            "Comportamento ambiental estatisticamente "
            "atipico. Verifique as condicoes da carga "
            "e a qualidade das leituras do sensor."
        )

    else:

        status = "NAO_SINALIZADO"

        recomendacao = (
            "Nenhuma anomalia sinalizada pelo modelo. "
            "Mantenha o monitoramento preventivo."
        )

    return {
        "status": status,
        "anomalia": anomalia,
        "score": round(score, 6),
        "limite": round(limite, 6),
        "algoritmo": "Isolation Forest",
        "versao": VERSAO,
        "origem": "MEDICOES_FORNECIDAS",
        "data_hora": ultima.iloc[0][
            "data_hora"
        ].isoformat(),
        "fatores_considerados": fatores,
        "recomendacao": recomendacao,
        "limitacao": LIMITACAO,
    }


def obter_historico():

    arquivo = (
        PASTA_RESULTADOS / "resumo_avaliacao.json"
    )

    if not arquivo.is_file():
        raise ModeloIndisponivelError(
            "Resultados historicos nao encontrados."
        )

    with open(
        arquivo,
        encoding="utf-8",
    ) as leitura:

        resumo = json.load(leitura)

    return {
        "origem": "HISTORICO_THINGSPEAK",
        "monitoramento_tempo_real": False,
        "resultado": resumo,
        "limitacao": LIMITACAO,
    }