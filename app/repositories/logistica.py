from app.models.empresa import Empresa
from app.models.logistica import Veiculo, Motorista, Viagem, Carga, Caixa
from app.repositories.operacional import Repository


class EmpresaOperacionalRepository(Repository):
    model = Empresa


class VeiculoRepository(Repository):
    model = Veiculo


class MotoristaRepository(Repository):
    model = Motorista


class ViagemRepository(Repository):
    model = Viagem


class CargaRepository(Repository):
    model = Carga


class CaixaRepository(Repository):
    model = Caixa
