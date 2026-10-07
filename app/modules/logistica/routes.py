from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_database_session
from app.modules.logistica.schemas import (
    VeiculoCreate, VeiculoUpdate, VeiculoResponse, MotoristaCreate, MotoristaUpdate,
    MotoristaResponse, ViagemCreate, ViagemUpdate, ViagemResponse, CargaCreate,
    CargaUpdate, CargaResponse, CaixaCreate, CaixaUpdate, CaixaResponse,
)
from app.models.enums import StatusViagem, StatusCarga
from app.modules.logistica.service import (
    VeiculoService, MotoristaService, ViagemService, CargaService, CaixaService,
)

router = APIRouter(prefix="/api/v1", tags=["Logistica"])


@router.post("/veiculos", response_model=VeiculoResponse, status_code=201)
def create_veiculos(data: VeiculoCreate, db: Session = Depends(get_database_session)):
    return VeiculoService(db).create(data)


@router.get("/veiculos", response_model=list[VeiculoResponse])
def list_veiculos(
    empresa_id: UUID | None = None,
    ativo: bool | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    db: Session = Depends(get_database_session),
):
    return VeiculoService(db).list({"empresa_id": empresa_id, "ativo": ativo}, limit, offset)


@router.get("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def get_veiculos(veiculo_id: UUID, db: Session = Depends(get_database_session)):
    return VeiculoService(db).get(veiculo_id)


@router.patch("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def update_veiculos(veiculo_id: UUID, data: VeiculoUpdate, db: Session = Depends(get_database_session)):
    return VeiculoService(db).update(veiculo_id, data)


@router.post("/motoristas", response_model=MotoristaResponse, status_code=201)
def create_motoristas(data: MotoristaCreate, db: Session = Depends(get_database_session)):
    return MotoristaService(db).create(data)


@router.get("/motoristas", response_model=list[MotoristaResponse])
def list_motoristas(
    empresa_id: UUID | None = None,
    ativo: bool | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    db: Session = Depends(get_database_session),
):
    return MotoristaService(db).list({"empresa_id": empresa_id, "ativo": ativo}, limit, offset)


@router.get("/motoristas/{motorista_id}", response_model=MotoristaResponse)
def get_motoristas(motorista_id: UUID, db: Session = Depends(get_database_session)):
    return MotoristaService(db).get(motorista_id)


@router.patch("/motoristas/{motorista_id}", response_model=MotoristaResponse)
def update_motoristas(motorista_id: UUID, data: MotoristaUpdate, db: Session = Depends(get_database_session)):
    return MotoristaService(db).update(motorista_id, data)


@router.post("/viagens", response_model=ViagemResponse, status_code=201)
def create_viagens(data: ViagemCreate, db: Session = Depends(get_database_session)):
    return ViagemService(db).create(data)


@router.get("/viagens", response_model=list[ViagemResponse])
def list_viagens(
    empresa_id: UUID | None = None,
    status: StatusViagem | None = None,
    veiculo_id: UUID | None = None,
    motorista_id: UUID | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    db: Session = Depends(get_database_session),
):
    return ViagemService(db).list({"transportadora_id": empresa_id, "status": status, "veiculo_id": veiculo_id, "motorista_id": motorista_id}, limit, offset)


@router.get("/viagens/{viagem_id}", response_model=ViagemResponse)
def get_viagens(viagem_id: UUID, db: Session = Depends(get_database_session)):
    return ViagemService(db).get(viagem_id)


@router.patch("/viagens/{viagem_id}", response_model=ViagemResponse)
def update_viagens(viagem_id: UUID, data: ViagemUpdate, db: Session = Depends(get_database_session)):
    return ViagemService(db).update(viagem_id, data)


@router.post("/viagens/{viagem_id}/cargas", response_model=CargaResponse, status_code=201)
def create_carga(viagem_id: UUID, data: CargaCreate, db: Session = Depends(get_database_session)):
    return CargaService(db).create(data, viagem_id=viagem_id)


@router.get("/viagens/{viagem_id}/cargas", response_model=list[CargaResponse])
def list_cargas(viagem_id: UUID, produto_id: UUID | None = None, status: StatusCarga | None = None,
                limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                db: Session = Depends(get_database_session)):
    return CargaService(db).list_for_trip(viagem_id, {"produto_id": produto_id, "status": status}, limit, offset)


@router.get("/cargas/{carga_id}", response_model=CargaResponse)
def get_carga(carga_id: UUID, db: Session = Depends(get_database_session)):
    return CargaService(db).get(carga_id)


@router.patch("/cargas/{carga_id}", response_model=CargaResponse)
def update_carga(carga_id: UUID, data: CargaUpdate, db: Session = Depends(get_database_session)):
    return CargaService(db).update(carga_id, data)


@router.post("/cargas/{carga_id}/caixas", response_model=CaixaResponse, status_code=201)
def create_caixa(carga_id: UUID, data: CaixaCreate, db: Session = Depends(get_database_session)):
    return CaixaService(db).create(data, carga_id=carga_id)


@router.get("/cargas/{carga_id}/caixas", response_model=list[CaixaResponse])
def list_caixas(carga_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                db: Session = Depends(get_database_session)):
    return CaixaService(db).list_for_cargo(carga_id, limit, offset)


@router.get("/caixas/{caixa_id}", response_model=CaixaResponse)
def get_caixa(caixa_id: UUID, db: Session = Depends(get_database_session)):
    return CaixaService(db).get(caixa_id)


@router.patch("/caixas/{caixa_id}", response_model=CaixaResponse)
def update_caixa(caixa_id: UUID, data: CaixaUpdate, db: Session = Depends(get_database_session)):
    return CaixaService(db).update(caixa_id, data)
