import json

import joblib
import pandas as pd

from preparacao_dados import (
    FEATURES,
    PASTA_DADOS,
    identificar_sessoes,
    criar_features,
    carregar_dados,
)


PASTA_RESULTADOS = PASTA_DADOS / "resultados"

ARQUIVO_MODELO = (
    PASTA_DADOS / "modelos" / "isolation_forest.joblib"
)


def criar_cenario(
    temperaturas,
    umidades,
    interrupcao=False,
):
    """Cria uma sequencia de medicoes simuladas."""

    datas = pd.date_range(
        start="2026-01-01 12:00:00",
        periods=len(temperaturas),
        freq="16s",
        tz="UTC",
    ).tolist()

    if interrupcao:
        datas[-1] += pd.Timedelta(minutes=10)

    return pd.DataFrame({
        "created_at": datas,
        "entry_id": range(1, len(datas) + 1),
        "field1": temperaturas,
        "field2": umidades,
    })


def definir_cenarios():
    """Define os casos de teste controlados."""

    return [
        {
            "id": "CT-IA-001",
            "cenario": "Condicoes estaveis",
            "temperaturas": [25, 25, 25.1, 25, 25.1],
            "umidades": [40, 40.1, 40, 40.2, 40],
            "esperado": "NAO_SINALIZADO",
        },
        {
            "id": "CT-IA-002",
            "cenario": "Aumento brusco de temperatura",
            "temperaturas": [25, 25, 25, 25, 40],
            "umidades": [40, 40, 40, 40, 40],
            "esperado": "ANOMALIA_DETECTADA",
        },
        {
            "id": "CT-IA-003",
            "cenario": "Aumento brusco de umidade",
            "temperaturas": [25, 25, 25, 25, 25],
            "umidades": [40, 40, 40, 40, 95],
            "esperado": "ANOMALIA_DETECTADA",
        },
        {
            "id": "CT-IA-004",
            "cenario": "Aumento simultaneo de temperatura e umidade",
            "temperaturas": [25, 25, 25, 25, 40],
            "umidades": [40, 40, 40, 40, 95],
            "esperado": "ANOMALIA_DETECTADA",
        },
        {
            "id": "CT-IA-005",
            "cenario": "Reducao brusca de temperatura",
            "temperaturas": [28, 28, 28, 28, 10],
            "umidades": [45, 45, 45, 45, 45],
            "esperado": "ANOMALIA_DETECTADA",
        },
        {
            "id": "CT-IA-006",
            "cenario": "Variacao ambiental gradual",
            "temperaturas": [25, 25.1, 25.2, 25.3, 25.4],
            "umidades": [40, 40.2, 40.4, 40.6, 40.8],
            "esperado": "NAO_SINALIZADO",
        },
        {
            "id": "CT-IA-007",
            "cenario": "Historico insuficiente",
            "temperaturas": [25, 25.1],
            "umidades": [40, 41],
            "esperado": "DADOS_INSUFICIENTES",
        },
        {
            "id": "CT-IA-008",
            "cenario": "Interrupcao entre medicoes",
            "temperaturas": [25, 25, 25, 25, 35],
            "umidades": [40, 40, 40, 40, 90],
            "interrupcao": True,
            "esperado": "DADOS_INSUFICIENTES",
        },
        {
            "id": "CT-IA-009",
            "cenario": "Umidade invalida",
            "temperaturas": [25, 25, 25, 25, 25],
            "umidades": [40, 40, 40, 40, 150],
            "esperado": "DADOS_INVALIDOS",
        },
    ]


def avaliar_cenario(cenario, modelo, limite):
    """Processa um cenario utilizando o modelo treinado."""

    dados = criar_cenario(
        cenario["temperaturas"],
        cenario["umidades"],
        cenario.get("interrupcao", False),
    )

    ultima_medicao = int(dados["entry_id"].iloc[-1])

    score = None

    valores_invalidos = (
        dados["field1"].isna().any()
        or dados["field2"].isna().any()
        or (dados["field1"] < -273.15).any()
        or (~dados["field2"].between(0, 100)).any()
    )

    if valores_invalidos:

        classificacao = "DADOS_INVALIDOS"

    else:

        dados = dados.rename(columns={
            "created_at": "data_hora",
            "field1": "temperatura",
            "field2": "umidade",
        })

        dados = identificar_sessoes(dados)

        dados = criar_features(dados)

        ultima = dados[
            dados["entry_id"] == ultima_medicao
        ]

        if ultima.empty:

            classificacao = "DADOS_INSUFICIENTES"

        else:

            score = float(
                -modelo.score_samples(
                    ultima[FEATURES]
                )[0]
            )

            classificacao = (
                "ANOMALIA_DETECTADA"
                if score > limite
                else "NAO_SINALIZADO"
            )

    resultado = {
        "id": cenario["id"],
        "cenario": cenario["cenario"],
        "origem": "SIMULADO",
        "esperado": cenario["esperado"],
        "obtido": classificacao,
        "score": round(score, 6) if score is not None else None,
        "limite": round(limite, 6),
        "resultado": (
            "APROVADO"
            if classificacao == cenario["esperado"]
            else "DIVERGENTE"
        ),
    }

    return resultado


def executar_validacao():

    pacote = joblib.load(ARQUIVO_MODELO)

    modelo = pacote["modelo"]
    limite = pacote["limite"]

    if pacote["features"] != FEATURES:
        raise ValueError("Features incompativeis.")

    resultados = []

    print("=" * 65)
    print("CHICO SENSE - VALIDACAO CONTROLADA DA IA")
    print("=" * 65)

    print("Algoritmo: Isolation Forest")
    print("Limite:", round(limite, 6))

    for cenario in definir_cenarios():

        resultado = avaliar_cenario(
            cenario,
            modelo,
            limite,
        )

        resultados.append(resultado)

        print("\n" + resultado["id"])
        print("Cenario:", resultado["cenario"])
        print("Esperado:", resultado["esperado"])
        print("Obtido:", resultado["obtido"])
        print("Score:", resultado["score"])
        print("Resultado:", resultado["resultado"])

    aprovados = sum(
        r["resultado"] == "APROVADO"
        for r in resultados
    )

    divergentes = len(resultados) - aprovados

    resumo = {
        "total_testes": len(resultados),
        "aprovados": aprovados,
        "divergentes": divergentes,
        "origem": "Cenarios simulados",
        "limitacao": (
            "A concordancia com cenarios simulados "
            "nao representa acuracia em operacao real."
        ),
        "testes": resultados,
    }

    PASTA_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    pd.DataFrame(resultados).to_csv(
        PASTA_RESULTADOS / "validacao_controlada.csv",
        index=False,
    )

    with open(
        PASTA_RESULTADOS / "validacao_controlada.json",
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            resumo,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )

    print("\n" + "=" * 65)
    print("RESUMO DA VALIDACAO")
    print("Total de testes:", len(resultados))
    print("Aprovados:", aprovados)
    print("Divergentes:", divergentes)
    print("Evidencias salvas com sucesso.")
    print("=" * 65)


if __name__ == "__main__":
    executar_validacao()