"""Authenticated session history/acquisition endpoints, with no ethylene calculations."""
from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response
from pydantic import AwareDatetime
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_database_session
from app.models.usuario import Usuario
from app.modules.integracoes.thingspeak.service import ThingSpeakService
from app.modules.monitoramento.routes import ERROS
from app.modules.monitoramento.historico_service import HistoricoIoTService
from app.modules.monitoramento.historico_consulta import HistoricoConsultaService
from app.modules.monitoramento.historico_schemas import (
    SincronizacaoCreate, SincronizacaoResponse, HistoricoResponse, EstadoSincronizacaoResponse, QualidadeResponse,
)

router=APIRouter(prefix='/api/v1/monitoramentos',tags=['Historico IoT'],responses=ERROS)


def thingspeak_service():
    from fastapi import HTTPException
    try:
        return ThingSpeakService.from_settings()
    except (ValueError,TypeError):
        raise HTTPException(409,'Configuracao ThingSpeak invalida; nenhum segredo e retornado.') from None


def consultas(db:Session=Depends(get_database_session),user:Usuario=Depends(get_current_user)):
    return HistoricoConsultaService(db,user)


@router.post('/{sessao_id}/sincronizacoes',response_model=SincronizacaoResponse,
             responses={202:{'model':SincronizacaoResponse,'description':'A mesma requisicao ainda esta em execucao.'}},
             summary='Sincronizar explicitamente o historico de uma sessao')
async def sincronizar(sessao_id:UUID,data:SincronizacaoCreate,response:Response,
                     db:Session=Depends(get_database_session),user:Usuario=Depends(get_current_user),
                     thingspeak=Depends(thingspeak_service)):
    """THINGSPEAK usa o cliente existente; BANCO reassocia somente medicoes externas da origem fixada.

    Encerrada exige complementar_encerrada, justificativa e ADMIN/GESTOR. Cancelada nao recebe dados.
    Falha de aquisicao retorna estado FALHA/PARCIAL auditado; nao e confundida com sucesso de coleta.
    """
    run=await HistoricoIoTService(db,user,thingspeak).sincronizar(sessao_id,data)
    if run.estado=='EM_EXECUCAO': response.status_code=202
    return run


@router.get('/{sessao_id}/sincronizacoes',response_model=EstadoSincronizacaoResponse,
            summary='Consultar estado e tentativas de sincronizacao')
def estado(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(consultas)):
    return svc.estado(sessao_id,limit,offset)


@router.get('/{sessao_id}/leituras',response_model=HistoricoResponse,
            summary='Consultar leituras e marcadores invalidos em ordem cronologica')
def leituras(sessao_id:UUID,limit:int=Query(100,ge=1,le=1000),offset:int=Query(0,ge=0),
             tipo:str|None=Query(None,pattern='^(TEMPERATURA|UMIDADE)$'),revisao:int|None=Query(None,ge=1),
             inicio:AwareDatetime|None=None,fim:AwareDatetime|None=None,svc=Depends(consultas)):
    """Janela inclusiva de amostras [inicio,fim], com amostra final apenas para fechar intervalos.

    Revisoes preservam a incorporacao anterior; nao se altera registro ou valor em silencio.
    recebida_em=None identifica horario de recebimento desconhecido no historico legado.
    """
    return svc.historico(sessao_id,limit,offset,tipo,revisao,inicio,fim)


@router.get('/{sessao_id}/qualidade',response_model=QualidadeResponse,
            summary='Consultar lacunas e cobertura temporal, sem estimativa de etileno')
def qualidade(sessao_id:UUID,intervalo_maximo_s:Decimal=Query(...,gt=0,max_digits=12,decimal_places=3),
              revisao:int|None=Query(None,ge=1),inicio:AwareDatetime|None=None,fim:AwareDatetime|None=None,
              svc=Depends(consultas)):
    """G e parametro operacional obrigatorio, sem valor padrao cientifico.

    Dois extremos utilizaveis, gaps integrais, sem interpolacao ou extrapolacao.
    Cobertura de aquisicao nao e cobertura de aplicabilidade do modelo cientifico.
    """
    return svc.qualidade(sessao_id,intervalo_maximo_s,revisao,inicio,fim)
