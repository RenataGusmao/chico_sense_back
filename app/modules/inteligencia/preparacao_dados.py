from pathlib import Path

import numpy as np
import pandas as pd


# Configuracoes da preparacao dos dados
INTERVALO_MAXIMO = 60
JANELA_MOVEL = 5

FEATURES = [
    "temperatura",
    "umidade",
    "variacao_temperatura",
    "variacao_umidade",
    "media_temperatura",
    "media_umidade",
]

BACKEND_DIR = Path(__file__).resolve().parents[3]

PASTA_DADOS = BACKEND_DIR / "data" / "ia"

ARQUIVO_ORIGINAL = PASTA_DADOS / "feeds.csv"


def carregar_dados(caminho=ARQUIVO_ORIGINAL):
    """Carrega e valida os dados historicos do ThingSpeak."""

    df = pd.read_csv(caminho)

    df = df[
        ["created_at", "entry_id", "field1", "field2"]
    ].copy()

    df = df.rename(
        columns={
            "created_at": "data_hora",
            "field1": "temperatura",
            "field2": "umidade",
        }
    )

    df["data_hora"] = pd.to_datetime(
        df["data_hora"],
        utc=True,
        errors="coerce",
    )

    for coluna in ["temperatura", "umidade"]:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce",
        )

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.dropna(
        subset=[
            "data_hora",
            "entry_id",
            "temperatura",
            "umidade",
        ]
    )

    df = df.drop_duplicates(subset=["entry_id"])
    df = df.drop_duplicates(subset=["data_hora"])

    df = df[
        (df["temperatura"] >= -273.15)
        & (df["umidade"].between(0, 100))
    ]

    df = df.sort_values("data_hora")
    df = df.reset_index(drop=True)

    return df


def identificar_sessoes(df):
    """Separa as coletas quando existem interrupcoes."""

    df = df.copy()

    df["intervalo_segundos"] = (
        df["data_hora"].diff().dt.total_seconds()
    )

    df["sessao"] = (
        df["intervalo_segundos"] > INTERVALO_MAXIMO
    ).cumsum() + 1

    return df


def criar_features(df):
    """Cria atributos temporais sem atravessar sessoes."""

    df = df.copy()

    grupos = df.groupby("sessao")

    df["variacao_temperatura"] = (
        grupos["temperatura"].diff()
    )

    df["variacao_umidade"] = (
        grupos["umidade"].diff()
    )

    df["media_temperatura"] = grupos[
        "temperatura"
    ].transform(
        lambda valores: valores.rolling(
            window=JANELA_MOVEL,
            min_periods=JANELA_MOVEL,
        ).mean()
    )

    df["media_umidade"] = grupos[
        "umidade"
    ].transform(
        lambda valores: valores.rolling(
            window=JANELA_MOVEL,
            min_periods=JANELA_MOVEL,
        ).mean()
    )

    df = df.dropna(subset=FEATURES)

    return df.reset_index(drop=True)


def separar_dados(df):
    """Separa as bases cronologicamente."""

    treino = df[df["sessao"] <= 10].copy()

    calibracao = df[df["sessao"] == 11].copy()

    avaliacao = df[df["sessao"] == 12].copy()

    if treino.empty or calibracao.empty or avaliacao.empty:
        raise ValueError(
            "Uma ou mais bases estao vazias."
        )

    return treino, calibracao, avaliacao


def executar_preparacao():
    """Executa o fluxo completo de preparacao."""

    dados = carregar_dados()

    total_original = len(dados)

    dados = identificar_sessoes(dados)

    total_sessoes = dados["sessao"].nunique()

    dados = criar_features(dados)

    treino, calibracao, avaliacao = separar_dados(dados)

    dados.to_csv(
        PASTA_DADOS / "dados_preparados.csv",
        index=False,
    )

    treino.to_csv(
        PASTA_DADOS / "treino.csv",
        index=False,
    )

    calibracao.to_csv(
        PASTA_DADOS / "calibracao.csv",
        index=False,
    )

    avaliacao.to_csv(
        PASTA_DADOS / "avaliacao.csv",
        index=False,
    )

    print("=" * 50)
    print("CHICO SENSE - PREPARACAO DOS DADOS")
    print("=" * 50)

    print("Registros validos de entrada:", total_original)
    print("Sessoes identificadas:", total_sessoes)
    print("Registros preparados:", len(dados))
    print("Registros descartados:", total_original - len(dados))

    print("\nDIVISAO DA BASE")
    print("Treinamento:", len(treino))
    print("Calibracao:", len(calibracao))
    print("Avaliacao:", len(avaliacao))

    print("\nFEATURES UTILIZADAS")

    for feature in FEATURES:
        print("-", feature)

    print("\nArquivos CSV gerados com sucesso.")
    print("=" * 50)


if __name__ == "__main__":
    executar_preparacao()