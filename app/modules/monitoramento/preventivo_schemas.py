"""Explicit operational configuration. No cultivar calibration or scientific risk thresholds."""
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import AwareDatetime, Field, model_validator, field_validator
from app.schemas.operacional import Input,Response
from app.modules.monitoramento.etileno import EstagioMaturacao
from app.modules.monitoramento.service import utc


class ConfiguracaoCreate(Input):
    chave_idempotencia:UUID
    temperatura_min_c:Decimal=Field(max_digits=7,decimal_places=3)
    temperatura_max_c:Decimal=Field(max_digits=7,decimal_places=3)
    umidade_min_percentual:Decimal=Field(ge=0,le=100,max_digits=6,decimal_places=3)
    umidade_max_percentual:Decimal=Field(ge=0,le=100,max_digits=6,decimal_places=3)
    intervalo_maximo_s:Decimal=Field(gt=0,max_digits=12,decimal_places=3)
    cobertura_min_percentual:Decimal=Field(gt=0,le=100,max_digits=6,decimal_places=3)
    exposicao_continua_s:Decimal|None=Field(default=None,gt=0,max_digits=12,decimal_places=3)
    maturacoes_aplicaveis:list[EstagioMaturacao]=Field(min_length=1,max_length=5)
    ambiente:Literal['TRANSPORTE_REFRIGERADO','LABORATORIO']
    fundamento:Literal['OPERACIONAL','EXPERIMENTAL']
    justificativa:str=Field(min_length=10,max_length=4000)
    referencias:list[str]=Field(default_factory=list,max_length=10)
    prioridade:Literal['INFORMATIVO','ATENCAO']='ATENCAO'

    @model_validator(mode='after')
    def coerencia(self):
        if self.temperatura_min_c>=self.temperatura_max_c or self.umidade_min_percentual>=self.umidade_max_percentual:
            raise ValueError('Faixas devem ter minimo estritamente menor que maximo.')
        if len(set(self.maturacoes_aplicaveis))!=len(self.maturacoes_aplicaveis):
            raise ValueError('Maturacoes aplicaveis nao podem se repetir.')
        return self


class AvaliacaoCreate(Input):
    chave_idempotencia:UUID
    configuracao_id:UUID|None=None
    inicio:AwareDatetime|None=None
    fim:AwareDatetime|None=None
    corte_aquisicao:AwareDatetime|None=None
    revisao:int|None=Field(default=None,ge=0)
    analise_etileno_id:UUID|None=None


class DecisaoCreate(Input):
    chave_idempotencia:UUID
    acao:Literal['RECONHECER','OBSERVAR','RESOLVER','DESCARTAR']
    justificativa:str=Field(min_length=1,max_length=4000)


class UTCResponse(Response):
    @field_validator('created_at','updated_at')
    @classmethod
    def data_utc(cls,value): return utc(value)


class ConfiguracaoResponse(UTCResponse):
    sessao_id:UUID
    usuario_id:UUID
    chave_idempotencia:UUID
    versao:int
    registrada_em:datetime
    parametros:dict
    @field_validator('registrada_em')
    @classmethod
    def registro_utc(cls,v): return utc(v)


class AvaliacaoResponse(UTCResponse):
    sessao_id:UUID
    usuario_id:UUID
    configuracao_id:UUID|None
    anterior_id:UUID|None
    analise_etileno_id:UUID|None
    chave_idempotencia:UUID
    executada_em:datetime
    inicio:datetime
    fim:datetime
    corte_aquisicao:datetime
    revisao:int
    hash_entrada:str
    hash_resultado:str
    entrada_snapshot:dict
    resultado:dict
    alertas_ids:list[UUID]
    @field_validator('executada_em','inicio','fim','corte_aquisicao')
    @classmethod
    def janela_utc(cls,v): return utc(v)


class DecisaoResponse(UTCResponse):
    sessao_id:UUID
    alerta_id:UUID
    ocorrencia_id:UUID
    usuario_id:UUID
    acao:str
    justificativa:str
    estado_anterior:str|None
    estado_posterior:str
    registrada_em:datetime
    @field_validator('registrada_em')
    @classmethod
    def registro_utc(cls,v): return utc(v)


class AlertaResponse(Input):
    id:UUID
    sessao_id:UUID
    viagem_id:UUID
    carga_id:UUID|None
    tipo:str
    nivel:Literal['INFORMATIVO','ATENCAO','CRITICO']
    status:Literal['ABERTO','EM_ANALISE','RESOLVIDO','DESCARTADO']
    iniciado_em:datetime
    finalizado_em:datetime|None
    evidencias_total:int
    classificacao_risco_etileno:Literal['NAO_AVALIADO']='NAO_AVALIADO'
    intervencao:Literal['AVALIACAO_HUMANA_NECESSARIA']='AVALIACAO_HUMANA_NECESSARIA'


class ListaConfiguracoes(Input):
    total:int
    limit:int
    offset:int
    configuracoes:list[ConfiguracaoResponse]

class ListaAvaliacoes(Input):
    total:int
    limit:int
    offset:int
    avaliacoes:list[AvaliacaoResponse]

class ListaAlertas(Input):
    total:int
    limit:int
    offset:int
    alertas:list[AlertaResponse]

class ListaDecisoes(Input):
    total:int
    limit:int
    offset:int
    decisoes:list[DecisaoResponse]

class ListaEvidencias(Input):
    total:int
    limit:int
    offset:int
    evidencias:list[dict]
