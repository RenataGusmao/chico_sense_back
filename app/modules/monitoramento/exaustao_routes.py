"""Authenticated supervised virtual actuator API; never sends hardware commands."""
from uuid import UUID
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from app.api.deps import get_current_user,get_database_session
from app.models.usuario import Usuario
from app.modules.monitoramento.routes import ERROS
from app.modules.monitoramento.exaustao_service import ExaustaoSimuladaService
from app.modules.monitoramento.exaustao_schemas import (IntervencaoCreate,AcaoCreate,IntervencaoResponse,AcaoResponse,ListaIntervencoes,ListaAcoes,EstadoIntervencao)

router=APIRouter(prefix='/api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas',
    tags=['Exaustao exclusivamente simulada'],responses=ERROS|{503:{'description':'Falha transacional; consulte ou repita mesma chave.'}})


def servico(db:Session=Depends(get_database_session),user:Usuario=Depends(get_current_user)):
    return ExaustaoSimuladaService(db,user)


@router.post('',response_model=IntervencaoResponse,summary='Solicitar intervencao virtual com justificativa humana')
def solicitar(sessao_id:UUID,data:IntervencaoCreate,svc=Depends(servico)):
    """Sessao/logistica ativas; alerta opcional da mesma sessao, ABERTO ou EM_ANALISE.

    Uma solicitacao nao autoriza nem inicia. Duracao de demonstracao <=86400s, sem eficacia cientifica.
    Referencias sao contextuais. Payload nao aceita dispositivos, protocolo, comandos fisicos ou estado imposto.
    """
    return svc.solicitar(sessao_id,data)


@router.get('',response_model=ListaIntervencoes,summary='Listar intervencoes da sessao')
def listar(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),estado:EstadoIntervencao|None=None,svc=Depends(servico)):
    return svc.listar(sessao_id,limit,offset,estado)


@router.get('/{intervencao_id}',response_model=IntervencaoResponse,summary='Consultar estado logico e permissoes atuais')
def consultar(sessao_id:UUID,intervencao_id:UUID,svc=Depends(servico)):
    """virtual_ligado reflete apenas EM_EXECUCAO persistido. Prazo excedido nao conclui a execucao.

    consultado_em fixa o instante da projecao; nenhuma consulta altera estado. Nao estima remocao de gas.
    """
    return svc.consultar(sessao_id,intervencao_id)


@router.post('/{intervencao_id}/acoes',response_model=AcaoResponse,summary='Registrar decisao humana ou transicao virtual')
def agir(sessao_id:UUID,intervencao_id:UUID,data:AcaoCreate,svc=Depends(servico)):
    """GESTOR/ADMIN autoriza, recusa, inicia, cancela e registra falha. Solicitante OPERADOR retira
    SOLICITADA ou encerra a propria execucao. CONSULTA somente le. Encerramento administrativo funciona
    mesmo apos fim/cancelamento da sessao. Autorizacao e inicio sao acoes separadas; nao ha scheduler.
    Justificativa obrigatoria, sem credenciais. Repeticao idempotente recupera a mesma acao historica.
    """
    return svc.agir(sessao_id,intervencao_id,data)


@router.get('/{intervencao_id}/acoes',response_model=ListaAcoes,summary='Consultar trilha ordenada de decisoes e transicoes')
def historico(sessao_id:UUID,intervencao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.historico(sessao_id,intervencao_id,limit,offset)
