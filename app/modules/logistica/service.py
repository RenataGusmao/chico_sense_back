from datetime import datetime, timezone

from fastapi import HTTPException

from app.models.enums import TipoEmpresa, StatusViagem, StatusCarga, StatusCaixa
from app.repositories.logistica import (
    EmpresaOperacionalRepository, VeiculoRepository, MotoristaRepository,
    ViagemRepository, CargaRepository, CaixaRepository,
)
from app.modules.produtos.service import ProdutoService
from app.services.operacional import CrudService, invalid


def company(db, company_id, tipo, active=False):
    record = EmpresaOperacionalRepository(db).get(company_id)
    if record is None:
        raise HTTPException(404, "Empresa nao encontrada.")
    if record.tipo != tipo or (active and not record.ativo):
        invalid("Empresa inativa ou de tipo incompativel.")
    return record


def transition(old, new, allowed):
    if new != old and new not in allowed.get(old, ()):
        invalid("Transicao de status nao permitida.")


def utc(value):
    if value is None:
        return None
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


class VeiculoService(CrudService):
    repository = VeiculoRepository

    def validate(self, values, previous=None, changed=None):
        company(self.db, values["empresa_id"], TipoEmpresa.TRANSPORTADORA, active=previous is None)


class MotoristaService(CrudService):
    repository = MotoristaRepository

    def validate(self, values, previous=None, changed=None):
        company(self.db, values["empresa_id"], TipoEmpresa.TRANSPORTADORA, active=previous is None)


class ViagemService(CrudService):
    repository = ViagemRepository
    transitions = {
        StatusViagem.PLANEJADA: (StatusViagem.EM_ANDAMENTO, StatusViagem.CANCELADA),
        StatusViagem.EM_ANDAMENTO: (StatusViagem.CONCLUIDA,),
    }

    def validate(self, values, previous=None, changed=None):
        status = values.get("status", StatusViagem.PLANEJADA)
        old = previous["status"] if previous else StatusViagem.PLANEJADA
        if previous:
            transition(old, status, self.transitions)
            if old != StatusViagem.PLANEJADA and set(changed) - {"status", "inicio_real", "chegada_em", "observacoes"}:
                invalid("A estrutura de viagem iniciada nao pode ser alterada.")
            if old in (StatusViagem.CONCLUIDA, StatusViagem.CANCELADA) and set(changed) - {"status", "observacoes"}:
                invalid("Viagem encerrada permite somente observacoes.")
        active = previous is None or old != status and status == StatusViagem.EM_ANDAMENTO
        company(self.db, values["transportadora_id"], TipoEmpresa.TRANSPORTADORA, active)
        vehicle = VeiculoService(self.db).get(values["veiculo_id"])
        driver = MotoristaService(self.db).get(values["motorista_id"])
        if vehicle.empresa_id != values["transportadora_id"] or driver.empresa_id != values["transportadora_id"]:
            invalid("Veiculo e motorista devem pertencer a transportadora da viagem.")
        if (active or changed and ({"veiculo_id", "motorista_id"} & set(changed))) and (not vehicle.ativo or not driver.ativo):
            invalid("Veiculo e motorista devem estar ativos.")
        if old != status:
            if status == StatusViagem.EM_ANDAMENTO and values.get("inicio_real") is None:
                values["inicio_real"] = datetime.now(timezone.utc)
            if status == StatusViagem.CONCLUIDA and values.get("chegada_em") is None:
                values["chegada_em"] = datetime.now(timezone.utc)
        time_fields = {"saida_em", "previsao_chegada_em", "inicio_real", "chegada_em"}
        if previous and old == status and not time_fields.intersection(changed):
            # Existing historical trips may predate the new inicio_real column.
            return
        start, end = utc(values.get("saida_em")), utc(values.get("previsao_chegada_em"))
        if end and end < start:
            invalid("Previsao de chegada anterior a saida prevista.")
        real, arrival = utc(values.get("inicio_real")), utc(values.get("chegada_em"))
        if arrival and (real is None or arrival < real):
            invalid("Chegada real requer inicio real anterior.")
        if status == StatusViagem.PLANEJADA and (real or arrival):
            invalid("Viagem planejada nao possui inicio ou chegada real.")
        if status == StatusViagem.EM_ANDAMENTO and (real is None or arrival):
            invalid("Viagem em andamento requer inicio real e nao pode ter chegada real.")
        if status == StatusViagem.CONCLUIDA and (real is None or arrival is None):
            invalid("Viagem concluida requer inicio e chegada reais.")


class CargaService(CrudService):
    repository = CargaRepository
    transitions = {
        StatusCarga.PLANEJADA: (StatusCarga.EM_TRANSITO, StatusCarga.CANCELADA),
        StatusCarga.EM_TRANSITO: (StatusCarga.ENTREGUE,),
    }

    def validate(self, values, previous=None, changed=None):
        trip = ViagemService(self.db).get(values["viagem_id"])
        product = ProdutoService(self.db).get(values["produto_id"])
        company(self.db, values["produtor_id"], TipoEmpresa.PRODUTOR, active=previous is None)
        if values.get("cliente_id"):
            company(self.db, values["cliente_id"], TipoEmpresa.CLIENTE, active=previous is None)
        if previous is None and (not product.ativo or trip.status in (StatusViagem.CONCLUIDA, StatusViagem.CANCELADA)):
            invalid("Carga exige produto ativo e viagem aberta.")
        if bool(values.get("quantidade") is not None) != bool(values.get("unidade")):
            invalid("Quantidade e unidade devem ser informadas juntas.")
        if previous:
            status = values["status"]
            transition(previous["status"], status, self.transitions)
            if previous["status"] in (StatusCarga.ENTREGUE, StatusCarga.CANCELADA) and set(changed) - {"status", "observacoes"}:
                invalid("Carga encerrada permite somente observacoes.")
            if status != previous["status"]:
                if status == StatusCarga.EM_TRANSITO and trip.status != StatusViagem.EM_ANDAMENTO:
                    invalid("Carga em transito exige viagem em andamento.")
                if status == StatusCarga.ENTREGUE and trip.status not in (StatusViagem.EM_ANDAMENTO, StatusViagem.CONCLUIDA):
                    invalid("Entrega exige viagem iniciada.")

    def list_for_trip(self, trip_id, filters, limit, offset):
        ViagemService(self.db).get(trip_id)
        return self.list(filters | {"viagem_id": trip_id}, limit, offset)


class CaixaService(CrudService):
    repository = CaixaRepository
    transitions = {
        StatusCaixa.REGISTRADA: (StatusCaixa.EM_TRANSITO, StatusCaixa.AVARIADA),
        StatusCaixa.EM_TRANSITO: (StatusCaixa.ENTREGUE, StatusCaixa.AVARIADA),
    }

    def validate(self, values, previous=None, changed=None):
        cargo = CargaService(self.db).get(values["carga_id"])
        if previous is None and cargo.status in (StatusCarga.ENTREGUE, StatusCarga.CANCELADA):
            invalid("Nao e possivel adicionar caixa a carga encerrada.")
        if previous is None:
            trip = ViagemService(self.db).get(cargo.viagem_id)
            if trip.status == StatusViagem.CANCELADA:
                invalid("Nao e possivel adicionar caixa a viagem cancelada.")
        if previous:
            status = values["status"]
            transition(previous["status"], status, self.transitions)
            if previous["status"] in (StatusCaixa.ENTREGUE, StatusCaixa.AVARIADA) and set(changed) - {"status", "observacoes"}:
                invalid("Caixa encerrada permite somente observacoes.")
            if status != previous["status"]:
                if status == StatusCaixa.EM_TRANSITO and cargo.status != StatusCarga.EM_TRANSITO:
                    invalid("Caixa em transito exige carga em transito.")
                if status == StatusCaixa.ENTREGUE and cargo.status not in (StatusCarga.EM_TRANSITO, StatusCarga.ENTREGUE):
                    invalid("Entrega exige carga em transito ou entregue.")

    def list_for_cargo(self, cargo_id, limit, offset):
        CargaService(self.db).get(cargo_id)
        return self.list({"carga_id": cargo_id}, limit, offset)
