import json

import joblib
import pandas as pd

from preparacao_dados import FEATURES, PASTA_DADOS


PASTA_MODELOS = PASTA_DADOS / "modelos"

PASTA_RESULTADOS = PASTA_DADOS / "resultados"

ARQUIVO_MODELO = (
    PASTA_MODELOS / "isolation_forest.joblib"
)


def carregar_modelo():
    """Carrega o modelo treinado localmente."""

    pacote = joblib.load(ARQUIVO_MODELO)

    return (
        pacote["modelo"],
        pacote["limite"],
        pacote["features"],
    )


def avaliar_historico():
    """Avalia os dados historicos reservados."""

    modelo, limite, features = carregar_modelo()

    if features != FEATURES:
        raise ValueError(
            "Features incompativeis com o modelo."
        )

    dados = pd.read_csv(
        PASTA_DADOS / "avaliacao.csv"
    )

    dados["score_anomalia"] = (
        -modelo.score_samples(dados[features])
    )

    dados["anomalia"] = (
        dados["score_anomalia"] > limite
    )

    dados["classificacao"] = dados[
        "anomalia"
    ].map(
        {
            True: "ANOMALIA_DETECTADA",
            False: "NAO_SINALIZADO",
        }
    )

    return dados, limite


def gerar_resultados(dados, limite):
    """Gera os indicadores da avaliacao."""

    total = len(dados)

    sinalizados = dados[
        dados["anomalia"]
    ].copy()

    quantidade_anomalias = len(sinalizados)

    quantidade_nao_sinalizados = (
        total - quantidade_anomalias
    )

    percentual_anomalias = (
        quantidade_anomalias / total * 100
    )

    resumo = {
        "algoritmo": "Isolation Forest",
        "versao_modelo": "1.0.0",
        "origem_dados": "Historico real ThingSpeak",
        "sessao_avaliada": 12,
        "total_avaliado": total,
        "registros_sinalizados": quantidade_anomalias,
        "registros_nao_sinalizados": quantidade_nao_sinalizados,
        "percentual_sinalizado": round(
            percentual_anomalias, 4
        ),
        "limite_anomalia": float(limite),
        "score_minimo": float(
            dados["score_anomalia"].min()
        ),
        "score_maximo": float(
            dados["score_anomalia"].max()
        ),
        "score_medio": float(
            dados["score_anomalia"].mean()
        ),
        "limitacao": (
            "Dados historicos sem rotulos de anomalias. "
            "Os resultados representam comportamentos "
            "estatisticamente atipicos, nao comprovacao "
            "de risco ou dano a carga."
        ),
    }

    PASTA_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    dados.to_csv(
        PASTA_RESULTADOS / "avaliacao_completa.csv",
        index=False,
    )

    sinalizados = sinalizados.sort_values(
        "score_anomalia",
        ascending=False,
    )

    sinalizados.to_csv(
        PASTA_RESULTADOS / "anomalias_detectadas.csv",
        index=False,
    )

    with open(
        PASTA_RESULTADOS / "resumo_avaliacao.json",
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            resumo,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )

    return resumo, sinalizados


def executar_avaliacao():
    """Executa e apresenta a avaliacao historica."""

    print("=" * 60)
    print("CHICO SENSE - AVALIACAO DA IA")
    print("=" * 60)

    dados, limite = avaliar_historico()

    resumo, sinalizados = gerar_resultados(
        dados,
        limite,
    )

    print("\nRESULTADOS DA AVALIACAO")

    print(
        "Total avaliado:",
        resumo["total_avaliado"],
    )

    print(
        "Limite de anomalia:",
        round(limite, 6),
    )

    print(
        "Registros sinalizados:",
        resumo["registros_sinalizados"],
    )

    print(
        "Registros nao sinalizados:",
        resumo["registros_nao_sinalizados"],
    )

    print(
        "Percentual sinalizado:",
        resumo["percentual_sinalizado"],
        "%",
    )

    print("\nESTATISTICAS DOS SCORES")

    print(
        "Score minimo:",
        round(resumo["score_minimo"], 6),
    )

    print(
        "Score maximo:",
        round(resumo["score_maximo"], 6),
    )

    print(
        "Score medio:",
        round(resumo["score_medio"], 6),
    )

    print("\nTOP 10 - ANOMALIAS DETECTADAS")

    if sinalizados.empty:

        print("Nenhuma anomalia sinalizada.")

    else:

        colunas = [
            "data_hora",
            "temperatura",
            "umidade",
            "variacao_temperatura",
            "variacao_umidade",
            "score_anomalia",
        ]

        print(
            sinalizados[colunas]
            .head(10)
            .to_string(index=False)
        )

    print("\nLIMITACOES")
    print(resumo["limitacao"])

    print("\nArquivos de resultados gerados.")
    print("=" * 60)


if __name__ == "__main__":
    executar_avaliacao()