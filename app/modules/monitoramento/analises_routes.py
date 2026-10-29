"""Session-scoped potential ethylene production; never a gas concentration or alert."""
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_database_session
from app.models.usuario import Usuario
from app.modules.monitoramento.routes import ERROS
from app.modules.monitoramento.analises_service import AnalisesEtilenoService
from app.modules.monitoramento.analises_schemas import AnaliseCreate, AnaliseResponse, AnaliseLista

router=APIRouter(prefix='/api/v1/monitoramentos',tags=['Analises de etileno'],responses=ERROS)


def servico(db:Session=Depends(get_database_session),user:Usuario=Depends(get_current_user)):
    return AnalisesEtilenoService(db,user)


@router.post('/{sessao_id}/analises-etileno',response_model=AnaliseResponse,
    responses={503:{'description':'Falha de persistencia; consulte ou repita a mesma chave idempotente.'}},
    summary='Calcular e persistir producao potencial com o motor cientifico existente')
def executar(sessao_id:UUID,data:AnaliseCreate,svc=Depends(servico)):
    """Fixa janela, corte, revisao e snapshots. ATIVA exige corte explicito; CANCELADA rejeita novas analises.

    G ausente gera CONFIGURACAO_INCOMPLETA. Subtotal coberto nunca substitui total da janela.
    Mesma chave/autor/payload recupera o resultado anterior. Nova chave cria outra analise.
    Decimais sao strings JSON. Risco permanece NAO_AVALIADO, sem inferir concentracao real.
    """
    return svc.executar(sessao_id,data)


@router.get('/{sessao_id}/analises-etileno',response_model=AnaliseLista,summary='Listar analises preservadas da sessao')
def listar(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.listar(sessao_id,limit,offset)


@router.get('/{sessao_id}/analises-etileno/{analise_id}',response_model=AnaliseResponse,
    summary='Consultar resultado e entradas fixados, sem recalcular')
def consultar(sessao_id:UUID,analise_id:UUID,svc=Depends(servico)):
    return svc.consultar(sessao_id,analise_id)
