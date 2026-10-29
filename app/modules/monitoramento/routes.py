"""Authenticated monitoring operations; legacy routers keep their contracts."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response as HttpResponse
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_database_session
from app.models.usuario import Usuario
from app.modules.monitoramento.schemas import (
    CargaMonitoramentoPut, CargaMonitoramentoResponse,
    SessaoCreate, SessaoFinalizar, SessaoResponse,
)
from app.modules.monitoramento.service import MonitoramentoService

ERROS = {
    401: {"description": "Autenticacao ausente, invalida ou usuario inativo."},
    403: {"description": "Perfil ou vinculo empresarial sem permissao."},
    404: {"description": "Carga, viagem, configuracao, sessao ou sensor nao encontrado."},
    409: {"description": "Conflito temporal, estado, integridade ou chave idempotente."},
    422: {"description": "Dados, horarios, massa ou sensores invalidos."},
}
router = APIRouter(prefix="/api/v1", tags=["Monitoramento ambiental"], responses=ERROS)


def service(db: Session = Depends(get_database_session), user: Usuario = Depends(get_current_user)) -> MonitoramentoService:
    return MonitoramentoService(db, user)


@router.put("/cargas/{carga_id}/monitoramento", response_model=CargaMonitoramentoResponse,
            summary="Declarar ou substituir os dados adicionais da carga")
def configurar(carga_id: UUID, data: CargaMonitoramentoPut, svc: MonitoramentoService = Depends(service)):
    """PUT idempotente, autorizado para ADMIN/GESTOR/OPERADOR da transportadora.

    Identidade Tommy Atkins e lote hipotetico sao declarados pelo operador;
    o produto existente da carga nao e renomeado ou inferido por seu nome.
    """
    return svc.configurar(carga_id, data)


@router.get("/cargas/{carga_id}/monitoramento", response_model=CargaMonitoramentoResponse,
            summary="Consultar os dados adicionais de monitoramento")
def configuracao(carga_id: UUID, svc: MonitoramentoService = Depends(service)):
    return svc.consultar_configuracao(carga_id)


@router.post("/cargas/{carga_id}/monitoramentos", response_model=SessaoResponse, status_code=201,
             responses={200: {"model": SessaoResponse, "description": "Repeticao idempotente da criacao."}},
             summary="Iniciar uma sessao com janela efetiva explicita")
def iniciar(carga_id: UUID, data: SessaoCreate, response: HttpResponse,
            svc: MonitoramentoService = Depends(service)):
    """Exige viagem EM_ANDAMENTO, carga EM_TRANSITO e configuracao valida.

    Chave idempotente por usuario; repeticao igual retorna 200, conteudo diferente 409.
    Inicio nao e a data de cadastro. Nao consulta ou associa medicoes.
    """
    sessao, criada = svc.criar_sessao(carga_id, data)
    response.status_code = 201 if criada else 200
    return sessao


@router.get("/cargas/{carga_id}/monitoramentos", response_model=list[SessaoResponse],
            summary="Listar sessoes da carga com paginacao")
def listar_carga(carga_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                 svc: MonitoramentoService = Depends(service)):
    return svc.listar_carga(carga_id, limit, offset)


@router.get("/viagens/{viagem_id}/monitoramentos", response_model=list[SessaoResponse],
            summary="Listar sessoes da viagem com paginacao")
def listar_viagem(viagem_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                  svc: MonitoramentoService = Depends(service)):
    return svc.listar_viagem(viagem_id, limit, offset)


@router.get("/monitoramentos/{sessao_id}", response_model=SessaoResponse,
            summary="Consultar a sessao e seu snapshot de rastreabilidade")
def consultar(sessao_id: UUID, svc: MonitoramentoService = Depends(service)):
    return svc.consultar_sessao(sessao_id)


@router.post("/monitoramentos/{sessao_id}/encerrar", response_model=SessaoResponse,
             summary="Encerrar uma sessao ativa, com horario e motivo")
def encerrar(sessao_id: UUID, data: SessaoFinalizar, svc: MonitoramentoService = Depends(service)):
    """Transicao imutavel e auditada. Repeticao identica e idempotente."""
    return svc.finalizar(sessao_id, data, "ENCERRADA")


@router.post("/monitoramentos/{sessao_id}/cancelar", response_model=SessaoResponse,
             summary="Cancelar uma sessao ativa, sem apagar sua janela historica")
def cancelar(sessao_id: UUID, data: SessaoFinalizar, svc: MonitoramentoService = Depends(service)):
    return svc.finalizar(sessao_id, data, "CANCELADA")
