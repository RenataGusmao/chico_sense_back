"""Operational alert acceptance through real JWT, SQLite and mocked IoT acquisition."""
from datetime import datetime,timezone,timedelta
from decimal import Decimal
from uuid import uuid4,UUID
import pytest
from sqlalchemy import select,func
from sqlalchemy.exc import OperationalError,IntegrityError
from app.models.monitoramento import Alerta,Ocorrencia
from app.models.preventivo import ConfiguracaoAmbiental,AvaliacaoPreventiva,AlertaSessao,EvidenciaPreventiva,DecisaoAlerta
from app.models.sessoes_monitoramento import SessaoMonitoramento,EventoMonitoramento
from app.models.analises_etileno import AnaliseEtileno
from app.modules.monitoramento.preventivo_motor import avaliar_ambiente
from app.modules.monitoramento.analises_adapter import hash_documento
from tests.test_monitoramento_sessoes import world,headers,stamp,finish,count,BASE,start,start_body
from tests.test_historico_iot import iot,sync,feed
from tests.test_analises_etileno import analyses,acquired,execute as estimar


@pytest.fixture
def preventive(analyses):
    w=analyses
    for m in (Alerta,Ocorrencia,ConfiguracaoAmbiental,AvaliacaoPreventiva,AlertaSessao,EvidenciaPreventiva,DecisaoAlerta):
        m.__table__.create(w['db'].get_bind())
    w['payload']['feeds']=[feed(1,10,'13','92'),feed(2,70,'13','92'),feed(3,130,'13','92')]
    return w


def root(w): return '/api/v1/monitoramentos/'+w['session']['id']


def config_body(**changes):
    return dict(chave_idempotencia=str(uuid4()),temperatura_min_c='12',temperatura_max_c='14',
        umidade_min_percentual='90',umidade_max_percentual='95',intervalo_maximo_s='3600',
        cobertura_min_percentual='100',exposicao_continua_s='3600',maturacoes_aplicaveis=['MISTA'],
        ambiente='TRANSPORTE_REFRIGERADO',fundamento='EXPERIMENTAL',
        justificativa='Fixture hipotetica; limites operacionais sem validacao fisiologica.',prioridade='ATENCAO')|changes


def configure(w,payload=None,role='GESTOR',**changes):
    return w['client'].post(root(w)+'/configuracoes-ambientais',headers=headers(w,role),json=(payload or config_body())|changes)


def setup(w,closed=True,**changes):
    response=configure(w,**changes); assert response.status_code==200,response.text
    acquired(w,closed); return response.json()


def eval_body(**changes):
    return dict(chave_idempotencia=str(uuid4()),fim=stamp(130),corte_aquisicao=datetime.now(timezone.utc).isoformat())|changes


def evaluate(w,payload=None,role='OPERADOR',**changes):
    return w['client'].post(root(w)+'/avaliacoes-preventivas',headers=headers(w,role),json=(payload or eval_body())|changes)


def evaluation(w,**changes):
    r=evaluate(w,**changes); assert r.status_code==200,r.text; return r.json()


def get(w,suffix,role='OPERADOR',**params):
    return w['client'].get(root(w)+suffix,headers=headers(w,role),params=params)


def decide(w,alerta,acao='RECONHECER',payload=None,role='OPERADOR',**changes):
    data=payload or dict(chave_idempotencia=str(uuid4()),acao=acao,justificativa='Operador verificou a evidencia ambiental.')
    return w['client'].post(root(w)+f'/alertas/{alerta}/decisoes',headers=headers(w,role),json=data|changes)


def rules(e): return {r['regra']:r for r in e['resultado']['achados']}


def test_in_range_has_no_alert_and_reproduces_without_io(preventive):
    w=preventive; setup(w); e=evaluation(w)
    assert e['resultado']['status']=='AVALIADO' and e['alertas_ids']==[]
    assert rules(e)=={} and count(w,Alerta)==0 and count(w,Ocorrencia)==0
    assert avaliar_ambiente(e['entrada_snapshot'])==e['resultado']
    assert hash_documento(e['entrada_snapshot'])==e['hash_entrada']
    assert hash_documento(e['resultado'])==e['hash_resultado']


@pytest.mark.parametrize('temp,hum,expected',[
    ('15','92','TEMPERATURA_FORA_DA_FAIXA'),('11','92','TEMPERATURA_FORA_DA_FAIXA'),
    ('13','89','UMIDADE_FORA_DA_FAIXA'),('13','96','UMIDADE_FORA_DA_FAIXA'),
    ('25','92','TEMPERATURA_FORA_DA_FAIXA'),
])
def test_observed_outside_range_has_explainable_evidence(preventive,temp,hum,expected):
    w=preventive
    for row in w['payload']['feeds']: row.update(field4=temp,field7=hum)
    setup(w); e=evaluation(w); r=rules(e)
    assert expected in r and 'EXPOSICAO_AMBIENTAL_PROLONGADA' in r
    assert len(e['alertas_ids'])==2
    assert r[expected]['evidencia']['pontos'][0]['valor']==str(Decimal(temp if 'TEMPERATURA' in expected else hum).quantize(Decimal('.0001')))
    assert r['EXPOSICAO_AMBIENTAL_PROLONGADA']['evidencia']['sequencias'][0]['duracao_s']=='7200'
    assert all(get(w,'/alertas/'+a).json()['nivel']=='ATENCAO' for a in e['alertas_ids'])


@pytest.mark.parametrize('temp,hum',[('12','90'),('14','95')])
def test_range_boundaries_are_inclusive(preventive,temp,hum):
    w=preventive
    for row in w['payload']['feeds']: row.update(field4=temp,field7=hum)
    setup(w); assert rules(evaluation(w))=={}


def test_isolated_outlier_does_not_prove_prolonged_exposure(preventive):
    w=preventive; w['payload']['feeds'][0]['field4']='20'; setup(w)
    r=rules(evaluation(w)); assert 'TEMPERATURA_FORA_DA_FAIXA' in r
    assert 'EXPOSICAO_AMBIENTAL_PROLONGADA' not in r


def test_gaps_are_not_bridged_and_coverage_is_inconclusive(preventive):
    w=preventive
    for row in w['payload']['feeds']: row['field4']='20'
    setup(w,intervalo_maximo_s='600'); e=evaluation(w); r=rules(e)
    assert 'EXPOSICAO_AMBIENTAL_PROLONGADA' not in r
    assert {'COBERTURA_INSUFICIENTE','FALHA_MONITORAMENTO'}<=r.keys()
    assert e['resultado']['status']=='INCONCLUSIVO'
    assert all(Decimal(c['percentual_cobertura'])==0 for c in e['resultado']['canais'])


def test_no_readings_never_means_safe(preventive):
    w=preventive; assert configure(w).status_code==200
    e=evaluation(w); assert 'COBERTURA_INSUFICIENTE' in rules(e)
    assert e['revisao']==0 and e['resultado']['status']=='INCONCLUSIVO'


@pytest.mark.parametrize('maturity',['MISTA','DESCONHECIDA'])
def test_maturity_requires_explicit_applicability(preventive,maturity):
    w=preventive; s=w['db'].get(SessaoMonitoramento,UUID(w['session']['id'])); s.maturacao=maturity; w['db'].commit()
    assert configure(w,maturacoes_aplicaveis=['VERDE_MADURA']).status_code==409
    setup(w,maturacoes_aplicaveis=[maturity]); e=evaluation(w)
    assert e['resultado']['status']=='AVALIADO'
    assert any('mista/desconhecida' in x for x in e['resultado']['limitacoes'])


def test_missing_configuration_is_informational_not_scientific_guess(preventive):
    w=preventive; acquired(w); e=evaluation(w)
    assert e['configuracao_id'] is None
    assert e['resultado']['status']=='CONFIGURACAO_INSUFICIENTE'
    assert set(rules(e))=={'CONFIGURACAO_AMBIENTAL_AUSENTE'}
    assert get(w,'/alertas/'+e['alertas_ids'][0]).json()['nivel']=='INFORMATIVO'


@pytest.mark.parametrize('changes',[
    {'temperatura_min_c':'14','temperatura_max_c':'12'}, {'temperatura_min_c':'14'},
    {'umidade_max_percentual':'101'}, {'umidade_min_percentual':'-1'}, {'intervalo_maximo_s':'0'},
    {'intervalo_maximo_s':'NaN'}, {'exposicao_continua_s':'-1'}, {'cobertura_min_percentual':'0'},
    {'cobertura_min_percentual':'101'}, {'maturacoes_aplicaveis':[]}, {'maturacoes_aplicaveis':['MISTA','MISTA']},
    {'prioridade':'CRITICO'}, {'fundamento':'CIENTIFICO_VALIDADO'}, {'justificativa':' '},
])
def test_invalid_configuration_rejected(preventive,changes):
    assert configure(preventive,**changes).status_code==422
    assert count(preventive,ConfiguracaoAmbiental)==0


def test_config_versions_immutable_and_old_evaluation_frozen(preventive):
    w=preventive; c1=setup(w,closed=False); a=evaluation(w)
    c2=configure(w,temperatura_max_c='12.5').json(); b=evaluation(w)
    assert c2['versao']==2 and c1['id']!=c2['id']
    assert 'TEMPERATURA_FORA_DA_FAIXA' in rules(b)
    assert get(w,'/avaliacoes-preventivas/'+a['id']).json()==a
    assert b['anterior_id']==a['id'] and b['configuracao_id']==c2['id']
    assert get(w,'/configuracoes-ambientais',limit=1).json()['configuracoes'][0]['id']==c2['id']


def test_config_idempotency_and_role(preventive):
    w=preventive; p=config_body(); a=configure(w,p).json()
    assert configure(w,p).json()['id']==a['id']
    assert configure(w,p,temperatura_max_c='15').status_code==409
    assert configure(w,p,role='ADMIN').status_code==409
    assert configure(w,role='OPERADOR').status_code==403


def test_evaluation_idempotency_and_alert_dedup_across_duplicate_revision(preventive):
    w=preventive
    for row in w['payload']['feeds']: row['field4']='20'
    setup(w,False); p=eval_body(); a=evaluate(w,p).json(); n=count(w,Alerta)
    assert evaluate(w,p).json()==a
    assert evaluate(w,p,role='GESTOR').status_code==409
    assert evaluate(w,p,fim=stamp(70)).status_code==409
    b=evaluation(w); assert b['id']!=a['id'] and b['alertas_ids']==a['alertas_ids']
    assert count(w,Alerta)==n and count(w,EvidenciaPreventiva)==2*n
    assert sync(w).status_code==200
    c=evaluation(w); assert c['revisao']==2 and c['alertas_ids']==a['alertas_ids']
    assert count(w,Alerta)==n


def test_revision_conflict_creates_new_evidence_preserves_previous(preventive):
    w=preventive; setup(w,False); a=evaluation(w)
    w['payload']['feeds'][1]['field4']='20'; sync(w)
    b=evaluation(w)
    assert {'FALHA_MONITORAMENTO','COBERTURA_INSUFICIENTE'}<=rules(b).keys()
    assert b['anterior_id']==a['id'] and b['revisao']==2
    assert get(w,'/avaliacoes-preventivas/'+a['id']).json()==a
    assert avaliar_ambiente(a['entrada_snapshot'])==a['resultado']


def test_return_to_range_never_auto_resolves_alerts(preventive):
    w=preventive; w['payload']['feeds']=[feed(1,10,'20'),feed(2,70,'20')]
    setup(w,False); a=evaluation(w,fim=stamp(70)); ids=a['alertas_ids']
    w['payload']['feeds']=[feed(3,71,'13'),feed(4,130,'13')]; sync(w)
    b=evaluation(w,inicio=stamp(71)); assert rules(b)=={}
    assert all(get(w,'/alertas/'+i).json()['status']=='ABERTO' for i in ids)


def test_unknown_timestamp_disables_duration_and_coverage_claims(preventive):
    w=preventive
    for row in w['payload']['feeds']: row['field4']='20'
    w['payload']['feeds'].append(feed(4,80,created_at='invalid')); setup(w)
    e=evaluation(w); r=rules(e)
    assert 'EXPOSICAO_AMBIENTAL_PROLONGADA' not in r
    assert all(c['percentual_cobertura'] is None for c in e['resultado']['canais'])
    assert {'COBERTURA_INSUFICIENTE','FALHA_MONITORAMENTO'}<=r.keys()


def test_decision_lifecycle_reuses_existing_alert_occurrence_models(preventive):
    w=preventive; w['payload']['feeds'][0]['field4']='20'; setup(w); e=evaluation(w); alerta=e['alertas_ids'][0]
    assert count(w,Alerta)==1 and count(w,Ocorrencia)==1
    p=dict(chave_idempotencia=str(uuid4()),acao='RECONHECER',justificativa='Operador iniciou verificacao presencial.')
    r=decide(w,alerta,payload=p); assert r.status_code==200,r.text
    d=r.json(); assert d['estado_anterior']=='ABERTO' and d['estado_posterior']=='EM_ANALISE'
    assert d['usuario_id']==str(w['users']['OPERADOR'].id)
    assert decide(w,alerta,payload=p).json()==d
    assert decide(w,alerta).status_code==409
    assert decide(w,alerta,'OBSERVAR').status_code==200
    assert decide(w,alerta,'RESOLVER').status_code==200
    assert get(w,'/alertas/'+alerta).json()['status']=='RESOLVIDO'
    for acao in ('RESOLVER','DESCARTAR','RECONHECER'): assert decide(w,alerta,acao).status_code==409
    h=get(w,'/alertas/'+alerta+'/decisoes').json()
    assert [x['acao'] for x in h['decisoes']]==['CRIAR','RECONHECER','OBSERVAR','RESOLVER']
    assert count(w,Ocorrencia)==4 and count(w,DecisaoAlerta)==4
    assert h['decisoes'][1]['justificativa']==p['justificativa']
    assert get(w,'/alertas/'+alerta+'/decisoes',limit=1,offset=1).json()['decisoes'][0]==d


def test_discard_requires_justification_and_terminal_evidence_stays(preventive):
    w=preventive; w['payload']['feeds'][0]['field4']='20'; setup(w); a=evaluation(w)['alertas_ids'][0]
    assert decide(w,a,'DESCARTAR',justificativa=' ').status_code==422
    assert decide(w,a,'DESCARTAR',justificativa='Leitura requer verificacao de calibracao.').status_code==200
    assert get(w,'/alertas/'+a).json()['status']=='DESCARTADO'
    assert decide(w,a,'OBSERVAR').status_code==200
    e=evaluation(w); assert a in e['alertas_ids']
    assert get(w,'/alertas/'+a).json()['status']=='DESCARTADO'
    assert get(w,'/alertas/'+a+'/evidencias').json()['total']==2


def test_cancelled_keeps_decisions_and_rejects_new_eval_config(preventive):
    w=preventive; w['payload']['feeds'][0]['field4']='20'; setup(w,False)
    p=eval_body(); a=evaluate(w,p).json()
    assert finish(w,w['session']['id'],action='cancelar',fim=stamp(130)).status_code==200
    assert evaluate(w).status_code==409 and configure(w).status_code==409
    assert evaluate(w,p).json()==a
    assert decide(w,a['alertas_ids'][0]).status_code==200
    assert get(w,'/avaliacoes-preventivas/'+a['id']).json()==a


def test_environment_never_invokes_ethylene_calculation(preventive,monkeypatch):
    import app.modules.monitoramento.analises_service as module
    def forbidden(*args): raise AssertionError('No ethylene computation in environmental rules')
    monkeypatch.setattr(module,'estimar_etileno',forbidden)
    w=preventive; setup(w); e=evaluation(w)
    assert e['resultado']['classificacao_risco_etileno']=='NAO_AVALIADO'
    assert e['entrada_snapshot']['estimativa_etileno_contextual'] is None
    assert count(w,AnaliseEtileno)==0


def test_persisted_ethylen_analysis_context_preserved(preventive):
    w=preventive; setup(w); response=estimar(w); assert response.status_code==200,response.text
    a=response.json(); e=evaluation(w,analise_etileno_id=a['id'])
    assert e['entrada_snapshot']['estimativa_etileno_contextual']['resultado']==a['resultado']
    assert e['resultado']['classificacao_risco_etileno']=='NAO_AVALIADO'
    assert e['alertas_ids']==[]
    assert evaluation(w)['resultado']==e['resultado']
    assert evaluate(w,analise_etileno_id=a['id'],fim=stamp(70)).status_code==409


@pytest.mark.parametrize('path_suffix',['/configuracoes-ambientais','/avaliacoes-preventivas','/alertas'])
def test_read_auth_required(preventive,path_suffix):
    assert preventive['client'].get(root(preventive)+path_suffix).status_code==401


@pytest.mark.parametrize('role',['CONSULTA','OUTRO'])
def test_writes_require_operational_role(preventive,role):
    w=preventive; setup(w)
    assert evaluate(w,role=role).status_code==403
    assert configure(w,role=role).status_code==403


def test_reader_scope_and_pagination(preventive):
    w=preventive; w['payload']['feeds'][0]['field4']='20'; setup(w); a=evaluation(w); b=evaluation(w)
    page=get(w,'/avaliacoes-preventivas',limit=1,role='CONSULTA').json()
    assert page['total']==2 and page['avaliacoes'][0]['id']==b['id']
    assert get(w,'/avaliacoes-preventivas',limit=1,offset=1).json()['avaliacoes'][0]['id']==a['id']
    alerta=a['alertas_ids'][0]
    assert decide(w,alerta,role='CONSULTA').status_code==403
    assert get(w,'/alertas/'+alerta,role='CONSULTA').status_code==200
    assert get(w,'/alertas',status='ABERTO',limit=1).json()['total']==1
    assert get(w,'/alertas',status='RESOLVIDO').json()['total']==0
    assert get(w,'/alertas',limit=0).status_code==422
    w['trip'].transportadora_id=w['outsider'].id; w['db'].commit()
    for suffix in ['/alertas','/alertas/'+alerta,'/alertas/'+alerta+'/decisoes','/alertas/'+alerta+'/evidencias',
                   '/avaliacoes-preventivas','/avaliacoes-preventivas/'+a['id'],'/configuracoes-ambientais']:
        assert get(w,suffix).status_code==403
    assert evaluate(w).status_code==403 and decide(w,alerta).status_code==403


def test_active_cutoff_revision_window_and_session_scoping(preventive):
    w=preventive; setup(w,False)
    assert evaluate(w,corte_aquisicao=None).status_code==422
    assert evaluate(w,inicio=stamp(9)).status_code==422
    assert evaluate(w,corte_aquisicao=stamp(129)).status_code==422
    assert evaluate(w,corte_aquisicao=(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()).status_code==422
    assert evaluate(w,revisao=99).status_code==404
    assert evaluate(w,configuracao_id=str(uuid4())).status_code==404
    assert get(w,'/alertas/'+str(uuid4())).status_code==404
    assert get(w,'/avaliacoes-preventivas/'+str(uuid4())).status_code==404


@pytest.mark.parametrize('point',['audit','commit'])
def test_evaluation_atomic_on_failure(preventive,monkeypatch,point):
    from app.modules.monitoramento.service import MonitoramentoService
    w=preventive; w['payload']['feeds'][0]['field4']='20'; setup(w)
    before=count(w,EventoMonitoramento)
    def fail(*a,**k): raise OperationalError('SECRET',{},Exception('PRIVATE'))
    if point=='audit': monkeypatch.setattr(MonitoramentoService,'evento',fail)
    else: monkeypatch.setattr(w['db'],'commit',fail)
    r=evaluate(w); assert r.status_code==503 and 'PRIVATE' not in r.text
    for m in (AvaliacaoPreventiva,AlertaSessao,EvidenciaPreventiva,DecisaoAlerta,Alerta,Ocorrencia): assert count(w,m)==0
    assert count(w,EventoMonitoramento)==before


def test_decision_failure_rolls_back_status_and_history(preventive,monkeypatch):
    from app.modules.monitoramento.service import MonitoramentoService
    w=preventive; w['payload']['feeds'][0]['field4']='20'; setup(w); alerta=evaluation(w)['alertas_ids'][0]
    def fail(*a,**k): raise OperationalError('SQL',{},Exception('Failure'))
    monkeypatch.setattr(MonitoramentoService,'evento',fail)
    assert decide(w,alerta).status_code==503
    assert get(w,'/alertas/'+alerta).json()['status']=='ABERTO'
    assert count(w,Ocorrencia)==count(w,DecisaoAlerta)==1


def test_openapi_and_no_gas_detection_labels(preventive):
    w=preventive; schema=w['application'].openapi(); p='/api/v1/monitoramentos/{sessao_id}'
    for suffix,methods in [('/configuracoes-ambientais',['get','post']),('/avaliacoes-preventivas',['get','post']),
        ('/avaliacoes-preventivas/{avaliacao_id}',['get']),('/alertas',['get']),('/alertas/{alerta_id}',['get']),
        ('/alertas/{alerta_id}/decisoes',['get','post']),('/alertas/{alerta_id}/evidencias',['get'])]:
        for method in methods: assert schema['paths'][p+suffix][method]['security']==[{'HTTPBearer':[]}]
    w['payload']['feeds'][0]['field4']='20'; setup(w); e=evaluation(w)
    text=str(e).lower()
    assert 'etileno detectado' not in text and 'concentracao perigosa' not in text
    assert e['resultado']['classificacao_risco_etileno']=='NAO_AVALIADO'
    assert all(get(w,'/alertas/'+a).json()['intervencao']=='AVALIACAO_HUMANA_NECESSARIA' for a in e['alertas_ids'])


def test_active_extension_attaches_evidence_to_existing_open_cases(preventive):
    w=preventive
    for row in w['payload']['feeds']: row['field4']='20'
    setup(w,False)
    p=eval_body(); p.pop('fim')
    a=evaluate(w,p).json(); b=evaluation(w,fim=None)
    assert b['alertas_ids']==a['alertas_ids'] and count(w,Alerta)==len(a['alertas_ids'])
    assert a['fim']!=b['fim'] and b['anterior_id']==a['id']
    for alerta in a['alertas_ids']: assert get(w,'/alertas/'+alerta+'/evidencias').json()['total']==2


def test_real_new_condition_after_resolution_creates_new_case(preventive):
    w=preventive; w['payload']['feeds']=[feed(1,10,'20'),feed(2,70,'13')]
    setup(w,False); a=evaluation(w,fim=stamp(70)); old=a['alertas_ids'][0]
    assert decide(w,old,'RESOLVER').status_code==200
    assert evaluation(w,fim=stamp(70))['alertas_ids']==[old]
    w['payload']['feeds']=[feed(3,130,'20')]; sync(w)
    b=evaluation(w)
    assert any(x!=old for x in b['alertas_ids'])
    assert get(w,'/alertas/'+old).json()['status']=='RESOLVIDO'


def test_closed_late_complement_adds_evidence_without_rewriting_old(preventive):
    w=preventive; w['payload']['feeds']=[feed(1,10,'13'),feed(2,70,'13')]; setup(w)
    a=evaluation(w); assert 'COBERTURA_INSUFICIENTE' in rules(a)
    w['payload']['feeds']=[feed(3,130,'13')]
    assert sync(w,role='GESTOR',complementar_encerrada=True,justificativa='Completar leitura de fechamento').status_code==200
    b=evaluation(w); assert b['resultado']['status']=='AVALIADO' and b['alertas_ids']==[]
    assert get(w,'/avaliacoes-preventivas/'+a['id']).json()==a
    assert get(w,'/alertas/'+a['alertas_ids'][0]).json()['status']=='ABERTO'


def test_historical_cut_and_running_revision_exclude_future_data(preventive):
    from app.models.historico_iot import SincronizacaoIoT
    w=preventive; assert configure(w).status_code==200
    corte=datetime.now(timezone.utc).isoformat(); acquired(w,False)
    a=evaluation(w,corte_aquisicao=corte); assert a['revisao']==0
    assert evaluate(w,corte_aquisicao=corte,revisao=1).status_code==409
    run=w['db'].scalar(select(SincronizacaoIoT)); run.estado='EM_EXECUCAO'; run.finalizada_em=None; w['db'].commit()
    assert evaluate(w,revisao=1).status_code==409
    assert evaluation(w)['revisao']==0


def test_cross_session_api_and_composite_evidence_fk(preventive):
    w=preventive; w['payload']['feeds'][0]['field4']='20'; config=setup(w); a=evaluation(w); alerta=a['alertas_ids'][0]
    response=start(w,start_body(w,inicio=stamp(140))); assert response.status_code==201,response.text
    other=response.json()['id']; otherroot='/api/v1/monitoramentos/'+other
    for suffix in ['/alertas/'+alerta,'/alertas/'+alerta+'/decisoes','/alertas/'+alerta+'/evidencias','/avaliacoes-preventivas/'+a['id']]:
        assert w['client'].get(otherroot+suffix,headers=headers(w)).status_code==404
    assert w['client'].post(otherroot+'/avaliacoes-preventivas',headers=headers(w),json=eval_body(inicio=stamp(140),fim=stamp(150),configuracao_id=config['id'])).status_code==404
    row=w['db'].scalar(select(EvidenciaPreventiva)); row.sessao_id=UUID(other)
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback()
    assert get(w,'/alertas/'+alerta+'/evidencias').json()['total']==1


@pytest.mark.parametrize('temp,humidity',[('-1000','92'),('NaN','92'),('13','NaN')])
def test_invalid_sensor_data_is_not_treated_as_normal(preventive,temp,humidity):
    w=preventive; w['payload']['feeds'][1].update(field4=temp,field7=humidity); setup(w)
    r=rules(evaluation(w))
    assert {'COBERTURA_INSUFICIENTE','FALHA_MONITORAMENTO'}<=r.keys()
    assert 'EXPOSICAO_AMBIENTAL_PROLONGADA' not in r


def test_out_of_order_and_duplicates_do_not_extend_exposure(preventive):
    w=preventive
    for row in w['payload']['feeds']: row['field4']='20'
    w['payload']['feeds'].append(feed(4,70,'20','92')); w['payload']['feeds'].reverse(); setup(w)
    a=evaluation(w); r=rules(a)
    assert r['EXPOSICAO_AMBIENTAL_PROLONGADA']['evidencia']['sequencias'][0]['duracao_s']=='7200'
    assert all(c['duracao_coberta_s']=='7200' for c in a['resultado']['canais'])


def test_tolerance_threshold_is_configured_and_not_physiological(preventive):
    w=preventive; w['payload']['feeds']=[feed(1,10),feed(2,70)]; setup(w,cobertura_min_percentual='50',prioridade='INFORMATIVO')
    e=evaluation(w)
    assert 'COBERTURA_INSUFICIENTE' not in rules(e)
    assert e['resultado']['status']=='AVALIADO'
    assert all(c['percentual_cobertura']=='50' for c in e['resultado']['canais'])
    assert any('sem criterios validados' in x for x in e['resultado']['limitacoes'])


def test_configuration_can_disable_duration_rule_explicitly(preventive):
    w=preventive
    for row in w['payload']['feeds']: row['field4']='20'
    setup(w,exposicao_continua_s=None)
    assert set(rules(evaluation(w)))=={'TEMPERATURA_FORA_DA_FAIXA'}


def test_exemplo_executavel_alerta_reconhecimento_historico(preventive):
    import json
    w=preventive; w['payload']['feeds'][0]['field4']='20'; config=setup(w)
    e=evaluation(w); alerta=e['alertas_ids'][0]
    assert get(w,'/alertas/'+alerta).json()['status']=='ABERTO'
    d=decide(w,alerta); assert d.status_code==200,d.text
    historico=get(w,'/alertas/'+alerta+'/decisoes').json()['decisoes']
    assert [x['acao'] for x in historico]==['CRIAR','RECONHECER']
    assert count(w,Alerta)==1 and count(w,Ocorrencia)==2 and count(w,DecisaoAlerta)==2
    print(json.dumps(dict(ambiente='SQLite em memoria; dados hipoteticos',sessao_id=w['session']['id'],
        configuracao_versao=config['versao'],temperatura_observada_c='20',faixa_operacional_c=['12','14'],
        regra=rules(e)['TEMPERATURA_FORA_DA_FAIXA']['regra'],alerta_id=alerta,
        estado=get(w,'/alertas/'+alerta).json()['status'],historico=[dict(acao=x['acao'],
        usuario_id=x['usuario_id'],registrada_em=x['registrada_em']) for x in historico],
        risco_etileno=e['resultado']['classificacao_risco_etileno']),ensure_ascii=False,indent=2))
