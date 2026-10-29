from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_database_session, get_current_user
from app.models.usuario import Usuario
from app.models.logistica import Veiculo, Motorista, Viagem, Carga, Caixa
from app.modules.logistica.access import LogisticaAccess, ERROS_ACESSO
from app.modules.logistica.schemas import (
    VeiculoCreate, VeiculoUpdate, VeiculoResponse, MotoristaCreate, MotoristaUpdate,
    MotoristaResponse, ViagemCreate, ViagemUpdate, ViagemResponse, CargaCreate,
    CargaUpdate, CargaResponse, CaixaCreate, CaixaUpdate, CaixaResponse,
)
from app.models.enums import StatusViagem, StatusCarga

router = APIRouter(prefix="/api/v1", tags=["Logistica"], responses=ERROS_ACESSO)


def authorized(db: Session = Depends(get_database_session), user: Usuario = Depends(get_current_user)):
    return LogisticaAccess(db, user)


@router.post("/veiculos", response_model=VeiculoResponse, status_code=201)
def create_veiculos(data: VeiculoCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Veiculo, data)


@router.get("/veiculos", response_model=list[VeiculoResponse])
def list_veiculos(
    empresa_id: UUID | None = None,
    ativo: bool | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    access: LogisticaAccess = Depends(authorized),
):
    return access.list_owned(Veiculo, {"empresa_id": empresa_id, "ativo": ativo}, limit, offset)


@router.get("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def get_veiculos(veiculo_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Veiculo, veiculo_id)


@router.patch("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def update_veiculos(veiculo_id: UUID, data: VeiculoUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Veiculo, veiculo_id, data)


@router.post("/motoristas", response_model=MotoristaResponse, status_code=201)
def create_motoristas(data: MotoristaCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Motorista, data)


@router.get("/motoristas", response_model=list[MotoristaResponse])
def list_motoristas(
    empresa_id: UUID | None = None,
    ativo: bool | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    access: LogisticaAccess = Depends(authorized),
):
    return access.list_owned(Motorista, {"empresa_id": empresa_id, "ativo": ativo}, limit, offset)


@router.get("/motoristas/{motorista_id}", response_model=MotoristaResponse)
def get_motoristas(motorista_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Motorista, motorista_id)


@router.patch("/motoristas/{motorista_id}", response_model=MotoristaResponse)
def update_motoristas(motorista_id: UUID, data: MotoristaUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Motorista, motorista_id, data)


@router.post("/viagens", response_model=ViagemResponse, status_code=201)
def create_viagens(data: ViagemCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Viagem, data)


@router.get("/viagens", response_model=list[ViagemResponse])
def list_viagens(
    empresa_id: UUID | None = None,
    status: StatusViagem | None = None,
    veiculo_id: UUID | None = None,
    motorista_id: UUID | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    access: LogisticaAccess = Depends(authorized),
):
    return access.list_owned(Viagem, {"transportadora_id": empresa_id, "status": status, "veiculo_id": veiculo_id, "motorista_id": motorista_id}, limit, offset)


@router.get("/viagens/{viagem_id}", response_model=ViagemResponse)
def get_viagens(viagem_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Viagem, viagem_id)


@router.patch("/viagens/{viagem_id}", response_model=ViagemResponse)
def update_viagens(viagem_id: UUID, data: ViagemUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Viagem, viagem_id, data)


@router.post("/viagens/{viagem_id}/cargas", response_model=CargaResponse, status_code=201)
def create_carga(viagem_id: UUID, data: CargaCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Carga, data, parent_id=viagem_id)


@router.get("/viagens/{viagem_id}/cargas", response_model=list[CargaResponse])
def list_cargas(viagem_id: UUID, produto_id: UUID | None = None, status: StatusCarga | None = None,
                limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                access: LogisticaAccess = Depends(authorized)):
    return access.list_cargas(viagem_id, {"produto_id": produto_id, "status": status}, limit, offset)


@router.get("/cargas/{carga_id}", response_model=CargaResponse)
def get_carga(carga_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Carga, carga_id)


@router.patch("/cargas/{carga_id}", response_model=CargaResponse)
def update_carga(carga_id: UUID, data: CargaUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Carga, carga_id, data)


@router.post("/cargas/{carga_id}/caixas", response_model=CaixaResponse, status_code=201)
def create_caixa(carga_id: UUID, data: CaixaCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Caixa, data, parent_id=carga_id)


@router.get("/cargas/{carga_id}/caixas", response_model=list[CaixaResponse])
def list_caixas(carga_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                access: LogisticaAccess = Depends(authorized)):
    return access.list_caixas(carga_id, limit, offset)


@router.get("/caixas/{caixa_id}", response_model=CaixaResponse)
def get_caixa(caixa_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Caixa, caixa_id)


@router.patch("/caixas/{caixa_id}", response_model=CaixaResponse)
def update_caixa(caixa_id: UUID, data: CaixaUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Caixa, caixa_id, data)
