"""One SQL statement over authorized resources, not a scan of every API page."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_database_session
from app.models.usuario import Usuario
from app.models.logistica import Carga, Viagem
from app.models.monitoramento import Alerta
from app.models.enums import StatusAlerta, StatusViagem
from app.models.sessoes_monitoramento import CargaMonitoramento, SessaoMonitoramento
from app.modules.logistica.escopo import EscopoLogistico
from app.schemas.operacional import Input


class ResumoResponse(Input):
    consultado_em: datetime
    viagens_total: int
    viagens_em_transito: int
    cargas_total: int
    cargas_monitoradas: int
    sessoes_ativas: int
    alertas_abertos: int


router = APIRouter(prefix='/api/v1/monitoramento', tags=['Resumo autorizado'])


@router.get('/resumo', response_model=ResumoResponse)
def resumo(db: Session = Depends(get_database_session), user: Usuario = Depends(get_current_user)):
    scope = EscopoLogistico(db, user)
    cargos = scope.cargas_visiveis()
    trips = select(Viagem.id).where(scope.condicao_viagem())
    def count(model, *conditions):
        return select(func.count()).select_from(model).where(*conditions).scalar_subquery()
    # Cargo-level conditions remain essential for mixed producer/client trips.
    statement = select(
        count(Viagem, Viagem.id.in_(trips)).label('viagens_total'),
        count(Viagem, Viagem.id.in_(trips), Viagem.status == StatusViagem.EM_ANDAMENTO).label('viagens_em_transito'),
        count(Carga, Carga.id.in_(cargos)).label('cargas_total'),
        count(CargaMonitoramento, CargaMonitoramento.carga_id.in_(cargos)).label('cargas_monitoradas'),
        count(SessaoMonitoramento, SessaoMonitoramento.carga_id.in_(cargos), SessaoMonitoramento.estado == 'ATIVA').label('sessoes_ativas'),
        count(Alerta, Alerta.carga_id.in_(cargos), Alerta.status.in_([StatusAlerta.ABERTO, StatusAlerta.EM_ANALISE])).label('alertas_abertos'),
    )
    return dict(db.execute(statement).mappings().one()) | {'consultado_em': datetime.now(timezone.utc)}
