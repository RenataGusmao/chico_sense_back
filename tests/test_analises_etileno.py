"""Real engine through acquisition, database and authenticated HTTP; no external I/O."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace
from uuid import UUID,uuid4
import pytest
from sqlalchemy import select,func
from sqlalchemy.exc import OperationalError, IntegrityError
from app.models.analises_etileno import AnaliseEtileno
from app.models.sessoes_monitoramento import SessaoMonitoramento,CargaMonitoramento,EventoMonitoramento
from app.models.historico_iot import SincronizacaoIoT,RegistroSessaoIoT,OcorrenciaIoT,FonteSessaoIoT
from app.modules.monitoramento.analises_adapter import montar_entrada,restaurar_entrada,serializar,hash_documento
from app.modules.monitoramento.etileno import estimar_etileno
from tests.test_monitoramento_sessoes import world,headers,stamp,finish,count,BASE
from tests.test_historico_iot import iot,sync,feed


@pytest.fixture
def analyses(iot):
    AnaliseEtileno.__table__.create(iot['db'].get_bind())
    iot['payload']['feeds']=[feed(1,10,'13'),feed(2,70,'20'),feed(3,130,'20')]
    return iot


def path(w): return f"/api/v1/monitoramentos/{w['session']['id']}/analises-etileno"


def body(**changes):
    return dict(chave_idempotencia=str(uuid4()),intervalo_maximo_s='3600',fim=stamp(130),
                corte_aquisicao=datetime.now(timezone.utc).isoformat())|changes


def execute(w,payload=None,role='OPERADOR',**changes):
    return w['client'].post(path(w),headers=headers(w,role),json=(payload or body())|changes)


def acquired(w,closed=True):
    response=sync(w); assert response.status_code==200,response.text
    if closed: assert finish(w,w['session']['id'],fim=stamp(130)).status_code==200


def result(w,**changes):
    response=execute(w,**changes); assert response.status_code==200,response.text
    return response.json()


def test_real_engine_end_to_end_700_9000_and_persistence(analyses):
    w=analyses; acquired(w); data=result(w); r=data['resultado']
    assert data['status_calculo']==r['status_calculo']=='COMPLETO_NO_MODELO'
    assert Decimal(r['volume_janela_min_ul'])==700
    assert Decimal(r['volume_janela_max_ul'])==9000
    assert Decimal(r['percentual_cobertura'])==100
    assert Decimal(r['duracao_nao_coberta_s'])==0
    assert Decimal(r['duracao_coberta_s'])==7200
    assert data['classificacao_risco_etileno']==r['classificacao_risco_etileno']=='NAO_AVALIADO'
    assert r['unidade_volume']=='µL' and data['modo']=='MODO_RESTRITO'
    assert data['revisao_aquisicao']==1 and len(data['entrada_snapshot']['registros'])==3
    assert count(w,AnaliseEtileno)==1
    assert w['db'].scalar(select(func.count()).select_from(EventoMonitoramento).where(EventoMonitoramento.tipo=='ANALISE_ETILENO'))==1
    assert all(x['sensor_id']==str(w['temp'].id) for x in data['entrada_snapshot']['entrada']['leituras'])
    assert data['hash_entrada']==hash_documento(data['entrada_snapshot'])
    assert data['hash_resultado']==hash_documento(w['db'].get(AnaliseEtileno,UUID(data['id'])).resultado)


def test_snapshot_replays_actual_public_engine_without_live_queries(analyses):
    acquired(analyses); data=result(analyses)
    replay=serializar(estimar_etileno(restaurar_entrada(data['entrada_snapshot'])))
    replay.pop('entrada'); replay.pop('observacoes')
    assert replay==data['resultado']


def test_get_and_paginated_stable_history(analyses):
    w=analyses; acquired(w); a=result(w); b=result(w)
    fetched=w['client'].get(path(w)+'/'+a['id'],headers=headers(w)).json()
    assert fetched==a
    first=w['client'].get(path(w),headers=headers(w),params={'limit':1}).json()
    second=w['client'].get(path(w),headers=headers(w),params={'limit':1,'offset':1}).json()
    assert first['total']==2 and first['analises'][0]['id']==b['id']
    assert second['analises'][0]['id']==a['id']
    assert w['client'].get(path(w),headers=headers(w),params={'offset':2}).json()['analises']==[]


@pytest.mark.parametrize('mode,expected', [('MODO_RESTRITO','SEM_ESTIMATIVA'),('MODO_EXPLORATORIO','COMPLETO_NO_MODELO')])
def test_restricted_and_exploratory_delegate_rates_to_engine(analyses,mode,expected):
    w=analyses; w['payload']['feeds']=[feed(1,10,'12'),feed(2,70,'12')]; acquired(w)
    data=result(w,modo=mode,fim=stamp(70)); r=data['resultado']
    assert data['status_calculo']==expected
    if mode=='MODO_EXPLORATORIO':
        assert Decimal(r['volume_janela_min_ul'])==Decimal('166.666667')
        assert Decimal(r['volume_janela_max_ul'])==Decimal('833.333333')
        assert r['interpolacao_utilizada'] is True
    else: assert r['volume_coberto_min_ul'] is None


def test_gaps_are_partial_subtotal_never_window_total(analyses):
    w=analyses; w['payload']['feeds']=[feed(1,10,'13'),feed(2,40,'13'),feed(3,130,'20')]; acquired(w)
    r=result(w)['resultado']
    assert r['status_calculo']=='PARCIAL' and Decimal(r['volume_coberto_min_ul'])==100
    assert r['volume_janela_min_ul'] is None and Decimal(r['percentual_cobertura'])==25
    assert Decimal(r['duracao_nao_coberta_s'])==5400


@pytest.mark.parametrize('temperature',['25','9','None',None,'NaN'])
def test_invalid_or_out_of_domain_is_not_zero(analyses,temperature):
    w=analyses; w['payload']['feeds']=[feed(1,10,temperature),feed(2,70,temperature)]; acquired(w)
    r=result(w,fim=stamp(70))['resultado']
    assert r['status_calculo']=='SEM_ESTIMATIVA'
    assert r['volume_coberto_min_ul'] is None and r['volume_janela_max_ul'] is None
    assert Decimal(r['percentual_cobertura'])==0


def test_no_measurements_and_no_acquisition_revision(analyses):
    r=result(analyses); assert r['revisao_aquisicao']==0
    assert r['status_calculo']=='SEM_ESTIMATIVA'
    assert r['resultado']['volume_coberto_min_ul'] is None
    assert r['entrada_snapshot']['registros']==[]


def test_g_not_supplied_is_persisted_configuration_incomplete(analyses):
    acquired(analyses); data=result(analyses,intervalo_maximo_s=None)
    assert data['status_calculo']=='CONFIGURACAO_INCOMPLETA'
    assert data['resultado']['percentual_cobertura'] is None
    assert data['resultado']['volume_janela_min_ul'] is None


@pytest.mark.parametrize('gap',['0','-1','NaN','Infinity',True,'0.0001'])
def test_invalid_gap_rejected_at_api(analyses,gap):
    assert execute(analyses,intervalo_maximo_s=gap).status_code==422
    assert count(analyses,AnaliseEtileno)==0


def test_unknown_maturity_is_not_corrected_and_snapshot_mass_used(analyses):
    w=analyses; s=w['db'].get(SessaoMonitoramento,UUID(w['session']['id']))
    s.maturacao='DESCONHECIDA'; w['db'].commit(); acquired(w)
    config=w['db'].get(CargaMonitoramento,s.configuracao_id); config.massa_kg=Decimal('2000'); w['db'].commit()
    data=result(w)
    assert Decimal(data['massa_kg'])==1000 and data['maturacao']=='DESCONHECIDA'
    assert Decimal(data['resultado']['volume_janela_min_ul'])==700
    assert data['resultado']['limitacoes']


@pytest.mark.parametrize('mass',[None,Decimal('0'),Decimal('-1'),Decimal('NaN')])
def test_adapter_preserves_invalid_snapshot_mass_for_engine(mass):
    session=SimpleNamespace(id=uuid4(),sensor_temperatura_id=uuid4(),sensor_umidade_id=None,massa_kg=mass,maturacao='DESCONHECIDA')
    entrada,snapshot=montar_entrada(session,BASE,BASE+timedelta(hours=1),BASE+timedelta(hours=2),
        'MODO_RESTRITO',Decimal(3600),[],[],[])
    r=estimar_etileno(entrada)
    assert r.status_calculo.value=='ENTRADA_INVALIDA' and r.volume_janela_min_ul is None
    assert 'MASSA_INVALIDA' in [m.value for m in r.motivos]


def test_mass_constraint_rejects_corrupt_session(analyses):
    s=analyses['db'].get(SessaoMonitoramento,UUID(analyses['session']['id'])); s.massa_kg=Decimal(0)
    with pytest.raises(IntegrityError): analyses['db'].commit()
    analyses['db'].rollback()


def test_precision_tiny_mass_no_binary_float_in_snapshot(analyses):
    w=analyses; s=w['db'].get(SessaoMonitoramento,UUID(w['session']['id'])); s.massa_kg=Decimal('.0001'); w['db'].commit()
    acquired(w); data=result(w)
    assert data['resultado']['volume_janela_min_ul']=='0.000070'
    assert data['resultado']['volume_janela_max_ul']=='0.000900'
    def check(v):
        assert not isinstance(v,float)
        if isinstance(v,dict):
            for x in v.values(): check(x)
        if isinstance(v,list):
            for x in v: check(x)
    check(data['entrada_snapshot']); check(data['resultado'])


def test_active_requires_explicit_cutoff_and_freezes_window(analyses):
    w=analyses; acquired(w,False)
    assert execute(w,corte_aquisicao=None).status_code==422
    cutoff=datetime.now(timezone.utc).isoformat(); data=result(w,corte_aquisicao=cutoff)
    assert datetime.fromisoformat(data['corte_aquisicao'])==datetime.fromisoformat(cutoff)
    assert data['entrada_snapshot']['sessao']['estado']=='ATIVA'
    assert data['fim'].startswith(stamp(130)[:19])


@pytest.mark.parametrize('changes',[
    {'inicio':stamp(9)}, {'fim':stamp(131)}, {'fim':stamp(10)},
    {'inicio':stamp(140)}, {'corte_aquisicao':stamp(129)},
    {'corte_aquisicao':(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()},
    {'inicio':'2026-01-01T00:00:00'}, {'modo':'OTHER'},
])
def test_invalid_window_cutoff_and_mode_rejected(analyses,changes):
    acquired(analyses); assert execute(analyses,**changes).status_code==422
    assert count(analyses,AnaliseEtileno)==0


def test_cancelled_preserves_old_analyses_and_exact_replay(analyses):
    w=analyses; acquired(w,False); payload=body(); a=execute(w,payload).json()
    assert finish(w,w['session']['id'],action='cancelar',fim=stamp(130)).status_code==200
    assert execute(w).status_code==409
    assert execute(w,payload).json()['id']==a['id']
    assert w['client'].get(path(w)+'/'+a['id'],headers=headers(w)).json()==a


def test_duplicate_request_is_stable_after_new_revision(analyses):
    w=analyses; acquired(w,False); payload=body(); a=execute(w,payload).json()
    assert sync(w).status_code==200
    assert execute(w,payload).json()==a and count(w,AnaliseEtileno)==1
    assert execute(w,payload,intervalo_maximo_s='7200').status_code==409
    assert execute(w,payload,role='GESTOR').status_code==409
    assert result(w)['revisao_aquisicao']==2


def test_future_conflict_revision_does_not_mutate_old_analysis(analyses):
    w=analyses; acquired(w,False); a=result(w)
    w['payload']['feeds']=[feed(1,10,'20'),feed(2,70,'20'),feed(3,130,'20')]
    assert sync(w).status_code==200
    b=result(w)
    assert b['revisao_aquisicao']==2 and b['status_calculo']=='PARCIAL'
    assert b['resultado']['volume_janela_min_ul'] is None
    assert Decimal(b['resultado']['volume_coberto_min_ul'])==500
    assert w['client'].get(path(w)+'/'+a['id'],headers=headers(w)).json()==a
    old=result(w,revisao_aquisicao=1)
    assert old['status_calculo']=='COMPLETO_NO_MODELO'
    assert old['resultado']==a['resultado'] or old['resultado']['volume_janela_min_ul']==a['resultado']['volume_janela_min_ul']
    assert old['id']!=a['id']


def test_late_complement_requires_new_analysis_not_mutation(analyses):
    w=analyses; w['payload']['feeds']=[feed(1,10,'13'),feed(2,70,'20')]; acquired(w)
    a=result(w); assert a['status_calculo']=='PARCIAL'
    w['payload']['feeds']=[feed(3,130,'20')]
    assert sync(w,role='GESTOR',complementar_encerrada=True,justificativa='Completar amostra final').status_code==200
    b=result(w); assert b['status_calculo']=='COMPLETO_NO_MODELO'
    assert w['client'].get(path(w)+'/'+a['id'],headers=headers(w)).json()==a
    assert any(x['apos_encerramento'] for x in b['entrada_snapshot']['registros'])


def test_historical_cut_excludes_later_consolidated_revision(analyses):
    w=analyses; acquired(w,False); cutoff=datetime.now(timezone.utc).isoformat()
    w['payload']['feeds']=[feed(1,10,'20')]; sync(w)
    a=result(w,corte_aquisicao=cutoff)
    assert a['revisao_aquisicao']==1 and a['status_calculo']=='COMPLETO_NO_MODELO'
    assert execute(w,corte_aquisicao=cutoff,revisao_aquisicao=2).status_code==409
    assert execute(w,revisao_aquisicao=99).status_code==404
    assert result(w,revisao_aquisicao=0)['status_calculo']=='SEM_ESTIMATIVA'


def test_invalid_interior_sample_is_a_barrier(analyses):
    w=analyses; w['payload']['feeds']=[feed(1,10,'13'),feed(2,40,None),feed(3,70,'13'),feed(4,130,'20')]; acquired(w)
    r=result(w)['resultado']
    assert r['status_calculo']=='PARCIAL' and Decimal(r['duracao_coberta_s'])==3600
    assert Decimal(r['volume_coberto_min_ul'])==200


def test_unlocatable_temperature_timestamp_prevents_false_complete(analyses):
    w=analyses; w['payload']['feeds'].append(feed(4,80,created_at='invalid')); acquired(w)
    data=result(w)
    assert data['status_calculo']=='ENTRADA_INVALIDA'
    assert 'HORARIO_INVALIDO' in data['resultado']['motivos']
    assert data['resultado']['volume_janela_min_ul'] is None


def test_humidity_invalidity_cannot_change_temperature_calculation(analyses):
    w=analyses
    for row in w['payload']['feeds']: row['field7']='NaN'
    acquired(w); data=result(w)
    assert data['status_calculo']=='COMPLETO_NO_MODELO'
    assert Decimal(data['resultado']['volume_janela_min_ul'])==700
    assert all(o['fonte_id']!=str(w['hum'].id) for o in data['entrada_snapshot']['ocorrencias'])


def test_same_timestamp_equal_temperature_does_not_duplicate_exposure(analyses):
    w=analyses; w['payload']['feeds'].append(feed(4,70,'20')); acquired(w)
    assert Decimal(result(w)['resultado']['volume_janela_min_ul'])==700


def test_out_of_order_input_is_sorted_by_existing_engine(analyses):
    w=analyses; w['payload']['feeds'].reverse(); acquired(w)
    assert Decimal(result(w)['resultado']['volume_janela_min_ul'])==700


@pytest.mark.parametrize('operation',['post','list','get'])
def test_authentication_required(analyses,operation):
    client=analyses['client']; url=path(analyses)
    response=client.post(url,json=body()) if operation=='post' else client.get(url+('/'+str(uuid4()) if operation=='get' else ''))
    assert response.status_code==401


@pytest.mark.parametrize('role',['CONSULTA','OUTRO'])
def test_write_role_denied(analyses,role):
    assert execute(analyses,role=role).status_code==403


def test_reader_can_read_but_other_company_cannot(analyses):
    w=analyses; acquired(w); a=result(w)
    assert w['client'].get(path(w),headers=headers(w,'CONSULTA')).status_code==200
    assert w['client'].get(path(w)+'/'+a['id'],headers=headers(w,'CONSULTA')).status_code==200
    w['trip'].transportadora_id=w['outsider'].id; w['db'].commit()
    assert execute(w).status_code==403
    assert w['client'].get(path(w),headers=headers(w)).status_code==403
    assert w['client'].get(path(w)+'/'+a['id'],headers=headers(w)).status_code==403


def test_missing_session_and_analysis_or_wrong_session(analyses):
    w=analyses; acquired(w); a=result(w)
    url=f'/api/v1/monitoramentos/{uuid4()}/analises-etileno'
    assert w['client'].post(url,headers=headers(w),json=body()).status_code==404
    assert w['client'].get(path(w)+'/'+str(uuid4()),headers=headers(w)).status_code==404
    # A new valid session in the same scope still cannot claim this analysis.
    from tests.test_monitoramento_sessoes import start,start_body
    response=start(w,start_body(w,inicio=stamp(140)))
    assert response.status_code==201,response.text
    other=response.json()['id']
    assert w['client'].get(f'/api/v1/monitoramentos/{other}/analises-etileno/'+a['id'],headers=headers(w)).status_code==404


@pytest.mark.parametrize('point',['audit','commit'])
def test_transaction_failure_rolls_back_analysis_and_audit(analyses,monkeypatch,point):
    from app.modules.monitoramento.service import MonitoramentoService
    w=analyses; acquired(w); before=count(w,EventoMonitoramento)
    def fail(*args,**kwargs): raise OperationalError('REDACTED',{},Exception('PRIVATE'))
    if point=='audit': monkeypatch.setattr(MonitoramentoService,'evento',fail)
    else: monkeypatch.setattr(w['db'],'commit',fail)
    response=execute(w)
    assert response.status_code==503 and 'PRIVATE' not in response.text
    assert count(w,AnaliseEtileno)==0 and count(w,EventoMonitoramento)==before


def test_openapi_documents_three_authenticated_operations(analyses):
    schema=analyses['application'].openapi(); p='/api/v1/monitoramentos/{sessao_id}/analises-etileno'
    for operation in [schema['paths'][p]['post'],schema['paths'][p]['get'],schema['paths'][p+'/{analise_id}']['get']]:
        assert operation['security']==[{'HTTPBearer':[]}]
    assert 'AnaliseCreate' in schema['components']['schemas']
    assert 'intervalo_maximo_s' in schema['components']['schemas']['AnaliseCreate']['properties']
    assert 'NAO_AVALIADO' in str(schema['components']['schemas']['ResultadoResponse'])


def test_active_without_explicit_end_uses_exact_frozen_cutoff(analyses):
    w=analyses; acquired(w,False); cutoff=datetime.now(timezone.utc).isoformat()
    payload=body(corte_aquisicao=cutoff); payload.pop('fim')
    response=execute(w,payload); assert response.status_code==200,response.text
    data=response.json()
    assert datetime.fromisoformat(data['fim'])==datetime.fromisoformat(cutoff)
    assert data['status_calculo']=='PARCIAL'
    assert data['resultado']['volume_janela_min_ul'] is None


def test_unsealed_revision_cannot_leak_into_analysis(analyses):
    w=analyses; acquired(w,False)
    run=w['db'].scalar(select(SincronizacaoIoT)); run.estado='EM_EXECUCAO'; run.finalizada_em=None; w['db'].commit()
    assert execute(w,revisao_aquisicao=1).status_code==409
    data=result(w)
    assert data['revisao_aquisicao']==0 and data['status_calculo']=='SEM_ESTIMATIVA'
    assert data['entrada_snapshot']['registros']==[]


def test_humidity_conflict_is_context_only(analyses):
    w=analyses; acquired(w,False)
    for row in w['payload']['feeds']: row['field7']='80'
    sync(w)
    data=result(w)
    assert data['status_calculo']=='COMPLETO_NO_MODELO'
    assert Decimal(data['resultado']['volume_janela_min_ul'])==700
    assert data['entrada_snapshot']['ocorrencias']==[]


def test_all_readings_are_used_beyond_history_default_page(analyses):
    w=analyses
    w['payload']['feeds']=[feed(n+1,10+n,'13') for n in range(121)]
    acquired(w)
    data=result(w,intervalo_maximo_s='60')
    assert len(data['entrada_snapshot']['registros'])==121
    assert Decimal(data['resultado']['percentual_cobertura'])==100
    assert Decimal(data['resultado']['volume_janela_min_ul'])==400
    assert Decimal(data['resultado']['volume_janela_max_ul'])==2000


def test_missing_configuration_is_explicit_conflict(analyses,monkeypatch):
    w=analyses; original=w['db'].get
    def missing(model,*args,**kwargs):
        if model is CargaMonitoramento: return None
        return original(model,*args,**kwargs)
    monkeypatch.setattr(w['db'],'get',missing)
    assert execute(w).status_code==409
    assert count(w,AnaliseEtileno)==0


def test_locatable_persistence_error_is_a_temperature_barrier(analyses):
    w=analyses; acquired(w,False)
    fonte=w['db'].scalar(select(FonteSessaoIoT).where(FonteSessaoIoT.tipo=='TEMPERATURA'))
    run=w['db'].scalar(select(SincronizacaoIoT))
    w['db'].add(OcorrenciaIoT(sincronizacao_id=run.id,fonte_id=fonte.id,entry_id=18,
        medida_em=BASE+timedelta(minutes=40),processada_em=datetime.now(timezone.utc),
        codigo='FALHA_PERSISTENCIA',detalhes={}))
    w['db'].commit()
    data=result(w)
    assert data['status_calculo']=='PARCIAL'
    assert Decimal(data['resultado']['volume_coberto_min_ul'])==500
    assert data['resultado']['volume_janela_min_ul'] is None


@pytest.mark.parametrize('column,value',[
    ('classificacao_risco_etileno','BAIXO'),('status_calculo','SUCESSO'),('revisao_aquisicao',-1),
    ('fim',BASE+timedelta(minutes=9)),
])
def test_database_checks_reject_inconsistent_analysis(analyses,column,value):
    w=analyses; acquired(w); data=result(w)
    row=w['db'].get(AnaliseEtileno,UUID(data['id'])); setattr(row,column,value)
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback()
    assert w['client'].get(path(w)+'/'+data['id'],headers=headers(w)).json()==data


def test_real_engine_called_once_and_get_never_recalculates(analyses,monkeypatch):
    import app.modules.monitoramento.analises_service as module
    original=module.estimar_etileno; calls=[]
    def traced(entrada):
        calls.append(entrada); return original(entrada)
    monkeypatch.setattr(module,'estimar_etileno',traced)
    w=analyses; acquired(w); payload=body(); a=execute(w,payload).json()
    execute(w,payload)
    w['client'].get(path(w)+'/'+a['id'],headers=headers(w))
    w['client'].get(path(w),headers=headers(w))
    assert len(calls)==1
