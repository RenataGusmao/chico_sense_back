"""Per-field persistence using the existing ThingSpeak mapper and measurement repos."""
from datetime import datetime, timezone
from decimal import Decimal, DecimalException
from hashlib import sha256
import json
from pydantic import ValidationError
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.models.enums import ContextoMedicao
from app.models.iot import Medicao
from app.models.historico_iot import RegistroSessaoIoT, OcorrenciaIoT
from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
from app.modules.integracoes.thingspeak.schemas import ThingSpeakFeed, ThingSpeakMappingConfig, ThingSpeakFieldMapping
from app.repositories.integracoes import LeituraExternaRepository
from app.repositories.medicoes import MedicaoRepository
from app.repositories.historico_iot import HistoricoIoTRepository
from app.modules.monitoramento.service import utc


def timestamp_origem(value):
    if not isinstance(value,str):
        raise ValueError("TIMESTAMP_INVALIDO")
    parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("TIMESTAMP_INVALIDO")
    return parsed.astimezone(timezone.utc)


class IncorporadorIoT:
    def __init__(self,db,sessao,execucao,limite_atraso_s):
        self.db,self.sessao,self.execucao=db,sessao,execucao
        self.repo=HistoricoIoTRepository(db)
        self.limite_atraso_s=limite_atraso_s
        self.ultimo={}
        self.contadores=dict(novas=0,duplicadas=0,invalidas=0,fora_janela=0,erros=0,tardias=0,fora_de_ordem=0)

    def ocorrencia(self,codigo,fonte=None,entry=None,medida=None,erro=True,**detalhes):
        self.db.add(OcorrenciaIoT(sincronizacao_id=self.execucao.id,fonte_id=fonte.id if fonte else None,
                    entry_id=entry,medida_em=medida,codigo=codigo,detalhes=detalhes,processada_em=datetime.now(timezone.utc)))
        self.contadores['erros']+=int(erro)

    def _valor(self,fonte,raw,entry,medida):
        try:
            # Build only this mapped field so one malformed field cannot discard its sibling.
            config=ThingSpeakMappingConfig(fields={fonte.field_name:ThingSpeakFieldMapping(
                sensor_id=fonte.sensor_id,tipo=fonte.tipo,contexto=fonte.contexto,unidade=fonte.unidade)})
            feed=ThingSpeakFeed.from_api_payload(dict(created_at=medida,entry_id=entry,**{fonte.field_name:raw}))
            leitura=ThingSpeakFieldMapper(config).map_feed(fonte.channel_id,feed)[0]
            if leitura.ignorada or leitura.valor is None or not leitura.valor.is_finite():
                return None,"VALOR_INVALIDO"
            valor=leitura.valor
            if abs(valor)>=100000000 or valor!=valor.quantize(Decimal('0.0001')):
                return None,"PRECISAO_OU_FAIXA_PERSISTENCIA"
            if fonte.tipo=='UMIDADE' and not 0<=valor<=100:
                return None,"UMIDADE_FORA_PERCENTUAL"
            return valor,None
        except (ValidationError,ValueError,TypeError,DecimalException):
            return None,"VALOR_INVALIDO"

    def incorporar(self,fonte,payload,recebida_em):
        if not isinstance(payload,dict):
            self.ocorrencia("FEED_INVALIDO",fonte); return
        entry=payload.get('entry_id')
        if isinstance(entry,bool) or not isinstance(entry,int) or not 0<entry<=2147483647:
            self.ocorrencia("ENTRY_ID_INVALIDO",fonte); return
        original=payload.get('created_at')
        try:
            medida=timestamp_origem(original)
        except (ValueError,TypeError,OverflowError):
            self.ocorrencia("TIMESTAMP_INVALIDO",fonte,entry); return
        if not utc(self.execucao.inicio_janela)<=medida<=utc(self.execucao.fim_janela):
            self.contadores['fora_janela']+=1
            self.ocorrencia("FORA_DA_JANELA",fonte,entry,medida,erro=False); return
        if recebida_em is not None and medida>recebida_em:
            self.ocorrencia("HORARIO_FUTURO",fonte,entry,medida); return
        raw=payload.get(fonte.field_name)
        valor,motivo=self._valor(fonte,raw,entry,medida)
        assinatura=sha256(json.dumps({
            't':medida.isoformat(),'v':str(valor.normalize()) if valor is not None else None,
            'invalido':sha256(str(raw).encode()).hexdigest() if valor is None else None,
            'sensor':str(fonte.sensor_id),'unidade':fonte.unidade,
        },sort_keys=True).encode()).hexdigest()
        anterior=self.repo.registro(fonte.id,entry)
        if anterior:
            if anterior.assinatura==assinatura:
                self.contadores['duplicadas']+=1
            else:
                self.ocorrencia("CONFLITO_ORIGEM",fonte,entry,medida,
                    instantes_afetados=[utc(anterior.medida_em).isoformat(),medida.isoformat()])
            return
        maximo=self.ultimo.get(fonte.id)
        if maximo is None:
            maximo=self.db.scalar(select(func.max(RegistroSessaoIoT.medida_em)).where(RegistroSessaoIoT.fonte_id==fonte.id))
            maximo=utc(maximo) if maximo else None
        fora_ordem=maximo is not None and medida<maximo
        self.ultimo[fonte.id]=max(maximo,medida) if maximo else medida
        try:
            with self.db.begin_nested():
                self._gravar(fonte,entry,medida,original,recebida_em,valor,motivo,assinatura,fora_ordem)
        except IntegrityError:
            # A different session may have inserted the shared source identity concurrently.
            # Only retry if the exact external identity exists; never label every FK error a duplicate.
            if self.repo.externa(fonte,entry) is not None:
                try:
                    with self.db.begin_nested():
                        self._gravar(fonte,entry,medida,original,recebida_em,valor,motivo,assinatura,fora_ordem)
                except IntegrityError:
                    self.ocorrencia("FALHA_INTEGRIDADE",fonte,entry,medida)
            else:
                self.ocorrencia("FALHA_INTEGRIDADE",fonte,entry,medida)

        except Exception as exc:
            # Savepoint isolates this field; retain a sanitized failure, never the upstream URL/key.
            self.ocorrencia("FALHA_PERSISTENCIA",fonte,entry,medida,classe=type(exc).__name__)

    def _gravar(self,fonte,entry,medida,original,recebida,valor,motivo,assinatura,fora_ordem):
        medicao=None
        if valor is not None:
            externa=self.repo.externa(fonte,entry)
            if externa:
                existente=self.db.get(Medicao,externa.medicao_id)
                coerente=(existente.sensor_id==fonte.sensor_id and utc(existente.medida_em)==medida
                    and existente.valor==valor and existente.unidade==fonte.unidade
                    and existente.contexto.value==fonte.contexto
                    and existente.carga_id in (None,self.sessao.carga_id)
                    and existente.viagem_id in (None,self.sessao.viagem_id))
                if not coerente:
                    self.ocorrencia("CONFLITO_ORIGEM",fonte,entry,medida,instantes_afetados=[utc(existente.medida_em).isoformat(),medida.isoformat()])
                    return
                medicao=existente
            else:
                medicao=MedicaoRepository(self.db).create(sensor_id=fonte.sensor_id,
                    viagem_id=None,carga_id=None,caixa_id=None,medida_em=medida,
                    contexto=ContextoMedicao(fonte.contexto),valor=valor,unidade=fonte.unidade)
                LeituraExternaRepository(self.db).create(origem=fonte.origem,channel_id=fonte.channel_id,
                    entry_id=entry,field_name=fonte.field_name,medicao_id=medicao.id)
        posterior=self.sessao.estado=='ENCERRADA'
        # Later association is known; legacy receipt time may still be unknown.
        tardia=None
        if recebida is not None:
            if self.sessao.fim is not None and recebida>utc(self.sessao.fim):
                tardia=True
            elif self.limite_atraso_s is not None:
                delta=recebida-medida
                latencia=Decimal(delta.days*86400+delta.seconds)+Decimal(delta.microseconds)/1000000
                tardia=latencia>self.limite_atraso_s
        registro=RegistroSessaoIoT(sessao_id=self.sessao.id,fonte_id=fonte.id,sincronizacao_id=self.execucao.id,
            medicao_id=medicao.id if medicao else None,entry_id=entry,medida_em=medida,timestamp_origem=original,
            recebida_em=recebida,processada_em=datetime.now(timezone.utc),valor=valor,
            estado='VALIDA' if valor is not None else 'INVALIDA',motivo=motivo,assinatura=assinatura,
            tardia=tardia,apos_encerramento=posterior,fora_de_ordem=fora_ordem)
        self.db.add(registro); self.db.flush()
        self.contadores['novas']+=1
        self.contadores['invalidas']+=int(valor is None)
        self.contadores['tardias']+=int(tardia is True)
        self.contadores['fora_de_ordem']+=int(fora_ordem)
