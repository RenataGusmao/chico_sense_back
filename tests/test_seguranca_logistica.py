"""Logistics access regression: real JWT, roles and two carriers in isolated SQLite."""
from datetime import datetime,timedelta,timezone
from uuid import UUID,uuid4
import re
import jwt
import pytest
from sqlalchemy import select,func
from app.core.config import settings
from app.models.usuario import EmpresaUsuario
from app.models.logistica import Veiculo,Motorista,Viagem,Carga,Caixa
from app.models.produto import ParametroProduto
from app.models.enums import StatusViagem,StatusCarga,StatusCaixa
from tests.test_monitoramento_sessoes import world,headers,BASE,opened


@pytest.fixture
def secured(world):
    w=world
    for model in (ParametroProduto,Caixa): model.__table__.create(w['db'].get_bind())
    vehicle=Veiculo(empresa_id=w['outsider'].id,identificador='PRIVADO-B',descricao='SEGREDO_DA_EMPRESA_B',ativo=True)
    driver=Motorista(empresa_id=w['outsider'].id,nome='MOTORISTA-PRIVADO-B',documento='DADO-PRIVADO-B',ativo=True)
    w['db'].add_all([vehicle,driver]); w['db'].flush()
    trip=Viagem(transportadora_id=w['outsider'].id,veiculo_id=vehicle.id,motorista_id=driver.id,
        origem='ORIGEM-PRIVADA-B',destino='Destino B',saida_em=BASE,inicio_real=BASE,status=StatusViagem.EM_ANDAMENTO)
    w['db'].add(trip); w['db'].flush()
    cargo=Carga(viagem_id=trip.id,produto_id=w['product'].id,produtor_id=w['producer'].id,
        identificacao='CARGA-PRIVADA-B',status=StatusCarga.EM_TRANSITO)
    w['db'].add(cargo); w['db'].flush()
    box_a=Caixa(carga_id=w['cargo'].id,identificacao='CAIXA-A',status=StatusCaixa.REGISTRADA)
    box_b=Caixa(carga_id=cargo.id,identificacao='CAIXA-PRIVADA-B',status=StatusCaixa.REGISTRADA)
    w['db'].add_all([box_a,box_b]); w['db'].commit()
    w['a']={'veiculos':w['db'].get(Veiculo,w['trip'].veiculo_id),'motoristas':w['db'].get(Motorista,w['trip'].motorista_id),
        'viagens':w['trip'],'cargas':w['cargo'],'caixas':box_a}
    w['b']={'veiculos':vehicle,'motoristas':driver,'viagens':trip,'cargas':cargo,'caixas':box_b}
    return w


def call(w,method,path,role='OPERADOR',payload=None,**kwargs):
    return w['client'].request(method,'/api/v1'+path,headers=headers(w,role),json=payload,**kwargs)


def protected_operations(w):
    return [(method,path) for path,ops in w['application'].openapi()['paths'].items()
        for method,operation in ops.items() if method in ('get','post','put','patch','delete')
        and set(operation.get('tags',[])) & {'Logistica','Produtos'}]


@pytest.mark.parametrize('kind',['missing','invalid','expired'])
def test_all_27_routes_reject_missing_invalid_or_expired_jwt(secured,kind):
    w=secured; auth={}
    if kind=='invalid': auth={'Authorization':'Bearer INVALID_FIXTURE_TOKEN'}
    elif kind=='expired':
        now=datetime.now(timezone.utc)
        token=jwt.encode(dict(sub=str(w['users']['OPERADOR'].id),iat=now-timedelta(hours=2),
            exp=now-timedelta(hours=1),iss='chicosense-api',aud='chicosense-api',type='access'),settings.secret_key,algorithm='HS256')
        auth={'Authorization':'Bearer '+token}
    operations=protected_operations(w); assert len(operations)==27
    for method,path in operations:
        url=re.sub(r'\{[^}]+\}',str(uuid4()),path)
        response=w['client'].request(method,url,headers=auth,json={} if method in ('post','patch') else None)
        assert response.status_code==401,(method,path,response.text)


@pytest.mark.parametrize('resource',['veiculos','motoristas','viagens','cargas','caixas'])
@pytest.mark.parametrize('role',['GESTOR','OPERADOR','CONSULTA'])
def test_detail_isolation_by_stored_ancestry(secured,resource,role):
    w=secured
    assert call(w,'GET',f'/{resource}/{w["a"][resource].id}',role).status_code==200
    response=call(w,'GET',f'/{resource}/{w["b"][resource].id}',role)
    assert response.status_code==403 and 'PRIVAD' not in response.text and 'SEGREDO' not in response.text
    assert call(w,'GET',f'/{resource}/{uuid4()}',role).status_code==404
    assert call(w,'GET',f'/{resource}/{w["b"][resource].id}','ADMIN').status_code==200


@pytest.mark.parametrize('resource',['veiculos','motoristas','viagens'])
def test_unfiltered_and_explicit_lists_scope_before_pagination(secured,resource):
    w=secured
    for model in w['b'].values(): model.created_at=BASE-timedelta(days=1)
    w['db'].commit()
    for role in ('GESTOR','OPERADOR','CONSULTA'):
        response=call(w,'GET','/'+resource,role,params={'limit':1,'offset':0})
        assert response.status_code==200 and [r['id'] for r in response.json()]==[str(w['a'][resource].id)]
        assert call(w,'GET','/'+resource,role,params={'offset':1}).json()==[]
        assert call(w,'GET','/'+resource,role,params={'empresa_id':str(w['outsider'].id)}).status_code==403
    assert len(call(w,'GET','/'+resource,'ADMIN').json())==2


@pytest.mark.parametrize('parent,child',[('viagens','cargas'),('cargas','caixas')])
def test_nested_lists_cannot_use_foreign_parent_ids(secured,parent,child):
    w=secured
    a=call(w,'GET',f'/{parent}/{w["a"][parent].id}/{child}','CONSULTA')
    assert a.status_code==200 and len(a.json())==1
    assert call(w,'GET',f'/{parent}/{w["b"][parent].id}/{child}','CONSULTA').status_code==403


@pytest.mark.parametrize('resource',['veiculos','motoristas','viagens','cargas','caixas'])
def test_foreign_update_is_denied_and_preserves_record(secured,resource):
    w=secured; body={'descricao':'Nao aplicar'} if resource=='veiculos' else {'telefone':'Nao aplicar'} if resource=='motoristas' else {'observacoes':'Nao aplicar'}
    before={c.name:getattr(w['b'][resource],c.name) for c in w['b'][resource].__table__.columns}
    r=call(w,'PATCH',f'/{resource}/{w["b"][resource].id}','GESTOR',body)
    assert r.status_code==403
    w['db'].refresh(w['b'][resource])
    assert {c.name:getattr(w['b'][resource],c.name) for c in w['b'][resource].__table__.columns}==before


@pytest.mark.parametrize('resource',['veiculos','motoristas'])
def test_fleet_management_requires_gestor_and_own_carrier(secured,resource):
    w=secured; payload={'empresa_id':str(w['transport'].id)}
    payload.update({'identificador':'V-NOVO'} if resource=='veiculos' else {'nome':'Motorista novo'})
    assert call(w,'POST','/'+resource,'OPERADOR',payload).status_code==403
    assert call(w,'POST','/'+resource,'CONSULTA',payload).status_code==403
    assert call(w,'POST','/'+resource,'GESTOR',payload|{'empresa_id':str(w['outsider'].id)}).status_code==403
    r=call(w,'POST','/'+resource,'GESTOR',payload); assert r.status_code==201,r.text
    update={'descricao':'Atualizacao'} if resource=='veiculos' else {'telefone':'Contato operacional'}
    assert call(w,'PATCH',f'/{resource}/{r.json()["id"]}','OPERADOR',update).status_code==403
    assert call(w,'PATCH',f'/{resource}/{r.json()["id"]}','GESTOR',update).status_code==200


def trip_body(w):
    return dict(transportadora_id=str(w['transport'].id),veiculo_id=str(w['a']['veiculos'].id),
        motorista_id=str(w['a']['motoristas'].id),origem='Origem teste',destino='Destino teste',saida_em=BASE.isoformat())


def test_trip_creation_does_not_trust_client_company_or_foreign_fleet(secured):
    w=secured; p=trip_body(w)
    assert call(w,'POST','/viagens','OPERADOR',p|{'transportadora_id':str(w['outsider'].id)}).status_code==403
    for field,resource in [('veiculo_id','veiculos'),('motorista_id','motoristas')]:
        assert call(w,'POST','/viagens','OPERADOR',p|{field:str(w['b'][resource].id)}).status_code==403
    response=call(w,'POST','/viagens','OPERADOR',p); assert response.status_code==201,response.text
    tid=response.json()['id']
    assert call(w,'PATCH','/viagens/'+tid,'OPERADOR',{'veiculo_id':str(w['b']['veiculos'].id)}).status_code==403
    assert call(w,'PATCH','/viagens/'+tid,'OPERADOR',{'observacoes':'Operacao propria'}).status_code==200
    assert call(w,'POST','/viagens','CONSULTA',p).status_code==403


def test_cargo_and_box_writes_follow_parent_not_request_payload(secured):
    w=secured; body=dict(produto_id=str(w['product'].id),produtor_id=str(w['producer'].id),identificacao='CARGA-NOVA')
    assert call(w,'POST',f'/viagens/{w["b"]["viagens"].id}/cargas','OPERADOR',body).status_code==403
    assert call(w,'POST',f'/viagens/{w["trip"].id}/cargas','CONSULTA',body).status_code==403
    r=call(w,'POST',f'/viagens/{w["trip"].id}/cargas','OPERADOR',body); assert r.status_code==201,r.text
    assert r.json()['viagem_id']==str(w['trip'].id)
    assert call(w,'POST',f'/cargas/{w["b"]["cargas"].id}/caixas','OPERADOR',{'identificacao':'Nao criar'}).status_code==403
    box=call(w,'POST','/cargas/'+r.json()['id']+'/caixas','OPERADOR',{'identificacao':'Caixa nova'})
    assert box.status_code==201,box.text
    assert call(w,'PATCH','/caixas/'+box.json()['id'],'CONSULTA',{'observacoes':'Nao aplicar'}).status_code==403
    assert call(w,'PATCH','/caixas/'+box.json()['id'],'OPERADOR',{'observacoes':'Vinculo preservado'}).status_code==200
    assert call(w,'PATCH',f'/cargas/{w["cargo"].id}','OPERADOR',{'viagem_id':str(w['b']['viagens'].id)}).status_code==422


@pytest.mark.parametrize('role',['GESTOR','OPERADOR','CONSULTA'])
def test_global_product_catalog_is_read_only_for_non_admin(secured,role):
    w=secured; product=call(w,'POST','/produtos','ADMIN',{'nome':'Catalogo compartilhado'})
    assert product.status_code==201,product.text
    pid=product.json()['id']
    assert call(w,'GET','/produtos',role).status_code==200
    assert call(w,'GET','/produtos/'+pid,role).status_code==200
    assert call(w,'POST','/produtos',role,{'nome':'Nao criar'}).status_code==403
    assert call(w,'PATCH','/produtos/'+pid,role,{'nome':'Nao aplicar'}).status_code==403
    parameter=call(w,'POST','/produtos/'+pid+'/parametros','ADMIN',{'nome_parametro':'Referencia operacional','unidade':'C'})
    assert parameter.status_code==201,parameter.text
    assert call(w,'GET','/produtos/'+pid+'/parametros',role).status_code==200
    assert call(w,'POST','/produtos/'+pid+'/parametros',role,{'nome_parametro':'Nao criar'}).status_code==403
    assert call(w,'PATCH',f'/produtos/{pid}/parametros/{parameter.json()["id"]}',role,{'observacao':'Nao alterar'}).status_code==403


def test_inactive_membership_company_and_multiple_carrier_links(secured):
    w=secured; user=w['users']['OPERADOR']
    link=EmpresaUsuario(empresa_id=w['outsider'].id,usuario_id=user.id,ativo=True); w['db'].add(link); w['db'].commit()
    assert len(call(w,'GET','/viagens').json())==2
    assert call(w,'GET',f'/cargas/{w["b"]["cargas"].id}').status_code==200
    link.ativo=False; w['db'].commit()
    assert len(call(w,'GET','/viagens').json())==1
    assert call(w,'GET',f'/cargas/{w["b"]["cargas"].id}').status_code==403
    w['transport'].ativo=False; w['db'].commit()
    assert call(w,'GET','/viagens').json()==[]
    assert call(w,'GET',f'/viagens/{w["trip"].id}').status_code==403
    assert call(w,'GET',f'/viagens/{w["trip"].id}','ADMIN').status_code==200
    assert call(w,'PATCH',f'/viagens/{w["trip"].id}','ADMIN',{'observacoes':'Nao escrever'}).status_code==409


def test_unknown_profile_inactive_user_and_missing_profile_are_denied(secured):
    w=secured
    for path in ['/produtos','/viagens',f'/cargas/{w["cargo"].id}']:
        assert call(w,'GET',path,'OUTRO').status_code==403
    w['users']['OPERADOR'].perfil_id=None; w['db'].commit()
    assert call(w,'GET','/viagens').status_code==403
    w['users']['CONSULTA'].ativo=False; w['db'].commit()
    assert call(w,'GET','/produtos','CONSULTA').status_code==401


def test_secured_logistics_preserves_monitoring_snapshot_and_scope(secured):
    w=secured; session=opened(w); sid=session['id']
    assert call(w,'PATCH',f'/cargas/{w["cargo"].id}','OPERADOR',{'observacoes':'Atualizacao autorizada'}).status_code==200
    read=w['client'].get('/api/v1/monitoramentos/'+sid,headers=headers(w)).json()
    assert read['massa_kg']==session['massa_kg'] and read['configuracao_versao']==session['configuracao_versao']
    assert read['carga_id']==str(w['cargo'].id) and read['viagem_id']==str(w['trip'].id)
    w['db'].add(EmpresaUsuario(empresa_id=w['outsider'].id,usuario_id=w['users']['OUTRO'].id,ativo=True))
    w['users']['OUTRO'].perfil_id=w['users']['OPERADOR'].perfil_id
    own_link=w['db'].scalar(select(EmpresaUsuario).where(EmpresaUsuario.usuario_id==w['users']['OUTRO'].id,EmpresaUsuario.empresa_id==w['transport'].id))
    own_link.ativo=False; w['db'].commit()
    assert call(w,'GET',f'/cargas/{w["cargo"].id}','OUTRO').status_code==403
    assert w['client'].get('/api/v1/monitoramentos/'+sid,headers=headers(w,'OUTRO')).status_code==403


def test_openapi_documents_bearer_for_every_logistics_and_product_operation(secured):
    schema=secured['application'].openapi()
    for method,path in protected_operations(secured):
        operation=schema['paths'][path][method]
        assert operation['security']==[{'HTTPBearer':[]}]
        assert all(str(status) in operation['responses'] for status in (401,403,404))
