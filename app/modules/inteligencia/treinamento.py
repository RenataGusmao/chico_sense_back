import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

from sklearn.ensemble import IsolationForest

from preparacao_dados import FEATURES, PASTA_DADOS


# Configuracoes do modelo
SEMENTE = 42
NUMERO_ARVORES = 200
PERCENTIL_LIMITE = 95

PASTA_MODELOS = PASTA_DADOS / "modelos"

ARQUIVO_MODELO = PASTA_MODELOS / "isolation_forest.joblib"

ARQUIVO_METADADOS = PASTA_MODELOS / "metadados.json"


def carregar_bases():
    """Carrega as bases de treinamento e calibracao."""

    treino = pd.read_csv(
        PASTA_DADOS / "treino.csv"
    )

    calibracao = pd.read_csv(
        PASTA_DADOS / "calibracao.csv"
    )

    return treino, calibracao


def treinar_modelo(treino):
    """Treina o modelo de deteccao de anomalias."""

    modelo = IsolationForest(
        n_estimators=NUMERO_ARVORES,
        contamination="auto",
        random_state=SEMENTE,
        n_jobs=2,
    )

    modelo.fit(treino[FEATURES])

    return modelo


def calcular_scores(modelo, dados):
    """Quanto maior o score, mais atipica a medicao."""

    return -modelo.score_samples(
        dados[FEATURES]
    )


def calibrar_limite(modelo, calibracao):
    """Define um limite experimental para as anomalias."""

    scores = calcular_scores(
        modelo,
        calibracao,
    )

    limite = float(
        np.percentile(
            scores,
            PERCENTIL_LIMITE,
        )
    )

    return limite


def salvar_modelo(modelo, limite, treino, calibracao):
    """Salva o modelo e suas informacoes tecnicas."""

    PASTA_MODELOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    pacote = {
        "modelo": modelo,
        "limite": limite,
        "features": FEATURES,
    }

    joblib.dump(
        pacote,
        ARQUIVO_MODELO,
    )

    metadados = {
        "algoritmo": "Isolation Forest",
        "tipo": "Machine Learning Nao Supervisionado",
        "versao_modelo": "1.0.0",
        "versao_scikit_learn": sklearn.__version__,
        "numero_arvores": NUMERO_ARVORES,
        "random_state": SEMENTE,
        "percentil_calibracao": PERCENTIL_LIMITE,
        "limite_anomalia": limite,
        "registros_treinamento": len(treino),
        "registros_calibracao": len(calibracao),
        "features": FEATURES,
        "origem": "Historico ThingSpeak - canal 3493148",
        "limitacao": (
            "Modelo experimental sem rotulos reais "
            "de anomalias ou danos a carga."
        ),
    }

    with open(
        ARQUIVO_METADADOS,
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            metadados,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def executar_treinamento():
    """Executa o treinamento e a calibracao."""

    print("=" * 55)
    print("CHICO SENSE - TREINAMENTO DA IA")
    print("=" * 55)

    treino, calibracao = carregar_bases()

    print("Registros de treinamento:", len(treino))
    print("Registros de calibracao:", len(calibracao))
    print("Quantidade de features:", len(FEATURES))

    print("\nTreinando Isolation Forest...")

    modelo = treinar_modelo(treino)

    print("Treinamento concluido.")

    print("\nCalibrando limite de anomalias...")

    limite = calibrar_limite(
        modelo,
        calibracao,
    )

    scores_treino = calcular_scores(
        modelo,
        treino,
    )

    scores_calibracao = calcular_scores(
        modelo,
        calibracao,
    )

    anomalias_treino = int(
        (scores_treino > limite).sum()
    )

    anomalias_calibracao = int(
        (scores_calibracao > limite).sum()
    )

    print("\nRESULTADOS")
    print("Algoritmo: Isolation Forest")
    print("Numero de arvores:", NUMERO_ARVORES)
    print("Limite de anomalia:", round(limite, 6))

    print("\nTREINAMENTO")
    print("Score minimo:", round(scores_treino.min(), 6))
    print("Score maximo:", round(scores_treino.max(), 6))
    print("Score medio:", round(scores_treino.mean(), 6))
    print("Registros sinalizados:", anomalias_treino)

    print("\nCALIBRACAO")
    print("Score minimo:", round(scores_calibracao.min(), 6))
    print("Score maximo:", round(scores_calibracao.max(), 6))
    print("Score medio:", round(scores_calibracao.mean(), 6))
    print("Registros sinalizados:", anomalias_calibracao)

    salvar_modelo(
        modelo,
        limite,
        treino,
        calibracao,
    )

    print("\nModelo salvo com sucesso.")
    print("Metadados salvos com sucesso.")
    print("=" * 55)


if __name__ == "__main__":
    executar_treinamento()