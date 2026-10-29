"""JWT-backed access boundary for legacy logistics, without changing business services."""
from fastapi import HTTPException
from sqlalchemy import select
from app.models.empresa import Empresa
from app.models.usuario import EmpresaUsuario
from app.models.logistica import Veiculo,Motorista,Viagem,Carga,Caixa
from app.models.enums import TipoEmpresa
from app.modules.empresas.service import EmpresaService
from app.modules.logistica.service import VeiculoService,MotoristaService,ViagemService,CargaService,CaixaService

SERVICES={Veiculo:VeiculoService,Motorista:MotoristaService,Viagem:ViagemService,Carga:CargaService,Caixa:CaixaService}
ERROS_ACESSO={401:{'description':'JWT ausente, invalido, expirado ou usuario inativo.'},
    403:{'description':'Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado.'},
    404:{'description':'Recurso inexistente.'},409:{'description':'Conflito de integridade ou transportadora inativa para escrita.'}}


class LogisticaAccess:
    def __init__(self,db,user):
        self.db,self.user=db,user

    def perfil(self,write=False,gestao=False):
        allowed=('ADMIN','GESTOR') if gestao else (('ADMIN','GESTOR','OPERADOR') if write else ('ADMIN','GESTOR','OPERADOR','CONSULTA'))
        if not self.user.ativo or not self.user.perfil or self.user.perfil.nome not in allowed:
            raise HTTPException(403,'Perfil sem permissao para esta operacao logistica.')

    def company(self,company_id,write=False):
        company=EmpresaService(self.db).authorize(company_id,self.user)
        if write and not company.ativo:
            raise HTTPException(409,'Transportadora inativa nao permite escrita logistica.')
        return company

    def resource(self,model,record_id,write=False):
        self.perfil(write,gestao=write and model in (Veiculo,Motorista))
        record=SERVICES[model](self.db).get(record_id)
        if model in (Veiculo,Motorista): self.company(record.empresa_id,write)
        elif model is Viagem: self.company(record.transportadora_id,write)
        elif model is Carga: self.resource(Viagem,record.viagem_id,write)
        elif model is Caixa: self.resource(Carga,record.carga_id,write)
        return record

    def trip_references(self,data):
        # Client-provided IDs are references, never grants of authorization.
        for name,model in [('veiculo_id',Veiculo),('motorista_id',Motorista)]:
            value=getattr(data,name,None)
            if value is not None: self.resource(model,value)

    def create(self,model,data,parent_id=None):
        self.perfil(True,gestao=model in (Veiculo,Motorista))
        service=SERVICES[model](self.db)
        if model in (Veiculo,Motorista):
            self.company(data.empresa_id,True)
            return service.create(data)
        if model is Viagem:
            self.company(data.transportadora_id,True); self.trip_references(data)
            return service.create(data)
        if model is Carga:
            self.resource(Viagem,parent_id,True)
            return service.create(data,viagem_id=parent_id)
        self.resource(Carga,parent_id,True)
        return service.create(data,carga_id=parent_id)

    def update(self,model,record_id,data):
        self.resource(model,record_id,True)
        if model is Viagem: self.trip_references(data)
        return SERVICES[model](self.db).update(record_id,data)

    def list_owned(self,model,filters,limit,offset):
        self.perfil()
        owner='transportadora_id' if model is Viagem else 'empresa_id'
        if filters.get(owner) is not None: self.company(filters[owner])
        query=select(model)
        if self.user.perfil.nome!='ADMIN':
            companies=select(EmpresaUsuario.empresa_id).join(Empresa,Empresa.id==EmpresaUsuario.empresa_id).where(
                EmpresaUsuario.usuario_id==self.user.id,EmpresaUsuario.ativo.is_(True),
                Empresa.ativo.is_(True),Empresa.tipo==TipoEmpresa.TRANSPORTADORA)
            query=query.where(getattr(model,owner).in_(companies))
        for name,value in filters.items():
            if value is not None: query=query.where(getattr(model,name)==value)
        # Scope in SQL before limit/offset: no unscoped pagination or in-memory filtering.
        return list(self.db.scalars(query.order_by(model.created_at,model.id).limit(limit).offset(offset)))

    def list_cargas(self,trip_id,filters,limit,offset):
        self.resource(Viagem,trip_id)
        return CargaService(self.db).list_for_trip(trip_id,filters,limit,offset)

    def list_caixas(self,cargo_id,limit,offset):
        self.resource(Carga,cargo_id)
        return CaixaService(self.db).list_for_cargo(cargo_id,limit,offset)
