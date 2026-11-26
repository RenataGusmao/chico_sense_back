from __future__ import annotations

import math
from datetime import datetime, timezone

from starlette.concurrency import run_in_threadpool

from app.modules.integracoes.thingspeak.exceptions import ThingSpeakConfigurationError
from app.modules.integracoes.thingspeak.http_security import validate_http_config
from app.modules.integracoes.thingspeak.service import (
    ThingSpeakService,
)

from app.modules.inteligencia.preparacao_dados import INTERVALO_MAXIMO, JANELA_MOVEL
from app.modules.inteligencia.service import TEMPERATURA_MAXIMA_MODELO, analisar_medicoes


LIMITE_ATUALIZACAO_SEGUNDOS = 120
INTERVALO_MAXIMO_SEGUNDOS = INTERVALO_MAXIMO
QUANTIDADE_MEDICOES = JANELA_MOVEL


async def analisar_thingspeak():
    try:
        servico = ThingSpeakService.from_settings()
        if servico.config.channel_id:
            validate_http_config(servico)
    except (TypeError, ValueError) as erro:
        raise ThingSpeakConfigurationError(
            "Configuracao HTTP ThingSpeak invalida ou insegura."
        ) from erro

    canal = servico.config.channel_id

    resposta = {
        "origem": "THINGSPEAK",
        "canal": canal,
        "consultado_em": None,
        "ultima_medicao": None,
        "idade_leitura_segundos": None,
        "dados_recentes": False,
        "status": "AGUARDANDO_DADOS",
        "medicoes": [],
        "resultado": None,
        "mensagem": "",
    }

    if not canal:
        resposta["status"] = "CANAL_NAO_CONFIGURADO"
        resposta["mensagem"] = (
            "O canal ThingSpeak não está configurado."
        )
        return resposta

    feeds = await servico.get_feeds(
        results=QUANTIDADE_MEDICOES
    )

    agora = datetime.now(timezone.utc)

    resposta["consultado_em"] = agora.isoformat()

    medicoes = []

    for feed in feeds:
        try:
            temperatura = float(feed.fields.get("field1"))
            umidade = float(feed.fields.get("field2"))

            if not math.isfinite(temperatura):
                continue

            if not math.isfinite(umidade):
                continue

            if not -273.15 <= temperatura <= TEMPERATURA_MAXIMA_MODELO:
                continue

            if not 0 <= umidade <= 100:
                continue

            data_hora = feed.created_at

            if data_hora.tzinfo is None:
                continue

            data_hora = data_hora.astimezone(timezone.utc)

            medicoes.append({
                "data_hora": data_hora,
                "temperatura": temperatura,
                "umidade": umidade,
            })

        except (TypeError, ValueError):
            continue

    medicoes.sort(
        key=lambda medicao: medicao["data_hora"]
    )

    resposta["medicoes"] = medicoes

    if not medicoes:
        resposta["status"] = "DADOS_INSUFICIENTES"
        resposta["mensagem"] = (
            "Nenhuma medição válida foi recebida."
        )
        return resposta

    ultima_medicao = medicoes[-1]["data_hora"]

    idade = (agora - ultima_medicao).total_seconds()

    resposta["ultima_medicao"] = ultima_medicao.isoformat()
    resposta["idade_leitura_segundos"] = round(idade, 1)

    if idade < 0:
        resposta["status"] = "HORARIO_INVALIDO"
        resposta["mensagem"] = (
            "A última medição possui horário posterior "
            "ao horário da consulta."
        )
        return resposta

    if idade > LIMITE_ATUALIZACAO_SEGUNDOS:
        resposta["status"] = "DADOS_DESATUALIZADOS"
        resposta["mensagem"] = (
            "O ThingSpeak não recebeu uma leitura válida "
            "nos últimos 120 segundos. Verifique o sensor."
        )
        return resposta

    resposta["dados_recentes"] = True

    if len(medicoes) < QUANTIDADE_MEDICOES:
        resposta["status"] = "DADOS_INSUFICIENTES"
        resposta["mensagem"] = (
            "São necessárias cinco medições válidas "
            "para executar a análise."
        )
        return resposta

    for anterior, atual in zip(medicoes, medicoes[1:]):
        intervalo = (
            atual["data_hora"] - anterior["data_hora"]
        ).total_seconds()

        if intervalo <= 0:
            resposta["status"] = "DADOS_INVALIDOS"
            resposta["mensagem"] = (
                "Foram encontrados horários duplicados."
            )
            return resposta

        if intervalo > INTERVALO_MAXIMO_SEGUNDOS:
            resposta["status"] = "INTERRUPCAO_DETECTADA"
            resposta["mensagem"] = (
                "Foi identificada uma interrupção superior "
                "a 60 segundos entre as medições."
            )
            return resposta

    resultado = await run_in_threadpool(analisar_medicoes, medicoes)
    resultado["origem"] = "THINGSPEAK"

    resposta["status"] = resultado["status"]
    resposta["resultado"] = resultado
    resposta["mensagem"] = resultado["recomendacao"]

    return resposta
