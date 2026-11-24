"""Cargo ownership is independent from carrier membership; no production I/O."""
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select
from app.models.empresa import Empresa
from app.models.enums import TipoEmpresa, StatusCarga, StatusViagem
from app.models.logistica import Carga, Caixa, Viagem, Veiculo, Motorista
from app.models.usuario import Usuario, EmpresaUsuario
from tests.test_monitoramento_sessoes import world, headers, BASE, stamp, config, config_body, start_body, start
from tests.test_historico_iot import iot, sync, feed
from tests.test_analises_etileno import analyses, execute as estimate
from tests.test_preventivo import preventive, configure, evaluate
from tests.test_exaustao_simulada import simulation, requested, act


def call(w, method, path, role, **kwargs):
    return w['client'].request(method, '/api/v1'+path, headers=headers(w,role), **kwargs)


def parties(w):
    db=w['db']
    producer_b=Empresa(nome='Produtor B PRIVADO',tipo=TipoEmpresa.PRODUTOR,ativo=True)
    client_a=Empresa(nome='Cliente A',tipo=TipoEmpresa.CLIENTE,ativo=True)
    client_b=Empresa(nome='Cliente B PRIVADO',tipo=TipoEmpresa.CLIENTE,ativo=True)
    db.add_all([producer_b,client_a,client_b]); db.flush()
    w['producer_b'],w['client_a'],w['client_b']=producer_b,client_a,client_b
    for label,company,profile in [('PRODUTOR_A',w['producer'],'CONSULTA'),('CLIENTE_A',client_a,'CONSULTA'),
                                  ('PRODUTOR_B',producer_b,'CONSULTA'),('CLIENTE_B',client_b,'CONSULTA'),
                                  ('PRODUTOR_GESTOR',w['producer'],'GESTOR')]:
        user=Usuario(nome=label,email=label.lower()+'@example.com',ativo=True,perfil=w['users'][profile].perfil)
        db.add(user); db.flush()
        db.add(EmpresaUsuario(empresa_id=company.id,usuario_id=user.id,ativo=True));w['users'][label]=user
    w['cargo'].cliente_id=client_a.id
    db.commit()


@pytest.fixture
def mixed(world):
    w=world;parties(w);db=w['db']
    Caixa.__table__.create(db.get_bind())
    cargo_b=Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['producer_b'].id,
                  cliente_id=w['client_b'].id,identificacao='CARGA-B-PRIVADA',status=StatusCarga.EM_TRANSITO)
    cargo_ac=Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['producer'].id,
                   cliente_id=w['client_b'].id,identificacao='CARGA-PRODUTOR-A-CLIENTE-B',status=StatusCarga.EM_TRANSITO)
    vehicle=Veiculo(empresa_id=w['outsider'].id,identificador='OUTRO-CAM',ativo=True)
    driver=Motorista(empresa_id=w['outsider'].id,nome='PRIVADO-OUTRO-MOTORISTA',ativo=True)
    db.add_all([cargo_b,cargo_ac,vehicle,driver]);db.flush()
    other=Viagem(transportadora_id=w['outsider'].id,veiculo_id=vehicle.id,motorista_id=driver.id,
                 origem='OUTRA-VIAGEM-PRIVADA',destino='Outro destino',saida_em=BASE,
                 inicio_real=BASE,status=StatusViagem.EM_ANDAMENTO)
    db.add(other);db.flush()
    other_cargo=Carga(viagem_id=other.id,produto_id=w['product'].id,produtor_id=w['producer_b'].id,
                      cliente_id=w['client_b'].id,identificacao='CARGA-OUTRA-VIAGEM',status=StatusCarga.EM_TRANSITO)
    db.add(other_cargo);db.flush()
    boxes=[]
    for c in [w['cargo'],cargo_b,cargo_ac,other_cargo]:
        box=Caixa(carga_id=c.id,identificacao='CAIXA-'+c.identificacao);db.add(box);boxes.append(box)
    db.commit()
    w.update(cargo_b=cargo_b,cargo_ac=cargo_ac,other=other,other_cargo=other_cargo,boxes=boxes)
    return w


@pytest.mark.parametrize('role,keys',[
    ('PRODUTOR_A',['cargo','cargo_ac']),('CLIENTE_A',['cargo']),('CLIENTE_B',['cargo_b','cargo_ac']),
    ('PRODUTOR_B',['cargo_b']),('CONSULTA',['cargo','cargo_b','cargo_ac']),
])
def test_mixed_trip_returns_only_own_cargos_before_pagination(mixed,role,keys):
    w=mixed;path=f'/viagens/{w["trip"].id}/cargas'
    expected={str(w[k].id) for k in keys}
    r=call(w,'GET',path,role);assert r.status_code==200,r.text
    assert {c['id'] for c in r.json()}==expected
    pages=[call(w,'GET',path,role,params={'limit':1,'offset':i}).json() for i in range(len(keys)+1)]
    assert all(len(p)==1 for p in pages[:-1]) and pages[-1]==[]
    assert {p[0]['id'] for p in pages[:-1]}==expected


@pytest.mark.parametrize('role',['PRODUTOR_A','CLIENTE_A','PRODUTOR_GESTOR'])
def test_ids_do_not_grant_other_cargo_or_box_on_visible_trip(mixed,role):
    w=mixed
    assert call(w,'GET',f'/viagens/{w["trip"].id}',role).status_code==200
    assert call(w,'GET',f'/cargas/{w["cargo"].id}',role).status_code==200
    for path in [f'/cargas/{w["cargo_b"].id}',f'/cargas/{w["cargo_b"].id}/caixas',f'/caixas/{w["boxes"][1].id}']:
        r=call(w,'GET',path,role);assert r.status_code==403 and 'PRIVAD' not in r.text
    assert call(w,'GET',f'/cargas/{uuid4()}',role).status_code==404


@pytest.mark.parametrize('role',['PRODUTOR_A','CLIENTE_A'])
def test_trip_list_filters_in_sql_and_explicit_carrier_is_only_a_filter(mixed,role):
    w=mixed;w['other'].created_at=BASE;w['db'].commit()
    r=call(w,'GET','/viagens',role,params={'limit':1});assert r.status_code==200
    assert [t['id'] for t in r.json()]==[str(w['trip'].id)]
    assert call(w,'GET','/viagens',role,params={'offset':1}).json()==[]
    assert len(call(w,'GET','/viagens',role,params={'empresa_id':str(w['transport'].id)}).json())==1
    assert call(w,'GET','/viagens',role,params={'empresa_id':str(w['outsider'].id)}).status_code==403
    assert call(w,'GET',f'/viagens/{w["other"].id}',role).status_code==403


def test_producer_can_follow_own_cargo_on_multiple_carriers_without_carrier_membership(mixed):
    w=mixed
    r=call(w,'GET','/viagens','PRODUTOR_B')
    assert r.status_code==200 and {t['id'] for t in r.json()}=={str(w['trip'].id),str(w['other'].id)}
    companies=call(w,'GET','/auth/me','PRODUTOR_B').json()['empresas']
    assert [c['id'] for c in companies]==[str(w['producer_b'].id)]
    assert call(w,'GET',f'/empresas/{w["transport"].id}','PRODUTOR_B').status_code==403


def test_admin_keeps_missing_company_filter_policy(mixed):
    assert call(mixed,'GET','/viagens','ADMIN',params={'empresa_id':str(uuid4())}).status_code==404


@pytest.mark.parametrize('role',['PRODUTOR_A','CLIENTE_A'])
def test_company_relationship_does_not_grant_fleet_or_global_iot(mixed,role):
    w=mixed
    assert call(w,'GET','/veiculos',role).json()==[]
    assert call(w,'GET','/motoristas',role).json()==[]
    assert call(w,'GET',f'/veiculos/{w["trip"].veiculo_id}',role).status_code==403
    assert call(w,'GET',f'/motoristas/{w["trip"].motorista_id}',role).status_code==403
    assert call(w,'GET','/integracoes/thingspeak/status',role).status_code==403


@pytest.mark.parametrize('change',['membership','company','carrier','company_type','user'])
def test_revoked_inactive_or_incompatible_links_fail_closed(mixed,change):
    w=mixed;u=w['users']['PRODUTOR_A']
    if change=='membership':
        row=w['db'].scalar(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==u.id));row.ativo=False
    elif change=='company':w['producer'].ativo=False
    elif change=='carrier':w['transport'].ativo=False
    elif change=='company_type':w['producer'].tipo=TipoEmpresa.CLIENTE
    else:u.ativo=False
    w['db'].commit()
    assert call(w,'GET',f'/cargas/{w["cargo"].id}','PRODUTOR_A').status_code==(401 if change=='user' else 403)
    if change!='user':assert call(w,'GET','/viagens','PRODUTOR_A').json()==[]


@pytest.mark.parametrize('role',['PRODUTOR_A','CLIENTE_A','PRODUTOR_GESTOR'])
def test_no_producer_client_write_even_with_manager_profile(mixed,role):
    w=mixed
    assert call(w,'PATCH',f'/cargas/{w["cargo"].id}',role,json={'observacoes':'NAO GRAVAR'}).status_code==403
    assert call(w,'PATCH',f'/viagens/{w["trip"].id}',role,json={'observacoes':'NAO GRAVAR'}).status_code==403
    assert call(w,'PUT',f'/cargas/{w["cargo"].id}/monitoramento',role,json=config_body()).status_code==403
    assert call(w,'POST',f'/cargas/{w["cargo"].id}/monitoramentos',role,json=start_body(w)).status_code==403


@pytest.fixture
def scoped_monitoring(simulation):
    w=simulation;parties(w)
    w['payload']['feeds'][0]['field4']='20'
    assert sync(w).status_code==200
    cfg=configure(w);assert cfg.status_code==200,cfg.text
    a=estimate(w);assert a.status_code==200,a.text
    e=evaluate(w);assert e.status_code==200,e.text
    w['analysis']=a.json();w['evaluation']=e.json();w['alert_id']=e.json()['alertas_ids'][0]
    w['intervention']=requested(w)
    return w


@pytest.mark.parametrize('role',['PRODUTOR_A','CLIENTE_A'])
def test_read_all_own_monitoring_resources_but_no_mutation(scoped_monitoring,role):
    w=scoped_monitoring;s=w['session']['id'];base=f'/monitoramentos/{s}';alert=w['alert_id'];i=w['intervention']['id']
    paths=[base,f'/cargas/{w["cargo"].id}/monitoramento',f'/cargas/{w["cargo"].id}/monitoramentos',
           f'/viagens/{w["trip"].id}/monitoramentos',base+'/sincronizacoes',base+'/leituras',
           base+'/qualidade?intervalo_maximo_s=3600',base+'/analises-etileno',
           base+'/analises-etileno/'+w['analysis']['id'],base+'/configuracoes-ambientais',
           base+'/avaliacoes-preventivas',base+'/avaliacoes-preventivas/'+w['evaluation']['id'],
           base+'/alertas',base+'/alertas/'+alert,base+'/alertas/'+alert+'/evidencias',
           base+'/alertas/'+alert+'/decisoes',base+'/intervencoes-simuladas',
           base+'/intervencoes-simuladas/'+i,base+'/intervencoes-simuladas/'+i+'/acoes']
    for p in paths:
        r=call(w,'GET',p,role);assert r.status_code==200,(p,r.text)
    assert call(w,'GET',base+'/intervencoes-simuladas/'+i,role).json()['acoes_permitidas']==[]
    payloads=[('/encerrar',dict(fim=stamp(130),motivo='NAO GRAVAR')),
              ('/sincronizacoes',dict(chave_idempotencia=str(uuid4()),origem_dados='BANCO')),
              ('/analises-etileno',dict(chave_idempotencia=str(uuid4()),intervalo_maximo_s='3600',corte_aquisicao=datetime.now(timezone.utc).isoformat())),
              ('/avaliacoes-preventivas',dict(chave_idempotencia=str(uuid4()),corte_aquisicao=datetime.now(timezone.utc).isoformat())),
              ('/alertas/'+alert+'/decisoes',dict(chave_idempotencia=str(uuid4()),acao='OBSERVAR',justificativa='NAO GRAVAR')),
              ('/intervencoes-simuladas',dict(chave_idempotencia=str(uuid4()),duracao_planejada_s='60',justificativa='NAO GRAVAR'))]
    for suffix,payload in payloads:
        r=call(w,'POST',base+suffix,role,json=payload);assert r.status_code==403,(suffix,r.text)


@pytest.mark.parametrize('role',['PRODUTOR_A','CLIENTE_A'])
def test_other_cargo_on_same_trip_does_not_leak_session_or_children(scoped_monitoring,role):
    w=scoped_monitoring;s=w['session']['id']
    # Existing monitored cargo becomes another producer/client's cargo, same trip remains visible.
    w['cargo'].produtor_id=w['producer_b'].id;w['cargo'].cliente_id=w['client_b'].id
    extra=Carga(viagem_id=w['trip'].id,produto_id=w['product'].id,produtor_id=w['producer'].id,
                cliente_id=w['client_a'].id,identificacao='OUTRA CARGA VISIVEL',status=StatusCarga.EM_TRANSITO)
    w['db'].add(extra);w['db'].commit()
    assert call(w,'GET',f'/viagens/{w["trip"].id}',role).status_code==200
    assert call(w,'GET',f'/viagens/{w["trip"].id}/monitoramentos',role).json()==[]
    for suffix in ['', '/leituras','/sincronizacoes','/qualidade?intervalo_maximo_s=3600',
                   '/analises-etileno','/analises-etileno/'+w['analysis']['id'],
                   '/avaliacoes-preventivas','/alertas','/alertas/'+w['alert_id']+'/evidencias',
                   '/intervencoes-simuladas/'+w['intervention']['id']+'/acoes']:
        r=call(w,'GET',f'/monitoramentos/{s}'+suffix,role);assert r.status_code==403,(suffix,r.text)


def test_business_manager_cannot_operate_or_authorize_virtual_intervention(scoped_monitoring):
    w=scoped_monitoring;s=w['session']['id'];i=w['intervention']['id']
    assert call(w,'GET',f'/monitoramentos/{s}/intervencoes-simuladas/{i}','PRODUTOR_GESTOR').json()['acoes_permitidas']==[]
    for suffix,payload in [('',dict(chave_idempotencia=str(uuid4()),duracao_planejada_s='60',justificativa='NAO GRAVAR')),
                           ('/'+i+'/acoes',dict(chave_idempotencia=str(uuid4()),acao='AUTORIZAR',justificativa='NAO GRAVAR'))]:
        r=call(w,'POST',f'/monitoramentos/{s}/intervencoes-simuladas'+suffix,'PRODUTOR_GESTOR',json=payload)
        assert r.status_code==403,r.text
