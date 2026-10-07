from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.models.enums import TipoEmpresa
from app.models.logistica import Veiculo, Motorista, Viagem, Carga
from app.models.usuario import EmpresaUsuario, Usuario


class EmpresaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, company_id: UUID) -> Empresa | None:
        return self.db.get(Empresa, company_id)

    def has_incompatible_logistics_links(self, company_id: UUID, new_type: TipoEmpresa) -> bool:
        links = (
            (TipoEmpresa.TRANSPORTADORA, Veiculo.empresa_id),
            (TipoEmpresa.TRANSPORTADORA, Motorista.empresa_id),
            (TipoEmpresa.TRANSPORTADORA, Viagem.transportadora_id),
            (TipoEmpresa.PRODUTOR, Carga.produtor_id),
            (TipoEmpresa.CLIENTE, Carga.cliente_id),
        )
        for required_type, company_column in links:
            if new_type != required_type:
                query = select(select(company_column).where(company_column == company_id).exists())
                if self.db.scalar(query):
                    return True
        return False

    def list(self, offset: int, limit: int, user_id: UUID | None = None) -> list[Empresa]:
        query = select(Empresa)
        if user_id is not None:
            query = query.join(EmpresaUsuario).where(EmpresaUsuario.usuario_id == user_id, EmpresaUsuario.ativo.is_(True), Empresa.ativo.is_(True))
        return list(self.db.scalars(query.order_by(Empresa.created_at, Empresa.id).offset(offset).limit(limit)))


class EmpresaUsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, company_id: UUID, user_id: UUID) -> EmpresaUsuario | None:
        return self.db.scalar(select(EmpresaUsuario).where(EmpresaUsuario.empresa_id == company_id, EmpresaUsuario.usuario_id == user_id))

    def companies(self, user_id: UUID) -> list[Empresa]:
        return list(self.db.scalars(select(Empresa).join(EmpresaUsuario).where(EmpresaUsuario.usuario_id == user_id, EmpresaUsuario.ativo.is_(True), Empresa.ativo.is_(True)).order_by(Empresa.nome, Empresa.id)))

    def users(self, company_id: UUID, offset: int, limit: int) -> list[Usuario]:
        return list(self.db.scalars(select(Usuario).join(EmpresaUsuario).where(EmpresaUsuario.empresa_id == company_id, EmpresaUsuario.ativo.is_(True)).order_by(Usuario.created_at, Usuario.id).offset(offset).limit(limit)))
