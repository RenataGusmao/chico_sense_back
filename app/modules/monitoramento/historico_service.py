"""Explicit, audited historical acquisition. No ethylene engine is invoked."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from hashlib import sha256
import json
import re
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select, func

from app.models.historico_iot import FonteSessaoIoT, SincronizacaoIoT
from app.models.sessoes_monitoramento import SessaoMonitoramento
from app.modules.integracoes.thingspeak.exceptions import ThingSpeakError
from app.modules.monitoramento.service import MonitoramentoService, utc
from app.modules.monitoramento.historico_schemas import SincronizacaoCreate
from app.modules.monitoramento.incorporacao_iot import IncorporadorIoT
from app.repositories.historico_iot import HistoricoIoTRepository


LIMITE_FEEDS = 8000


class HistoricoIoTService:
    def __init__(self,db,user,thingspeak=None):
        self.db,self.user,self.thingspeak=db,user,thingspeak
        self.base=MonitoramentoService(db,user)
        self.repo=HistoricoIoTRepository(db)

    def _sessao(self,sessao_id,escrita=False):
        original=self.base.obter(SessaoMonitoramento,sessao_id)
        self.base.carga(original.carga_id,escrita)
        return self.base.obter(SessaoMonitoramento,sessao_id,lock=escrita)

    def _permitir(self,sessao,data):
        if sessao.estado=='CANCELADA':
            raise HTTPException(409,"Sessao cancelada permite consulta, mas nao incorporacao de leituras.")
        if sessao.estado=='ENCERRADA':
            if not data.complementar_encerrada or not data.justificativa:
                raise HTTPException(409,"Sessao encerrada exige complementacao explicita e justificada.")
            if self.user.perfil.nome not in ('ADMIN','GESTOR'):
                raise HTTPException(403,"Complementacao de sessao encerrada exige ADMIN ou GESTOR.")

    def _fontes(self,sessao):
        fontes=self.repo.fontes(sessao.id)
        if fontes:
            return fontes
        if not self.thingspeak or not self.thingspeak.config.channel_id:
            raise HTTPException(409,"Canal ThingSpeak nao configurado.")
        channel=str(self.thingspeak.config.channel_id)
        if not re.fullmatch(r'[1-9][0-9]*',channel):
            raise HTTPException(409,"Identificador de canal invalido.")
        mapping=self.thingspeak.mapper.mapping_config.fields
        for papel,sensor_id in (('temperatura',sessao.sensor_temperatura_id),('umidade',sessao.sensor_umidade_id)):
            if sensor_id is None:
                continue
            snapshot=sessao.origem_sensor.get(papel)
            encontrados=[(campo,m) for campo,m in mapping.items() if m.sensor_id==sensor_id]
            if len(encontrados)!=1 or not isinstance(snapshot,dict) or snapshot.get("sensor_id")!=str(sensor_id) or not all(k in snapshot for k in ("tipo","contexto","unidade")):
                raise HTTPException(409,"Mapeamento ausente ou ambiguo para um sensor da sessao.")
            campo,m=encontrados[0]
            if not re.fullmatch(r'field[1-8]',campo) or any((
                m.tipo!=snapshot['tipo'],m.contexto!=snapshot['contexto'],m.unidade!=snapshot['unidade'],
                m.viagem_id not in (None,sessao.viagem_id),m.carga_id not in (None,sessao.carga_id),m.caixa_id is not None,
            )):
                raise HTTPException(409,"Mapeamento incompativel com o snapshot; corrija a configuracao antes de sincronizar.")
            fonte=FonteSessaoIoT(sessao_id=sessao.id,sensor_id=sensor_id,origem='THINGSPEAK',
                channel_id=channel,field_name=campo,tipo=snapshot['tipo'],contexto=snapshot['contexto'],
                unidade=snapshot['unidade'],snapshot=snapshot)
            self.db.add(fonte)
        self.db.flush()
        return self.repo.fontes(sessao.id)

    def _reservar(self,sessao_id,data):
        assinatura_data=data.model_dump(mode='json')
        for campo in ('inicio','fim'):
            if getattr(data,campo): assinatura_data[campo]=utc(getattr(data,campo)).isoformat()
        assinatura=sha256(json.dumps(assinatura_data,sort_keys=True).encode()).hexdigest()
        with self.base.transacao():
            sessao=self._sessao(sessao_id,True)
            existente=self.db.scalar(select(SincronizacaoIoT).where(
                SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.chave_idempotencia==data.chave_idempotencia))
            if existente:
                if existente.assinatura!=assinatura or existente.usuario_id!=self.user.id:
                    raise HTTPException(409,"Chave idempotente reutilizada com outro conteudo ou autor.")
                if existente.estado=='EM_EXECUCAO' and utc(existente.expira_em)<=datetime.now(timezone.utc):
                    existente.estado='INTERROMPIDA'; existente.finalizada_em=datetime.now(timezone.utc)
                    existente.resumo=existente.resumo|{'interrupcao':'PRAZO_EXECUCAO_EXPIRADO'}
                    self.base.evento(sessao.configuracao_id,'IOT_INTERROMPIDA',{'sincronizacao_id':str(existente.id)},sessao.id)
                return existente.id,False
            self._permitir(sessao,data)
            now=datetime.now(timezone.utc)
            ativa=self.db.scalar(select(SincronizacaoIoT).where(SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.estado=='EM_EXECUCAO'))
            if ativa:
                if utc(ativa.expira_em)>now:
                    raise HTTPException(409,"Ja existe sincronizacao em execucao para a sessao.")
                ativa.estado='INTERROMPIDA'; ativa.finalizada_em=now
                ativa.resumo=ativa.resumo|{'interrupcao':'PRAZO_EXECUCAO_EXPIRADO'}
                self.base.evento(sessao.configuracao_id,'IOT_INTERROMPIDA',{'sincronizacao_id':str(ativa.id)},sessao.id)
                self.db.flush()
            fontes=self._fontes(sessao)
            inicio=utc(data.inicio) if data.inicio else utc(sessao.inicio)
            limite_fim=utc(sessao.fim) if sessao.fim else now
            fim=utc(data.fim) if data.fim else limite_fim
            if inicio<utc(sessao.inicio) or fim>limite_fim or fim<inicio:
                raise HTTPException(422,"Periodo solicitado deve estar dentro da janela da sessao.")
            timeout=self.thingspeak.config.timeout_seconds if self.thingspeak else 10
            run=SincronizacaoIoT(sessao_id=sessao.id,usuario_id=self.user.id,
                revisao=self.repo.ultima_revisao(sessao.id)+1,chave_idempotencia=data.chave_idempotencia,
                assinatura=assinatura,origem_dados=data.origem_dados,estado='EM_EXECUCAO',
                inicio_janela=inicio,fim_janela=fim,iniciada_em=now,
                expira_em=now+timedelta(seconds=max(1,timeout)*data.max_requisicoes+60),
                complementacao=sessao.estado=='ENCERRADA',justificativa=data.justificativa,
                resumo={'janela_sessao_inicio':utc(sessao.inicio).isoformat(),
                        'janela_sessao_fim':limite_fim.isoformat(),'estado_sessao':sessao.estado,
                        'limite_atraso_s':str(data.limite_atraso_s) if data.limite_atraso_s is not None else None,
                        'limite_requisicoes':data.max_requisicoes,'fontes':[{'id':str(f.id),'sensor_id':str(f.sensor_id),
                        'channel_id':f.channel_id,'field_name':f.field_name,'tipo':f.tipo,'unidade':f.unidade} for f in fontes]})
            self.db.add(run); self.db.flush()
            self.base.evento(sessao.configuracao_id,'IOT_SOLICITADA',{'sincronizacao_id':str(run.id),'revisao':run.revisao,
                                'complementacao':run.complementacao,'justificativa':data.justificativa},sessao.id)
            run_id=run.id
        return run_id,True

    async def _buscar(self,channel,inicio,fim,maximo):
        pendentes=[(inicio,fim)]; paginas=[]; problemas=[]; requisicoes=0
        while pendentes:
            a,b=pendentes.pop()
            if requisicoes>=maximo:
                problemas.append(('LIMITE_REQUISICOES',{'inicio':a.isoformat(),'fim':b.isoformat()})); continue
            requisicoes+=1
            try:
                payload=await self.thingspeak.client.get_feeds_historicos(channel,a,b,results=LIMITE_FEEDS)
                recebida=datetime.now(timezone.utc)
                feeds=payload['feeds']
                paginas.append((feeds,recebida))
                if len(feeds)>=LIMITE_FEEDS:
                    # Queries have second precision; do not recurse forever on one dense second.
                    meio=(a+(b-a)/2).replace(microsecond=0)
                    if a<meio<b:
                        pendentes.extend(((meio,b),(a,meio)))
                    else:
                        problemas.append(('POSSIVEL_TRUNCAMENTO',{'inicio':a.isoformat(),'fim':b.isoformat()}))
            except ThingSpeakError as exc:
                problemas.append(('FALHA_THINGSPEAK',{'classe':type(exc).__name__,'inicio':a.isoformat(),'fim':b.isoformat()}))
        return paginas,problemas,requisicoes

    async def sincronizar(self,sessao_id,data:SincronizacaoCreate):
        run_id,nova=self._reservar(sessao_id,data)
        if not nova:
            return self.db.get(SincronizacaoIoT,run_id)
        run=self.db.get(SincronizacaoIoT,run_id)
        fonte=self.repo.fontes(sessao_id)[0]
        channel,inicio,fim=fonte.channel_id,utc(run.inicio_janela),utc(run.fim_janela)
        self.db.commit()  # No network waits while holding session/cargo row locks.
        paginas=[]; problemas=[]; requisicoes=0
        if data.origem_dados=='THINGSPEAK':
            paginas,problemas,requisicoes=await self._buscar(channel,inicio,fim,data.max_requisicoes)
        with self.base.transacao():
            sessao=self._sessao(sessao_id,True)
            run=self.base.obter(SincronizacaoIoT,run_id,lock=True)
            if run.estado!='EM_EXECUCAO':
                return run  # Expired worker cannot commit into a replacement execution.
            processador=IncorporadorIoT(self.db,sessao,run,data.limite_atraso_s)
            if datetime.now(timezone.utc)>utc(run.expira_em):
                processador.ocorrencia('PRAZO_EXECUCAO_EXPIRADO')
                run.estado='INTERROMPIDA'
            else:
                try:
                    self._permitir(sessao,data)
                    if sessao.fim and utc(run.fim_janela)>utc(sessao.fim):
                        raise HTTPException(409,"Janela alterada durante a aquisicao.")
                except HTTPException:
                    processador.ocorrencia('ESTADO_OU_JANELA_ALTERADA')
                    run.estado='FALHA'
                fontes=self.repo.fontes(sessao_id)
                if run.estado=='EM_EXECUCAO':
                    for codigo,detalhes in problemas:
                        processador.ocorrencia(codigo,**detalhes)
                    if data.origem_dados=='BANCO':
                        for fonte in fontes:
                            for medicao,externa in self.repo.locais(fonte,inicio,fim):
                                processador.incorporar(fonte,{'entry_id':externa.entry_id,'created_at':utc(medicao.medida_em).isoformat(),
                                                            fonte.field_name:str(medicao.valor)},None)
                    else:
                        for feeds,recebida in paginas:
                            for feed in feeds:
                                for fonte in fontes:
                                    processador.incorporar(fonte,feed,recebida)
                    cont=processador.contadores
                    run.estado=('PARCIAL' if cont['novas'] or cont['duplicadas'] else 'FALHA') if cont['erros'] or cont['invalidas'] else 'CONCLUIDA'
            run.finalizada_em=datetime.now(timezone.utc)
            run.resumo=run.resumo|processador.contadores|{'requisicoes':requisicoes,'feeds_recebidos':sum(len(p[0]) for p in paginas)}
            self.base.evento(sessao.configuracao_id,'IOT_'+run.estado,{'sincronizacao_id':str(run.id),
                'revisao':run.revisao,'resumo':run.resumo},sessao.id)
        return run

    def estado(self,sessao_id,limit=20,offset=0):
        self._sessao(sessao_id)
        runs=list(self.db.scalars(select(SincronizacaoIoT).where(SincronizacaoIoT.sessao_id==sessao_id)
                        .order_by(SincronizacaoIoT.revisao.desc()).limit(limit).offset(offset)))
        em_execucao=self.db.scalar(select(SincronizacaoIoT.id).where(SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.estado=='EM_EXECUCAO'))
        revisao=self.db.scalar(select(func.max(SincronizacaoIoT.revisao)).where(SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.estado!='EM_EXECUCAO')) or 0
        return dict(sessao_id=sessao_id,revisao_disponivel=revisao,em_execucao=em_execucao,tentativas=runs)
