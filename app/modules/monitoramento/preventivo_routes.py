"""Authenticated operational monitoring; no automatic intervention or scientific risk."""
from uuid import UUID
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from app.api.deps import get_current_user,get_database_session
from app.models.usuario import Usuario
from app.modules.monitoramento.routes import ERROS
from app.modules.monitoramento.preventivo_service import PreventivoService
from app.modules.monitoramento.preventivo_schemas import (ConfiguracaoCreate,ConfiguracaoResponse,AvaliacaoCreate,
    AvaliacaoResponse,DecisaoCreate,DecisaoResponse,AlertaResponse,ListaConfiguracoes,ListaAvaliacoes,ListaAlertas,ListaDecisoes,ListaEvidencias)

router=APIRouter(prefix='/api/v1/monitoramentos/{sessao_id}',tags=['Monitoramento preventivo'],
    responses=ERROS|{503:{'description':'Falha transacional; consultar ou repetir mesma chave idempotente.'}})


def servico(db:Session=Depends(get_database_session),user:Usuario=Depends(get_current_user)):
    return PreventivoService(db,user)


@router.post('/configuracoes-ambientais',response_model=ConfiguracaoResponse,summary='Registrar versao imutavel de parametros operacionais')
def configurar(sessao_id:UUID,data:ConfiguracaoCreate,svc=Depends(servico)):
    """ADMIN/GESTOR. Sem faixas ou duracoes cientificas automaticas. Maturacao/ambiente precisam corresponder explicitamente a sessao."""
    return svc.configurar(sessao_id,data)


@router.get('/configuracoes-ambientais',response_model=ListaConfiguracoes,summary='Listar versoes da configuracao operacional')
def configuracoes(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.listar(sessao_id,'configuracoes',limit,offset)


@router.post('/avaliacoes-preventivas',response_model=AvaliacaoResponse,summary='Avaliar dados ambientais e registrar alertas explicaveis')
def avaliar(sessao_id:UUID,data:AvaliacaoCreate,svc=Depends(servico)):
    """ATIVA exige corte explicito. Fixa revisao, configuracao e evidencias. Nova chave gera avaliacao relacionada a anterior.

    Evidencia igual reutiliza alerta. Evidencia nova se vincula ao caso aberto da regra/configuracao; sem sobrescrita.
    Ausencia de dados e inconclusiva. Analise de etileno opcional e somente contextual, da mesma janela/revisao.
    Nao mede gas, nao classifica risco cientifico e nao determina intervencao. Risco etileno NAO_AVALIADO.
    """
    return svc.avaliar(sessao_id,data)


@router.get('/avaliacoes-preventivas',response_model=ListaAvaliacoes,summary='Listar avaliacoes imutaveis')
def avaliacoes(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.listar(sessao_id,'avaliacoes',limit,offset)


@router.get('/avaliacoes-preventivas/{avaliacao_id}',response_model=AvaliacaoResponse,summary='Consultar snapshot e resultado sem reavaliar')
def avaliacao(sessao_id:UUID,avaliacao_id:UUID,svc=Depends(servico)):
    return svc.consultar_avaliacao(sessao_id,avaliacao_id)


@router.get('/alertas',response_model=ListaAlertas,summary='Listar alertas operacionais da sessao')
def alertas(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),
    status:str|None=Query(None,pattern='^(ABERTO|EM_ANALISE|RESOLVIDO|DESCARTADO)$'),svc=Depends(servico)):
    return svc.listar(sessao_id,'alertas',limit,offset,status)


@router.get('/alertas/{alerta_id}',response_model=AlertaResponse,summary='Consultar alerta ambiental')
def alerta(sessao_id:UUID,alerta_id:UUID,svc=Depends(servico)):
    return svc.consultar_alerta(sessao_id,alerta_id)


@router.post('/alertas/{alerta_id}/decisoes',response_model=DecisaoResponse,summary='Reconhecer, observar, resolver ou descartar com justificativa')
def decidir(sessao_id:UUID,alerta_id:UUID,data:DecisaoCreate,svc=Depends(servico)):
    """RECONHECER: ABERTO→EM_ANALISE (estado legado). Resolver/descartar: ABERTO ou EM_ANALISE→terminal.

    Justificativa, ator e horario sao obrigatorios. OBSERVAR acrescenta nota sem mudar estado, inclusive apos fechamento.
    Nenhuma transicao ou leitura posterior reabre ou encerra automaticamente um alerta.
    """
    return svc.decidir(sessao_id,alerta_id,data)


@router.get('/alertas/{alerta_id}/decisoes',response_model=ListaDecisoes,summary='Consultar historico auditavel de decisoes')
def decisoes(sessao_id:UUID,alerta_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.historico(sessao_id,alerta_id,'decisoes',limit,offset)


@router.get('/alertas/{alerta_id}/evidencias',response_model=ListaEvidencias,summary='Consultar evidencias e avaliacoes que sustentam o alerta')
def evidencias(sessao_id:UUID,alerta_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.historico(sessao_id,alerta_id,'evidencias',limit,offset)
