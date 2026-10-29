"""Atomic snapshot/calculate/persist orchestration; q(T) belongs only to etileno."""
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from app.models.analises_etileno import AnaliseEtileno
from app.models.historico_iot import SincronizacaoIoT
from app.models.sessoes_monitoramento import CargaMonitoramento
from app.modules.monitoramento.etileno import estimar_etileno
from app.modules.monitoramento.historico_service import HistoricoIoTService
from app.modules.monitoramento.analises_adapter import montar_entrada, serializar, hash_documento
from app.modules.monitoramento.service import utc


class AnalisesEtilenoService(HistoricoIoTService):
    def executar(self,sessao_id,data):
        try:
            with self.base.transacao():
                # Same trip/cargo/session lock order as acquisition sealing and session close.
                sessao=self._sessao(sessao_id,escrita=True)
                assinatura=hash_documento(data.model_dump())
                anterior=self.db.scalar(select(AnaliseEtileno).where(
                    AnaliseEtileno.sessao_id==sessao_id,AnaliseEtileno.chave_idempotencia==data.chave_idempotencia))
                if anterior is not None:
                    if anterior.usuario_id!=self.user.id or anterior.assinatura_requisicao!=assinatura:
                        raise HTTPException(409,'Chave idempotente ja utilizada com outro autor ou parametros.')
                    return anterior  # Replays survive session cancellation and later revisions.
                if sessao.estado=='CANCELADA':
                    raise HTTPException(409,'Sessao cancelada permite consultar analises anteriores, sem novas execucoes.')
                if not sessao.configuracao_id or self.db.get(CargaMonitoramento,sessao.configuracao_id) is None:
                    raise HTTPException(409,'Sessao sem configuracao de carga rastreavel.')
                agora=datetime.now(timezone.utc)
                if sessao.estado=='ATIVA' and data.corte_aquisicao is None:
                    raise HTTPException(422,'Sessao ativa exige corte_aquisicao explicito.')
                corte=utc(data.corte_aquisicao) if data.corte_aquisicao else agora
                if corte>agora: raise HTTPException(422,'Corte de aquisicao nao pode estar no futuro.')
                a=utc(data.inicio) if data.inicio else utc(sessao.inicio)
                limite=utc(sessao.fim) if sessao.fim else corte
                b=utc(data.fim) if data.fim else limite
                if a<utc(sessao.inicio) or b>limite or b>corte or b<=a:
                    raise HTTPException(422,'Janela deve ser positiva e estar integralmente dentro da sessao e do corte.')
                elegiveis=select(SincronizacaoIoT).where(SincronizacaoIoT.sessao_id==sessao_id,
                    SincronizacaoIoT.estado!='EM_EXECUCAO',SincronizacaoIoT.finalizada_em<=corte)
                if data.revisao_aquisicao is None:
                    run=self.db.scalar(elegiveis.order_by(SincronizacaoIoT.revisao.desc()).limit(1))
                    revisao=run.revisao if run else 0
                else:
                    revisao=data.revisao_aquisicao
                    if revisao:
                        run=self.db.scalar(select(SincronizacaoIoT).where(
                            SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.revisao==revisao))
                        if run is None: raise HTTPException(404,'Revisao de aquisicao inexistente.')
                        if run.estado=='EM_EXECUCAO' or not run.finalizada_em or utc(run.finalizada_em)>corte:
                            raise HTTPException(409,'Revisao ainda nao consolidada no corte solicitado.')
                rows=self.db.execute(self.repo.registros(sessao_id,revisao,a,b,'TEMPERATURA')).all()
                rows=[row for row in rows if utc(row[0].processada_em)<=corte]
                ocorrencias=[o for o in self.repo.ocorrencias(sessao_id,revisao) if utc(o.processada_em)<=corte]
                fontes=self.repo.fontes(sessao_id)
                entrada,snapshot=montar_entrada(sessao,a,b,corte,data.modo,data.intervalo_maximo_s,rows,ocorrencias,fontes)
                snapshot['sessao']=serializar(dict(id=sessao.id,estado=sessao.estado,inicio=sessao.inicio,fim=sessao.fim,
                    configuracao_id=sessao.configuracao_id,configuracao_versao=sessao.configuracao_versao,
                    produto_identificado=sessao.produto_identificado,lote_codigo=sessao.lote_codigo,
                    lote_hipotetico=sessao.lote_hipotetico,origem_sensor=sessao.origem_sensor))
                runs=list(self.db.scalars(elegiveis.where(SincronizacaoIoT.revisao<=revisao).order_by(SincronizacaoIoT.revisao)))
                snapshot['aquisicao']=serializar(dict(revisao=revisao,corte=corte,
                    tentativas=[dict(id=r.id,revisao=r.revisao,estado=r.estado,
                        finalizada_em=r.finalizada_em,inicio_janela=r.inicio_janela,fim_janela=r.fim_janela) for r in runs]))
                resultado=estimar_etileno(entrada)
                saida=serializar(resultado)
                # Full inputs are already stored once. Intervals and reference rates remain in output.
                saida.pop('entrada',None); saida.pop('observacoes',None)
                analise=AnaliseEtileno(sessao_id=sessao_id,usuario_id=self.user.id,
                    chave_idempotencia=data.chave_idempotencia,assinatura_requisicao=assinatura,
                    executada_em=agora,inicio=a,fim=b,corte_aquisicao=corte,revisao_aquisicao=revisao,
                    massa_kg=resultado.massa_kg,maturacao=sessao.maturacao,modo=data.modo.value,
                    intervalo_maximo_s=data.intervalo_maximo_s,versao_modelo=resultado.versao_modelo,
                    status_calculo=resultado.status_calculo.value,classificacao_risco_etileno=resultado.classificacao_risco_etileno,
                    hash_entrada=hash_documento(snapshot),hash_resultado=hash_documento(saida),
                    entrada_snapshot=snapshot,resultado=saida)
                self.db.add(analise); self.db.flush()
                self.base.evento(sessao.configuracao_id,'ANALISE_ETILENO',dict(analise_id=str(analise.id),
                    revisao=revisao,hash_entrada=analise.hash_entrada,hash_resultado=analise.hash_resultado),sessao_id)
                self.db.flush()
            return analise
        except SQLAlchemyError:
            # No partial result survives failure; do not expose SQL, credentials or parameters.
            self.db.rollback()
            raise HTTPException(503,'Falha ao confirmar a analise; consulte ou repita a mesma chave idempotente.') from None

    def consultar(self,sessao_id,analise_id):
        self._sessao(sessao_id)
        analise=self.db.scalar(select(AnaliseEtileno).where(AnaliseEtileno.id==analise_id,AnaliseEtileno.sessao_id==sessao_id))
        if analise is None: raise HTTPException(404,'Analise inexistente nesta sessao.')
        return analise

    def listar(self,sessao_id,limit=20,offset=0):
        self._sessao(sessao_id)
        query=select(AnaliseEtileno).where(AnaliseEtileno.sessao_id==sessao_id)
        total=self.db.scalar(select(func.count()).select_from(query.subquery()))
        rows=list(self.db.scalars(query.order_by(AnaliseEtileno.executada_em.desc(),AnaliseEtileno.id.desc()).limit(limit).offset(offset)))
        return dict(sessao_id=sessao_id,total=total,limit=limit,offset=offset,analises=rows)
