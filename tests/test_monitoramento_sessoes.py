"""Monitoring HTTP/domain acceptance tests, using isolated SQLite and real JWT auth."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

import app.models
from app.api.deps import get_database_session
from app.core.config import settings
from app.core.security import create_access_token
from app.main import create_app
from app.models.empresa import Empresa
from app.models.enums import ContextoMedicao, StatusCarga, StatusDispositivo, StatusSensor, StatusViagem, TipoEmpresa, TipoSensor
from app.models.iot import Dispositivo, Sensor
from app.models.logistica import Carga, Motorista, Veiculo, Viagem
from app.models.produto import Produto
from app.models.usuario import EmpresaUsuario, Perfil, Usuario
from app.models.sessoes_monitoramento import CargaMonitoramento, EventoMonitoramento, SessaoMonitoramento

BASE = datetime.now(timezone.utc) - timedelta(hours=4)


def stamp(minutes=10):
    return (BASE + timedelta(minutes=minutes)).isoformat()


@pytest.fixture
def world(monkeypatch):
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    @event.listens_for(engine, "connect")
    def fks(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")
    models = (Perfil, Usuario, Empresa, EmpresaUsuario, Produto, Veiculo, Motorista, Viagem, Carga,
              Dispositivo, Sensor, CargaMonitoramento, SessaoMonitoramento, EventoMonitoramento)
    app.models.sessoes_monitoramento.Base.metadata.create_all(engine, tables=[m.__table__ for m in models])
    monkeypatch.setattr(settings, "secret_key", "monitoramento-test-only-signing-key-at-least-32-bytes")
    with Session(engine) as db:
        transport = Empresa(nome="Transportadora", tipo=TipoEmpresa.TRANSPORTADORA, ativo=True)
        outsider = Empresa(nome="Outra transportadora", tipo=TipoEmpresa.TRANSPORTADORA, ativo=True)
        producer = Empresa(nome="Produtor", tipo=TipoEmpresa.PRODUTOR, ativo=True)
        product = Produto(nome="Manga cadastrada", ativo=True)
        db.add_all([transport, outsider, producer, product]); db.flush()
        vehicle = Veiculo(empresa_id=transport.id, identificador="CAM-1", ativo=True)
        driver = Motorista(empresa_id=transport.id, nome="Motorista", ativo=True)
        db.add_all([vehicle, driver]); db.flush()
        trip = Viagem(transportadora_id=transport.id, veiculo_id=vehicle.id, motorista_id=driver.id,
                      origem="Petrolina", destino="Destino", saida_em=BASE, inicio_real=BASE,
                      status=StatusViagem.EM_ANDAMENTO)
        db.add(trip); db.flush()
        cargo = Carga(viagem_id=trip.id, produto_id=product.id, produtor_id=producer.id,
                      identificacao="CARGA-1", status=StatusCarga.EM_TRANSITO)
        device = Dispositivo(identificador="ESP-1", viagem_id=trip.id, veiculo_id=vehicle.id,
                             status=StatusDispositivo.ATIVO)
        db.add_all([cargo, device]); db.flush()
        temp = Sensor(dispositivo_id=device.id, identificador="TEMP", tipo=TipoSensor.TEMPERATURA,
                      contexto=ContextoMedicao.AMBIENTE, unidade="C", status=StatusSensor.ATIVO)
        hum = Sensor(dispositivo_id=device.id, identificador="HUM", tipo=TipoSensor.UMIDADE,
                     contexto=ContextoMedicao.AMBIENTE, unidade="%", status=StatusSensor.ATIVO)
        db.add_all([temp, hum])
        users = {}
        for role in ("ADMIN", "GESTOR", "OPERADOR", "CONSULTA", "OUTRO"):
            profile = Perfil(nome=role)
            user = Usuario(nome=role, email=f"{role.lower()}@example.com", perfil=profile, ativo=True)
            db.add(user); db.flush()
            db.add(EmpresaUsuario(empresa_id=transport.id, usuario_id=user.id, ativo=True))
            users[role] = user
        db.commit()
        application = create_app()
        def override():
            yield db
        application.dependency_overrides[get_database_session] = override
        with TestClient(application) as client:
            yield dict(db=db, client=client, application=application, cargo=cargo, trip=trip,
                       transport=transport, outsider=outsider, producer=producer, product=product,
                       temp=temp, hum=hum, device=device, users=users)
    engine.dispose()


def headers(w, role="OPERADOR"):
    return {"Authorization": f"Bearer {create_access_token(w['users'][role].id)}"}


def config_body(**changes):
    return dict(produto_identificado="MANGA_TOMMY_ATKINS", massa_kg="1000.0000",
                maturacao="MISTA", lote_codigo="DEMO-001", lote_hipotetico=True,
                rastreabilidade="Lote hipotetico; declaracao do operador.") | changes


def config(w, role="OPERADOR", cargo_id=None, **changes):
    return w['client'].put(f"/api/v1/cargas/{cargo_id or w['cargo'].id}/monitoramento",
                           headers=headers(w, role), json=config_body(**changes))


def start_body(w, **changes):
    return dict(inicio=stamp(), sensor_temperatura_id=str(w['temp'].id),
                sensor_umidade_id=str(w['hum'].id), ambiente_aquisicao="TRANSPORTE_REFRIGERADO",
                chave_idempotencia=str(uuid4())) | changes


def start(w, body=None, role="OPERADOR", cargo_id=None):
    return w['client'].post(f"/api/v1/cargas/{cargo_id or w['cargo'].id}/monitoramentos",
                            headers=headers(w, role), json=body or start_body(w))


def opened(w):
    assert config(w).status_code == 200
    response = start(w)
    assert response.status_code == 201, response.text
    return response.json()


def finish(w, session_id, action="encerrar", role="OPERADOR", **changes):
    return w['client'].post(f"/api/v1/monitoramentos/{session_id}/{action}",
                            headers=headers(w, role), json=dict(fim=stamp(40), motivo="Operacao registrada") | changes)


def count(w, model):
    return w['db'].scalar(select(func.count()).select_from(model))


def test_configure_preserves_legacy_cargo_and_product(world):
    w=world
    response=config(w)
    assert response.status_code == 200, response.text
    data=response.json()
    assert data['carga_id'] == str(w['cargo'].id)
    assert Decimal(data['massa_kg']) == 1000
    assert data['maturacao'] == 'MISTA'
    assert data['versao'] == 1
    assert w['cargo'].quantidade is None and w['cargo'].unidade is None
    assert w['product'].nome == 'Manga cadastrada'
    assert count(w,Carga) == 1 and count(w,CargaMonitoramento) == 1
    assert count(w,EventoMonitoramento) == 1


@pytest.mark.parametrize('mass',["0", "-1", "NaN", "Infinity", True, None, "100000000", "0.00001"])
def test_invalid_mass_rejected_without_persistence(world,mass):
    response=config(world,massa_kg=mass)
    assert response.status_code == 422
    assert count(world,CargaMonitoramento) == 0


@pytest.mark.parametrize('mass',["0.0001","1","99999999.9999"])
def test_valid_mass_limits(world,mass):
    response=config(world,massa_kg=mass)
    assert response.status_code == 200
    assert Decimal(response.json()['massa_kg']) == Decimal(mass)


@pytest.mark.parametrize('stage',['VERDE_MADURA','EM_AMADURECIMENTO','MADURA','MISTA','DESCONHECIDA'])
def test_all_maturity_stages(world,stage):
    assert config(world,maturacao=stage).json()['maturacao'] == stage


def test_unknown_stage_when_not_informed(world):
    body=config_body(); del body['maturacao']
    response=world['client'].put(f"/api/v1/cargas/{world['cargo'].id}/monitoramento",headers=headers(world),json=body)
    assert response.status_code == 200
    assert response.json()['maturacao'] == 'DESCONHECIDA'


@pytest.mark.parametrize('changes',[{'maturacao':'IMATURA'},{'maturacao':None},{'produto_identificado':'UVA'},
                                    {'lote_codigo':'  '},{'rastreabilidade':' '},{'lote_hipotetico':'true'}])
def test_declaration_validation(world,changes):
    assert config(world,**changes).status_code == 422


def test_legacy_cargo_still_works_without_monitoring_configuration(world):
    w=world
    assert w['client'].get(f"/api/v1/cargas/{w['cargo'].id}",headers=headers(w)).status_code == 200
    assert w['client'].get(f"/api/v1/cargas/{w['cargo'].id}/monitoramento",headers=headers(w)).status_code == 404
    assert count(w,CargaMonitoramento) == 0
    response=w['client'].patch(f"/api/v1/cargas/{w['cargo'].id}",headers=headers(w),json={'observacoes':'Legado preservado'})
    assert response.status_code == 200
    assert count(w,CargaMonitoramento) == 0


def test_config_put_is_idempotent_and_versioned(world):
    w=world
    first=config(w).json(); second=config(w).json()
    assert first == second
    assert count(w,EventoMonitoramento) == 1
    changed=config(w,massa_kg='1200').json()
    assert changed['id'] == first['id'] and changed['versao'] == 2
    assert count(w,EventoMonitoramento) == 2
    event=w['db'].scalars(select(EventoMonitoramento).order_by(EventoMonitoramento.created_at,EventoMonitoramento.id)).all()
    assert any(e.dados.get('antes',{}).get('massa_kg') == '1000.0000' for e in event if e.dados.get('antes'))


def test_start_records_real_window_cargo_trip_and_source_snapshot(world):
    w=world; data=opened(w)
    assert data['estado'] == 'ATIVA' and data['fim'] is None
    assert data['carga_id'] == str(w['cargo'].id) and data['viagem_id'] == str(w['trip'].id)
    assert data['criada_por_id'] == str(w['users']['OPERADOR'].id)
    assert data['origem_sensor']['temperatura']['sensor_id'] == str(w['temp'].id)
    assert data['origem_sensor']['umidade']['unidade'] == '%'
    assert datetime.fromisoformat(data['inicio']).replace(tzinfo=timezone.utc) == BASE+timedelta(minutes=10)
    assert data['inicio'] != data['created_at']
    assert count(w,EventoMonitoramento) == 2


def test_start_requires_configuration(world):
    assert start(world).status_code == 409


@pytest.mark.parametrize('state',['PLANEJADA','CONCLUIDA','CANCELADA'])
def test_start_requires_in_progress_trip(world,state):
    assert config(world).status_code == 200
    world['trip'].status=StatusViagem(state); world['db'].commit()
    assert start(world).status_code == 409


@pytest.mark.parametrize('state',['PLANEJADA','ENTREGUE','CANCELADA'])
def test_start_requires_in_transit_cargo(world,state):
    assert config(world).status_code == 200
    world['cargo'].status=StatusCarga(state); world['db'].commit()
    assert start(world).status_code == 409


@pytest.mark.parametrize('inicio',[lambda:stamp(-1),lambda:(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat(),lambda:'2026-10-01T12:00:00'])
def test_start_rejects_bad_times(world,inicio):
    assert config(world).status_code == 200
    assert start(world,start_body(world,inicio=inicio())).status_code == 422


def test_same_creation_key_is_idempotent_even_after_end(world):
    w=world; assert config(w).status_code == 200
    body=start_body(w); first=start(w,body)
    assert first.status_code == 201
    again=start(w,body)
    assert again.status_code == 200 and again.json()['id'] == first.json()['id']
    assert count(w,SessaoMonitoramento) == 1 and count(w,EventoMonitoramento) == 2
    assert finish(w,first.json()['id']).status_code == 200
    assert start(w,body).json()['estado'] == 'ENCERRADA'
    assert count(w,EventoMonitoramento) == 3


def test_idempotency_key_different_content_conflicts(world):
    w=world; assert config(w).status_code == 200
    body=start_body(w); assert start(w,body).status_code == 201
    assert start(w,body | {'observacoes':'Outro conteudo'}).status_code == 409
    assert count(w,SessaoMonitoramento) == 1


def test_second_active_session_of_same_cargo_conflicts(world):
    opened(world)
    assert start(world).status_code == 409
    assert count(world,SessaoMonitoramento) == 1


def test_same_source_cannot_monitor_two_cargos_simultaneously(world):
    w=world; opened(w)
    cargo=Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['producer'].id,
                identificacao='CARGA-2',status=StatusCarga.EM_TRANSITO)
    w['db'].add(cargo); w['db'].commit()
    assert config(w,cargo_id=cargo.id).status_code == 200
    assert start(w,cargo_id=cargo.id).status_code == 409


@pytest.mark.parametrize('action,expected',[('encerrar','ENCERRADA'),('cancelar','CANCELADA')])
def test_finish_is_audited_and_idempotent(world,action,expected):
    w=world; data=opened(w)
    first=finish(w,data['id'],action)
    assert first.status_code == 200, first.text
    assert first.json()['estado'] == expected
    assert first.json()['finalizada_por_id'] == str(w['users']['OPERADOR'].id)
    assert finish(w,data['id'],action).json() == first.json()
    assert count(w,EventoMonitoramento) == 3
    assert finish(w,data['id'],action,motivo='Outra decisao').status_code == 409
    assert finish(w,data['id'],'cancelar' if action=='encerrar' else 'encerrar').status_code == 409


@pytest.mark.parametrize('fim',[lambda:stamp(10),lambda:stamp(5),lambda:(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat(),lambda:'2026-10-01T12:00:00'])
def test_bad_final_times_do_not_change_session(world,fim):
    w=world; data=opened(w)
    assert finish(w,data['id'],fim=fim()).status_code == 422
    assert w['db'].get(SessaoMonitoramento,UUID(data['id'])).estado == 'ATIVA'
    assert count(w,EventoMonitoramento) == 2


def test_historical_overlap_rejected_and_next_adjacent_window_allowed(world):
    w=world; data=opened(w); assert finish(w,data['id']).status_code == 200
    assert start(w,start_body(w,inicio=stamp(30))).status_code == 409
    response=start(w,start_body(w,inicio=stamp(40)))
    assert response.status_code == 201, response.text
    assert count(w,SessaoMonitoramento) == 2


def test_active_configuration_frozen_but_terminal_snapshot_survives_later_edit(world):
    w=world; data=opened(w)
    assert config(w).status_code == 200
    assert config(w,massa_kg='1500').status_code == 409
    assert finish(w,data['id']).status_code == 200
    assert config(w,massa_kg='1500').status_code == 200
    old=w['client'].get(f"/api/v1/monitoramentos/{data['id']}",headers=headers(w)).json()
    assert Decimal(old['massa_kg']) == 1000 and old['configuracao_versao'] == 1
    assert count(w,EventoMonitoramento) == 4


@pytest.mark.parametrize('method,path,payload',[
    ('put','/cargas/{cargo}/monitoramento','config'),
    ('get','/cargas/{cargo}/monitoramento',None),
    ('post','/cargas/{cargo}/monitoramentos','start'),
    ('get','/cargas/{cargo}/monitoramentos',None),
    ('get','/viagens/{trip}/monitoramentos',None),
    ('get','/monitoramentos/{session}',None),
    ('post','/monitoramentos/{session}/encerrar','end'),
    ('post','/monitoramentos/{session}/cancelar','end'),
])
def test_every_new_endpoint_requires_authentication(world,method,path,payload):
    w=world
    url='/api/v1'+path.format(cargo=w['cargo'].id,trip=w['trip'].id,session=uuid4())
    body={'config':config_body(),'start':start_body(w),'end':{'fim':stamp(40),'motivo':'Fim'}}.get(payload)
    response=w['client'].request(method,url,json=body)
    assert response.status_code == 401
    assert count(w,CargaMonitoramento) == 0


@pytest.mark.parametrize('role',['ADMIN','GESTOR','OPERADOR'])
def test_allowed_roles_can_configure_and_start(world,role):
    assert config(world,role).status_code == 200
    response=start(world,role=role)
    assert response.status_code == 201


def test_consulta_can_read_but_not_write(world):
    w=world; data=opened(w)
    assert config(w,'CONSULTA').status_code == 403
    assert start(w,role='CONSULTA').status_code == 403
    assert finish(w,data['id'],role='CONSULTA').status_code == 403
    assert w['client'].get(f"/api/v1/monitoramentos/{data['id']}",headers=headers(w,'CONSULTA')).status_code == 200
    assert w['client'].get(f"/api/v1/cargas/{w['cargo'].id}/monitoramento",headers=headers(w,'CONSULTA')).status_code == 200


def test_unknown_profile_is_denied(world):
    w=world
    assert config(w,'OUTRO').status_code == 403
    assert w['client'].get(f"/api/v1/cargas/{w['cargo'].id}/monitoramentos",headers=headers(w,'OUTRO')).status_code == 403


@pytest.mark.parametrize('inactive',['user','membership','company'])
def test_inactive_identity_membership_or_company_denied(world,inactive):
    w=world
    if inactive=='user':
        w['users']['OPERADOR'].ativo=False
    elif inactive=='membership':
        link=w['db'].scalar(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==w['users']['OPERADOR'].id))
        link.ativo=False
    else:
        w['transport'].ativo=False
    w['db'].commit()
    assert config(w).status_code == (401 if inactive=='user' else 403)


@pytest.mark.parametrize('endpoint',['config','start','session','list_cargo','list_trip'])
def test_other_company_cannot_access_objects_or_lists(world,endpoint):
    w=world; data=opened(w)
    user=w['users']['OPERADOR']
    link=w['db'].scalar(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==user.id))
    link.empresa_id=w['outsider'].id; w['db'].commit()
    if endpoint=='config':
        response=config(w)
    elif endpoint=='start':
        response=start(w)
    else:
        path={'session':f"/monitoramentos/{data['id']}",
              'list_cargo':f"/cargas/{w['cargo'].id}/monitoramentos",
              'list_trip':f"/viagens/{w['trip'].id}/monitoramentos"}[endpoint]
        response=w['client'].get('/api/v1'+path,headers=headers(w))
    assert response.status_code == 403


def test_lists_are_scoped_paginated_and_stably_ordered(world):
    w=world; first=opened(w); assert finish(w,first['id']).status_code==200
    second=start(w,start_body(w,inicio=stamp(40))).json()
    for path in (f"/cargas/{w['cargo'].id}/monitoramentos",f"/viagens/{w['trip'].id}/monitoramentos"):
        response=w['client'].get('/api/v1'+path+'?limit=1&offset=1',headers=headers(w))
        assert response.status_code==200 and [r['id'] for r in response.json()]==[second['id']]
        assert w['client'].get('/api/v1'+path+'?limit=101',headers=headers(w)).status_code==422


@pytest.mark.parametrize('change,expected',[
    ('missing',404),('wrong_type',422),('same',422),('inactive_sensor',409),
    ('inactive_device',409),('other_context',409),('unit',422),('prototype',422),
])
def test_source_validation(world,change,expected):
    w=world; assert config(w).status_code==200
    body=start_body(w)
    if change=='missing': body['sensor_temperatura_id']=str(uuid4())
    elif change=='wrong_type': body['sensor_temperatura_id']=str(w['hum'].id); body['sensor_umidade_id']=None
    elif change=='same': body['sensor_umidade_id']=str(w['temp'].id)
    elif change=='inactive_sensor': w['temp'].status=StatusSensor.INATIVO
    elif change=='inactive_device': w['device'].status=StatusDispositivo.MANUTENCAO
    elif change=='other_context':
        cargo=Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['producer'].id,identificacao='OTHER',status=StatusCarga.EM_TRANSITO)
        w['db'].add(cargo); w['db'].flush(); w['device'].carga_id=cargo.id
    elif change=='unit': w['temp'].unidade='unknown'
    elif change=='prototype': w['temp'].contexto=ContextoMedicao.PROTOTIPO
    w['db'].commit()
    response=start(w,body)
    assert response.status_code==expected, response.text
    assert count(w,SessaoMonitoramento)==0
    assert count(w,EventoMonitoramento)==1


def test_unbound_sensor_requires_admin_and_laboratory(world):
    w=world; assert config(w).status_code==200
    w['device'].viagem_id=None; w['device'].veiculo_id=None; w['db'].commit()
    body=start_body(w,ambiente_aquisicao='LABORATORIO')
    assert start(w,body).status_code==403
    assert start(w,body,role='ADMIN').status_code==201


def test_humidity_sensor_is_optional(world):
    w=world; assert config(w).status_code==200
    response=start(w,start_body(w,sensor_umidade_id=None))
    assert response.status_code==201
    assert response.json()['origem_sensor']['umidade'] is None


def test_session_end_must_not_exceed_real_trip_arrival(world):
    w=world; data=opened(w)
    w['trip'].chegada_em=BASE+timedelta(minutes=30); w['trip'].status=StatusViagem.CONCLUIDA; w['db'].commit()
    assert finish(w,data['id']).status_code==422
    assert finish(w,data['id'],fim=stamp(30)).status_code==200


def test_cancelled_sessions_reserve_their_historical_window(world):
    w=world; data=opened(w); assert finish(w,data['id'],'cancelar').status_code==200
    assert start(w,start_body(w,inicio=stamp(20))).status_code==409
    assert start(w,start_body(w,inicio=stamp(40))).status_code==201


def test_database_rejects_wrong_trip_even_with_existing_foreign_keys(world):
    w=world; data=opened(w)
    trip=Viagem(transportadora_id=w['transport'].id,veiculo_id=w['trip'].veiculo_id,
                motorista_id=w['trip'].motorista_id,origem='A',destino='B',saida_em=BASE,status=StatusViagem.PLANEJADA)
    w['db'].add(trip); w['db'].commit()
    session=w['db'].get(SessaoMonitoramento,UUID(data['id'])); session.viagem_id=trip.id
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback()
    assert w['db'].get(SessaoMonitoramento,UUID(data['id'])).viagem_id==w['cargo'].viagem_id


def test_database_partial_uniqueness_rejects_duplicate_active_session(world):
    w=world; data=opened(w)
    source=w['db'].get(SessaoMonitoramento,UUID(data['id']))
    values={c.key:getattr(source,c.key) for c in SessaoMonitoramento.__table__.columns if c.key not in ('id','created_at','updated_at')}
    values['chave_idempotencia']=uuid4()
    w['db'].add(SessaoMonitoramento(**values))
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback()
    assert count(w,SessaoMonitoramento)==1


def test_database_lifecycle_check_rejects_terminal_session_without_end(world):
    w=world; data=opened(w)
    session=w['db'].get(SessaoMonitoramento,UUID(data['id']))
    actor_id=w['users']['OPERADOR'].id
    session.estado='ENCERRADA'; session.finalizada_por_id=actor_id; session.motivo_fim='Incompleto'
    with pytest.raises(IntegrityError): w['db'].commit()
    w['db'].rollback()
    assert w['db'].get(SessaoMonitoramento,UUID(data['id'])).estado=='ATIVA'


def test_terminal_session_has_no_implicit_measurement_association_endpoint(world):
    w=world; data=opened(w); assert finish(w,data['id']).status_code==200
    response=w['client'].post(f"/api/v1/monitoramentos/{data['id']}/medicoes",headers=headers(w),json={'medicao_id':str(uuid4())})
    assert response.status_code==404
    from app.models.iot import Medicao
    assert 'sessao_id' not in Medicao.__table__.columns


def test_openapi_documents_authentication_schemas_and_status_codes(world):
    schema=world['application'].openapi()
    post=schema['paths']['/api/v1/cargas/{carga_id}/monitoramentos']['post']
    assert post['security'] == [{'HTTPBearer':[]}]
    assert set(('200','201','401','403','404','409','422')) <= set(post['responses'])
    assert post['requestBody']['content']['application/json']['schema']['$ref'].endswith('/SessaoCreate')
