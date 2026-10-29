"""Session acquisition tests use the existing ThingSpeak client with mocked HTTP."""
import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID, uuid4
import httpx
import pytest
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.models.iot import Medicao
from app.models.integracoes import LeituraExterna
from app.models.logistica import Caixa
from app.models.historico_iot import FonteSessaoIoT, SincronizacaoIoT, RegistroSessaoIoT, OcorrenciaIoT
from app.modules.integracoes.thingspeak.client import ThingSpeakClient
from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
from app.modules.integracoes.thingspeak.schemas import ThingSpeakChannelConfig, ThingSpeakMappingConfig, ThingSpeakFieldMapping
from app.modules.integracoes.thingspeak.service import ThingSpeakService
from app.modules.monitoramento.historico_routes import thingspeak_service
from tests.test_monitoramento_sessoes import world, headers, opened, finish, stamp, BASE, count


def feed(entry,minute,temp='13',hum='90',**changes):
    return dict(entry_id=entry,created_at=stamp(minute),field4=temp,field7=hum)|changes


@pytest.fixture
def iot(world):
    w=world
    for model in (Caixa,Medicao,LeituraExterna,FonteSessaoIoT,SincronizacaoIoT,RegistroSessaoIoT,OcorrenciaIoT):
        model.__table__.create(w['db'].get_bind())
    w['session']=opened(w)
    w['payload']={'channel':{'id':12345},'feeds':[feed(1,10),feed(2,20,'15'),feed(3,40,'20')]}
    w['requests']=[]
    def handle(request):
        w['requests'].append(request)
        if w.get('exception'): raise w['exception']
        payload=w['payload'](request) if callable(w['payload']) else w['payload']
        return httpx.Response(w.get('http_status',200),json=payload)
    http=httpx.AsyncClient(base_url='https://api.thingspeak.com',transport=httpx.MockTransport(handle))
    client=ThingSpeakClient('https://api.thingspeak.com',read_api_key='PRIVATE_READ_KEY',http_client=http)
    mapping=ThingSpeakMappingConfig(fields={
        'field4':ThingSpeakFieldMapping(sensor_id=w['temp'].id,tipo='TEMPERATURA',contexto='AMBIENTE',unidade='C'),
        'field7':ThingSpeakFieldMapping(sensor_id=w['hum'].id,tipo='UMIDADE',contexto='AMBIENTE',unidade='%'),
    })
    service=ThingSpeakService(ThingSpeakChannelConfig(base_url='https://api.thingspeak.com',channel_id='12345',timeout_seconds=1),client,ThingSpeakFieldMapper(mapping))
    w['thing']=service
    w['application'].dependency_overrides[thingspeak_service]=lambda:service
    yield w
    asyncio.run(http.aclose())


def sync(w,body=None,role='OPERADOR',**changes):
    payload=body or dict(chave_idempotencia=str(uuid4()))
    return w['client'].post(f"/api/v1/monitoramentos/{w['session']['id']}/sincronizacoes",
                            headers=headers(w,role),json=payload|changes)


def history(w,params=None,role='OPERADOR'):
    return w['client'].get(f"/api/v1/monitoramentos/{w['session']['id']}/leituras",headers=headers(w,role),params=params)


def quality(w,**params):
    return w['client'].get(f"/api/v1/monitoramentos/{w['session']['id']}/qualidade",headers=headers(w),
                           params={'intervalo_maximo_s':'600','fim':stamp(40)}|params)


def test_acquires_mapped_fields_and_reuses_existing_measurement_tables(iot):
    w=iot; response=sync(w)
    assert response.status_code==200,response.text
    assert response.json()['estado']=='CONCLUIDA'
    assert response.json()['resumo']['novas']==6
    assert count(w,Medicao)==count(w,LeituraExterna)==count(w,RegistroSessaoIoT)==6
    assert count(w,FonteSessaoIoT)==2
    result=history(w).json()
    assert result['total']==6 and result['revisao']==1
    assert {r['field_name'] for r in result['leituras']}=={'field4','field7'}
    assert {r['sensor_id'] for r in result['leituras']}=={str(w['temp'].id),str(w['hum'].id)}
    assert [r['medida_em'] for r in result['leituras']]==sorted(r['medida_em'] for r in result['leituras'])
    assert 'PRIVATE_READ_KEY' not in response.text+str(result)
    params=w['requests'][0].url.params
    assert params['timezone']=='UTC' and params['results']=='8000'
    assert all(k not in params for k in ('average','round','median','timescale'))


def test_original_measurement_receipt_and_processing_are_distinct(iot):
    w=iot; original=(BASE+timedelta(minutes=10)).astimezone(timezone(timedelta(hours=-3))).isoformat()
    w['payload']['feeds']=[feed(1,10,created_at=original)]
    assert sync(w).json()['estado']=='CONCLUIDA'
    row=history(w,{'tipo':'TEMPERATURA'}).json()['leituras'][0]
    assert row['timestamp_origem']==original
    measured=datetime.fromisoformat(row['medida_em'].replace('Z','+00:00'))
    received=datetime.fromisoformat(row['recebida_em'].replace('Z','+00:00'))
    processed=datetime.fromisoformat(row['processada_em'].replace('Z','+00:00'))
    assert measured==BASE+timedelta(minutes=10)
    assert measured<received<=processed
    assert row['tardia'] is None  # No invented operational lateness threshold.


def test_repeat_sync_and_same_request_do_not_duplicate_readings(iot):
    w=iot; body={'chave_idempotencia':str(uuid4())}
    first=sync(w,body).json(); again=sync(w,body).json()
    assert first['id']==again['id'] and len(w['requests'])==1
    third=sync(w).json()
    assert third['revisao']==2 and third['resumo']['duplicadas']==6
    assert count(w,Medicao)==count(w,RegistroSessaoIoT)==6
    assert history(w,{'revisao':1}).json()['total']==6


def test_idempotency_rejects_different_payload(iot):
    body={'chave_idempotencia':str(uuid4())}
    assert sync(iot,body).status_code==200
    assert sync(iot,body,limite_atraso_s='10').status_code==409


def test_wrong_sensor_mapping_is_rejected_before_network(iot):
    iot['thing'].mapper.mapping_config.fields['field4'].sensor_id=uuid4()
    response=sync(iot)
    assert response.status_code==409
    assert count(iot,RegistroSessaoIoT)==0 and not iot['requests']


def test_binding_snapshot_does_not_follow_later_config_changes(iot):
    w=iot; assert sync(w).status_code==200
    w['thing'].config.channel_id='999'
    w['thing'].mapper.mapping_config.fields.clear()
    assert sync(w).status_code==200
    assert '/12345/' in w['requests'][-1].url.path
    assert {r['field_name'] for r in history(w).json()['leituras']}=={'field4','field7'}


def test_session_window_filters_before_and_after_and_keeps_endpoint_sample(iot):
    w=iot
    assert finish(w,w['session']['id']).status_code==200
    w['payload']['feeds']=[feed(1,9),feed(2,10),feed(3,40),feed(4,41)]
    result=sync(w,role='GESTOR',complementar_encerrada=True,justificativa='Complementar janela original').json()
    assert result['resumo']['novas']==4
    assert result['resumo']['fora_janela']==4
    times={r['entry_id'] for r in history(w).json()['leituras']}
    assert times=={2,3}


def test_closed_session_requires_explicit_elevated_audited_complement(iot):
    w=iot; assert finish(w,w['session']['id']).status_code==200
    assert sync(w).status_code==409
    assert sync(w,complementar_encerrada=True).status_code==422
    assert sync(w,complementar_encerrada=True,justificativa='Solicitada').status_code==403
    response=sync(w,role='GESTOR',complementar_encerrada=True,justificativa='Recebimento tardio aprovado')
    assert response.status_code==200,response.text
    assert response.json()['complementacao']
    rows=history(w).json()['leituras']
    assert all(r['apos_encerramento'] and r['tardia'] for r in rows)
    from app.models.sessoes_monitoramento import SessaoMonitoramento,EventoMonitoramento
    session=w['db'].get(SessaoMonitoramento,UUID(w['session']['id']))
    assert session.estado=='ENCERRADA'
    assert w['db'].scalar(select(func.count()).select_from(EventoMonitoramento).where(EventoMonitoramento.tipo=='IOT_SOLICITADA'))==1


def test_cancelled_session_is_readable_but_not_synchronizable(iot):
    w=iot; assert sync(w).status_code==200
    assert finish(w,w['session']['id'],'cancelar').status_code==200
    assert sync(w,role='ADMIN',complementar_encerrada=True,justificativa='Nao permitido').status_code==409
    assert history(w).status_code==200
    assert quality(w).json()['cancelada_para_analise']


def test_out_of_order_readings_are_sorted_without_changing_their_times(iot):
    w=iot; w['payload']['feeds']=[feed(3,40),feed(1,10),feed(2,20)]
    response=sync(w).json()
    assert response['resumo']['fora_de_ordem']==4
    rows=history(w,{'tipo':'TEMPERATURA'}).json()['leituras']
    assert [r['entry_id'] for r in rows]==[1,2,3]
    assert [r['fora_de_ordem'] for r in rows]==[True,True,False]


def test_missing_or_bad_numeric_field_preserves_a_barrier_and_valid_sibling(iot):
    w=iot; w['payload']['feeds']=[feed(1,10),feed(2,20,'invalid','91'),feed(3,30)]
    response=sync(w).json()
    assert response['estado']=='PARCIAL' and response['resumo']['invalidas']==1
    assert count(w,Medicao)==5 and count(w,RegistroSessaoIoT)==6
    points=history(w,{'tipo':'TEMPERATURA'}).json()['leituras']
    assert points[1]['estado']=='INVALIDA' and points[1]['valor'] is None
    temp=next(i for i in quality(w,fim=stamp(30)).json()['indicadores'] if i['tipo']=='TEMPERATURA')
    assert Decimal(temp['duracao_coberta_s'])==0
    assert all(x['motivo'] is not None for x in temp['intervalos'])


def test_source_payload_conflict_creates_new_revision_not_a_value_overwrite(iot):
    w=iot; assert sync(w).json()['estado']=='CONCLUIDA'
    w['payload']['feeds']=[feed(2,20,'99')]
    result=sync(w).json()
    assert result['estado']=='PARCIAL'
    latest=history(w,{'tipo':'TEMPERATURA'}).json()['leituras']
    assert next(r for r in latest if r['entry_id']==2)['estado']=='CONFLITANTE'
    old=history(w,{'revisao':1,'tipo':'TEMPERATURA'}).json()['leituras']
    assert Decimal(next(r for r in old if r['entry_id']==2)['valor'])==15
    assert count(w,RegistroSessaoIoT)==6


def test_empty_history_and_no_operational_gap_default(iot):
    w=iot; assert history(w).json()['leituras']==[]
    url=f"/api/v1/monitoramentos/{w['session']['id']}/qualidade"
    assert w['client'].get(url,headers=headers(w)).status_code==422
    result=quality(w).json()
    assert Decimal(result['indicadores'][0]['duracao_coberta_s'])==0
    assert Decimal(result['indicadores'][0]['percentual_cobertura'])==0
    assert not any('volume' in key for key in result)
    assert 'COBERTURA_TEMPORAL' in result['natureza']


def test_temporal_gaps_are_not_filled(iot):
    w=iot; sync(w)
    temp=next(i for i in quality(w).json()['indicadores'] if i['tipo']=='TEMPERATURA')
    assert Decimal(temp['duracao_coberta_s'])==600
    assert Decimal(temp['duracao_nao_coberta_s'])==1200
    assert len(temp['intervalos'])==2
    assert temp['intervalos'][1]['motivo']=='LACUNA_EXCESSIVA'


@pytest.mark.parametrize('exception',[httpx.ReadTimeout('PRIVATE_READ_KEY'),httpx.ConnectError('PRIVATE_READ_KEY')])
def test_communication_failure_is_persisted_without_secrets(iot,exception,caplog):
    w=iot; w['exception']=exception
    response=sync(w)
    assert response.status_code==200 and response.json()['estado']=='FALHA'
    assert response.json()['resumo']['erros']==1
    assert count(w,RegistroSessaoIoT)==0
    assert count(w,OcorrenciaIoT)==1
    assert 'PRIVATE_READ_KEY' not in response.text+caplog.text
    state=w['client'].get(f"/api/v1/monitoramentos/{w['session']['id']}/sincronizacoes",headers=headers(w)).json()
    assert state['tentativas'][0]['estado']=='FALHA'


def test_history_pagination_and_type_filter(iot):
    w=iot; sync(w)
    response=history(w,{'tipo':'TEMPERATURA','limit':1,'offset':1}).json()
    assert response['total']==3 and len(response['leituras'])==1
    assert response['leituras'][0]['entry_id']==2
    assert history(w,{'limit':1001}).status_code==422


def test_reuses_legacy_external_history_without_fabricating_receipt_time(iot):
    from app.models.enums import ContextoMedicao
    w=iot
    m=Medicao(sensor_id=w['temp'].id,viagem_id=w['trip'].id,carga_id=w['cargo'].id,
              medida_em=BASE+timedelta(minutes=10),contexto=ContextoMedicao.AMBIENTE,valor=Decimal('13'),unidade='C')
    w['db'].add(m); w['db'].flush()
    w['db'].add(LeituraExterna(origem='THINGSPEAK',channel_id='12345',entry_id=17,field_name='field4',medicao_id=m.id)); w['db'].commit()
    response=sync(w,origem_dados='BANCO')
    assert response.status_code==200,response.text
    assert not w['requests'] and count(w,Medicao)==1
    row=history(w).json()['leituras'][0]
    assert row['medicao_id']==str(m.id) and row['recebida_em'] is None
    assert row['processada_em'] is not None and row['tardia'] is None


def test_existing_source_identity_of_other_sensor_is_not_reassigned(iot):
    from app.models.enums import ContextoMedicao
    w=iot
    m=Medicao(sensor_id=w['hum'].id,medida_em=BASE+timedelta(minutes=10),contexto=ContextoMedicao.AMBIENTE,valor=13,unidade='C')
    w['db'].add(m); w['db'].flush()
    w['db'].add(LeituraExterna(origem='THINGSPEAK',channel_id='12345',entry_id=1,field_name='field4',medicao_id=m.id)); w['db'].commit()
    response=sync(w).json()
    assert response['estado']=='PARCIAL'
    assert count(w,RegistroSessaoIoT)==5
    assert all(r['medicao_id']!=str(m.id) for r in history(w).json()['leituras'])


def test_late_complement_adds_revision_without_changing_previous_history(iot):
    w=iot; w['payload']['feeds']=[feed(1,10),feed(3,40)]
    assert sync(w).json()['revisao']==1
    assert finish(w,w['session']['id']).status_code==200
    w['payload']['feeds']=[feed(2,20,'15')]
    assert sync(w,role='GESTOR',complementar_encerrada=True,justificativa='Entrada disponibilizada posteriormente').json()['revisao']==2
    assert history(w,{'revisao':1}).json()['total']==4
    latest=history(w).json()
    assert latest['total']==6
    added=[r for r in latest['leituras'] if r['entry_id']==2]
    assert all(r['revisao_incorporacao']==2 and r['apos_encerramento'] for r in added)


def test_operational_lateness_limit_is_explicit_and_not_scientific(iot):
    result=sync(iot,limite_atraso_s='1').json()
    assert result['resumo']['tardias']==6
    assert result['resumo']['limite_atraso_s']=='1'


@pytest.mark.parametrize('change',[{'limite_atraso_s':'0'},{'limite_atraso_s':True},{'max_requisicoes':0},
                                  {'inicio':'2026-10-01T12:00:00'},{'fim':stamp(5)}])
def test_invalid_acquisition_parameters_are_rejected(iot,change):
    assert sync(iot,**change).status_code==422
    assert count(iot,SincronizacaoIoT)==0


@pytest.mark.parametrize('raw',[None,'NaN','Infinity','13.12345','100000000',True])
def test_invalid_values_are_markers_not_zero(iot,raw):
    w=iot; w['payload']['feeds']=[feed(1,10,raw,'90')]
    assert sync(w).json()['estado']=='PARCIAL'
    rows=history(w,{'tipo':'TEMPERATURA'}).json()['leituras']
    assert rows[0]['valor'] is None and rows[0]['medicao_id'] is None


@pytest.mark.parametrize('stamp_value',['2026-10-01T12:00:00','invalid',None])
def test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage(iot,stamp_value):
    w=iot; w['payload']['feeds']=[feed(1,10),feed(2,20,created_at=stamp_value),feed(3,40)]
    assert sync(w).json()['estado']=='PARCIAL'
    result=quality(w,intervalo_maximo_s='7200').json()
    assert result['metadados_temporais_invalidos']
    assert all(r['percentual_cobertura'] is None for r in result['indicadores'])
    assert history(w).json()['metadados_temporais_invalidos']


def test_same_timestamp_conflicting_values_block_coverage_without_overwriting(iot):
    w=iot; w['payload']['feeds']=[feed(1,10),feed(2,20,'14'),feed(3,20,'18'),feed(4,40)]
    assert sync(w).status_code==200
    temp=next(i for i in quality(w,intervalo_maximo_s='1800').json()['indicadores'] if i['tipo']=='TEMPERATURA')
    assert temp['instantes_conflitantes']==1 and Decimal(temp['duracao_coberta_s'])==0
    assert count(w,RegistroSessaoIoT)==8


def test_unrelated_channel_fields_are_not_imported(iot):
    w=iot; w['payload']['feeds']=[feed(1,10,field1='999',field8='777')]
    sync(w)
    assert count(w,RegistroSessaoIoT)==2
    assert {r['field_name'] for r in history(w).json()['leituras']}=={'field4','field7'}


def test_split_historical_requests_recover_more_than_one_page(iot,monkeypatch):
    import app.modules.monitoramento.historico_service as module
    from app.modules.monitoramento.incorporacao_iot import timestamp_origem
    monkeypatch.setattr(module,'LIMITE_FEEDS',2)
    w=iot; feeds=[feed(1,10),feed(2,20),feed(3,40)]
    def page(request):
        params=request.url.params
        a=datetime.fromisoformat(params['start']).replace(tzinfo=timezone.utc)
        b=datetime.fromisoformat(params['end']).replace(tzinfo=timezone.utc)
        selected=[f for f in feeds if a<=timestamp_origem(f['created_at'])<=b]
        return {'channel':{'id':12345},'feeds':selected[-2:]}
    w['payload']=page
    run=sync(w,fim=stamp(40)).json()
    assert run['estado']=='CONCLUIDA'
    assert run['resumo']['requisicoes']>1
    assert count(w,RegistroSessaoIoT)==6
    assert {r['entry_id'] for r in history(w).json()['leituras']}=={1,2,3}


def test_request_budget_reports_partial_instead_of_silent_truncation(iot,monkeypatch):
    import app.modules.monitoramento.historico_service as module
    monkeypatch.setattr(module,'LIMITE_FEEDS',2)
    w=iot; w['payload']['feeds']=[feed(2,20),feed(3,40)]
    run=sync(w,max_requisicoes=1,fim=stamp(40)).json()
    assert run['estado']=='PARCIAL'
    assert count(w,RegistroSessaoIoT)==4
    assert 'LIMITE_REQUISICOES' in quality(w).json()['codigos_ocorrencias']


def test_partial_network_failure_preserves_already_received_pages(iot,monkeypatch):
    import app.modules.monitoramento.historico_service as module
    monkeypatch.setattr(module,'LIMITE_FEEDS',2)
    w=iot
    def page(request):
        if len(w['requests'])==1: return {'channel':{'id':12345},'feeds':[feed(2,20),feed(3,40)]}
        raise httpx.ReadTimeout('PRIVATE_READ_KEY')
    w['payload']=page
    run=sync(w,fim=stamp(40)).json()
    assert run['estado']=='PARCIAL' and count(w,RegistroSessaoIoT)==4
    assert run['resumo']['erros']==2


def test_partial_persistence_failure_keeps_the_other_fields(iot,monkeypatch):
    from app.repositories.medicoes import MedicaoRepository
    original=MedicaoRepository.create
    def fail(self,**values):
        if values['sensor_id']==iot['temp'].id:
            raise RuntimeError('PRIVATE_READ_KEY')
        return original(self,**values)
    monkeypatch.setattr(MedicaoRepository,'create',fail)
    run=sync(iot).json()
    assert run['estado']=='PARCIAL' and run['resumo']['erros']==3
    assert count(iot,RegistroSessaoIoT)==3 and count(iot,Medicao)==3
    assert 'PRIVATE_READ_KEY' not in str(run)


@pytest.mark.parametrize('http_status',[404,429,500])
def test_http_provider_errors_are_auditable_failures(iot,http_status):
    iot['http_status']=http_status
    assert sync(iot).json()['estado']=='FALHA'


def test_expired_execution_is_recoverable_and_old_key_is_not_reexecuted(iot):
    w=iot; body={'chave_idempotencia':str(uuid4())}
    first=sync(w,body).json()
    run=w['db'].get(SincronizacaoIoT,UUID(first['id']))
    run.estado='EM_EXECUCAO'; run.finalizada_em=None; run.expira_em=datetime.now(timezone.utc)-timedelta(seconds=1)
    w['db'].commit()
    assert sync(w,body).json()['estado']=='INTERROMPIDA'
    assert len(w['requests'])==1
    assert sync(w).json()['estado']=='CONCLUIDA'


def test_running_request_replay_returns_202_and_second_key_is_blocked(iot):
    w=iot; body={'chave_idempotencia':str(uuid4())}
    first=sync(w,body).json()
    run=w['db'].get(SincronizacaoIoT,UUID(first['id'])); run.estado='EM_EXECUCAO'; run.finalizada_em=None
    run.expira_em=datetime.now(timezone.utc)+timedelta(minutes=1); w['db'].commit()
    assert sync(w,body).status_code==202
    assert sync(w).status_code==409
    assert len(w['requests'])==1


@pytest.mark.parametrize('method,path,params',[
    ('get','leituras',{}),('get','sincronizacoes',{}),('get','qualidade',{'intervalo_maximo_s':600}),
    ('post','sincronizacoes',{}),
])
def test_new_endpoints_require_authentication(iot,method,path,params):
    w=iot; url=f"/api/v1/monitoramentos/{w['session']['id']}/{path}"
    response=w['client'].request(method,url,params=params,json={'chave_idempotencia':str(uuid4())} if method=='post' else None)
    assert response.status_code==401
    assert not w['requests']


@pytest.mark.parametrize('role',['CONSULTA','OUTRO'])
def test_unauthorized_roles_cannot_sync(iot,role):
    assert sync(iot,role=role).status_code==403
    assert not iot['requests']


@pytest.mark.parametrize('path',['leituras','sincronizacoes','qualidade'])
def test_other_company_cannot_read_acquisition(iot,path):
    from app.models.usuario import EmpresaUsuario
    w=iot; sync(w)
    link=w['db'].scalar(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==w['users']['OPERADOR'].id))
    link.empresa_id=w['outsider'].id; w['db'].commit()
    response=w['client'].get(f"/api/v1/monitoramentos/{w['session']['id']}/{path}",headers=headers(w),params={'intervalo_maximo_s':600})
    assert response.status_code==403


def test_consulta_can_read_history_but_not_incorporate(iot):
    sync(iot)
    assert history(iot,role='CONSULTA').status_code==200
    assert sync(iot,role='CONSULTA').status_code==403


def test_httpx_info_logging_does_not_disclose_read_key(iot,caplog):
    import logging
    caplog.set_level(logging.INFO,logger='httpx')
    assert sync(iot).status_code==200
    assert 'PRIVATE_READ_KEY' not in caplog.text
    assert '[REDACTED]' in caplog.text


def test_math_engine_is_not_called(iot,monkeypatch):
    import app.modules.monitoramento.etileno.motor as engine
    def forbidden(*args,**kwargs): raise AssertionError('Ethylene engine must stay isolated')
    monkeypatch.setattr(engine,'estimar_etileno',forbidden)
    assert sync(iot).status_code==200
    assert history(iot).status_code==200
    assert quality(iot).status_code==200


def test_quality_requires_positive_operational_gap(iot):
    assert quality(iot,intervalo_maximo_s='0').status_code==422
    assert quality(iot,intervalo_maximo_s='NaN').status_code==422


def test_same_timestamp_same_value_is_not_double_exposure(iot):
    w=iot; w['payload']['feeds']=[feed(1,10),feed(2,10),feed(3,20)]
    sync(w)
    temp=next(i for i in quality(w,fim=stamp(20)).json()['indicadores'] if i['tipo']=='TEMPERATURA')
    assert len(temp['intervalos'])==1 and Decimal(temp['duracao_coberta_s'])==600


def test_queries_cannot_extend_session_window(iot):
    sync(iot)
    assert history(iot,{'inicio':stamp(9)}).status_code==422
    assert finish(iot,iot['session']['id']).status_code==200
    assert history(iot,{'fim':stamp(41)}).status_code==422


def test_closed_replay_is_not_a_new_complementation(iot):
    body={'chave_idempotencia':str(uuid4())}
    run=sync(iot,body).json()
    finish(iot,iot['session']['id'])
    # An exact replay returns the already-incorporated attempt; it cannot add readings.
    assert sync(iot,body).json()['id']==run['id']
    assert len(iot['requests'])==1


def test_old_thingSpeak_endpoints_and_routes_are_still_registered(iot):
    paths=iot['application'].openapi()['paths']
    for suffix in ('status','feeds','ultima-leitura','sincronizar'):
        assert '/api/v1/integracoes/thingspeak/'+suffix in paths
    new=paths['/api/v1/monitoramentos/{sessao_id}/sincronizacoes']['post']
    assert new['security']==[{'HTTPBearer':[]}]
    assert '202' in new['responses']
    assert 'volume_janela_min_ul' not in str(new)


def test_midflight_end_requires_a_new_explicit_complement_request(iot):
    w=iot
    def page(request):
        from app.models.sessoes_monitoramento import SessaoMonitoramento
        session=w['db'].get(SessaoMonitoramento,UUID(w['session']['id']))
        actor_id=w['users']['OPERADOR'].id
        session.estado='ENCERRADA'; session.fim=BASE+timedelta(minutes=40)
        session.finalizada_por_id=actor_id; session.motivo_fim='Encerrada durante consulta'
        w['db'].commit()
        return {'channel':{'id':12345},'feeds':[feed(1,10)]}
    w['payload']=page
    response=sync(w).json()
    assert response['estado']=='FALHA'
    assert count(w,RegistroSessaoIoT)==0


def test_global_deduplication_is_backed_by_existing_unique_identity(iot):
    sync(iot)
    row=iot['db'].scalar(select(LeituraExterna))
    duplicate=LeituraExterna(origem=row.origem,channel_id=row.channel_id,entry_id=row.entry_id,field_name=row.field_name,medicao_id=row.medicao_id)
    iot['db'].add(duplicate)
    with pytest.raises(IntegrityError): iot['db'].commit()
    iot['db'].rollback()
    assert count(iot,LeituraExterna)==6


def test_late_local_incorporation_does_not_fabricate_late_receipt(iot):
    from app.models.enums import ContextoMedicao
    w=iot
    m=Medicao(sensor_id=w['temp'].id,medida_em=BASE+timedelta(minutes=20),
              contexto=ContextoMedicao.AMBIENTE,valor=Decimal('13'),unidade='C')
    w['db'].add(m); w['db'].flush()
    w['db'].add(LeituraExterna(origem='THINGSPEAK',channel_id='12345',entry_id=18,field_name='field4',medicao_id=m.id))
    w['db'].commit()
    assert finish(w,w['session']['id']).status_code==200
    result=sync(w,role='GESTOR',origem_dados='BANCO',complementar_encerrada=True,justificativa='Associar historico local sem horario de recebimento')
    assert result.status_code==200,result.text
    row=history(w).json()['leituras'][0]
    assert row['apos_encerramento'] is True
    assert row['recebida_em'] is None and row['tardia'] is None
