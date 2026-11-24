"""Stored company links define cargo-level reads; only carriers may operate."""
from fastapi import HTTPException
from sqlalchemy import and_, exists, or_, select, true

from app.models.empresa import Empresa
from app.models.enums import TipoEmpresa
from app.models.logistica import Carga, Viagem
from app.models.usuario import EmpresaUsuario
from app.modules.empresas.service import EmpresaService


class EscopoLogistico:
    def __init__(self, db, user):
        self.db, self.user = db, user

    @property
    def admin(self):
        return bool(self.user.ativo and self.user.perfil and self.user.perfil.nome == "ADMIN")

    def _leitor(self):
        if not self.user.ativo or not self.user.perfil or self.user.perfil.nome not in ("ADMIN", "GESTOR", "OPERADOR", "CONSULTA"):
            raise HTTPException(403, "Perfil sem permissao para consulta logistica.")

    def empresas(self, tipo):
        return select(Empresa.id).join(EmpresaUsuario, EmpresaUsuario.empresa_id == Empresa.id).where(
            EmpresaUsuario.usuario_id == self.user.id, EmpresaUsuario.ativo.is_(True),
            Empresa.ativo.is_(True), Empresa.tipo == tipo,
        )

    def _viagens_ativas(self):
        return select(Viagem.id).join(Empresa, Empresa.id == Viagem.transportadora_id).where(
            Empresa.ativo.is_(True), Empresa.tipo == TipoEmpresa.TRANSPORTADORA,
        )

    def condicao_carga(self):
        self._leitor()
        if self.admin:
            return true()
        transportadas = select(Viagem.id).where(
            Viagem.transportadora_id.in_(self.empresas(TipoEmpresa.TRANSPORTADORA)),
        )
        return and_(Carga.viagem_id.in_(self._viagens_ativas()), or_(
            Carga.viagem_id.in_(transportadas),
            Carga.produtor_id.in_(self.empresas(TipoEmpresa.PRODUTOR)),
            Carga.cliente_id.in_(self.empresas(TipoEmpresa.CLIENTE)),
        ))

    def cargas_visiveis(self):
        return select(Carga.id).where(self.condicao_carga())

    def condicao_viagem(self):
        self._leitor()
        if self.admin:
            return true()
        # A carrier can read an empty trip; external companies need a cargo of theirs.
        propria = Viagem.transportadora_id.in_(self.empresas(TipoEmpresa.TRANSPORTADORA))
        relacionada = exists(select(Carga.id).where(
            Carga.viagem_id == Viagem.id, or_(
                Carga.produtor_id.in_(self.empresas(TipoEmpresa.PRODUTOR)),
                Carga.cliente_id.in_(self.empresas(TipoEmpresa.CLIENTE)),
            ),
        ))
        return and_(Viagem.id.in_(self._viagens_ativas()), or_(propria, relacionada))

    def autorizar_carga(self, carga_id):
        if self.db.scalar(select(Carga.id).where(Carga.id == carga_id, self.condicao_carga())) is None:
            raise HTTPException(403, "Acesso ao recurso nao permitido.")

    def autorizar_viagem(self, viagem_id):
        if self.db.scalar(select(Viagem.id).where(Viagem.id == viagem_id, self.condicao_viagem())) is None:
            raise HTTPException(403, "Acesso ao recurso nao permitido.")

    def opera_transportadora(self, empresa_id):
        """Never derive a write grant from ownership of the producer/client cargo."""
        if self.admin:
            return True
        self._leitor()
        return self.db.scalar(select(Empresa.id).where(
            Empresa.id == empresa_id, Empresa.id.in_(self.empresas(TipoEmpresa.TRANSPORTADORA)),
        )) is not None

    def autorizar_operacao(self, empresa_id):
        # Existing company policy preserves ADMIN cleanup of inactive carriers.
        EmpresaService(self.db).authorize(empresa_id, self.user)
        if not self.opera_transportadora(empresa_id):
            raise HTTPException(403, "Operacao exige vinculo com a transportadora.")

    def autorizar_filtro_transportadora(self, empresa_id):
        if self.admin:
            EmpresaService(self.db).get(empresa_id)
            return
        if self.opera_transportadora(empresa_id):
            return
        if self.db.scalar(select(Viagem.id).where(
            Viagem.transportadora_id == empresa_id, self.condicao_viagem(),
        ).limit(1)) is None:
            raise HTTPException(403, "Acesso ao recurso nao permitido.")
