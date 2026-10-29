"""Lossless temperature-only adapter to the public scientific engine contracts."""
from dataclasses import fields, is_dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from hashlib import sha256
import json
from uuid import UUID
from app.modules.monitoramento.etileno import EntradaEstimativa, LeituraTemperatura
from app.modules.monitoramento.service import utc
from app.modules.monitoramento.incorporacao_iot import timestamp_origem


def serializar(value):
    """JSON numbers never carry scientific decimals through binary floats."""
    if isinstance(value, Decimal): return str(value)
    if isinstance(value, datetime): return utc(value).isoformat().replace('+00:00','Z')
    if isinstance(value, UUID): return str(value)
    if isinstance(value, Enum): return value.value
    if is_dataclass(value): return {f.name: serializar(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, dict): return {str(k): serializar(v) for k,v in value.items()}
    if isinstance(value, (tuple,list)): return [serializar(v) for v in value]
    return value


def hash_documento(value):
    canonical=json.dumps(serializar(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return sha256(canonical.encode('utf-8')).hexdigest()


def montar_entrada(sessao, inicio, fim, corte, modo, intervalo_maximo_s, rows, ocorrencias, fontes):
    """Keep invalid samples and conflict barriers; never bridge a rejected timestamp."""
    sensor=str(sessao.sensor_temperatura_id); sessao_id=str(sessao.id)
    fontes_temp={f.id: f for f in fontes if f.tipo=='TEMPERATURA' and f.sensor_id==sessao.sensor_temperatura_id}
    leituras=[]; referencias=[]; incidentes=[]
    for r,f,revisao in rows:
        if f.id not in fontes_temp: continue
        leitura=LeituraTemperatura(utc(r.medida_em),r.valor if r.estado=='VALIDA' else None,
            sensor,sessao_id,f.unidade,f'{f.id}:{r.entry_id}',utc(r.recebida_em) if r.recebida_em else None)
        leituras.append(leitura)
        referencias.append(serializar(dict(registro_id=r.id,medicao_id=r.medicao_id,fonte_id=f.id,
            sincronizacao_id=r.sincronizacao_id,revisao=revisao,entry_id=r.entry_id,
            medida_em=r.medida_em,recebida_em=r.recebida_em,processada_em=r.processada_em,
            estado=r.estado,motivo=r.motivo,tardia=r.tardia,apos_encerramento=r.apos_encerramento,
            fora_de_ordem=r.fora_de_ordem,assinatura=r.assinatura)))
    erros_temporais={'TIMESTAMP_INVALIDO','FEED_INVALIDO','ENTRY_ID_INVALIDO','FALHA_INTEGRIDADE','FALHA_PERSISTENCIA','HORARIO_FUTURO'}
    for o in ocorrencias:
        if o.fonte_id is not None and o.fonte_id not in fontes_temp: continue  # Humidity cannot invalidate q(T).
        if o.medida_em is not None and not inicio<=utc(o.medida_em)<=fim and o.codigo!='CONFLITO_ORIGEM': continue
        fonte=fontes_temp.get(o.fonte_id)
        unidade=fonte.unidade if fonte else 'C'
        horarios=[]
        if o.codigo=='CONFLITO_ORIGEM':
            if not o.detalhes.get('instantes_afetados'): horarios.append(None)
            for raw in o.detalhes.get('instantes_afetados',[]):
                try: hora=timestamp_origem(raw)
                except (ValueError,TypeError,OverflowError): hora=None
                if hora is None or inicio<=hora<=fim: horarios.append(hora)
        elif o.codigo in erros_temporais:
            horarios=[utc(o.medida_em) if o.medida_em else None]
        # None is an intentional invalid input: the engine returns HORARIO_INVALIDO.
        # No invented time or zero-temperature substitute for an unlocatable error.
        for n,hora in enumerate(horarios):
            leituras.append(LeituraTemperatura(hora,None,sensor,sessao_id,unidade,f'ocorrencia:{o.id}:{n}'))
        incidentes.append(serializar(dict(id=o.id,fonte_id=o.fonte_id,codigo=o.codigo,
            medida_em=o.medida_em,processada_em=o.processada_em,detalhes=o.detalhes)))
    entrada=EntradaEstimativa(massa=sessao.massa_kg,inicio=inicio,fim=fim,sensor_id=sensor,sessao_id=sessao_id,
        leituras=tuple(leituras),intervalo_maximo_s=intervalo_maximo_s,modo=modo,
        maturacao=sessao.maturacao,corte_aquisicao=corte)
    origem=serializar([dict(id=f.id,sensor_id=f.sensor_id,origem=f.origem,channel_id=f.channel_id,
        field_name=f.field_name,unidade=f.unidade,contexto=f.contexto) for f in fontes_temp.values()])
    return entrada,dict(versao_adaptador='chicosense-sessao-etileno-1',entrada=serializar(entrada),
        registros=referencias,ocorrencias=incidentes,fontes_temperatura=origem,
        contexto_umidade=dict(sensor_id=str(sessao.sensor_umidade_id) if sessao.sensor_umidade_id else None,
            referencia='Historico IoT da mesma sessao e revisao; nao integra a formula.'))


def restaurar_entrada(snapshot):
    """Reconstruct public input from the stored snapshot without querying live data."""
    p=dict(snapshot['entrada'])
    for k in ('inicio','fim','corte_aquisicao'):
        p[k]=datetime.fromisoformat(p[k]) if p[k] else None
    leituras=[]
    for original in p['leituras']:
        row=dict(original)
        for k in ('medida_em','recebida_em'):
            row[k]=datetime.fromisoformat(row[k]) if row[k] else None
        leituras.append(LeituraTemperatura(**row))
    p['leituras']=tuple(leituras)
    return EntradaEstimativa(**p)
