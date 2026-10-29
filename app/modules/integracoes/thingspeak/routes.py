from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_database_session, require_profiles
from app.modules.integracoes.thingspeak.exceptions import (
    ThingSpeakConfigurationError, ThingSpeakConnectionError, ThingSpeakError,
    ThingSpeakHTTPError, ThingSpeakInvalidResponseError, ThingSpeakTimeoutError,
)
from app.modules.integracoes.thingspeak.schemas import (
    ThingSpeakFeed, ThingSpeakMappingResult, ThingSpeakSyncSummary, ThingSpeakStatusResponse,
)
from app.modules.integracoes.thingspeak.service import ThingSpeakService
from app.modules.integracoes.thingspeak.http_security import validate_http_config,safe_response,safe_latest

router = APIRouter(prefix='/api/v1/integracoes/thingspeak', tags=['integracoes','thingspeak'],
    dependencies=[Depends(require_profiles('ADMIN'))],responses={
        401:{'description':'JWT ausente, invalido, expirado ou usuario inativo.'},
        403:{'description':'Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN.'},
        503:{'description':'Configuracao insegura/invalida ou indisponibilidade da integracao.'},
    })


def http_service():
    try:
        service=ThingSpeakService.from_settings()
        validate_http_config(service)
        return service
    except (ValueError,TypeError,ThingSpeakConfigurationError):
        raise HTTPException(503,'Configuracao HTTP ThingSpeak invalida ou insegura.') from None


@router.get('/status',response_model=ThingSpeakStatusResponse,
    summary='Diagnostico administrativo privado da integracao global')
def get_status(service:ThingSpeakService=Depends(http_service)):
    return safe_response(service.get_status(),service)


@router.get('/feeds',response_model=ThingSpeakMappingResult,
    summary='Consultar leituras do canal global como ADMIN')
async def get_feeds(results:int|None=Query(default=10,ge=1,le=8000),service:ThingSpeakService=Depends(http_service)):
    """Nao e uma consulta por transportadora. Para operacao no escopo empresarial, usar historico por sessao."""
    try:
        return safe_response(await service.get_mapped_feeds(results=results),service)
    except ThingSpeakError as exc:
        _raise_http_error(exc)


@router.get('/ultima-leitura',response_model=ThingSpeakFeed|None,
    summary='Consultar ultimo feed do canal global como ADMIN')
async def get_latest_feed(service:ThingSpeakService=Depends(http_service)):
    """Campos raw adicionais nao documentados sao omitidos por seguranca; servicos internos preservam o original."""
    try:
        return safe_latest(await service.get_latest_feed(),service)
    except ThingSpeakError as exc:
        _raise_http_error(exc)


@router.post('/sincronizar',response_model=ThingSpeakSyncSummary,
    summary='Sincronizacao manual administrativa do canal global')
async def sincronizar_feeds(results:int|None=Query(default=100,ge=1,le=8000),
    db:Session=Depends(get_database_session),service:ThingSpeakService=Depends(http_service)):
    """Escrita global apenas por ADMIN; nao concede associacao a sessoes nem dispensa os controles do historico IoT."""
    try:
        return safe_response(await service.sincronizar_feeds(db=db,results=results),service)
    except ThingSpeakError as exc:
        _raise_http_error(exc)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(503,'ThingSpeak synchronization persistence failed.') from None


def _raise_http_error(exc:ThingSpeakError):
    # Upstream/configuration messages may contain URLs, tokens or provider payloads.
    if isinstance(exc,ThingSpeakConfigurationError): code,detail=400,'ThingSpeak channel or mapping is not configured.'
    elif isinstance(exc,ThingSpeakTimeoutError): code,detail=504,'ThingSpeak request timed out.'
    elif isinstance(exc,ThingSpeakConnectionError): code,detail=503,'ThingSpeak connection failed.'
    elif isinstance(exc,ThingSpeakHTTPError):
        code=exc.status_code if 400<=exc.status_code<=599 else 502
        detail='ThingSpeak upstream request failed.'
    elif isinstance(exc,ThingSpeakInvalidResponseError): code,detail=502,'Invalid ThingSpeak response.'
    else: code,detail=500,'Unexpected ThingSpeak integration error.'
    raise HTTPException(code,detail) from None
