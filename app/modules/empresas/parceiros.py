"""Minimal commercial selection without exposing company documents or users."""
from uuid import UUID
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Field
from sqlalchemy import exists, or_, select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_database_session
from app.models.empresa import Empresa
from app.models.enums import TipoEmpresa
from app.models.logistica import Carga, Viagem
from app.models.parceiro_comercial import ParceiroComercial
from app.models.usuario import Usuario
from app.modules.empresas.service import EmpresaService
from app.modules.logistica.escopo import EscopoLogistico
from app.schemas.operacional import Input, Response
from app.services.persistence import commit


class Aprovacao(Input):
    ativo: bool
    justificativa: str = Field(min_length=1, max_length=2000)


class VinculoComercialResponse(Response):
    transportadora_id: UUID
    empresa_id: UUID
    ativo: bool
    aprovado_por_id: UUID
    atualizado_por_id: UUID
    justificativa: str


class ParceiroResponse(Input):
    id: UUID
    nome: str
    tipo: TipoEmpresa
    ativo: bool
    aprovado: bool
    autorizado_para_novas_cargas: bool


class ParceirosService:
    def __init__(self, db, user):
        self.db, self.user = db, user
        self.escopo = EscopoLogistico(db, user)

    def transportadora(self, empresa_id):
        self.escopo.autorizar_operacao(empresa_id)
        empresa = EmpresaService(self.db).get(empresa_id)
        if empresa.tipo != TipoEmpresa.TRANSPORTADORA or not empresa.ativo:
            raise HTTPException(409, 'Transportadora ativa obrigatoria.')
        return empresa

    def aprovado(self, carrier_id, company_id):
        return self.db.scalar(select(ParceiroComercial.id).join(Empresa, Empresa.id == ParceiroComercial.empresa_id).where(
            ParceiroComercial.transportadora_id == carrier_id, ParceiroComercial.empresa_id == company_id,
            ParceiroComercial.ativo.is_(True), Empresa.ativo.is_(True),
            Empresa.tipo.in_([TipoEmpresa.PRODUTOR, TipoEmpresa.CLIENTE]),
        ).with_for_update(of=ParceiroComercial)) is not None

    def exigir(self, carrier_id, company_id):
        if company_id and not self.escopo.admin and not self.aprovado(carrier_id, company_id):
            raise HTTPException(403, 'Parceiro comercial nao aprovado para esta transportadora.')

    def listar(self, carrier_id, tipo, limit, offset, incluir_historico=False):
        self.transportadora(carrier_id)
        if self.user.perfil.nome not in ('ADMIN', 'GESTOR', 'OPERADOR'):
            raise HTTPException(403, 'Catalogo comercial exige perfil operacional.')
        approved = exists(select(ParceiroComercial.id).where(
            ParceiroComercial.transportadora_id == carrier_id, ParceiroComercial.empresa_id == Empresa.id,
            ParceiroComercial.ativo.is_(True)))
        permitted = approved
        if incluir_historico:
            history = exists(select(Carga.id).join(Viagem, Viagem.id == Carga.viagem_id).where(
                Viagem.transportadora_id == carrier_id, or_(Carga.produtor_id == Empresa.id, Carga.cliente_id == Empresa.id)))
            permitted = or_(approved, history)
        # ADMIN can select any active producer/client to approve. Ordinary users
        # never gain that global catalog, nor company membership from this table.
        if self.escopo.admin:
            permitted = True
        query = select(Empresa, approved.label('approved')).where(Empresa.ativo.is_(True),
            Empresa.tipo.in_([TipoEmpresa.PRODUTOR, TipoEmpresa.CLIENTE]), permitted)
        if tipo: query = query.where(Empresa.tipo == tipo)
        return [dict(id=e.id, nome=e.nome, tipo=e.tipo, ativo=e.ativo, aprovado=bool(grant),
                     autorizado_para_novas_cargas=bool(grant or self.escopo.admin))
                for e, grant in self.db.execute(query.order_by(Empresa.nome, Empresa.id).limit(limit).offset(offset))]

    def aprovar(self, carrier_id, company_id, data):
        if not self.escopo.admin:
            raise HTTPException(403, 'Aprovacao comercial exige ADMIN.')
        self.transportadora(carrier_id)
        company = EmpresaService(self.db).get(company_id)
        if company.tipo not in (TipoEmpresa.PRODUTOR, TipoEmpresa.CLIENTE) or (data.ativo and not company.ativo):
            raise HTTPException(409, 'Parceiro deve ser produtor/cliente ativo para aprovacao.')
        row = self.db.scalar(select(ParceiroComercial).where(ParceiroComercial.transportadora_id == carrier_id,
            ParceiroComercial.empresa_id == company_id).with_for_update())
        if row is None:
            row = ParceiroComercial(transportadora_id=carrier_id, empresa_id=company_id,
                aprovado_por_id=self.user.id, atualizado_por_id=self.user.id, **data.model_dump())
            self.db.add(row)
        else:
            row.ativo, row.justificativa, row.atualizado_por_id = data.ativo, data.justificativa, self.user.id
        commit(self.db)
        self.db.refresh(row)
        return row


router = APIRouter(prefix='/api/v1/transportadoras', tags=['Parceiros comerciais'])


@router.get('/{transportadora_id}/parceiros', response_model=list[ParceiroResponse])
def parceiros(transportadora_id: UUID, tipo: Literal['PRODUTOR', 'CLIENTE'] | None = None,
              incluir_historico: bool = False, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
              db: Session = Depends(get_database_session), user: Usuario = Depends(get_current_user)):
    return ParceirosService(db, user).listar(transportadora_id, tipo, limit, offset, incluir_historico)


@router.put('/{transportadora_id}/parceiros/{empresa_id}', response_model=VinculoComercialResponse)
def aprovar(transportadora_id: UUID, empresa_id: UUID, data: Aprovacao,
            db: Session = Depends(get_database_session), user: Usuario = Depends(get_current_user)):
    return ParceirosService(db, user).aprovar(transportadora_id, empresa_id, data)
