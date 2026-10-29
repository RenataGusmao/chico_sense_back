"""Stage 8: full local demonstration and security/contract regression checks."""
import asyncio
from datetime import datetime,timedelta,timezone
from decimal import Decimal
from pathlib import Path
from uuid import UUID,uuid4
import io,json,logging
import httpx
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import select,func
from app.models.iot import Medicao
from app.models.historico_iot import FonteSessaoIoT,RegistroSessaoIoT,SincronizacaoIoT
from app.models.analises_etileno import AnaliseEtileno
from app.models.preventivo import ConfiguracaoAmbiental,AvaliacaoPreventiva,AlertaSessao,EvidenciaPreventiva,DecisaoAlerta
from app.models.monitoramento import Alerta,Ocorrencia
from app.models.exaustao_simulada import IntervencaoSimulada,AcaoIntervencao
from app.models.sessoes_monitoramento import EventoMonitoramento
from app.modules.integracoes.thingspeak.client import ThingSpeakClient
from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
from app.modules.integracoes.thingspeak.schemas import ThingSpeakChannelConfig,ThingSpeakMappingConfig,ThingSpeakFieldMapping
from app.modules.integracoes.thingspeak.service import ThingSpeakService
from app.modules.monitoramento.historico_routes import thingspeak_service
from app.core.security import hash_password
from tests.test_monitoramento_sessoes import world,BASE,stamp,config_body,start_body,count

ROOT=Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('operation',['channel','feeds','latest','historical'])
def test_shared_thingspeak_client_masks_httpx_api_key_for_every_operation(caplog,operation):
    key='STAGE8_FAKE_KEY_MUST_NOT_BE_LOGGED'
    def handle(request):
        if request.url.path.endswith('last.json'):
            payload={'entry_id':1,'created_at':'2026-10-01T00:00:00Z','field1':'13'}
        else: payload={'channel':{'id':12345},'feeds':[]}
        return httpx.Response(200,json=payload)
    async def scenario():
        async with httpx.AsyncClient(base_url='https://api.thingspeak.com',transport=httpx.MockTransport(handle)) as http:
            client=ThingSpeakClient('https://api.thingspeak.com',read_api_key=key,http_client=http)
            if operation=='channel': await client.get_channel_info('12345')
            elif operation=='feeds': await client.get_feeds('12345')
            elif operation=='latest': await client.get_latest_feed('12345')
            else: await client.get_feeds_historicos('12345',BASE,BASE+timedelta(hours=1))
    with caplog.at_level(logging.INFO): asyncio.run(scenario())
    assert key not in caplog.text
    assert '[REDACTED]' in caplog.text


@pytest.fixture
def integrated(world,monkeypatch):
    from app.models.logistica import Caixa
    from app.models.integracoes import LeituraExterna
    w=world
    models=(Caixa,Medicao,LeituraExterna,FonteSessaoIoT,SincronizacaoIoT,RegistroSessaoIoT,
        __import__('app.models.historico_iot',fromlist=['OcorrenciaIoT']).OcorrenciaIoT,
        AnaliseEtileno,Alerta,Ocorrencia,ConfiguracaoAmbiental,AvaliacaoPreventiva,AlertaSessao,
        EvidenciaPreventiva,DecisaoAlerta,IntervencaoSimulada,AcaoIntervencao)
    for model in models: model.__table__.create(w['db'].get_bind())
    for role in ('OPERADOR','GESTOR','CONSULTA'):
        w['users'][role].senha_hash=hash_password('ChicoSense-stage8-fixture-only!')
    w['db'].commit()
    w['http_requests']=[]
    feeds=[dict(entry_id=n+1,created_at=stamp(minute),field4=temp,field7='92')
        for n,(minute,temp) in enumerate([(10,'13'),(70,'20'),(130,'20')])]
    def handle(req):
        w['http_requests'].append(req)
        return httpx.Response(200,json={'channel':{'id':12345},'feeds':feeds})
    http=httpx.AsyncClient(base_url='https://api.thingspeak.com',transport=httpx.MockTransport(handle))
    client=ThingSpeakClient('https://api.thingspeak.com',read_api_key='STAGE8_FAKE_KEY',http_client=http)
    mapping=ThingSpeakMappingConfig(fields={
        'field4':ThingSpeakFieldMapping(sensor_id=w['temp'].id,tipo='TEMPERATURA',contexto='AMBIENTE',unidade='C'),
        'field7':ThingSpeakFieldMapping(sensor_id=w['hum'].id,tipo='UMIDADE',contexto='AMBIENTE',unidade='%')})
    service=ThingSpeakService(ThingSpeakChannelConfig(base_url='https://api.thingspeak.com',channel_id='12345',timeout_seconds=1),
        client,ThingSpeakFieldMapper(mapping))
    w['application'].dependency_overrides[thingspeak_service]=lambda:service
    import app.modules.monitoramento.exaustao_service as virtual
    w['clock']=datetime.now(timezone.utc)
    monkeypatch.setattr(virtual,'agora_utc',lambda:w['clock'])
    yield w
    asyncio.run(http.aclose())


def test_fluxo_integrado_ponta_a_ponta_etapa8(integrated):
    w=integrated; client=w['client']; trace=[]; auth={}
    def call(method,path,payload=None,role='OPERADOR',expected=200):
        response=client.request(method,path,headers=auth.get(role,{}),json=payload)
        assert response.status_code==expected,response.text
        trace.append(dict(method=method,path=path,status=response.status_code,perfil=role))
        return response.json()
    # Real password verification and real JWT issuance; only these users/signing key are fixtures.
    for role in ('OPERADOR','GESTOR','CONSULTA'):
        login=client.post('/api/v1/auth/login',json={'email':w['users'][role].email,'senha':'ChicoSense-stage8-fixture-only!'})
        assert login.status_code==200,login.text
        auth[role]={'Authorization':'Bearer '+login.json()['access_token']}
        assert call('GET','/api/v1/auth/me',role=role)['perfil']==role
    trip=call('POST','/api/v1/viagens',dict(transportadora_id=str(w['transport'].id),veiculo_id=str(w['trip'].veiculo_id),
        motorista_id=str(w['trip'].motorista_id),origem='Petrolina hipotetica',destino='Destino didatico',saida_em=BASE.isoformat()),expected=201)
    cargo=call('POST',f"/api/v1/viagens/{trip['id']}/cargas",dict(produto_id=str(w['product'].id),produtor_id=str(w['producer'].id),
        identificacao='ETAPA8-CARGA-HIPOTETICA',observacoes='Fixture didatica; sem dados de producao.'),expected=201)
    call('PATCH',f"/api/v1/viagens/{trip['id']}",dict(status='EM_ANDAMENTO',inicio_real=BASE.isoformat()))
    call('PATCH',f"/api/v1/cargas/{cargo['id']}",dict(status='EM_TRANSITO'))
    # Device/sensor registration has no public API in this backend; bind fixture hardware metadata to the new trip.
    w['device'].viagem_id=UUID(trip['id']); w['db'].commit()
    profile=call('PUT',f"/api/v1/cargas/{cargo['id']}/monitoramento",config_body())
    assert profile['massa_kg']=='1000.0000' and profile['produto_identificado']=='MANGA_TOMMY_ATKINS'
    session=call('POST',f"/api/v1/cargas/{cargo['id']}/monitoramentos",start_body(w),expected=201)
    sid=session['id']; base='/api/v1/monitoramentos/'+sid
    sync=call('POST',base+'/sincronizacoes',dict(chave_idempotencia=str(uuid4())))
    assert sync['estado']=='CONCLUIDA' and sync['revisao']==1
    readings=call('GET',base+'/leituras?tipo=TEMPERATURA&revisao=1&fim='+stamp(130).replace('+','%2B'))
    assert readings['total']==3 and len(w['http_requests'])==1
    assert {x['field_name'] for x in readings['leituras']}=={'field4'}
    assert {x['sensor_id'] for x in readings['leituras']}=={str(w['temp'].id)}
    quality=call('GET',base+'/qualidade?intervalo_maximo_s=3600&revisao=1&fim='+stamp(130).replace('+','%2B'))
    assert all(Decimal(x['percentual_cobertura'])==100 for x in quality['indicadores'])
    analysis=call('POST',base+'/analises-etileno',dict(chave_idempotencia=str(uuid4()),intervalo_maximo_s='3600',
        fim=stamp(130),corte_aquisicao=datetime.now(timezone.utc).isoformat()))
    result=analysis['resultado']
    assert result['volume_janela_min_ul']=='700.000000' and result['volume_janela_max_ul']=='9000.000000'
    assert result['status_calculo']=='COMPLETO_NO_MODELO' and result['classificacao_risco_etileno']=='NAO_AVALIADO'
    assert call('GET',base+'/analises-etileno/'+analysis['id'])==analysis
    config=call('POST',base+'/configuracoes-ambientais',dict(chave_idempotencia=str(uuid4()),temperatura_min_c='12',temperatura_max_c='14',
        umidade_min_percentual='90',umidade_max_percentual='95',intervalo_maximo_s='3600',cobertura_min_percentual='100',
        exposicao_continua_s='3600',maturacoes_aplicaveis=['MISTA'],ambiente='TRANSPORTE_REFRIGERADO',fundamento='EXPERIMENTAL',
        justificativa='Parametros didaticos, sem validacao de dano fisiologico.',prioridade='ATENCAO'),role='GESTOR')
    evaluation=call('POST',base+'/avaliacoes-preventivas',dict(chave_idempotencia=str(uuid4()),fim=stamp(130),
        corte_aquisicao=datetime.now(timezone.utc).isoformat(),analise_etileno_id=analysis['id']))
    assert evaluation['configuracao_id']==config['id'] and evaluation['revisao']==analysis['revisao_aquisicao']
    alerts=call('GET',base+'/alertas')['alertas']; assert len(alerts)==2
    alert=next(a for a in alerts if a['tipo']=='TEMPERATURA_FORA_DA_FAIXA')
    call('POST',base+f"/alertas/{alert['id']}/decisoes",dict(chave_idempotencia=str(uuid4()),acao='RECONHECER',justificativa='Operador examinou a evidencia didatica.'))
    assert call('GET',base+f"/alertas/{alert['id']}")['status']=='EM_ANALISE'
    w['clock']=datetime.now(timezone.utc)
    intervention=call('POST',base+'/intervencoes-simuladas',dict(chave_idempotencia=str(uuid4()),duracao_planejada_s='60',
        justificativa='Demonstracao supervisionada, sem afirmar eficacia fisica.',alerta_id=alert['id'],
        avaliacao_id=evaluation['id'],analise_etileno_id=analysis['id']))
    iid=intervention['id']; vbase=base+'/intervencoes-simuladas/'+iid
    for action in ('AUTORIZAR','INICIAR'):
        call('POST',vbase+'/acoes',dict(chave_idempotencia=str(uuid4()),acao=action,justificativa='Gestor confirma somente a demonstracao virtual.'),role='GESTOR')
    assert call('GET',vbase)['virtual_ligado']
    w['clock']+=timedelta(seconds=60)
    call('POST',vbase+'/acoes',dict(chave_idempotencia=str(uuid4()),acao='ENCERRAR',justificativa='Solicitante encerra explicitamente a demonstracao.'))
    final=call('GET',vbase); history=call('GET',vbase+'/acoes')
    assert final['estado']=='CONCLUIDA' and final['duracao_registrada_s']=='60.000000' and not final['virtual_ligado']
    assert [a['acao'] for a in history['acoes']]==['SOLICITAR','AUTORIZAR','INICIAR','ENCERRAR']
    for item in (session,analysis,evaluation,alert,intervention):
        if 'sessao_id' in item: assert item['sessao_id']==sid
        if 'carga_id' in item: assert item['carga_id']==cargo['id']
        if 'viagem_id' in item: assert item['viagem_id']==trip['id']
    assert final['alerta_id']==alert['id'] and final['avaliacao_id']==evaluation['id'] and final['analise_etileno_id']==analysis['id']
    assert call('GET',base+'/analises-etileno/'+analysis['id'])==analysis
    assert call('GET',base+f"/alertas/{alert['id']}")['status']=='EM_ANALISE'
    assert count(w,IntervencaoSimulada)==1 and count(w,AcaoIntervencao)==4
    assert call('GET',base+'/intervencoes-simuladas',role='CONSULTA')['total']==1
    print(json.dumps(dict(ambiente='SQLite descartavel, JWT real de fixture, HTTP ThingSpeak mockado',
        viagem_id=trip['id'],carga_id=cargo['id'],sessao_id=sid,analise_id=analysis['id'],alerta_id=alert['id'],
        intervencao_id=iid,volume_potencial_ul=['700.000000','9000.000000'],cobertura_percentual='100',
        risco_etileno='NAO_AVALIADO',estado_virtual=final['estado'],acoes=[a['acao'] for a in history['acoes']],
        operacoes_http_locais=len(trace)+len(auth),aquisicoes_fisicas=0),ensure_ascii=False,indent=2))


def test_entire_migration_chain_compiles_postgresql_offline(monkeypatch):
    from app.core.config import settings
    from app.core.database import Base
    # Never use the environment's database configuration, even in offline mode.
    monkeypatch.setattr(settings,'database_url','postgresql+psycopg://127.0.0.1/chicosense_test_stage8')
    monkeypatch.setattr('logging.config.fileConfig',lambda *a,**k:None)
    output=io.StringIO(); config=Config(str(ROOT/'alembic.ini'),output_buffer=output)
    config.set_main_option('script_location',str(ROOT/'alembic'))
    command.upgrade(config,'head',sql=True)
    sql=output.getvalue()
    for name in Base.metadata.tables: assert 'CREATE TABLE '+name+' (' in sql
    assert '20261028_0010_exaustao_virtual' in sql and 'JSONB' in sql
    assert "WHERE estado = 'EM_EXECUCAO'" in sql
    assert sql.count('CREATE TABLE')==len(Base.metadata.tables)+1  # Includes alembic_version.
    down=io.StringIO(); config.output_buffer=down
    command.downgrade(config,'head:base',sql=True)
    for name in Base.metadata.tables: assert 'DROP TABLE '+name+';' in down.getvalue()


def test_all_new_monitoring_routes_declare_and_enforce_bearer_auth(world):
    schema=world['application'].openapi(); checked=[]
    for path,operations in schema['paths'].items():
        if '/monitoramento' not in path: continue
        for method,operation in operations.items():
            if method not in ('get','post','put','patch','delete'): continue
            assert operation.get('security')==[{'HTTPBearer':[]}],(method,path)
            import re
            url=re.sub(r'\{[^}]+\}',str(uuid4()),path)
            response=world['client'].request(method,url,json={} if method in ('post','put','patch') else None)
            assert response.status_code==401,(method,path,response.text)
            checked.append((method,path))
    assert len(checked)==30


def test_validation_errors_and_cors_do_not_expose_request_secrets(world):
    from tests.test_monitoramento_sessoes import headers
    payload={'chave_idempotencia':str(uuid4()),'justificativa':'demo','duracao_planejada_s':'60','api_key':'STAGE8_FAKE_SENSITIVE_INPUT'}
    response=world['client'].post(f'/api/v1/monitoramentos/{uuid4()}/intervencoes-simuladas',headers=headers(world),json=payload)
    assert response.status_code==422
    assert 'STAGE8_FAKE_SENSITIVE_INPUT' not in response.text and '"input"' not in response.text
    login=world['client'].post('/api/v1/auth/login',json={'email':'invalid','senha':'STAGE8_FAKE_PASSWORD'})
    assert login.status_code==422 and 'STAGE8_FAKE_PASSWORD' not in login.text
    cors=world['client'].options('/api/v1/auth/login',headers={'Origin':'http://localhost:5173','Access-Control-Request-Method':'POST'})
    assert cors.headers['access-control-allow-origin']=='http://localhost:5173'


def test_concurrent_mock_http_requests_keep_log_redaction_and_cleanup(caplog):
    logger=logging.getLogger('httpx'); before=list(logger.filters); key='STAGE8_CONCURRENT_FAKE_KEY'
    async def scenario():
        arrivals=0; gate=asyncio.Event()
        async def handle(request):
            nonlocal arrivals
            arrivals+=1
            if arrivals==2: gate.set()
            await asyncio.wait_for(gate.wait(),timeout=2)
            return httpx.Response(200,json={'channel':{'id':12345},'feeds':[]})
        async with httpx.AsyncClient(base_url='https://api.thingspeak.com',transport=httpx.MockTransport(handle)) as http:
            client=ThingSpeakClient('https://api.thingspeak.com',read_api_key=key,http_client=http)
            await asyncio.gather(client.get_feeds('12345'),client.get_channel_info('12345'))
    with caplog.at_level(logging.INFO): asyncio.run(scenario())
    assert key not in caplog.text and caplog.text.count('[REDACTED]')==2
    assert list(logger.filters)==before


def test_request_log_filter_is_removed_after_http_failure():
    from app.modules.integracoes.thingspeak.exceptions import ThingSpeakConnectionError
    logger=logging.getLogger('httpx'); before=list(logger.filters)
    async def scenario():
        def handle(request): raise httpx.ConnectError('Fixture transport failure',request=request)
        async with httpx.AsyncClient(base_url='https://api.thingspeak.com',transport=httpx.MockTransport(handle)) as http:
            client=ThingSpeakClient('https://api.thingspeak.com',read_api_key='STAGE8_FAKE_KEY',http_client=http)
            with pytest.raises(ThingSpeakConnectionError): await client.get_feeds('12345')
    asyncio.run(scenario()); assert list(logger.filters)==before
