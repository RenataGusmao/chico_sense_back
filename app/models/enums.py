from enum import Enum


class TipoEmpresa(str, Enum):
    PRODUTOR = "PRODUTOR"
    TRANSPORTADORA = "TRANSPORTADORA"
    CLIENTE = "CLIENTE"


class StatusViagem(str, Enum):
    PLANEJADA = "PLANEJADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"


class StatusCarga(str, Enum):
    PLANEJADA = "PLANEJADA"
    EM_TRANSITO = "EM_TRANSITO"
    ENTREGUE = "ENTREGUE"
    CANCELADA = "CANCELADA"


class StatusCaixa(str, Enum):
    REGISTRADA = "REGISTRADA"
    EM_TRANSITO = "EM_TRANSITO"
    ENTREGUE = "ENTREGUE"
    AVARIADA = "AVARIADA"


class StatusDispositivo(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    MANUTENCAO = "MANUTENCAO"


class TipoSensor(str, Enum):
    TEMPERATURA = "TEMPERATURA"
    UMIDADE = "UMIDADE"


class ContextoMedicao(str, Enum):
    AMBIENTE = "AMBIENTE"
    PRODUTO = "PRODUTO"
    CAIXA = "CAIXA"
    PROTOTIPO = "PROTOTIPO"


class StatusSensor(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    MANUTENCAO = "MANUTENCAO"


class NivelAlerta(str, Enum):
    INFORMATIVO = "INFORMATIVO"
    ATENCAO = "ATENCAO"
    CRITICO = "CRITICO"


class StatusAlerta(str, Enum):
    ABERTO = "ABERTO"
    EM_ANALISE = "EM_ANALISE"
    RESOLVIDO = "RESOLVIDO"
    DESCARTADO = "DESCARTADO"
