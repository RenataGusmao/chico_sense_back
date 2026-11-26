from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user, require_profiles

from app.modules.inteligencia.schemas import (
    AnaliseIARequest,
    AnaliseIAResponse,
    StatusIAResponse,
    HistoricoIAResponse,
)

from app.modules.inteligencia.service import (
    ModeloIndisponivelError,
    obter_status,
    obter_historico,
    analisar_medicoes,
)

from app.modules.inteligencia.thingspeak_service import (
    analisar_thingspeak,
)

from app.modules.integracoes.thingspeak.exceptions import (
    ThingSpeakConfigurationError,
    ThingSpeakConnectionError,
    ThingSpeakTimeoutError,
    ThingSpeakHTTPError,
    ThingSpeakInvalidResponseError,
    ThingSpeakError,
)


router = APIRouter(
    prefix="/ia",
    tags=["Inteligencia Artificial"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/status",
    response_model=StatusIAResponse,
    summary="Consultar disponibilidade da IA",
)
def status_ia():

    return obter_status()


@router.get(
    "/historico",
    response_model=HistoricoIAResponse,
    summary="Consultar avaliacao historica da IA",
    dependencies=[
        Depends(require_profiles("ADMIN"))
    ],
)
def historico_ia():

    try:

        return obter_historico()

    except ModeloIndisponivelError as erro:

        raise HTTPException(
            status_code=503,
            detail=str(erro),
        ) from erro


@router.post(
    "/analisar",
    response_model=AnaliseIAResponse,
    summary="Analisar anomalias ambientais",
)
def analisar_ia(dados: AnaliseIARequest):

    try:

        medicoes = [
            medicao.model_dump()
            for medicao in dados.medicoes
        ]

        return analisar_medicoes(medicoes)

    except ModeloIndisponivelError as erro:

        raise HTTPException(
            status_code=503,
            detail=str(erro),
        ) from erro


@router.get(
    "/thingspeak",
    summary="Analisar leituras recentes do ThingSpeak",
    dependencies=[
        Depends(require_profiles("ADMIN"))
    ],
)
async def thingspeak_ia():

    try:

        return await analisar_thingspeak()

    except ThingSpeakConfigurationError as erro:

        raise HTTPException(
            status_code=503,
            detail="Canal ThingSpeak nao configurado.",
        ) from erro

    except ThingSpeakTimeoutError as erro:

        raise HTTPException(
            status_code=504,
            detail="O ThingSpeak demorou para responder.",
        ) from erro

    except ThingSpeakConnectionError as erro:

        raise HTTPException(
            status_code=503,
            detail="Nao foi possivel conectar ao ThingSpeak.",
        ) from erro

    except ThingSpeakHTTPError as erro:

        raise HTTPException(
            status_code=502,
            detail="O ThingSpeak retornou um erro na consulta.",
        ) from erro

    except ThingSpeakInvalidResponseError as erro:

        raise HTTPException(
            status_code=502,
            detail="O ThingSpeak retornou dados invalidos.",
        ) from erro

    except ModeloIndisponivelError as erro:

        raise HTTPException(
            status_code=503,
            detail=str(erro),
        ) from erro

    except ThingSpeakError as erro:

        raise HTTPException(
            status_code=503,
            detail="Servico ThingSpeak indisponivel.",
        ) from erro