import json

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest

from preparacao_dados import (
    FEATURES,
    PASTA_DADOS,
    identificar_sessoes,
    criar_features,
)

from validacao import (
    definir_cenarios,
    criar_cenario,
)


PASTA_RESULTADOS = PASTA_DADOS / "resultados"

FEATURES_BASICAS = [
    "temperatura",
    "umidade",
]

ARQUIVO_MODELO = (
    PASTA_DADOS / "modelos" / "isolation_forest.joblib"
)


def calcular_scores(modelo, dados, features):

    return -modelo.score_samples(
        dados[features]
    )


def avaliar_base(modelo, dados, features, limite):

    scores = calcular_scores(
        modelo,
        dados,
        features,
    )

    sinalizados = int(
        (scores > limite).sum()
    )

    return {
        "registros": len(dados),
        "sinalizados": sinalizados,
        "percentual_sinalizado": round(
            sinalizados / len(dados) * 100, 4
        ),
        "score_medio": round(
            float(scores.mean()), 6
        ),
        "score_minimo": round(
            float(scores.min()), 6
        ),
        "score_maximo": round(
            float(scores.max()), 6
        ),
    }


def avaliar_cenarios(modelo, features, limite):

    resultados = []

    for cenario in definir_cenarios()[:6]:

        dados = criar_cenario(
            cenario["temperaturas"],
            cenario["umidades"],
        )

        dados = dados.rename(columns={
            "created_at": "data_hora",
            "field1": "temperatura",
            "field2": "umidade",
        })

        dados = identificar_sessoes(dados)

        dados = criar_features(dados)

        ultima = dados.tail(1)

        score = float(
            calcular_scores(
                modelo,
                ultima,
                features,
            )[0]
        )

        obtido = (
            "ANOMALIA_DETECTADA"
            if score > limite
            else "NAO_SINALIZADO"
        )

        resultados.append({
            "id": cenario["id"],
            "cenario": cenario["cenario"],
            "esperado": cenario["esperado"],
            "obtido": obtido,
            "score": round(score, 6),
            "resultado": (
                "APROVADO"
                if obtido == cenario["esperado"]
                else "DIVERGENTE"
            ),
        })

    return resultados


def executar_comparacao():

    treino = pd.read_csv(
        PASTA_DADOS / "treino.csv"
    )

    calibracao = pd.read_csv(
        PASTA_DADOS / "calibracao.csv"
    )

    avaliacao = pd.read_csv(
        PASTA_DADOS / "avaliacao.csv"
    )

    # MODELO A - SEM FEATURE ENGINEERING

    modelo_a = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=2,
    )

    modelo_a.fit(
        treino[FEATURES_BASICAS]
    )

    scores_calibracao_a = calcular_scores(
        modelo_a,
        calibracao,
        FEATURES_BASICAS,
    )

    limite_a = float(
        np.percentile(scores_calibracao_a, 95)
    )

    # MODELO B - COM FEATURE ENGINEERING

    pacote = joblib.load(ARQUIVO_MODELO)

    modelo_b = pacote["modelo"]
    limite_b = pacote["limite"]

    if pacote["features"] != FEATURES:
        raise ValueError(
            "Features incompativeis com o modelo B."
        )

    configuracoes = [
        (
            "Modelo A - 2 atributos",
            modelo_a,
            FEATURES_BASICAS,
            limite_a,
        ),
        (
            "Modelo B - 6 atributos",
            modelo_b,
            FEATURES,
            limite_b,
        ),
    ]

    resumo = []
    detalhes = []

    print("=" * 65)
    print("CHICO SENSE - COMPARACAO DOS MODELOS")
    print("=" * 65)

    for nome, modelo, features, limite in configuracoes:

        resultado_treino = avaliar_base(
            modelo, treino, features, limite
        )

        resultado_calibracao = avaliar_base(
            modelo, calibracao, features, limite
        )

        resultado_avaliacao = avaliar_base(
            modelo, avaliacao, features, limite
        )

        cenarios = avaliar_cenarios(
            modelo, features, limite
        )

        aprovados = sum(
            c["resultado"] == "APROVADO"
            for c in cenarios
        )

        divergentes = len(cenarios) - aprovados

        resumo.append({
            "modelo": nome,
            "quantidade_features": len(features),
            "features": features,
            "limite": limite,
            "treinamento": resultado_treino,
            "calibracao": resultado_calibracao,
            "avaliacao": resultado_avaliacao,
            "testes_simulados": len(cenarios),
            "aprovados": aprovados,
            "divergentes": divergentes,
        })

        for cenario in cenarios:

            detalhes.append({
                "modelo": nome,
                **cenario,
            })

        print("\n" + nome)

        print(
            "Quantidade de atributos:",
            len(features),
        )

        print(
            "Limite:",
            round(limite, 6),
        )

        print(
            "Sinalizados no treinamento:",
            resultado_treino["sinalizados"],
        )

        print(
            "Sinalizados na calibracao:",
            resultado_calibracao["sinalizados"],
        )

        print(
            "Sinalizados na avaliacao:",
            resultado_avaliacao["sinalizados"],
        )

        print(
            "Percentual na avaliacao:",
            resultado_avaliacao["percentual_sinalizado"],
            "%",
        )

        print(
            "Score medio na avaliacao:",
            resultado_avaliacao["score_medio"],
        )

        print(
            "Cenarios aprovados:",
            aprovados,
            "de",
            len(cenarios),
        )

        print(
            "Cenarios divergentes:",
            divergentes,
        )

        print("\nDETALHES DOS TESTES")

        for cenario in cenarios:

            print(
                cenario["id"],
                "| Score:",
                cenario["score"],
                "|",
                cenario["resultado"],
            )

    PASTA_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    pd.DataFrame(detalhes).to_csv(
        PASTA_RESULTADOS / "comparacao_modelos.csv",
        index=False,
    )

    relatorio = {
        "objetivo": (
            "Avaliar o impacto do Feature Engineering "
            "na deteccao de anomalias."
        ),
        "metodologia": (
            "Mesmas bases, algoritmo, numero de arvores, "
            "semente e percentil de calibracao."
        ),
        "limitacao": (
            "Comparacao exploratoria com dados sem rotulos "
            "reais e cenarios simulados previamente utilizados. "
            "Nao representa uma nova validacao independente."
        ),
        "modelos": resumo,
    }

    with open(
        PASTA_RESULTADOS / "comparacao_modelos.json",
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            relatorio,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )

    print("\n" + "=" * 65)
    print("COMPARACAO CONCLUIDA.")
    print("Evidencias salvas com sucesso.")
    print("Modelo original preservado.")
    print("=" * 65)


if __name__ == "__main__":
    executar_comparacao()