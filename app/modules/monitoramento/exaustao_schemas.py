"""Virtual-only public API; inputs cannot address hardware or set clocks/states."""
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import Field,field_validator
from app.schemas.operacional import Input,Response
from app.modules.monitoramento.service import utc

EstadoIntervencao=Literal['SOLICITADA','AUTORIZADA','RECUSADA','EM_EXECUCAO','CONCLUIDA','CANCELADA','FALHA_SIMULACAO']
AcaoHumana=Literal['AUTORIZAR','RECUSAR','INICIAR','ENCERRAR','CANCELAR','REGISTRAR_FALHA']


class IntervencaoCreate(Input):
    chave_idempotencia:UUID
    justificativa:str=Field(min_length=1,max_length=4000)
    duracao_planejada_s:Decimal=Field(gt=0,le=86400,max_digits=12,decimal_places=3,
        description='Duracao de demonstracao, ate 24h; sem eficacia cientifica ou encerramento automatico.')
    alerta_id:UUID|None=None
    avaliacao_id:UUID|None=None
    analise_etileno_id:UUID|None=None


class AcaoCreate(Input):
    chave_idempotencia:UUID
    acao:AcaoHumana
    justificativa:str=Field(min_length=1,max_length=4000)


class UTCResponse(Response):
    @field_validator('created_at','updated_at')
    @classmethod
    def normalizar(cls,v): return utc(v)


class IntervencaoResponse(UTCResponse):
    sessao_id:UUID
    viagem_id:UUID
    carga_id:UUID
    veiculo_id:UUID
    atuador_virtual_id:str
    alerta_id:UUID|None
    avaliacao_id:UUID|None
    analise_etileno_id:UUID|None
    solicitante_id:UUID
    decidida_por_id:UUID|None
    iniciada_por_id:UUID|None
    finalizada_por_id:UUID|None
    modalidade:Literal['SIMULADA']
    estado:EstadoIntervencao
    chave_idempotencia:UUID
    justificativa_solicitacao:str
    motivo_fim:str|None
    solicitada_em:datetime
    decidida_em:datetime|None
    iniciada_em:datetime|None
    prazo_planejado_em:datetime|None
    finalizada_em:datetime|None
    duracao_planejada_s:Decimal
    duracao_registrada_s:Decimal|None
    referencias_snapshot:dict
    hash_referencias:str
    referencias_atuais:dict
    hash_referencias_atuais:str
    virtual_ligado:bool
    atuador_virtual_ocupado:bool
    prazo_excedido:bool
    consultado_em:datetime
    sessao_terminal_com_execucao:bool
    contexto_logistico_alterado:bool
    acoes_permitidas:list[AcaoHumana]
    classificacao_risco_etileno:Literal['NAO_AVALIADO']='NAO_AVALIADO'
    resultado_operacional:str
    limitacoes:list[str]
    @field_validator('solicitada_em','decidida_em','iniciada_em','prazo_planejado_em','finalizada_em','consultado_em')
    @classmethod
    def datas_utc(cls,v): return utc(v) if v else None


class AcaoResponse(UTCResponse):
    sessao_id:UUID
    intervencao_id:UUID
    ocorrencia_id:UUID
    usuario_id:UUID
    chave_idempotencia:UUID
    numero:int
    acao:str
    justificativa:str
    estado_anterior:str|None
    estado_posterior:EstadoIntervencao
    registrada_em:datetime
    contexto_snapshot:dict
    @field_validator('registrada_em')
    @classmethod
    def data_utc(cls,v): return utc(v)


class ListaIntervencoes(Input):
    total:int
    limit:int
    offset:int
    intervencoes:list[IntervencaoResponse]


class ListaAcoes(Input):
    total:int
    limit:int
    offset:int
    acoes:list[AcaoResponse]
