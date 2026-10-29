"""Supervised state machine for a vehicle's virtual actuator. No network/device I/O."""
from contextlib import contextmanager
from datetime import datetime,timedelta,timezone
from decimal import Decimal
import re
from fastapi import HTTPException
from sqlalchemy import select,func
from sqlalchemy.exc import SQLAlchemyError
from app.models.exaustao_simulada import IntervencaoSimulada,AcaoIntervencao
from app.models.preventivo import AlertaSessao,AvaliacaoPreventiva,EvidenciaPreventiva
from app.models.analises_etileno import AnaliseEtileno
from app.models.monitoramento import Alerta,Ocorrencia
from app.models.logistica import Carga,Viagem,Veiculo
from app.models.empresa import Empresa
from app.models.enums import StatusViagem,StatusCarga
from app.models.sessoes_monitoramento import SessaoMonitoramento
from app.modules.monitoramento.historico_service import HistoricoIoTService
from app.modules.monitoramento.analises_adapter import serializar,hash_documento
from app.modules.monitoramento.service import utc

TRANSICOES={
    'SOLICITADA':{'AUTORIZAR':'AUTORIZADA','RECUSAR':'RECUSADA','CANCELAR':'CANCELADA'},
    'AUTORIZADA':{'INICIAR':'EM_EXECUCAO','CANCELAR':'CANCELADA'},
    'EM_EXECUCAO':{'ENCERRAR':'CONCLUIDA','CANCELAR':'CANCELADA','REGISTRAR_FALHA':'FALHA_SIMULACAO'},
}
LIMITACOES=[
    'Atuador exclusivamente virtual; nenhuma mensagem ou comando fisico e enviado.',
    'Duracao de demonstracao, sem eficacia cientifica ou encerramento automatico.',
    'Nao altera medicoes, analises, amadurecimento, concentracao ou volume de etileno.',
    'Finalizacao comprova somente a transicao logica registrada; risco etileno NAO_AVALIADO.',
]
SEGREDOS=re.compile(r'(?i)(?:\bbearer\s+\S+|\b(?:api[_ -]?key|senha|password|secret|token|authorization)\s*[:=]\s*\S+|\beyJ[\w-]+\.[\w-]+\.[\w-]+\b|-----BEGIN [\w ]*PRIVATE KEY-----|https?://[^\s/:]+:[^\s@]+@)')


def agora_utc(): return datetime.now(timezone.utc)


def validar_texto(texto):
    if SEGREDOS.search(texto):
        raise HTTPException(422,'Justificativa contem possivel credencial; remova o segredo antes de registrar.')


def segundos(a,b):
    d=b-a
    return Decimal(d.days*86400+d.seconds)+Decimal(d.microseconds)/1000000


class ExaustaoSimuladaService(HistoricoIoTService):
    @contextmanager
    def transacao(self):
        try:
            with self.base.transacao(): yield
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(503,'Falha ao confirmar intervencao; consulte ou repita a mesma chave idempotente.') from None

    def _escritor(self):
        if not self.user.perfil or self.user.perfil.nome not in ('ADMIN','GESTOR','OPERADOR'):
            raise HTTPException(403,'Perfil sem permissao para intervencoes simuladas.')

    def _sessao_administrativa(self,sessao_id):
        # Cleanup remains possible for terminal sessions; ADMIN can recover an inactive company.
        # Preserve enterprise scope and the established trip/cargo/session lock order.
        original=self.base.obter(SessaoMonitoramento,sessao_id)
        carga=self.base.obter(Carga,original.carga_id)
        viagem=self.base.obter(Viagem,carga.viagem_id,lock=True)
        self.base.autorizar_viagem(viagem,escrita=False)
        carga=self.base.obter(Carga,carga.id,lock=True)
        s=self.base.obter(SessaoMonitoramento,sessao_id,lock=True)
        if carga.viagem_id!=viagem.id or s.carga_id!=carga.id or s.viagem_id!=viagem.id:
            raise HTTPException(409,'Contexto da sessao mudou durante a operacao; repita a consulta.')
        return s

    def _contexto(self,s):
        return self.base.obter(Viagem,s.viagem_id),self.base.obter(Carga,s.carga_id)

    def _referencias(self,s,alerta_id,avaliacao_id,analise_id):
        snapshot=dict(sessao_id=s.id,estado_sessao=s.estado,viagem_id=s.viagem_id,carga_id=s.carga_id,
            maturacao=s.maturacao,ambiente=s.ambiente_aquisicao,alerta=None,avaliacao=None,analise=None)
        if alerta_id:
            link=self.db.scalar(select(AlertaSessao).where(AlertaSessao.sessao_id==s.id,AlertaSessao.alerta_id==alerta_id))
            if link is None: raise HTTPException(404,'Alerta inexistente nesta sessao.')
            alerta=self.base.obter(Alerta,alerta_id)
            evidencias=list(self.db.scalars(select(EvidenciaPreventiva).where(
                EvidenciaPreventiva.alerta_id==alerta.id,EvidenciaPreventiva.sessao_id==s.id).order_by(
                EvidenciaPreventiva.created_at,EvidenciaPreventiva.id)))
            snapshot['alerta']=dict(id=alerta.id,tipo=alerta.tipo,estado=alerta.status.value,nivel=alerta.nivel.value,
                contexto_compativel=alerta.viagem_id==s.viagem_id and alerta.carga_id==s.carga_id,
                evidencias=[dict(id=e.id,avaliacao_id=e.avaliacao_id,identidade=e.identidade,
                    hash_evidencia=hash_documento(e.evidencia)) for e in evidencias])
        if avaliacao_id:
            a=self.db.scalar(select(AvaliacaoPreventiva).where(AvaliacaoPreventiva.sessao_id==s.id,AvaliacaoPreventiva.id==avaliacao_id))
            if a is None: raise HTTPException(404,'Avaliacao inexistente nesta sessao.')
            if alerta_id and not self.db.scalar(select(EvidenciaPreventiva.id).where(
                EvidenciaPreventiva.avaliacao_id==a.id,EvidenciaPreventiva.alerta_id==alerta_id)):
                raise HTTPException(409,'Avaliacao indicada nao sustenta o alerta selecionado.')
            snapshot['avaliacao']=dict(id=a.id,hash_entrada=a.hash_entrada,hash_resultado=a.hash_resultado,
                revisao=a.revisao,inicio=a.inicio,fim=a.fim,status=a.resultado['status'])
        if analise_id:
            a=self.db.scalar(select(AnaliseEtileno).where(AnaliseEtileno.sessao_id==s.id,AnaliseEtileno.id==analise_id))
            if a is None: raise HTTPException(404,'Analise inexistente nesta sessao.')
            if avaliacao_id:
                av=snapshot['avaliacao']
                if utc(a.inicio)!=utc(av['inicio']) or utc(a.fim)!=utc(av['fim']) or a.revisao_aquisicao!=av['revisao']:
                    raise HTTPException(409,'Analise e avaliacao devem ter a mesma janela e revisao.')
            snapshot['analise']=dict(id=a.id,hash_resultado=a.hash_resultado,versao_modelo=a.versao_modelo,
                status=a.status_calculo,classificacao_risco_etileno='NAO_AVALIADO')
        return serializar(snapshot)

    def _referencias_atuais(self,i,s):
        try:
            return self._referencias(s,i.alerta_id,i.avaliacao_id,i.analise_etileno_id)
        except HTTPException as exc:
            # Inconsistent historical references must never prevent an administrative stop.
            return dict(referencias_inconsistentes=True,codigo=exc.status_code,
                alerta_id=str(i.alerta_id) if i.alerta_id else None,
                avaliacao_id=str(i.avaliacao_id) if i.avaliacao_id else None,
                analise_etileno_id=str(i.analise_etileno_id) if i.analise_etileno_id else None)

    def _mudou(self,i,s,viagem,carga):
        return i.viagem_id!=s.viagem_id or i.carga_id!=s.carga_id or carga.viagem_id!=i.viagem_id or viagem.veiculo_id!=i.veiculo_id

    def _contexto_liberado(self,i,s,viagem,carga,referencias):
        veiculo=self.base.obter(Veiculo,viagem.veiculo_id)
        empresa=self.base.obter(Empresa,viagem.transportadora_id)
        alerta=referencias.get('alerta')
        return (not referencias.get('referencias_inconsistentes') and s.estado=='ATIVA' and viagem.status==StatusViagem.EM_ANDAMENTO and carga.status==StatusCarga.EM_TRANSITO
            and veiculo.ativo and empresa.ativo and (i is None or not self._mudou(i,s,viagem,carga))
            and (not alerta or (alerta['contexto_compativel'] and alerta['estado'] in ('ABERTO','EM_ANALISE'))))

    def _replay(self,row,assinatura,autor):
        if row.assinatura!=assinatura or autor!=self.user.id:
            raise HTTPException(409,'Chave idempotente ja utilizada com outro autor ou parametros.')

    def solicitar(self,sessao_id,data):
        validar_texto(data.justificativa); self._escritor()
        with self.transacao():
            # Existing request replays are read-only, even after closure/inactivation.
            s=self._sessao_administrativa(sessao_id)
            assinatura=hash_documento(dict(acao='SOLICITAR',payload=data.model_dump()))
            antiga=self.db.scalar(select(IntervencaoSimulada).where(IntervencaoSimulada.sessao_id==s.id,
                IntervencaoSimulada.chave_idempotencia==data.chave_idempotencia))
            if antiga:
                self._replay(antiga,assinatura,antiga.solicitante_id)
                return self._dto(antiga,s)
            viagem,carga=self._contexto(s)
            refs=self._referencias(s,data.alerta_id,data.avaliacao_id,data.analise_etileno_id)
            if not self._contexto_liberado(None,s,viagem,carga,refs):
                raise HTTPException(409,'Nova solicitacao exige sessao/logistica ativas e alerta nao terminal/compativel, quando indicado.')
            refs['veiculo_id']=str(viagem.veiculo_id)
            agora=agora_utc()
            i=IntervencaoSimulada(sessao_id=s.id,viagem_id=s.viagem_id,carga_id=s.carga_id,veiculo_id=viagem.veiculo_id,
                alerta_id=data.alerta_id,avaliacao_id=data.avaliacao_id,analise_etileno_id=data.analise_etileno_id,
                solicitante_id=self.user.id,modalidade='SIMULADA',estado='SOLICITADA',chave_idempotencia=data.chave_idempotencia,
                assinatura=assinatura,justificativa_solicitacao=data.justificativa,solicitada_em=agora,
                duracao_planejada_s=data.duracao_planejada_s,referencias_snapshot=refs,hash_referencias=hash_documento(refs))
            self.db.add(i); self.db.flush()
            self._registrar(s,i,'SOLICITAR',None,'SOLICITADA',data.justificativa,data.chave_idempotencia,assinatura,refs,agora)
        return self._dto(i,s)

    def _papel_permite(self,i,acao):
        perfil=self.user.perfil.nome
        if perfil in ('ADMIN','GESTOR'): return True
        if perfil!='OPERADOR' or i.solicitante_id!=self.user.id: return False
        return acao=='ENCERRAR' or (acao=='CANCELAR' and i.estado=='SOLICITADA')

    def _ocupado(self,i):
        return self.db.scalar(select(IntervencaoSimulada.id).where(IntervencaoSimulada.veiculo_id==i.veiculo_id,
            IntervencaoSimulada.estado=='EM_EXECUCAO',IntervencaoSimulada.id!=i.id)) is not None

    def agir(self,sessao_id,intervencao_id,data):
        validar_texto(data.justificativa); self._escritor()
        with self.transacao():
            s=self._sessao_administrativa(sessao_id)
            i=self._obter(s.id,intervencao_id,lock=True)
            assinatura=hash_documento(data.model_dump())
            antiga=self.db.scalar(select(AcaoIntervencao).where(AcaoIntervencao.intervencao_id==i.id,
                AcaoIntervencao.chave_idempotencia==data.chave_idempotencia))
            if antiga:
                self._replay(antiga,assinatura,antiga.usuario_id); return self._dto_acao(antiga)
            if not self._papel_permite(i,data.acao): raise HTTPException(403,'Acao exige GESTOR/ADMIN ou responsabilidade de encerramento/retirada da propria solicitacao.')
            depois=TRANSICOES.get(i.estado,{}).get(data.acao)
            if depois is None: raise HTTPException(409,'Transicao de intervencao invalida; terminal nao pode ser reaberto.')
            viagem,carga=self._contexto(s)
            refs=self._referencias_atuais(i,s)
            if data.acao in ('AUTORIZAR','INICIAR') and not self._contexto_liberado(i,s,viagem,carga,refs):
                raise HTTPException(409,'Autorizacao/inicio exige sessao/logistica ativas e contexto/alerta compativeis.')
            # Shared vehicle row serializes starts/stops across sessions and trips.
            self.base.obter(Veiculo,i.veiculo_id,lock=True)
            if data.acao=='INICIAR' and self._ocupado(i): raise HTTPException(409,'Exaustor virtual deste veiculo ja esta em execucao.')
            agora=agora_utc()
            ultima=self.db.scalar(select(func.max(AcaoIntervencao.registrada_em)).where(AcaoIntervencao.intervencao_id==i.id))
            if ultima and agora<utc(ultima): raise HTTPException(409,'Relogio anterior ao ultimo evento; transicao nao registrada.')
            antes=i.estado
            # Flush only after all fields forming a lifecycle state are ready.
            usuario_id=self.user.id
            if data.acao in ('AUTORIZAR','RECUSAR'): i.decidida_em=agora; i.decidida_por_id=usuario_id
            if data.acao=='INICIAR':
                i.iniciada_em=agora; i.iniciada_por_id=usuario_id
                i.prazo_planejado_em=agora+timedelta(milliseconds=int(i.duracao_planejada_s*1000))
            if data.acao in ('ENCERRAR','CANCELAR','REGISTRAR_FALHA'):
                i.finalizada_em=agora; i.finalizada_por_id=usuario_id; i.motivo_fim=data.justificativa
                if i.iniciada_em: i.duracao_registrada_s=segundos(utc(i.iniciada_em),agora)
            i.estado=depois
            contexto=refs|dict(contexto_logistico_alterado=self._mudou(i,s,viagem,carga),
                modalidade='SIMULADA',hash_referencias_solicitacao=i.hash_referencias)
            acao=self._registrar(s,i,data.acao,antes,depois,data.justificativa,data.chave_idempotencia,assinatura,contexto,agora)
            self.db.flush(); resposta=self._dto_acao(acao)
        return resposta

    def _registrar(self,s,i,acao,antes,depois,texto,chave,assinatura,contexto,agora):
        numero=(self.db.scalar(select(func.max(AcaoIntervencao.numero)).where(AcaoIntervencao.intervencao_id==i.id)) or 0)+1
        o=Ocorrencia(viagem_id=i.viagem_id,carga_id=i.carga_id,tipo='INTERVENCAO_SIMULADA',
            titulo='Exaustor virtual: '+acao,descricao=texto,registrada_em=agora,status=depois)
        self.db.add(o); self.db.flush()
        a=AcaoIntervencao(sessao_id=s.id,intervencao_id=i.id,ocorrencia_id=o.id,usuario_id=self.user.id,
            chave_idempotencia=chave,assinatura=assinatura,numero=numero,acao=acao,estado_anterior=antes,
            estado_posterior=depois,registrada_em=agora,contexto_snapshot=serializar(contexto))
        self.db.add(a); self.db.flush()
        self.base.evento(s.configuracao_id,'EXAUSTAO_SIMULADA',dict(intervencao_id=str(i.id),acao_id=str(a.id),
            numero=numero,acao=acao,estado_anterior=antes,estado_posterior=depois,modalidade='SIMULADA'),s.id)
        self.db.flush(); return a

    def _obter(self,sessao_id,intervencao_id,lock=False):
        q=select(IntervencaoSimulada).where(IntervencaoSimulada.id==intervencao_id,IntervencaoSimulada.sessao_id==sessao_id)
        if lock: q=q.with_for_update().execution_options(populate_existing=True)
        row=self.db.scalar(q)
        if row is None: raise HTTPException(404,'Intervencao inexistente nesta sessao.')
        return row

    def _dto_acao(self,a):
        dados={c.name:getattr(a,c.name) for c in a.__table__.columns if c.name!='assinatura'}
        dados['justificativa']=self.base.obter(Ocorrencia,a.ocorrencia_id).descricao
        return dados

    def _dto(self,i,s):
        dados={c.name:getattr(i,c.name) for c in i.__table__.columns if c.name!='assinatura'}
        agora=agora_utc(); viagem,carga=self._contexto(s)
        refs=self._referencias_atuais(i,s)
        permitidas=[]
        for acao in TRANSICOES.get(i.estado,{}):
            if not self._papel_permite(i,acao): continue
            if acao in ('AUTORIZAR','INICIAR') and not self._contexto_liberado(i,s,viagem,carga,refs): continue
            if acao=='INICIAR' and self._ocupado(i): continue
            permitidas.append(acao)
        return dados|dict(atuador_virtual_id='EXAUSTOR_VIRTUAL:VEICULO:'+str(i.veiculo_id),virtual_ligado=i.estado=='EM_EXECUCAO',
            atuador_virtual_ocupado=i.estado=='EM_EXECUCAO' or self._ocupado(i),
            prazo_excedido=bool(i.estado=='EM_EXECUCAO' and i.prazo_planejado_em and agora>utc(i.prazo_planejado_em)),
            consultado_em=agora,sessao_terminal_com_execucao=s.estado!='ATIVA' and i.estado=='EM_EXECUCAO',
            contexto_logistico_alterado=self._mudou(i,s,viagem,carga),acoes_permitidas=permitidas,
            referencias_atuais=refs,hash_referencias_atuais=hash_documento(refs),
            resultado_operacional='ESTADO_VIRTUAL_'+i.estado,limitacoes=LIMITACOES)

    def consultar(self,sessao_id,intervencao_id):
        s=self._sessao(sessao_id)
        return self._dto(self._obter(sessao_id,intervencao_id),s)

    def listar(self,sessao_id,limit=20,offset=0,estado=None):
        s=self._sessao(sessao_id)
        q=select(IntervencaoSimulada).where(IntervencaoSimulada.sessao_id==sessao_id)
        if estado: q=q.where(IntervencaoSimulada.estado==estado)
        total=self.db.scalar(select(func.count()).select_from(q.subquery()))
        rows=list(self.db.scalars(q.order_by(IntervencaoSimulada.solicitada_em.desc(),IntervencaoSimulada.id.desc()).limit(limit).offset(offset)))
        return dict(total=total,limit=limit,offset=offset,intervencoes=[self._dto(i,s) for i in rows])

    def historico(self,sessao_id,intervencao_id,limit=20,offset=0):
        self._sessao(sessao_id); self._obter(sessao_id,intervencao_id)
        q=select(AcaoIntervencao).where(AcaoIntervencao.intervencao_id==intervencao_id,AcaoIntervencao.sessao_id==sessao_id)
        total=self.db.scalar(select(func.count()).select_from(q.subquery()))
        rows=list(self.db.scalars(q.order_by(AcaoIntervencao.numero).limit(limit).offset(offset)))
        return dict(total=total,limit=limit,offset=offset,acoes=[self._dto_acao(a) for a in rows])
