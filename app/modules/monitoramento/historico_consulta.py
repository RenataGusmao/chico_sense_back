"""Read-only projections of acquisition revisions and temporal quality."""
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select, func
from app.models.historico_iot import SincronizacaoIoT
from app.modules.monitoramento.service import utc
from app.modules.monitoramento.incorporacao_iot import timestamp_origem
from app.modules.monitoramento.historico_service import HistoricoIoTService
from app.modules.monitoramento.cobertura_iot import cobertura_temporal


class HistoricoConsultaService(HistoricoIoTService):
    def _visao(self,sessao_id,revisao=None,inicio=None,fim=None):
        sessao=self._sessao(sessao_id)
        if revisao is None:
            revisao=self.db.scalar(select(func.max(SincronizacaoIoT.revisao)).where(
                SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.estado!='EM_EXECUCAO')) or 0
        run=None
        if revisao:
            run=self.db.scalar(select(SincronizacaoIoT).where(SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.revisao==revisao))
            if run is None: raise HTTPException(404,"Revisao de aquisicao inexistente.")
            if run.estado=='EM_EXECUCAO': raise HTTPException(409,"Revisao em execucao ainda nao esta consolidada.")
        a=utc(sessao.inicio)
        b=utc(sessao.fim) if sessao.fim else (utc(run.iniciada_em) if run else datetime.now(timezone.utc))
        if inicio is not None:
            if utc(inicio)<a: raise HTTPException(422,"Inicio de consulta fora da sessao.")
            a=utc(inicio)
        if fim is not None:
            if utc(fim)>b: raise HTTPException(422,"Fim de consulta fora da sessao/corte de aquisicao.")
            b=utc(fim)
        if b<a: raise HTTPException(422,"Janela de consulta invalida.")
        ocorrencias=self.repo.ocorrencias(sessao_id,revisao)
        conflitos=set(); barreiras=defaultdict(set); invalidos_temporais=False
        for o in ocorrencias:
            if o.codigo in ('TIMESTAMP_INVALIDO','FEED_INVALIDO'):
                invalidos_temporais=True
            if o.codigo=='CONFLITO_ORIGEM':
                for t in o.detalhes.get('instantes_afetados',[]):
                    hora=timestamp_origem(t)
                    if a<=hora<=b: conflitos.add((o.fonte_id,hora)); barreiras[o.fonte_id].add(hora)
            elif o.codigo in ('ENTRY_ID_INVALIDO','FALHA_INTEGRIDADE','FALHA_PERSISTENCIA','HORARIO_FUTURO'):
                if o.medida_em and a<=utc(o.medida_em)<=b:
                    barreiras[o.fonte_id].add(utc(o.medida_em))
                elif o.medida_em is None:
                    invalidos_temporais=True
        return sessao,revisao,a,b,ocorrencias,conflitos,barreiras,invalidos_temporais

    def historico(self,sessao_id,limit=100,offset=0,tipo=None,revisao=None,inicio=None,fim=None):
        sessao,rev,a,b,ocorrencias,conflitos,_,invalidos=self._visao(sessao_id,revisao,inicio,fim)
        query=self.repo.registros(sessao_id,rev,a,b,tipo)
        total=self.db.scalar(select(func.count()).select_from(query.subquery()))
        rows=self.db.execute(query.limit(limit).offset(offset)).all()
        leituras=[]
        for r,f,numero in rows:
            conflito=(f.id,utc(r.medida_em)) in conflitos
            leituras.append(dict(id=r.id,fonte_id=f.id,medicao_id=r.medicao_id,sensor_id=f.sensor_id,
                tipo=f.tipo,channel_id=f.channel_id,field_name=f.field_name,unidade=f.unidade,entry_id=r.entry_id,
                medida_em=utc(r.medida_em),timestamp_origem=r.timestamp_origem,
                recebida_em=utc(r.recebida_em) if r.recebida_em else None,processada_em=utc(r.processada_em),
                valor=None if conflito else r.valor,estado='CONFLITANTE' if conflito else r.estado,
                motivo='CONFLITO_ORIGEM' if conflito else r.motivo,revisao_incorporacao=numero,
                tardia=r.tardia,apos_encerramento=r.apos_encerramento,fora_de_ordem=r.fora_de_ordem,
                conflito_observado=conflito))
        return dict(sessao_id=sessao_id,estado_sessao=sessao.estado,revisao=rev,inicio=a,fim=b,
            massa_kg=sessao.massa_kg,maturacao=sessao.maturacao,total=total,limit=limit,offset=offset,leituras=leituras,
            metadados_temporais_invalidos=invalidos,cancelada_para_analise=sessao.estado=='CANCELADA',
            ocorrencias=[dict(codigo=o.codigo,fonte_id=str(o.fonte_id) if o.fonte_id else None,
                         entry_id=o.entry_id,medida_em=utc(o.medida_em) if o.medida_em else None) for o in ocorrencias])

    def qualidade(self,sessao_id,intervalo_maximo_s:Decimal,revisao=None,inicio=None,fim=None):
        sessao,rev,a,b,ocorrencias,conflitos,barreiras,invalidos=self._visao(sessao_id,revisao,inicio,fim)
        rows=self.db.execute(self.repo.registros(sessao_id,rev,a,b)).all()
        por_fonte=defaultdict(list)
        for r,f,_ in rows: por_fonte[f.id].append(r)
        resultados=[]
        for fonte in self.repo.fontes(sessao_id):
            grupos=defaultdict(list)
            regs=por_fonte[fonte.id]
            for registro in regs: grupos[utc(registro.medida_em)].append(registro)
            for hora in barreiras[fonte.id]: grupos[hora]  # Include known failed instants as barriers, never bridge them.
            pontos=[]; conflitos_instante=0
            for hora,registros in sorted(grupos.items()):
                valores={r.valor for r in registros if r.estado=='VALIDA'}
                conflitante=len(valores)>1 or (fonte.id,hora) in conflitos
                valido=bool(registros) and len(valores)==1 and all(r.estado=='VALIDA' for r in registros) and not conflitante and hora not in barreiras[fonte.id]
                conflitos_instante+=int(conflitante)
                pontos.append((hora,valido))
            cobertura=cobertura_temporal(a,b,pontos,intervalo_maximo_s)
            if invalidos:
                cobertura['percentual_cobertura']=None
            resultados.append(dict(sensor_id=fonte.sensor_id,tipo=fonte.tipo,unidade=fonte.unidade,
                registros=len(regs),invalidos=sum(r.estado!='VALIDA' for r in regs),
                instantes_conflitantes=conflitos_instante,tardias=sum(r.tardia is True for r in regs),
                atraso_nao_classificado=sum(r.tardia is None for r in regs),fora_de_ordem=sum(r.fora_de_ordem for r in regs),
                **cobertura))
        if not resultados:
            resultados=[dict(tipo='TEMPERATURA',sensor_id=sessao.sensor_temperatura_id,
                **cobertura_temporal(a,b,[],intervalo_maximo_s))]
        return dict(sessao_id=sessao_id,revisao=rev,inicio=a,fim=b,intervalo_maximo_s=intervalo_maximo_s,
            natureza='COBERTURA_TEMPORAL_DE_AQUISICAO_NAO_E_ESTIMATIVA_DE_ETILENO',
            metadados_temporais_invalidos=invalidos,cancelada_para_analise=sessao.estado=='CANCELADA',
            indicadores=resultados,codigos_ocorrencias=sorted({o.codigo for o in ocorrencias}),
            limites='Sem interpolacao temporal ou preenchimento. Aplicabilidade termica e q(T) pertencem somente a Etapa 5.')
