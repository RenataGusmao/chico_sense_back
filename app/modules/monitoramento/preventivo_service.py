"""Transactional environmental evaluations, legacy alerts and auditable human decisions."""
from contextlib import contextmanager
from datetime import datetime,timezone
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select,func
from sqlalchemy.exc import SQLAlchemyError
from app.models.monitoramento import Alerta,Ocorrencia
from app.models.enums import NivelAlerta,StatusAlerta
from app.models.historico_iot import SincronizacaoIoT
from app.models.analises_etileno import AnaliseEtileno
from app.models.preventivo import ConfiguracaoAmbiental,AvaliacaoPreventiva,AlertaSessao,EvidenciaPreventiva,DecisaoAlerta
from app.modules.monitoramento.historico_service import HistoricoIoTService
from app.modules.monitoramento.analises_adapter import serializar,hash_documento
from app.modules.monitoramento.preventivo_motor import avaliar_ambiente,VERSAO
from app.modules.monitoramento.service import utc


class PreventivoService(HistoricoIoTService):
    @contextmanager
    def transacao(self):
        try:
            with self.base.transacao(): yield
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(503,'Falha ao confirmar operacao; consulte ou repita a mesma chave idempotente.') from None

    def configurar(self,sessao_id,data):
        with self.transacao():
            s=self._sessao(sessao_id,True)
            if self.user.perfil.nome not in ('ADMIN','GESTOR'): raise HTTPException(403,'Configuracao exige ADMIN ou GESTOR.')
            assinatura=hash_documento(data.model_dump())
            antiga=self.db.scalar(select(ConfiguracaoAmbiental).where(ConfiguracaoAmbiental.sessao_id==s.id,
                ConfiguracaoAmbiental.chave_idempotencia==data.chave_idempotencia))
            if antiga:
                self._replay(antiga,assinatura); return antiga
            if s.estado=='CANCELADA': raise HTTPException(409,'Sessao cancelada nao recebe nova configuracao.')
            if s.maturacao not in data.maturacoes_aplicaveis or s.ambiente_aquisicao!=data.ambiente:
                raise HTTPException(409,'Configuracao deve incluir explicitamente maturacao e ambiente da sessao.')
            versao=(self.db.scalar(select(func.max(ConfiguracaoAmbiental.versao)).where(ConfiguracaoAmbiental.sessao_id==s.id)) or 0)+1
            row=ConfiguracaoAmbiental(sessao_id=s.id,usuario_id=self.user.id,chave_idempotencia=data.chave_idempotencia,
                assinatura=assinatura,versao=versao,registrada_em=datetime.now(timezone.utc),
                parametros=serializar(data.model_dump(exclude={'chave_idempotencia'})))
            self.db.add(row); self.db.flush()
            self.base.evento(s.configuracao_id,'CONFIG_AMBIENTAL',dict(id=str(row.id),versao=versao),s.id)
        return row

    def _replay(self,row,assinatura):
        if row.usuario_id!=self.user.id or row.assinatura!=assinatura:
            raise HTTPException(409,'Chave idempotente ja usada com outro autor ou parametros.')

    def _janela(self,s,data,agora):
        if s.estado=='ATIVA' and data.corte_aquisicao is None: raise HTTPException(422,'Sessao ativa exige corte_aquisicao explicito.')
        corte=utc(data.corte_aquisicao) if data.corte_aquisicao else agora
        a=utc(data.inicio) if data.inicio else utc(s.inicio)
        limite=utc(s.fim) if s.fim else corte
        b=utc(data.fim) if data.fim else limite
        if corte>agora or a<utc(s.inicio) or b>limite or b>corte or b<=a:
            raise HTTPException(422,'Janela positiva deve estar integralmente na sessao e no corte nao futuro.')
        query=select(SincronizacaoIoT).where(SincronizacaoIoT.sessao_id==s.id,
            SincronizacaoIoT.estado!='EM_EXECUCAO',SincronizacaoIoT.finalizada_em<=corte)
        if data.revisao is None:
            run=self.db.scalar(query.order_by(SincronizacaoIoT.revisao.desc()).limit(1)); rev=run.revisao if run else 0
        else:
            rev=data.revisao
            if rev:
                run=self.db.scalar(select(SincronizacaoIoT).where(SincronizacaoIoT.sessao_id==s.id,SincronizacaoIoT.revisao==rev))
                if run is None: raise HTTPException(404,'Revisao inexistente nesta sessao.')
                if run.estado=='EM_EXECUCAO' or not run.finalizada_em or utc(run.finalizada_em)>corte:
                    raise HTTPException(409,'Revisao nao consolidada no corte.')
        runs=list(self.db.scalars(query.where(SincronizacaoIoT.revisao<=rev,
            SincronizacaoIoT.inicio_janela<=b,SincronizacaoIoT.fim_janela>=a).order_by(SincronizacaoIoT.revisao)))
        return a,b,corte,rev,runs

    def _snapshot(self,s,data,a,b,corte,rev,runs,config):
        fontes=self.repo.fontes(s.id); tipos={f.id:f.tipo for f in fontes}
        leituras=[]
        for r,f,revisao in self.db.execute(self.repo.registros(s.id,rev,a,b)).all():
            sensor=s.sensor_temperatura_id if f.tipo=='TEMPERATURA' else s.sensor_umidade_id
            if f.sensor_id!=sensor or utc(r.processada_em)>corte: continue
            leituras.append(dict(id=r.id,medicao_id=r.medicao_id,fonte_id=f.id,tipo=f.tipo,sensor_id=f.sensor_id,
                medida_em=utc(r.medida_em),recebida_em=r.recebida_em,processada_em=r.processada_em,
                valor=r.valor,unidade=f.unidade,estado=r.estado,motivo=r.motivo,entry_id=r.entry_id,
                revisao=revisao,assinatura=r.assinatura,tardia=r.tardia,apos_encerramento=r.apos_encerramento))
        ocorrencias=[]
        for o in self.repo.ocorrencias(s.id,rev):
            if utc(o.processada_em)>corte: continue
            if o.medida_em and not a<=utc(o.medida_em)<=b and o.codigo!='CONFLITO_ORIGEM': continue
            ocorrencias.append(dict(id=o.id,tipo=tipos.get(o.fonte_id),fonte_id=o.fonte_id,codigo=o.codigo,
                medida_em=o.medida_em,processada_em=o.processada_em,detalhes=o.detalhes))
        contexto=None
        if data.analise_etileno_id:
            analise=self.db.scalar(select(AnaliseEtileno).where(AnaliseEtileno.id==data.analise_etileno_id,AnaliseEtileno.sessao_id==s.id))
            if analise is None: raise HTTPException(404,'Analise de etileno inexistente nesta sessao.')
            if utc(analise.inicio)!=a or utc(analise.fim)!=b or analise.revisao_aquisicao!=rev:
                raise HTTPException(409,'Analise contextual deve corresponder a mesma janela e revisao.')
            contexto=dict(id=analise.id,versao_modelo=analise.versao_modelo,hash_resultado=analise.hash_resultado,
                resultado=analise.resultado,classificacao_risco_etileno='NAO_AVALIADO')
        return serializar(dict(versao_avaliador=VERSAO,inicio=a,fim=b,corte_aquisicao=corte,revisao=rev,
            sessao=dict(id=s.id,estado=s.estado,maturacao=s.maturacao,ambiente=s.ambiente_aquisicao,
                sensor_temperatura_id=s.sensor_temperatura_id,sensor_umidade_id=s.sensor_umidade_id),
            configuracao=config.parametros if config else None,
            configuracao_id=config.id if config else None,configuracao_versao=config.versao if config else None,
            fontes=[dict(id=f.id,tipo=f.tipo,sensor_id=f.sensor_id,unidade=f.unidade,contexto=f.contexto,
                origem=f.origem,channel_id=f.channel_id,field_name=f.field_name) for f in fontes],
            leituras=leituras,ocorrencias=ocorrencias,
            tentativas=[dict(id=r.id,revisao=r.revisao,estado=r.estado,finalizada_em=r.finalizada_em) for r in runs],
            estimativa_etileno_contextual=contexto))

    def avaliar(self,sessao_id,data):
        with self.transacao():
            s=self._sessao(sessao_id,True); assinatura=hash_documento(data.model_dump())
            antiga=self.db.scalar(select(AvaliacaoPreventiva).where(AvaliacaoPreventiva.sessao_id==s.id,
                AvaliacaoPreventiva.chave_idempotencia==data.chave_idempotencia))
            if antiga:
                self._replay(antiga,assinatura); return self._dto_avaliacao(antiga)
            if s.estado=='CANCELADA': raise HTTPException(409,'Sessao cancelada preserva consultas/decisoes, sem novas avaliacoes.')
            agora=datetime.now(timezone.utc); a,b,corte,rev,runs=self._janela(s,data,agora)
            cfgquery=select(ConfiguracaoAmbiental).where(ConfiguracaoAmbiental.sessao_id==s.id)
            if data.configuracao_id:
                config=self.db.scalar(cfgquery.where(ConfiguracaoAmbiental.id==data.configuracao_id))
                if config is None: raise HTTPException(404,'Configuracao inexistente nesta sessao.')
                if utc(config.registrada_em)>corte: raise HTTPException(409,'Configuracao ainda nao existia no corte.')
            else:
                config=self.db.scalar(cfgquery.where(ConfiguracaoAmbiental.registrada_em<=corte).order_by(ConfiguracaoAmbiental.versao.desc()).limit(1))
            snapshot=self._snapshot(s,data,a,b,corte,rev,runs,config)
            resultado=avaliar_ambiente(snapshot)
            anterior=self.db.scalar(select(AvaliacaoPreventiva).where(AvaliacaoPreventiva.sessao_id==s.id).order_by(
                AvaliacaoPreventiva.executada_em.desc(),AvaliacaoPreventiva.id.desc()).limit(1))
            row=AvaliacaoPreventiva(sessao_id=s.id,usuario_id=self.user.id,configuracao_id=config.id if config else None,
                anterior_id=anterior.id if anterior else None,analise_etileno_id=data.analise_etileno_id,
                chave_idempotencia=data.chave_idempotencia,assinatura=assinatura,executada_em=agora,
                inicio=a,fim=b,corte_aquisicao=corte,revisao=rev,entrada_snapshot=snapshot,resultado=resultado,
                hash_entrada=hash_documento(snapshot),hash_resultado=hash_documento(resultado))
            self.db.add(row); self.db.flush()
            for achado in resultado['achados']:
                # Same evidence in the same scope reuses an alert, even after a duplicate acquisition revision.
                identidade=hash_documento(dict(sessao_id=s.id,configuracao_id=row.configuracao_id,
                    inicio=a,fim=b,achado=achado))
                link=self.db.scalar(select(AlertaSessao).join(EvidenciaPreventiva,
                    EvidenciaPreventiva.alerta_id==AlertaSessao.alerta_id).where(
                    AlertaSessao.sessao_id==s.id,EvidenciaPreventiva.identidade==identidade).order_by(AlertaSessao.id).limit(1))
                if link is None:
                    # Keep one open operational case per rule/config version. Each evaluation adds immutable evidence.
                    link=self.db.scalar(select(AlertaSessao).join(Alerta,Alerta.id==AlertaSessao.alerta_id).join(
                        EvidenciaPreventiva,EvidenciaPreventiva.alerta_id==Alerta.id).join(
                        AvaliacaoPreventiva,AvaliacaoPreventiva.id==EvidenciaPreventiva.avaliacao_id).where(
                        AlertaSessao.sessao_id==s.id,AlertaSessao.regra==achado['regra'],
                        AvaliacaoPreventiva.configuracao_id==row.configuracao_id,
                        Alerta.status.in_([StatusAlerta.ABERTO,StatusAlerta.EM_ANALISE])).order_by(AlertaSessao.id).limit(1))
                if link is None:
                    alerta=Alerta(viagem_id=s.viagem_id,carga_id=s.carga_id,tipo=achado['regra'],
                        nivel=NivelAlerta(achado['nivel']),status=StatusAlerta.ABERTO,iniciado_em=agora)
                    self.db.add(alerta); self.db.flush()
                    link=AlertaSessao(alerta_id=alerta.id,sessao_id=s.id,identidade=identidade,regra=achado['regra'])
                    self.db.add(link); self.db.flush()
                    self._registrar_decisao(s,alerta,'CRIAR',achado['mensagem'],None,'ABERTO',uuid4(),identidade,agora)
                self.db.add(EvidenciaPreventiva(sessao_id=s.id,avaliacao_id=row.id,alerta_id=link.alerta_id,identidade=identidade,evidencia=achado))
            self.base.evento(s.configuracao_id,'AVALIACAO_PREVENTIVA',dict(id=str(row.id),revisao=rev,
                anterior_id=str(row.anterior_id) if row.anterior_id else None,hash_entrada=row.hash_entrada),s.id)
            self.db.flush()
        return self._dto_avaliacao(row)

    def _dto_avaliacao(self,row):
        dados={k:getattr(row,k) for k in ('id','created_at','updated_at','sessao_id','usuario_id','configuracao_id','anterior_id',
            'analise_etileno_id','chave_idempotencia','executada_em','inicio','fim','corte_aquisicao','revisao','hash_entrada','hash_resultado','entrada_snapshot','resultado')}
        dados['alertas_ids']=list(self.db.scalars(select(EvidenciaPreventiva.alerta_id).where(
            EvidenciaPreventiva.avaliacao_id==row.id).order_by(EvidenciaPreventiva.alerta_id)))
        return dados

    def _alerta(self,sessao_id,alerta_id,escrita=False):
        s=self._sessao(sessao_id,escrita)
        link=self.db.scalar(select(AlertaSessao).where(AlertaSessao.sessao_id==sessao_id,AlertaSessao.alerta_id==alerta_id))
        if link is None: raise HTTPException(404,'Alerta inexistente nesta sessao.')
        return s,self.base.obter(Alerta,alerta_id,lock=escrita)

    def _registrar_decisao(self,s,alerta,acao,texto,antes,depois,chave,assinatura,agora):
        o=Ocorrencia(viagem_id=s.viagem_id,carga_id=s.carga_id,tipo='DECISAO_ALERTA_PREVENTIVO',
            titulo='Alerta ambiental: '+acao,descricao=texto,registrada_em=agora,status=depois)
        self.db.add(o); self.db.flush()
        d=DecisaoAlerta(sessao_id=s.id,alerta_id=alerta.id,ocorrencia_id=o.id,usuario_id=self.user.id,
            acao=acao,estado_anterior=antes,estado_posterior=depois,registrada_em=agora,
            chave_idempotencia=chave,assinatura=assinatura)
        self.db.add(d); self.db.flush(); return d

    def decidir(self,sessao_id,alerta_id,data):
        with self.transacao():
            s,alerta=self._alerta(sessao_id,alerta_id,True); assinatura=hash_documento(data.model_dump())
            antiga=self.db.scalar(select(DecisaoAlerta).where(DecisaoAlerta.alerta_id==alerta_id,
                DecisaoAlerta.chave_idempotencia==data.chave_idempotencia))
            if antiga:
                self._replay(antiga,assinatura); return self._dto_decisao(antiga)
            antes=alerta.status.value
            if data.acao=='OBSERVAR': depois=antes
            elif data.acao=='RECONHECER' and antes=='ABERTO': depois='EM_ANALISE'
            elif data.acao in ('RESOLVER','DESCARTAR') and antes in ('ABERTO','EM_ANALISE'):
                depois='RESOLVIDO' if data.acao=='RESOLVER' else 'DESCARTADO'
            else: raise HTTPException(409,'Transicao de alerta invalida; estado terminal nao e reaberto automaticamente.')
            agora=datetime.now(timezone.utc)
            alerta.status=StatusAlerta(depois)
            if data.acao!='OBSERVAR' and depois in ('RESOLVIDO','DESCARTADO'): alerta.finalizado_em=agora
            d=self._registrar_decisao(s,alerta,data.acao,data.justificativa,antes,depois,data.chave_idempotencia,assinatura,agora)
            self.base.evento(s.configuracao_id,'DECISAO_ALERTA',dict(id=str(d.id),alerta_id=str(alerta.id),acao=data.acao),s.id)
            self.db.flush(); dto=self._dto_decisao(d)
        return dto

    def _dto_decisao(self,d):
        dados={k:getattr(d,k) for k in ('id','created_at','updated_at','sessao_id','alerta_id','ocorrencia_id','usuario_id',
            'acao','estado_anterior','estado_posterior','registrada_em')}
        dados['justificativa']=self.base.obter(Ocorrencia,d.ocorrencia_id).descricao
        return dados

    def consultar_alerta(self,sessao_id,alerta_id):
        _,a=self._alerta(sessao_id,alerta_id)
        total=self.db.scalar(select(func.count()).select_from(EvidenciaPreventiva).where(EvidenciaPreventiva.alerta_id==a.id))
        return dict(id=a.id,sessao_id=sessao_id,viagem_id=a.viagem_id,carga_id=a.carga_id,tipo=a.tipo,
            nivel=a.nivel.value,status=a.status.value,iniciado_em=utc(a.iniciado_em),
            finalizado_em=utc(a.finalizado_em) if a.finalizado_em else None,evidencias_total=total)

    def consultar_avaliacao(self,sessao_id,avaliacao_id):
        self._sessao(sessao_id)
        row=self.db.scalar(select(AvaliacaoPreventiva).where(AvaliacaoPreventiva.sessao_id==sessao_id,AvaliacaoPreventiva.id==avaliacao_id))
        if row is None: raise HTTPException(404,'Avaliacao inexistente nesta sessao.')
        return self._dto_avaliacao(row)

    def _pagina(self,query,limit,offset):
        total=self.db.scalar(select(func.count()).select_from(query.order_by(None).subquery()))
        return total,list(self.db.scalars(query.limit(limit).offset(offset)))

    def listar(self,sessao_id,tipo,limit=20,offset=0,status=None):
        self._sessao(sessao_id)
        model=ConfiguracaoAmbiental if tipo=='configuracoes' else AvaliacaoPreventiva
        if tipo=='alertas':
            q=select(AlertaSessao).join(Alerta,Alerta.id==AlertaSessao.alerta_id).where(AlertaSessao.sessao_id==sessao_id)
            if status: q=q.where(Alerta.status==StatusAlerta(status))
            q=q.order_by(Alerta.iniciado_em.desc(),Alerta.id.desc())
            total,rows=self._pagina(q,limit,offset)
            dados=[self.consultar_alerta(sessao_id,r.alerta_id) for r in rows]
        else:
            q=select(model).where(model.sessao_id==sessao_id).order_by(model.created_at.desc(),model.id.desc())
            if tipo=='configuracoes': q=q.order_by(None).order_by(model.versao.desc())
            else: q=q.order_by(None).order_by(model.executada_em.desc(),model.id.desc())
            total,dados=self._pagina(q,limit,offset)
            if tipo=='avaliacoes': dados=[self._dto_avaliacao(r) for r in dados]
        return dict(total=total,limit=limit,offset=offset,**{tipo:dados})

    def historico(self,sessao_id,alerta_id,tipo,limit=20,offset=0):
        self._alerta(sessao_id,alerta_id)
        model=DecisaoAlerta if tipo=='decisoes' else EvidenciaPreventiva
        q=select(model).where(model.alerta_id==alerta_id,model.sessao_id==sessao_id)
        q=q.order_by(model.registrada_em,model.id) if tipo=='decisoes' else q.order_by(model.created_at,model.id)
        total,rows=self._pagina(q,limit,offset)
        dados=[self._dto_decisao(r) for r in rows] if tipo=='decisoes' else [serializar(dict(id=r.id,
            avaliacao_id=r.avaliacao_id,alerta_id=r.alerta_id,identidade=r.identidade,evidencia=r.evidencia)) for r in rows]
        return dict(total=total,limit=limit,offset=offset,**{tipo:dados})
