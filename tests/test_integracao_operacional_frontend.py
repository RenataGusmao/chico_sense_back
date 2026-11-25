"""Real JWT and isolated SQLite. Never uses the app's configured DB connection."""
from uuid import UUID, uuid4
import pytest
from sqlalchemy import select, func
from app.core.database import Base
from app.models.empresa import Empresa
from app.models.enums import TipoEmpresa, StatusSensor, StatusDispositivo, ContextoMedicao
from app.models.iot import Sensor, Dispositivo
from app.models.parceiro_comercial import ParceiroComercial
from app.models.usuario import EmpresaUsuario
from tests.test_monitoramento_sessoes import world, headers, stamp, start, config, finish


@pytest.fixture
def operational(world):
    w = world
    from app.models.logistica import Caixa
    from app.models.iot import Medicao
    from app.models.monitoramento import Alerta
    for model in (ParceiroComercial, Caixa, Medicao, Alerta):
        model.__table__.create(w['db'].get_bind(), checkfirst=True)
    external = Empresa(nome='Cliente autorizado', tipo=TipoEmpresa.CLIENTE, ativo=True)
    hidden = Empresa(nome='EMPRESA-PRIVADA', documento='NAO-EXIBIR', tipo=TipoEmpresa.PRODUTOR, ativo=True)
    w['db'].add_all([external, hidden]); w['db'].commit()
    w.update(external=external, hidden=hidden)
    return w


def call(w, method, path, role='GESTOR', **kwargs):
    return w['client'].request(method, '/api/v1' + path, headers=headers(w, role), **kwargs)


def approve(w, company=None, active=True):
    return call(w, 'PUT', f'/transportadoras/{w["transport"].id}/parceiros/{(company or w["producer"]).id}', 'ADMIN',
                json=dict(ativo=active, justificativa='Aprovacao explicita de teste'))


def catalog(w, role='GESTOR', **params):
    return call(w, 'GET', f'/cargas/{w["cargo"].id}/sensores-disponiveis', role,
                params=dict(ambiente='TRANSPORTE_REFRIGERADO', inicio=stamp()) | params)


@pytest.mark.parametrize('path', ['/monitoramento/resumo', '/transportadoras/{carrier}/parceiros', '/cargas/{cargo}/sensores-disponiveis'])
@pytest.mark.parametrize('auth', [{}, {'Authorization':'Bearer invalid-fixture'}])
def test_new_queries_require_jwt(operational, path, auth):
    w=operational
    r=w['client'].get('/api/v1'+path.format(carrier=w['transport'].id,cargo=w['cargo'].id),headers=auth,
        params={'ambiente':'LABORATORIO'})
    assert r.status_code==401


def test_partner_minimal_approval_scope_and_revoke(operational):
    w=operational; path=f'/transportadoras/{w["transport"].id}/parceiros'
    assert call(w,'GET',path).json()==[]
    assert approve(w).status_code==200
    assert approve(w,w['external']).status_code==200
    result=call(w,'GET',path).json()
    assert {r['id'] for r in result}=={str(w['producer'].id),str(w['external'].id)}
    assert all(set(r)=={'id','nome','tipo','ativo','aprovado','autorizado_para_novas_cargas'} for r in result)
    assert call(w,'GET',path,params={'tipo':'PRODUTOR','limit':1}).json()[0]['id']==str(w['producer'].id)
    assert call(w,'GET',path,params={'offset':2}).json()==[]
    first=approve(w).json(); second=approve(w).json(); assert first['id']==second['id']
    assert w['db'].scalar(select(func.count()).select_from(ParceiroComercial))==2
    assert approve(w,active=False).status_code==200
    assert str(w['producer'].id) not in {r['id'] for r in call(w,'GET',path).json()}
    historical=call(w,'GET',path,params={'incluir_historico':True}).json()
    assert next(r for r in historical if r['id']==str(w['producer'].id))['autorizado_para_novas_cargas'] is False
    assert w['cargo'].produtor_id==w['producer'].id


@pytest.mark.parametrize('role',['GESTOR','OPERADOR','CONSULTA'])
def test_only_admin_can_approve(operational,role):
    w=operational
    assert call(w,'PUT',f'/transportadoras/{w["transport"].id}/parceiros/{w["producer"].id}',role,
        json={'ativo':True,'justificativa':'Nao autorizado'}).status_code==403


def test_ids_and_history_do_not_grant_commercial_write(operational):
    w=operational
    body=dict(produto_id=str(w['product'].id),produtor_id=str(w['producer'].id),identificacao='NOVA')
    url=f'/viagens/{w["trip"].id}/cargas'
    assert call(w,'POST',url,json=body).status_code==403
    assert approve(w).status_code==200
    assert call(w,'POST',url,json=body).status_code==201
    assert call(w,'POST',url,json=body|{'identificacao':'CRUZADA','cliente_id':str(w['external'].id)}).status_code==403
    assert approve(w,w['external']).status_code==200
    assert call(w,'POST',url,json=body|{'identificacao':'COM-CLIENTE','cliente_id':str(w['external'].id)}).status_code==201
    assert approve(w,active=False).status_code==200
    assert call(w,'POST',url,json=body|{'identificacao':'REVOGADA'}).status_code==403
    assert call(w,'PATCH',f'/cargas/{w["cargo"].id}',json={'observacoes':'Historico preservado'}).status_code==200


def test_partner_grant_does_not_grant_membership_or_read_of_other_carrier(operational):
    w=operational; assert approve(w).status_code==200
    assert call(w,'GET',f'/transportadoras/{w["outsider"].id}/parceiros').status_code==403
    assert call(w,'GET',f'/transportadoras/{w["transport"].id}/parceiros','CONSULTA').status_code==403
    links=w['db'].scalars(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==w['users']['GESTOR'].id)).all()
    assert all(link.empresa_id==w['transport'].id for link in links)


def test_sensor_catalog_first_session_without_history_and_no_secrets(operational):
    w=operational; r=catalog(w); assert r.status_code==200,r.text
    assert {row['id'] for row in r.json()['sensores']}=={str(w['temp'].id),str(w['hum'].id)}
    assert r.json()['disponibilidade_revalidada_ao_iniciar'] is True
    assert all(set(row)=={'id','identificador','tipo','contexto','unidade','dispositivo_id'} for row in r.json()['sensores'])
    assert catalog(w,tipo='UMIDADE').json()['sensores'][0]['id']==str(w['hum'].id)
    assert len(catalog(w,limit=1).json()['sensores'])==1
    assert len(catalog(w,limit=1,offset=1).json()['sensores'])==1


@pytest.mark.parametrize('change',['sensor_inativo','device_inativo','foreign_cargo','foreign_trip','prototype','unit'])
def test_catalog_filters_unusable_sensors(operational,change):
    w=operational
    if change=='sensor_inativo': w['temp'].status=StatusSensor.INATIVO
    if change=='device_inativo': w['device'].status=StatusDispositivo.INATIVO
    if change=='foreign_cargo': w['device'].carga_id=uuid4()  # checked before FK commit
    if change=='prototype': w['temp'].contexto=ContextoMedicao.PROTOTIPO
    if change=='unit': w['temp'].unidade='ppm'
    if change=='foreign_cargo':
        w['db'].rollback()
        # A real different cargo avoids relying on broken foreign keys.
        from app.models.logistica import Carga
        other=Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['producer'].id,identificacao='OUTRA')
        w['db'].add(other); w['db'].flush(); w['device'].carga_id=other.id
    if change=='foreign_trip':
        from app.models.logistica import Veiculo
        other=Veiculo(empresa_id=w['transport'].id,identificador='OUTRO-VEICULO',ativo=True)
        w['db'].add(other);w['db'].flush();w['device'].veiculo_id=other.id
    w['db'].commit()
    assert str(w['temp'].id) not in {r['id'] for r in catalog(w).json()['sensores']}


def test_unbound_sensor_only_admin_laboratory_and_reservation_revalidated(operational):
    w=operational
    w['device'].viagem_id=None; w['device'].veiculo_id=None; w['db'].commit()
    assert catalog(w).json()['sensores']==[]
    assert catalog(w,'ADMIN').json()['sensores']==[]
    assert len(catalog(w,'ADMIN',ambiente='LABORATORIO').json()['sensores'])==2
    w['device'].viagem_id=w['trip'].id;w['db'].commit()
    assert config(w).status_code==200
    assert start(w).status_code==201
    assert catalog(w).json()['sensores']==[]
    assert start(w).status_code==409


def test_admin_provisions_only_new_context_bound_devices(operational):
    w=operational; path=f'/cargas/{w["cargo"].id}/sensores'
    body=dict(identificador_dispositivo='NOVO',sensores=[dict(identificador='T',tipo='TEMPERATURA',contexto='AMBIENTE',unidade='C')])
    assert call(w,'POST',path,json=body).status_code==403
    r=call(w,'POST',path,'ADMIN',json=body);assert r.status_code==201,r.text
    sensor=w['db'].get(Sensor,UUID(r.json()[0]['id']));device=w['db'].get(Dispositivo,sensor.dispositivo_id)
    assert device.carga_id==w['cargo'].id and device.viagem_id==w['trip'].id
    assert call(w,'POST',path,'ADMIN',json=body).status_code==409
    assert call(w,'POST',path,'ADMIN',json=body|{'api_key':'FORBIDDEN'}).status_code==422
    assert call(w,'POST',path,'ADMIN',json=body|{'sensores':[dict(identificador='X',tipo='TEMPERATURA',contexto='AMBIENTE',unidade='ppm')]}).status_code==422


def test_external_company_manager_does_not_discover_devices_or_partners(operational):
    w=operational;actor=w['users']['GESTOR']
    from app.models.logistica import Carga
    w['db'].add(Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['hidden'].id,identificacao='OUTRA-EMPRESA'))
    for link in w['db'].scalars(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==actor.id)):link.ativo=False
    w['db'].add(EmpresaUsuario(empresa_id=w['producer'].id,usuario_id=actor.id,ativo=True));w['db'].commit()
    assert catalog(w).status_code==403
    assert call(w,'GET',f'/transportadoras/{w["transport"].id}/parceiros').status_code==403
    summary=call(w,'GET','/monitoramento/resumo');assert summary.status_code==200
    assert summary.json()['cargas_total']==1


def test_authorized_summary_and_revoked_link(operational):
    w=operational
    assert config(w).status_code==200
    assert start(w).status_code==201
    r=call(w,'GET','/monitoramento/resumo','CONSULTA');assert r.status_code==200,r.text
    assert r.json() | {} == dict(consultado_em=r.json()['consultado_em'],viagens_total=1,viagens_em_transito=1,
        cargas_total=1,cargas_monitoradas=1,sessoes_ativas=1,alertas_abertos=0)
    for link in w['db'].scalars(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==w['users']['CONSULTA'].id)):link.ativo=False
    w['db'].commit()
    assert call(w,'GET','/monitoramento/resumo','CONSULTA').json()['cargas_total']==0
    assert catalog(w,'CONSULTA').status_code==403
