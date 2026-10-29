"""Real JWT, isolated SQLite and deterministic clock; no physical or production I/O."""
from datetime import datetime,timedelta,timezone
from decimal import Decimal
from uuid import uuid4,UUID
import json
import pytest
from sqlalchemy import select,func
from sqlalchemy.exc import IntegrityError,OperationalError
from app.models.exaustao_simulada import IntervencaoSimulada,AcaoIntervencao
from app.models.monitoramento import Alerta,Ocorrencia
from app.models.sessoes_monitoramento import SessaoMonitoramento,EventoMonitoramento
from app.models.analises_etileno import AnaliseEtileno
from app.models.preventivo import AvaliacaoPreventiva,DecisaoAlerta
from app.models.logistica import Veiculo
from app.models.enums import StatusViagem,StatusCarga
from app.modules.monitoramento.analises_adapter import hash_documento
import app.modules.monitoramento.exaustao_service as module
from tests.test_monitoramento_sessoes import world,headers,finish,count,start,start_body,stamp
from tests.test_historico_iot import iot
from tests.test_analises_etileno import analyses,execute as estimate
from tests.test_preventivo import preventive,setup,evaluation,decide as decide_alert


@pytest.fixture
def simulation(preventive,monkeypatch):
    w=preventive
    for model in (IntervencaoSimulada,AcaoIntervencao): model.__table__.create(w['db'].get_bind())
    w['clock']=datetime.now(timezone.utc)
    monkeypatch.setattr(module,'agora_utc',lambda:w['clock'])
    return w


def root(w): return '/api/v1/monitoramentos/'+w['session']['id']+'/intervencoes-simuladas'


def request_body(**changes):
    return dict(chave_idempotencia=str(uuid4()),justificativa='Demonstracao supervisionada; sem efeito fisico ou cientifico.',duracao_planejada_s='60')|changes


def request(w,payload=None,role='OPERADOR',**changes):
    return w['client'].post(root(w),headers=headers(w,role),json=(payload or request_body())|changes)


def requested(w,**changes):
    r=request(w,**changes); assert r.status_code==200,r.text; return r.json()


def act(w,i,acao='AUTORIZAR',payload=None,role='GESTOR',**changes):
    data=payload or dict(chave_idempotencia=str(uuid4()),acao=acao,justificativa='Responsavel confirmou a decisao virtual.')
    return w['client'].post(root(w)+'/'+i+'/acoes',headers=headers(w,role),json=data|changes)


def view(w,i,role='OPERADOR'):
    r=w['client'].get(root(w)+'/'+i,headers=headers(w,role)); assert r.status_code==200,r.text; return r.json()


def history(w,i,**params):
    return w['client'].get(root(w)+'/'+i+'/acoes',headers=headers(w),params=params)


def started(w,**changes):
    i=requested(w,**changes)['id']
    for action in ('AUTORIZAR','INICIAR'):
        r=act(w,i,action); assert r.status_code==200,r.text
    return i


def with_alert(w):
    w['payload']['feeds'][0]['field4']='20'; setup(w,False)
    e=evaluation(w); return e['alertas_ids'][0],e


def test_request_without_alert_is_pending_and_audited(simulation):
    w=simulation; i=requested(w)
    assert i['estado']=='SOLICITADA' and i['modalidade']=='SIMULADA' and not i['virtual_ligado']
    assert i['alerta_id'] is None and i['decidida_por_id'] is None
    assert i['duracao_registrada_s'] is None
    assert i['acoes_permitidas']==['CANCELAR']
    assert i['hash_referencias']==hash_documento(i['referencias_snapshot'])
    assert i['atuador_virtual_id']=='EXAUSTOR_VIRTUAL:VEICULO:'+str(w['trip'].veiculo_id)
    assert count(w,IntervencaoSimulada)==count(w,AcaoIntervencao)==count(w,Ocorrencia)==1
    h=history(w,i['id']).json()['acoes'][0]
    assert h['acao']=='SOLICITAR' and h['usuario_id']==str(w['users']['OPERADOR'].id)


def test_authorization_is_separate_from_start_and_explicit_end(simulation):
    w=simulation; i=requested(w)['id']; a=act(w,i).json()
    assert a['estado_posterior']=='AUTORIZADA'
    approved=view(w,i); assert not approved['virtual_ligado']
    assert approved['decidida_por_id']==str(w['users']['GESTOR'].id)
    assert act(w,i,'INICIAR').status_code==200
    running=view(w,i); assert running['estado']=='EM_EXECUCAO' and running['virtual_ligado']
    w['clock']+=timedelta(seconds=120,microseconds=125000)
    overdue=view(w,i)
    assert overdue['prazo_excedido'] and overdue['estado']=='EM_EXECUCAO'
    assert overdue['finalizada_em'] is None and overdue['duracao_registrada_s'] is None
    assert act(w,i,'ENCERRAR',role='OPERADOR').status_code==200
    ended=view(w,i)
    assert ended['estado']=='CONCLUIDA' and not ended['virtual_ligado'] and not ended['prazo_excedido']
    assert ended['duracao_registrada_s']=='120.125000'
    assert ended['finalizada_por_id']==str(w['users']['OPERADOR'].id)
    assert [x['acao'] for x in history(w,i).json()['acoes']]==['SOLICITAR','AUTORIZAR','INICIAR','ENCERRAR']
    assert count(w,Ocorrencia)==count(w,AcaoIntervencao)==4


def test_refusal_never_resolves_original_alert(simulation):
    w=simulation; alerta,e=with_alert(w); i=requested(w,alerta_id=alerta,avaliacao_id=e['id'])['id']
    assert act(w,i,'RECUSAR').status_code==200
    v=view(w,i); assert v['estado']=='RECUSADA' and v['decidida_por_id']==str(w['users']['GESTOR'].id)
    assert not v['virtual_ligado'] and v['iniciada_em'] is None
    assert w['db'].get(Alerta,UUID(alerta)).status.value=='ABERTO'
    assert act(w,i,'INICIAR').status_code==409


@pytest.mark.parametrize('action',['AUTORIZAR','RECUSAR','INICIAR','REGISTRAR_FALHA'])
def test_operator_cannot_make_privileged_decisions(simulation,action):
    w=simulation; i=requested(w)['id']
    assert act(w,i,action,role='OPERADOR').status_code==403
    assert count(w,AcaoIntervencao)==1


def test_start_without_authorization_and_terminal_reopening_rejected(simulation):
    w=simulation; i=requested(w)['id']
    assert act(w,i,'INICIAR').status_code==409
    assert act(w,i,'ENCERRAR').status_code==409
    assert act(w,i,'CANCELAR',role='OPERADOR').status_code==200
    for action in ('AUTORIZAR','INICIAR','RECUSAR','ENCERRAR','CANCELAR'):
        assert act(w,i,action).status_code==409
    assert view(w,i)['duracao_registrada_s'] is None


@pytest.mark.parametrize('phase',['SOLICITADA','AUTORIZADA','EM_EXECUCAO'])
def test_manager_cancels_each_nonterminal_state(simulation,phase):
    w=simulation; i=requested(w)['id']
    if phase!='SOLICITADA': assert act(w,i).status_code==200
    if phase=='EM_EXECUCAO': assert act(w,i,'INICIAR').status_code==200
    w['clock']+=timedelta(seconds=10)
    assert act(w,i,'CANCELAR').status_code==200
    v=view(w,i); assert v['estado']=='CANCELADA' and v['motivo_fim']
    assert (v['duracao_registrada_s']=='10.000000') if phase=='EM_EXECUCAO' else (v['duracao_registrada_s'] is None)


def test_failure_is_explicit_simulated_and_terminal(simulation):
    w=simulation; i=started(w); w['clock']+=timedelta(seconds=3)
    r=act(w,i,'REGISTRAR_FALHA',justificativa='Falha logica introduzida somente para demonstracao.')
    assert r.status_code==200,r.text
    v=view(w,i); assert v['estado']=='FALHA_SIMULACAO' and not v['virtual_ligado']
    assert v['duracao_registrada_s']=='3.000000' and v['classificacao_risco_etileno']=='NAO_AVALIADO'
    assert act(w,i,'INICIAR').status_code==409


@pytest.mark.parametrize('changes',[
    {'justificativa':''},{'justificativa':' '},{'justificativa':None},{'duracao_planejada_s':None},
    {'duracao_planejada_s':'0'},{'duracao_planejada_s':'-1'},{'duracao_planejada_s':'NaN'},
    {'duracao_planejada_s':'Infinity'},{'duracao_planejada_s':True},{'duracao_planejada_s':'86400.001'},
    {'duracao_planejada_s':'1.0001'},
    {'dispositivo_id':str(uuid4())},{'modalidade':'FISICA'},{'comando':'LIGAR'},
    {'estado':'EM_EXECUCAO'},{'iniciada_em':'2026-10-28T10:00:00Z'},
])
def test_invalid_request_or_hardware_fields_rejected(simulation,changes):
    assert request(simulation,**changes).status_code==422
    assert count(simulation,IntervencaoSimulada)==0


@pytest.mark.parametrize('secret',[
    'api_key=DEMONSTRATION_SECRET','Bearer DUMMY_TOKEN','password: DUMMY_PASSWORD',
    'token=DUMMY_TOKEN','-----BEGIN PRIVATE KEY----- DEMO',
    'https://usuario:senha@example.invalid',
])
def test_sensitive_justification_not_persisted(simulation,secret):
    w=simulation
    r=request(w,justificativa='Nao registrar '+secret)
    assert r.status_code==422 and secret not in r.text
    assert count(w,IntervencaoSimulada)==count(w,AcaoIntervencao)==count(w,Ocorrencia)==0


def test_action_secret_validation_and_justification(simulation):
    w=simulation; i=requested(w)['id']
    assert act(w,i,justificativa=' ').status_code==422
    assert act(w,i,justificativa='api_key=DEMO_ONLY').status_code==422
    assert act(w,i,acao='LIGAR_FISICAMENTE').status_code==422
    assert act(w,i,dispositivo_id=str(uuid4())).status_code==422
    assert count(w,AcaoIntervencao)==1


def test_idempotent_request_and_actions_return_existing_records(simulation):
    w=simulation; p=request_body(); i=request(w,p).json()['id']
    assert request(w,p).json()['id']==i
    assert request(w,p,duracao_planejada_s='90').status_code==409
    assert request(w,p,role='GESTOR').status_code==409
    a=dict(chave_idempotencia=str(uuid4()),acao='AUTORIZAR',justificativa='Gestor autorizou esta demonstracao.')
    d=act(w,i,payload=a).json(); assert act(w,i,payload=a).json()==d
    assert act(w,i,payload=a,role='ADMIN').status_code==409
    assert act(w,i,payload=a,justificativa='Outra justificativa.').status_code==409
    assert act(w,i,'INICIAR').status_code==200
    assert act(w,i,payload=a).json()==d
    assert count(w,IntervencaoSimulada)==1 and count(w,AcaoIntervencao)==3


@pytest.mark.parametrize('terminal',['encerrar','cancelar'])
def test_terminal_session_blocks_new_actions_but_allows_administrative_stop(simulation,terminal):
    w=simulation; i=started(w)
    pending=requested(w)['id']
    assert finish(w,w['session']['id'],action=terminal,fim=stamp(130)).status_code==200
    assert request(w).status_code==409
    assert act(w,pending,'AUTORIZAR').status_code==409
    v=view(w,i); assert v['virtual_ligado'] and v['sessao_terminal_com_execucao']
    assert act(w,i,'ENCERRAR').status_code==200
    assert view(w,i)['estado']=='CONCLUIDA'
    assert act(w,pending,'RECUSAR').status_code==200


def test_closed_session_after_authorization_prevents_start(simulation):
    w=simulation; i=requested(w)['id']; act(w,i)
    assert finish(w,w['session']['id'],fim=stamp(130)).status_code==200
    assert act(w,i,'INICIAR').status_code==409
    assert act(w,i,'CANCELAR').status_code==200
    assert not view(w,i)['virtual_ligado']


@pytest.mark.parametrize('alert_action',['RESOLVER','DESCARTAR'])
def test_terminal_alert_blocks_request_authorization_and_start(simulation,alert_action):
    w=simulation; alerta,e=with_alert(w)
    pending=requested(w,alerta_id=alerta)['id']; approved=requested(w,alerta_id=alerta)['id']; act(w,approved)
    assert decide_alert(w,alerta,alert_action).status_code==200
    assert request(w,alerta_id=alerta).status_code==409
    assert act(w,pending).status_code==409 and act(w,approved,'INICIAR').status_code==409
    assert act(w,pending,'RECUSAR').status_code==200
    assert act(w,approved,'CANCELAR').status_code==200


def test_recognized_alert_is_context_not_automatic_authorization(simulation):
    w=simulation; alerta,e=with_alert(w); assert decide_alert(w,alerta).status_code==200
    i=requested(w,alerta_id=alerta,avaliacao_id=e['id'])
    assert i['estado']=='SOLICITADA' and i['referencias_snapshot']['alerta']['estado']=='EM_ANALISE'
    assert not i['virtual_ligado'] and act(w,i['id'],'INICIAR').status_code==409


def test_logical_conflict_and_partial_unique_index(simulation):
    w=simulation; first=started(w); second=requested(w)['id']; assert act(w,second).status_code==200
    assert act(w,second,'INICIAR').status_code==409
    assert 'INICIAR' not in view(w,second,role='GESTOR')['acoes_permitidas']
    original=w['db'].get(IntervencaoSimulada,UUID(first))
    values={c.name:getattr(original,c.name) for c in original.__table__.columns if c.name not in ('id','created_at','updated_at','chave_idempotencia')}
    w['db'].add(IntervencaoSimulada(**values,chave_idempotencia=uuid4()))
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback()
    assert act(w,first,'ENCERRAR').status_code==200
    assert act(w,second,'INICIAR').status_code==200
    assert view(w,second)['virtual_ligado']


def test_precision_and_deadline_are_not_a_scientific_effect(simulation):
    w=simulation; i=started(w,duracao_planejada_s='1.234'); v=view(w,i)
    assert datetime.fromisoformat(v['prazo_planejado_em'])-datetime.fromisoformat(v['iniciada_em'])==timedelta(microseconds=1234000)
    w['clock']+=timedelta(microseconds=1234567)
    assert act(w,i,'ENCERRAR').status_code==200
    v=view(w,i); assert v['duracao_registrada_s']=='1.234567'
    assert 'concentracao' not in v and 'percentual_remocao' not in v
    assert v['resultado_operacional']=='ESTADO_VIRTUAL_CONCLUIDA'


def test_clock_regression_rejects_transition_without_partial_state(simulation):
    w=simulation; i=requested(w)['id']; w['clock']-=timedelta(seconds=1)
    assert act(w,i).status_code==409
    assert view(w,i)['estado']=='SOLICITADA' and count(w,AcaoIntervencao)==1


def test_inactive_company_allows_cleanup_but_not_start(simulation):
    w=simulation; i=started(w); p=requested(w)['id']; act(w,p)
    w['transport'].ativo=False; w['db'].commit()
    assert request(w).status_code==403
    assert act(w,p,'INICIAR').status_code==403
    assert act(w,p,'INICIAR',role='ADMIN').status_code==409
    assert act(w,i,'ENCERRAR',role='ADMIN').status_code==200
    assert act(w,p,'CANCELAR',role='ADMIN').status_code==200


def test_vehicle_change_does_not_move_execution_or_allow_new_start(simulation):
    w=simulation; i=started(w); pending=requested(w)['id']; act(w,pending)
    other=Veiculo(empresa_id=w['transport'].id,identificador='OUTRO-VEICULO',ativo=True)
    w['db'].add(other); w['db'].flush(); w['trip'].veiculo_id=other.id; w['db'].commit()
    assert view(w,i)['contexto_logistico_alterado']
    assert act(w,pending,'INICIAR').status_code==409
    assert act(w,i,'ENCERRAR').status_code==200
    assert view(w,i)['veiculo_id']!=str(other.id)


def test_reader_pagination_and_ownership_rules(simulation):
    w=simulation; a=requested(w)['id']; w['clock']+=timedelta(seconds=1); b=requested(w)['id']
    page=w['client'].get(root(w),headers=headers(w,'CONSULTA'),params={'limit':1}).json()
    assert page['total']==2 and page['intervencoes'][0]['id']==b
    assert w['client'].get(root(w),headers=headers(w),params={'offset':1,'limit':1}).json()['intervencoes'][0]['id']==a
    assert request(w,role='CONSULTA').status_code==403
    assert act(w,a,role='CONSULTA').status_code==403
    assert view(w,a,role='CONSULTA')['acoes_permitidas']==[]
    actor=w['users']['OUTRO']; actor.perfil_id=w['users']['OPERADOR'].perfil_id; w['db'].commit()
    assert act(w,a,'CANCELAR',role='OUTRO').status_code==403
    act(w,a); act(w,a,'INICIAR')
    assert act(w,a,'ENCERRAR',role='OUTRO').status_code==403
    assert act(w,a,'CANCELAR',role='OPERADOR').status_code==403
    assert act(w,a,'ENCERRAR',role='OPERADOR').status_code==200
    assert history(w,a,limit=1,offset=1).json()['acoes'][0]['acao']=='AUTORIZAR'


@pytest.mark.parametrize('operation',['request','list','get','action','history'])
def test_all_routes_require_authentication(simulation,operation):
    w=simulation; url=root(w)+'/'+str(uuid4())
    if operation=='request': r=w['client'].post(root(w),json=request_body())
    elif operation=='list': r=w['client'].get(root(w))
    elif operation=='get': r=w['client'].get(url)
    elif operation=='history': r=w['client'].get(url+'/acoes')
    else: r=w['client'].post(url+'/acoes',json={'chave_idempotencia':str(uuid4()),'acao':'AUTORIZAR','justificativa':'Demo'})
    assert r.status_code==401


def test_transport_scope_applies_to_reads_writes_and_cleanup(simulation):
    w=simulation; i=started(w)
    w['trip'].transportadora_id=w['outsider'].id; w['db'].commit()
    assert request(w).status_code==403 and act(w,i,'ENCERRAR').status_code==403
    assert w['client'].get(root(w),headers=headers(w)).status_code==403
    assert w['client'].get(root(w)+'/'+i,headers=headers(w)).status_code==403
    assert history(w,i).status_code==403
    assert act(w,i,'ENCERRAR',role='ADMIN').status_code==200


def test_transaction_failure_request_and_action_rollback(simulation,monkeypatch):
    from app.modules.monitoramento.service import MonitoramentoService
    w=simulation; before=count(w,EventoMonitoramento)
    def fail(*args,**kwargs): raise OperationalError('REDACTED',{},Exception('SECRET'))
    original=MonitoramentoService.evento; monkeypatch.setattr(MonitoramentoService,'evento',fail)
    r=request(w); assert r.status_code==503 and 'SECRET' not in r.text
    assert count(w,IntervencaoSimulada)==count(w,AcaoIntervencao)==count(w,Ocorrencia)==0
    assert count(w,EventoMonitoramento)==before
    monkeypatch.setattr(MonitoramentoService,'evento',original); i=requested(w)['id']
    monkeypatch.setattr(MonitoramentoService,'evento',fail)
    assert act(w,i).status_code==503
    assert view(w,i)['estado']=='SOLICITADA' and view(w,i)['decidida_por_id'] is None
    assert count(w,AcaoIntervencao)==count(w,Ocorrencia)==1


def test_commit_failure_rolls_back_request(simulation,monkeypatch):
    def fail(*args,**kwargs): raise OperationalError('SQL',{},Exception('SECRET'))
    monkeypatch.setattr(simulation['db'],'commit',fail)
    assert request(simulation).status_code==503
    assert count(simulation,IntervencaoSimulada)==count(simulation,AcaoIntervencao)==0


def test_scientific_records_and_alerts_are_unchanged_and_no_io(simulation,monkeypatch):
    import httpx
    w=simulation; alerta,e=with_alert(w)
    scientific=estimate(w); assert scientific.status_code==200,scientific.text
    scientific=scientific.json()
    before_analise=w['db'].get(AnaliseEtileno,UUID(scientific['id'])).resultado
    before_eval=w['db'].get(AvaliacaoPreventiva,UUID(e['id'])).resultado
    requests_before=len(w['requests']); decisions_before=count(w,DecisaoAlerta)
    def forbidden(*a,**k): raise AssertionError('No network or scientific calculation during virtual intervention')
    monkeypatch.setattr(httpx.AsyncClient,'request',forbidden)
    import app.modules.monitoramento.analises_service as estimator
    monkeypatch.setattr(estimator,'estimar_etileno',forbidden)
    i=started(w,alerta_id=alerta,avaliacao_id=e['id'],analise_etileno_id=scientific['id'])
    assert act(w,i,'ENCERRAR').status_code==200
    assert w['db'].get(AnaliseEtileno,UUID(scientific['id'])).resultado==before_analise
    assert w['db'].get(AvaliacaoPreventiva,UUID(e['id'])).resultado==before_eval
    assert w['db'].get(Alerta,UUID(alerta)).status.value=='ABERTO'
    assert count(w,DecisaoAlerta)==decisions_before and len(w['requests'])==requests_before


def test_openapi_is_virtual_authenticated_and_minimal(simulation):
    w=simulation; schema=w['application'].openapi(); p='/api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas'
    for suffix,methods in [('',('post','get')),('/{intervencao_id}',('get',)),('/{intervencao_id}/acoes',('post','get'))]:
        for method in methods: assert schema['paths'][p+suffix][method]['security']==[{'HTTPBearer':[]}]
    fields=schema['components']['schemas']['IntervencaoCreate']['properties']
    assert 'dispositivo_id' not in fields and 'comando' not in fields and 'estado' not in fields
    assert '86400' in str(fields['duracao_planejada_s'])


def other_session(w):
    from app.models.logistica import Carga
    from app.models.iot import Sensor
    from app.models.enums import TipoSensor,ContextoMedicao,StatusSensor
    from tests.test_monitoramento_sessoes import config
    c=Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['producer'].id,
        identificacao='SEGUNDA-CARGA',status=StatusCarga.EM_TRANSITO)
    sensor=Sensor(dispositivo_id=w['device'].id,identificador='TEMP-SEGUNDO',tipo=TipoSensor.TEMPERATURA,
        contexto=ContextoMedicao.AMBIENTE,unidade='C',status=StatusSensor.ATIVO)
    w['db'].add_all([c,sensor]); w['db'].commit()
    assert config(w,cargo_id=c.id).status_code==200
    response=start(w,start_body(w,sensor_temperatura_id=str(sensor.id),sensor_umidade_id=None),cargo_id=c.id)
    assert response.status_code==201,response.text
    return w|{'session':response.json()}


def test_one_vehicle_excludes_simultaneous_runs_from_different_sessions(simulation):
    w=simulation; first=started(w); other=other_session(w); second=requested(other)['id']
    assert act(other,second).status_code==200
    assert act(other,second,'INICIAR').status_code==409
    v=view(other,second,role='GESTOR')
    assert v['atuador_virtual_ocupado'] and not v['virtual_ligado']
    assert act(w,first,'ENCERRAR').status_code==200
    assert act(other,second,'INICIAR').status_code==200
    assert view(w,first)['atuador_virtual_ocupado']


def test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied(simulation):
    w=simulation; alerta,e=with_alert(w); scientific=estimate(w).json()
    i=requested(w,alerta_id=alerta)['id']; other=other_session(w)
    assert request(other,alerta_id=alerta).status_code==404
    assert request(other,avaliacao_id=e['id']).status_code==404
    assert request(other,analise_etileno_id=scientific['id']).status_code==404
    assert other['client'].get(root(other)+'/'+i,headers=headers(other)).status_code==404
    assert act(other,i).status_code==404 and history(other,i).status_code==404
    acao=w['db'].scalar(select(AcaoIntervencao)); acao.sessao_id=UUID(other['session']['id'])
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback()
    assert history(w,i).json()['total']==1


def test_evaluation_must_sustain_selected_alert(simulation):
    w=simulation; alerta,e=with_alert(w)
    other_evaluation=evaluation(w,inicio=stamp(70))
    assert other_evaluation['alertas_ids']==[]
    assert request(w,alerta_id=alerta,avaliacao_id=other_evaluation['id']).status_code==409
    scientific=estimate(w,fim=stamp(70)).json()
    assert request(w,avaliacao_id=e['id'],analise_etileno_id=scientific['id']).status_code==409


def test_inconsistent_references_do_not_prevent_administrative_stop(simulation):
    from app.models.preventivo import EvidenciaPreventiva
    w=simulation; alerta,e=with_alert(w); i=started(w,alerta_id=alerta,avaliacao_id=e['id'])
    # Deliberate isolated corruption, not an application operation: remove an evidence link.
    row=w['db'].scalar(select(EvidenciaPreventiva)); w['db'].delete(row); w['db'].commit()
    assert act(w,i,'ENCERRAR').status_code==200
    assert view(w,i)['estado']=='CONCLUIDA'
    last=history(w,i).json()['acoes'][-1]
    assert last['contexto_snapshot']['referencias_inconsistentes'] is True


def test_no_automatic_actions_or_data_changes_when_time_passes(simulation):
    from app.models.historico_iot import RegistroSessaoIoT
    w=simulation; alerta,e=with_alert(w); i=started(w,alerta_id=alerta)
    before=[(r.id,r.valor,r.medida_em) for r in w['db'].scalars(select(RegistroSessaoIoT))]
    n=count(w,AcaoIntervencao)
    w['clock']+=timedelta(days=2)
    for _ in range(2):
        v=view(w,i); assert v['estado']=='EM_EXECUCAO' and v['prazo_excedido']
    assert count(w,AcaoIntervencao)==n
    assert [(r.id,r.valor,r.medida_em) for r in w['db'].scalars(select(RegistroSessaoIoT))]==before
    assert act(w,i,'ENCERRAR').status_code==200
    assert Decimal(view(w,i)['duracao_registrada_s'])==172800


def test_approval_by_admin_and_self_approval_policy_is_explicit(simulation):
    w=simulation; response=request(w,role='GESTOR'); assert response.status_code==200
    i=response.json()['id']
    assert act(w,i,'AUTORIZAR',role='GESTOR').status_code==200
    assert act(w,i,'INICIAR',role='ADMIN').status_code==200
    assert act(w,i,'ENCERRAR',role='ADMIN').status_code==200


@pytest.mark.parametrize('field,value',[
    ('modalidade','FISICA'),('estado','LIGADO'),('duracao_planejada_s',Decimal(0)),
    ('iniciada_em',datetime.now(timezone.utc)),
])
def test_database_checks_reject_inconsistent_intervention(simulation,field,value):
    w=simulation; i=requested(w)['id']; row=w['db'].get(IntervencaoSimulada,UUID(i)); setattr(row,field,value)
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback(); assert view(w,i)['estado']=='SOLICITADA'


def test_start_failure_rolls_back_all_execution_fields(simulation,monkeypatch):
    from app.modules.monitoramento.service import MonitoramentoService
    w=simulation; i=requested(w)['id']; act(w,i)
    before=count(w,Ocorrencia)
    def fail(*a,**k): raise OperationalError('SQL',{},Exception('DEMO_FAILURE'))
    monkeypatch.setattr(MonitoramentoService,'evento',fail)
    assert act(w,i,'INICIAR').status_code==503
    v=view(w,i)
    assert v['estado']=='AUTORIZADA' and v['iniciada_em'] is None and v['prazo_planejado_em'] is None
    assert not v['atuador_virtual_ocupado'] and count(w,Ocorrencia)==before


def test_request_replay_after_session_close_keeps_same_history(simulation):
    w=simulation; p=request_body(); i=request(w,p).json()['id']
    assert finish(w,w['session']['id'],fim=stamp(130)).status_code==200
    assert request(w,p).json()['id']==i
    assert count(w,IntervencaoSimulada)==1 and history(w,i).json()['total']==1


def test_exemplo_executavel_solicitar_autorizar_iniciar_encerrar(simulation):
    w=simulation
    i=requested(w,justificativa='Operador solicita demonstracao virtual supervisionada.')['id']
    assert act(w,i,'AUTORIZAR',justificativa='Gestor avaliou e autorizou somente a simulacao.').status_code==200
    assert act(w,i,'INICIAR',justificativa='Gestor inicia execucao virtual autorizada.').status_code==200
    assert view(w,i)['virtual_ligado']
    w['clock']+=timedelta(seconds=60)
    assert act(w,i,'ENCERRAR',role='OPERADOR',justificativa='Solicitante encerra demonstracao, sem afirmar eficacia.').status_code==200
    v=view(w,i); h=history(w,i).json()['acoes']
    assert [a['acao'] for a in h]==['SOLICITAR','AUTORIZAR','INICIAR','ENCERRAR']
    assert v['estado']=='CONCLUIDA' and not v['virtual_ligado'] and v['duracao_registrada_s']=='60.000000'
    assert count(w,IntervencaoSimulada)==1 and count(w,AcaoIntervencao)==count(w,Ocorrencia)==4
    print(json.dumps(dict(ambiente='SQLite descartavel; relogio controlado; sem dispositivo fisico',
        intervencao_id=i,modalidade=v['modalidade'],estado=v['estado'],virtual_ligado=v['virtual_ligado'],
        duracao_planejada_s=v['duracao_planejada_s'],duracao_registrada_s=v['duracao_registrada_s'],
        risco_etileno=v['classificacao_risco_etileno'],historico=[dict(numero=a['numero'],acao=a['acao'],
        usuario_id=a['usuario_id'],registrada_em=a['registrada_em']) for a in h]),ensure_ascii=False,indent=2))


def test_decisions_pin_evidence_set_as_it_existed_at_each_action(simulation):
    w=simulation; alerta,e=with_alert(w); i=requested(w,alerta_id=alerta)['id']
    original=view(w,i)['referencias_snapshot']
    assert len(original['alerta']['evidencias'])==1
    evaluation(w)
    current=view(w,i)
    assert current['referencias_snapshot']==original
    assert len(current['referencias_atuais']['alerta']['evidencias'])==2
    assert current['hash_referencias_atuais']==hash_documento(current['referencias_atuais'])
    response=act(w,i); assert response.status_code==200,response.text
    h=history(w,i).json()['acoes']
    assert len(h[0]['contexto_snapshot']['alerta']['evidencias'])==1
    assert len(h[1]['contexto_snapshot']['alerta']['evidencias'])==2
    assert all('hash_evidencia' in x for x in h[1]['contexto_snapshot']['alerta']['evidencias'])
