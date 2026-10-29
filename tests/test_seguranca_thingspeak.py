"""Global legacy integration is ADMIN-only; scoped session acquisition stays separate."""
import asyncio,logging
from datetime import datetime,timedelta,timezone
from uuid import uuid4
import httpx,jwt,pytest
from sqlalchemy import select,func
from app.core.config import settings
from app.models.logistica import Caixa
from app.models.iot import Medicao
from app.models.integracoes import LeituraExterna
from app.modules.integracoes.thingspeak.client import ThingSpeakClient
from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
from app.modules.integracoes.thingspeak.schemas import ThingSpeakChannelConfig,ThingSpeakMappingConfig,ThingSpeakFieldMapping
from app.modules.integracoes.thingspeak.service import ThingSpeakService
from app.modules.integracoes.thingspeak import routes
from app.modules.integracoes.thingspeak.exceptions import (ThingSpeakConfigurationError,ThingSpeakConnectionError,
    ThingSpeakTimeoutError,ThingSpeakHTTPError,ThingSpeakInvalidResponseError,ThingSpeakError)
from tests.test_monitoramento_sessoes import world,headers,BASE,count
from tests.test_historico_iot import iot,sync,history,quality

PATH='/api/v1/integracoes/thingspeak'
ENDPOINTS=[('get','/status'),('get','/feeds'),('get','/ultima-leitura'),('post','/sincronizar')]


@pytest.fixture
def global_channel(world,monkeypatch):
    w=world
    for model in (Caixa,Medicao,LeituraExterna): model.__table__.create(w['db'].get_bind())
    w['device'].carga_id=w['cargo'].id; w['db'].commit()
    w['http_calls']=[]; w['factory_calls']=[]
    raw=dict(entry_id=12,created_at=BASE.isoformat(),field4='13',field7='92',api_key='UPSTREAM_FAKE_SECRET',
        private_metadata={'token':'UPSTREAM_FAKE_TOKEN'},status='not needed by normalized DTO')
    w['raw_feed']=raw
    def handler(request):
        w['http_calls'].append(request)
        if w.get('transport_error'): raise w['transport_error'](request)
        payload=raw if request.url.path.endswith('last.json') else {'channel':{'id':12345},'feeds':[raw]}
        return httpx.Response(200,json=payload)
    http=httpx.AsyncClient(base_url='https://api.thingspeak.com',transport=httpx.MockTransport(handler))
    client=ThingSpeakClient('https://api.thingspeak.com',read_api_key='GLOBAL_CHANNEL_FAKE_KEY',http_client=http)
    mapping=ThingSpeakMappingConfig(fields={
        'field4':ThingSpeakFieldMapping(sensor_id=w['temp'].id,tipo='TEMPERATURA',contexto='AMBIENTE',unidade='C'),
        'field7':ThingSpeakFieldMapping(sensor_id=w['hum'].id,tipo='UMIDADE',contexto='AMBIENTE',unidade='%')})
    service=ThingSpeakService(ThingSpeakChannelConfig(base_url='https://api.thingspeak.com',channel_id='12345',
        read_api_key='GLOBAL_CHANNEL_FAKE_KEY'),client,ThingSpeakFieldMapper(mapping))
    def factory(cls): w['factory_calls'].append(True); return service
    monkeypatch.setattr(ThingSpeakService,'from_settings',classmethod(factory))
    w['global_service']=service
    yield w
    asyncio.run(http.aclose())


def call(w,method,suffix,role='ADMIN',auth=None,**kwargs):
    return w['client'].request(method,PATH+suffix,headers=headers(w,role) if auth is None else auth,**kwargs)


@pytest.mark.parametrize('mode',['missing','invalid','expired','inactive'])
def test_all_global_operations_require_valid_active_jwt_before_factory(global_channel,mode):
    w=global_channel; auth={}
    if mode=='invalid': auth={'Authorization':'Bearer FAKE_INVALID_TOKEN'}
    if mode=='expired':
        now=datetime.now(timezone.utc)
        token=jwt.encode(dict(sub=str(w['users']['ADMIN'].id),iat=now-timedelta(hours=2),exp=now-timedelta(hours=1),
            iss='chicosense-api',aud='chicosense-api',type='access'),settings.secret_key,algorithm='HS256')
        auth={'Authorization':'Bearer '+token}
    if mode=='inactive':
        w['users']['ADMIN'].ativo=False; w['db'].commit(); auth=headers(w,'ADMIN')
    for method,path in ENDPOINTS:
        assert call(w,method,path,auth=auth).status_code==401
    assert not w['factory_calls'] and not w['http_calls'] and count(w,Medicao)==0


@pytest.mark.parametrize('role',['GESTOR','OPERADOR','CONSULTA','OUTRO'])
def test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user(global_channel,role):
    w=global_channel
    for method,path in ENDPOINTS:
        r=call(w,method,path,role=role,params={'empresa_id':str(w['transport'].id),
            'sensor_id':str(w['temp'].id),'channel_id':'12345'})
        assert r.status_code==403 and '12345' not in r.text
    assert not w['factory_calls'] and not w['http_calls']


def test_scoped_reader_can_see_own_session_history_but_not_global_channel(iot,monkeypatch):
    w=iot
    assert sync(w).status_code==200
    assert history(w,role='CONSULTA').status_code==200
    assert quality(w).status_code==200
    for method,path in ENDPOINTS: assert call(w,method,path,role='OPERADOR').status_code==403
    w['trip'].transportadora_id=w['outsider'].id; w['db'].commit()
    assert history(w,role='CONSULTA').status_code==403
    assert call(w,'get','/feeds',role='CONSULTA').status_code==403


def test_admin_queries_preserve_dtos_and_sanitize_last_feed_without_mutation(global_channel):
    w=global_channel
    status=call(w,'get','/status'); assert status.status_code==200,status.text
    assert status.json()['configured'] and set(status.json())=={'configured','base_url','channel_id','message'}
    feeds=call(w,'get','/feeds'); assert feeds.status_code==200,feeds.text
    assert feeds.json()['feeds_processados']==1 and len(feeds.json()['leituras_normalizadas'])==2
    latest=call(w,'get','/ultima-leitura'); assert latest.status_code==200,latest.text
    assert latest.json()['fields']=={'field4':'13','field7':'92'}
    assert set(latest.json()['raw'])=={'entry_id','created_at','field4','field7'}
    assert 'GLOBAL_CHANNEL_FAKE_KEY' not in status.text+feeds.text+latest.text
    assert 'UPSTREAM_FAKE' not in latest.text
    internal=asyncio.run(w['global_service'].get_latest_feed())
    assert internal.raw['api_key']=='UPSTREAM_FAKE_SECRET' and w['raw_feed']['private_metadata']['token']=='UPSTREAM_FAKE_TOKEN'


def test_admin_sync_uses_real_deduplication_and_internal_services_need_no_http_token(global_channel):
    w=global_channel
    first=call(w,'post','/sincronizar'); assert first.status_code==200,first.text
    assert first.json()['medicoes_criadas']==2 and count(w,Medicao)==count(w,LeituraExterna)==2
    second=call(w,'post','/sincronizar'); assert second.json()['duplicados']==2
    internal=asyncio.run(w['global_service'].sincronizar_feeds(w['db'],results=1))
    assert internal.duplicados==2 and count(w,Medicao)==2
    assert all(m.carga_id==w['cargo'].id and m.viagem_id==w['trip'].id for m in w['db'].scalars(select(Medicao)))


@pytest.mark.parametrize('url',[
    'https://user:FAKE_PASSWORD@example.invalid','https://api.thingspeak.com?api_key=FAKE',
    'https://api.thingspeak.com#FAKE_TOKEN','file:///etc/example','https://api.thingspeak.com:invalid',
])
def test_unsafe_base_url_rejected_without_network_or_value_in_response(global_channel,url):
    w=global_channel; w['global_service'].config.base_url=url
    for method,path in ENDPOINTS:
        r=call(w,method,path); assert r.status_code==503,r.text
        assert 'FAKE' not in r.text and 'user:' not in r.text
    assert not w['http_calls'] and count(w,Medicao)==0


@pytest.mark.parametrize('channel',['12345/../other','12345?api_key=FAKE','abc','0'])
def test_configured_channel_cannot_inject_path_or_parameters(global_channel,channel):
    w=global_channel; w['global_service'].config.channel_id=channel
    r=call(w,'get','/feeds'); assert r.status_code==503 and channel not in r.text
    assert not w['http_calls']


def test_missing_channel_remains_private_diagnostic_and_queries_fail_generically(global_channel):
    w=global_channel; w['global_service'].config.channel_id=None
    assert call(w,'get','/status').json()['configured'] is False
    for method,path in ENDPOINTS[1:]: assert call(w,method,path).status_code==400
    assert not w['http_calls']


@pytest.mark.parametrize('exc,code',[
    (ThingSpeakConfigurationError('https://user:FAKE@host?token=FAKE'),400),
    (ThingSpeakConnectionError('password=FAKE'),503),
    (ThingSpeakTimeoutError('api_key=FAKE'),504),
    (ThingSpeakHTTPError(429,'secret=FAKE'),429),
    (ThingSpeakInvalidResponseError('token=FAKE'),502),
    (ThingSpeakError('private configuration FAKE'),500),
])
def test_upstream_error_messages_are_not_echoed(global_channel,monkeypatch,exc,code):
    w=global_channel
    async def failed(*a,**k): raise exc
    monkeypatch.setattr(w['global_service'],'get_mapped_feeds',failed)
    r=call(w,'get','/feeds'); assert r.status_code==code,r.text
    assert 'FAKE' not in r.text and 'password' not in r.text and 'https://' not in r.text


def test_configuration_parse_failure_never_exposes_values(global_channel,monkeypatch):
    def factory(cls): raise ValueError('api_key=FAKE_FROM_CONFIG')
    monkeypatch.setattr(ThingSpeakService,'from_settings',classmethod(factory))
    r=call(global_channel,'get','/status'); assert r.status_code==503 and 'FAKE_FROM_CONFIG' not in r.text


def test_known_secret_in_original_field_is_sanitized_on_copy(global_channel):
    w=global_channel; w['raw_feed']['field4']='GLOBAL_CHANNEL_FAKE_KEY'
    r=call(w,'get','/feeds'); assert r.status_code==200,r.text
    assert 'GLOBAL_CHANNEL_FAKE_KEY' not in r.text
    original=asyncio.run(w['global_service'].get_mapped_feeds())
    assert original.leituras_normalizadas[0].valor_original=='GLOBAL_CHANNEL_FAKE_KEY'


def test_private_global_endpoints_preserve_shared_http_log_protection(global_channel,caplog):
    w=global_channel
    with caplog.at_level(logging.INFO):
        for method,path in ENDPOINTS: assert call(w,method,path).status_code==200
    assert 'GLOBAL_CHANNEL_FAKE_KEY' not in caplog.text
    assert '[REDACTED]' in caplog.text


def test_openapi_and_runtime_router_inventory(global_channel):
    w=global_channel; s=w['application'].openapi()
    assert {p for p in s['paths'] if p.startswith(PATH)}=={PATH+p for _,p in ENDPOINTS}
    for method,path in ENDPOINTS:
        op=s['paths'][PATH+path][method]
        assert op['security']==[{'HTTPBearer':[]}]
        assert all(str(code) in op['responses'] for code in (401,403,503))
    expected_public={('GET','/'),('GET','/health'),('POST','/api/v1/auth/login')}
    public={(method.upper(),path) for path,ops in s['paths'].items() for method,o in ops.items()
        if method in ('get','post','put','patch','delete') and not o.get('security')}
    assert public==expected_public
    for path in ('/docs','/docs/oauth2-redirect','/redoc','/openapi.json'):
        assert w['client'].get(path).status_code==200


@pytest.mark.parametrize('url,hidden',[
    ('https://FAKE_USER:FAKE_PASS@api.thingspeak.com',('FAKE_USER','FAKE_PASS')),
    ('https://api.thingspeak.com?token=FAKE_URL_TOKEN',('FAKE_URL_TOKEN',)),
    ('https://api.thingspeak.com?api_key=FAKE_URL_KEY',('FAKE_URL_KEY',)),
])
def test_internal_http_logging_masks_sensitive_urls_even_without_http_boundary(caplog,url,hidden):
    async def scenario():
        async with httpx.AsyncClient(base_url=url,transport=httpx.MockTransport(lambda request:
            httpx.Response(200,json={'channel':{'id':12345},'feeds':[]}))) as http:
            client=ThingSpeakClient(url,read_api_key='FAKE_READ_KEY',http_client=http)
            await client.get_feeds('12345')
    with caplog.at_level(logging.INFO): asyncio.run(scenario())
    assert all(value not in caplog.text for value in hidden)
    assert 'FAKE_READ_KEY' not in caplog.text


def test_admin_last_reading_still_returns_null_when_no_feed(global_channel,monkeypatch):
    async def empty(): return None
    monkeypatch.setattr(global_channel['global_service'],'get_latest_feed',empty)
    r=call(global_channel,'get','/ultima-leitura')
    assert r.status_code==200 and r.json() is None


def test_sync_persistence_failure_rolls_back_without_connection_details(global_channel,monkeypatch):
    from sqlalchemy.exc import OperationalError
    from decimal import Decimal
    from app.models.enums import ContextoMedicao
    w=global_channel
    async def fail(db,results=None):
        db.add(Medicao(sensor_id=w['temp'].id,medida_em=BASE,contexto=ContextoMedicao.AMBIENTE,
            valor=Decimal('13'),unidade='C',viagem_id=w['trip'].id,carga_id=w['cargo'].id))
        db.flush()
        raise OperationalError('postgresql://user:FAKE_PASSWORD@example.invalid',{},Exception('token=FAKE_DB_TOKEN'))
    monkeypatch.setattr(w['global_service'],'sincronizar_feeds',fail)
    response=call(w,'post','/sincronizar')
    assert response.status_code==503
    assert 'FAKE' not in response.text and 'postgresql' not in response.text
    assert count(w,Medicao)==0
