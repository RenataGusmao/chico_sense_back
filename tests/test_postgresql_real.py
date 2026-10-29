"""Prepared opt-in PostgreSQL acceptance tests.

Skipped without all three safety opt-ins. Collection/skip is not PostgreSQL validation.
"""
from decimal import Decimal
from uuid import UUID,uuid4
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from tests.pg_support import HEAD,isolated_database,pg_world,attach_iot,race
from tests.test_monitoramento_sessoes import config,start,start_body,opened,finish,stamp,headers
from tests.test_historico_iot import sync,feed
from tests.test_analises_etileno import body as analysis_body,execute as estimate
from tests.test_preventivo import configure,evaluate,eval_body,decide
from tests.test_exaustao_simulada import requested,act
from app.core.database import Base
from app.models.sessoes_monitoramento import SessaoMonitoramento,EventoMonitoramento
from app.models.historico_iot import RegistroSessaoIoT,SincronizacaoIoT
from app.models.integracoes import LeituraExterna
from app.models.iot import Medicao
from app.models.analises_etileno import AnaliseEtileno
from app.models.preventivo import AvaliacaoPreventiva,AlertaSessao,DecisaoAlerta
from app.models.monitoramento import Alerta
from app.models.exaustao_simulada import IntervencaoSimulada,AcaoIntervencao


@pytest.fixture(scope='module')
def pg_database():
    with isolated_database() as db:
        yield db


@pytest.fixture
def pg(pg_database,monkeypatch):
    yield from pg_world(pg_database,monkeypatch)


@pytest.fixture
def acquired(pg):
    attach_iot(pg)
    response=sync(pg)
    assert response.status_code==200,response.text
    assert response.json()['estado']=='CONCLUIDA'
    return pg


def total(w,model,condition=None):
    # Never assert through the seed identity map or a transaction from a worker.
    with Session(w['engine']) as db:
        q=sa.select(sa.func.count()).select_from(model)
        if condition is not None: q=q.where(condition)
        return db.scalar(q)


def ok(response,status=200):
    assert response.status_code==status,response.text
    return response.json()


def test_pg_01_complete_migration_downgrade_upgrade(pg_database):
    d=pg_database
    assert d.connection.scalar(sa.text('SELECT version_num FROM alembic_version'))==HEAD
    d.connection.commit()
    assert set(sa.inspect(d.connection).get_table_names())==set(Base.metadata.tables)|{'alembic_version'}
    d.connection.commit()
    d.migrate('downgrade','base')
    assert set(sa.inspect(d.connection).get_table_names())=={'alembic_version'}
    assert d.connection.scalar(sa.text("SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE t.typtype='e' AND n.nspname='public'"))==0
    d.connection.commit()
    d.migrate('upgrade',HEAD)
    assert d.connection.scalar(sa.text('SELECT version_num FROM alembic_version'))==HEAD
    d.connection.commit()


def index_expression_signature(connection,table,expression):
    """Let PostgreSQL parse/deparse equivalent SQL syntax without executing it."""
    name=connection.dialect.identifier_preparer.quote(table.name)
    plan=connection.execute(sa.text(
        f'EXPLAIN (VERBOSE, FORMAT JSON, COSTS OFF) SELECT {expression} FROM public.{name}'
    )).scalar_one()
    return plan[0]['Plan']['Output']


def test_pg_02_catalog_columns_foreign_keys_checks_indexes_types(pg_database):
    d=pg_database; d.verify()
    inspector=sa.inspect(d.connection)
    for table in Base.metadata.sorted_tables:
        columns={c['name']:c for c in inspector.get_columns(table.name)}
        assert set(columns)==set(table.c.keys()),table.name
        for column in table.c:
            actual=columns[column.name]
            assert actual['nullable']==column.nullable,(table.name,column.name)
            assert str(actual['type'].compile(dialect=d.engine.dialect))==str(column.type.compile(dialect=d.engine.dialect)),(table.name,column.name)
        actual_fks={(tuple(f['constrained_columns']),f['referred_table'],tuple(f['referred_columns'])) for f in inspector.get_foreign_keys(table.name)}
        expected_fks={(tuple(f.column_keys),next(iter(f.elements)).column.table.name,tuple(e.column.name for e in f.elements)) for f in table.foreign_key_constraints}
        assert actual_fks==expected_fks,table.name
        # New monitoring constraints are explicitly named. Legacy implicit names
        # are server-generated and are compared by structure instead.
        expected_checks={c.name for c in table.constraints if isinstance(c,sa.CheckConstraint)}
        assert expected_checks <= {c['name'] for c in inspector.get_check_constraints(table.name)},table.name
        actual_unique={tuple(c['column_names']) for c in inspector.get_unique_constraints(table.name)}
        assert {tuple(c.columns.keys()) for c in table.constraints if isinstance(c,sa.UniqueConstraint)}<=actual_unique,table.name
        actual_indexes={i['name']:i for i in inspector.get_indexes(table.name)}
        for index in table.indexes:
            actual=actual_indexes[index.name]
            assert actual['unique']==index.unique
            if all(isinstance(expression,sa.Column) for expression in index.expressions):
                assert actual['column_names']==[c.name for c in index.expressions]
            else:
                # Reflection uses None for functional keys; never skip their expressions.
                expressions=actual.get('expressions')
                assert expressions and len(expressions)==len(index.expressions),index.name
                for expected_expression,reflected_expression in zip(index.expressions,expressions):
                    expected_sql=str(expected_expression.compile(dialect=d.engine.dialect,
                        compile_kwargs={'literal_binds':True,'include_table':False}))
                    assert index_expression_signature(d.connection,table,expected_sql)==index_expression_signature(d.connection,table,reflected_expression),index.name
            expected=index.dialect_options['postgresql'].get('where')
            if expected is not None:
                predicate=actual['dialect_options'].get('postgresql_where','')
                assert predicate
                assert index_expression_signature(d.connection,table,str(expected))==index_expression_signature(d.connection,table,predicate),index.name
    # Inspect raw autogenerate too: Alembic 1.13 compares trim syntax textually.
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext
    context=MigrationContext.configure(d.connection,opts={
        'include_object':lambda obj,name,kind,reflected,compare_to: name=='usuarios' if kind=='table' else True})
    differences=compare_metadata(context,Base.metadata)
    if differences:
        # Permit only a proven equivalent functional-index rebuild, not arbitrary
        # expression/name/uniqueness changes or unrelated DDL proposals.
        assert [change[0] for change in differences]==['remove_index','add_index']
        reflected,declared=[change[1] for change in differences]
        assert reflected.name==declared.name=='uq_usuarios_email_normalizado'
        assert reflected.table.name==declared.table.name=='usuarios'
        assert reflected.unique is True and declared.unique is True
        assert len(reflected.expressions)==len(declared.expressions)==1
        expressions=[str(index.expressions[0].compile(dialect=d.engine.dialect,
            compile_kwargs={'literal_binds':True,'include_table':False})) for index in (reflected,declared)]
        assert index_expression_signature(d.connection,declared.table,expressions[0])==index_expression_signature(d.connection,declared.table,expressions[1])
        assert index_expression_signature(d.connection,declared.table,expressions[0])!=index_expression_signature(d.connection,declared.table,'lower(email)')
    d.connection.commit()


def test_pg_03_real_check_fk_and_transaction_rollback(pg):
    from app.models.usuario import Perfil
    from app.models.logistica import Carga
    original=total(pg,Perfil)
    with Session(pg['engine']) as db:
        db.add(Perfil(nome='ROLLBACK_ONLY'));db.flush()
        with pytest.raises(IntegrityError):
            with db.begin_nested():
                db.execute(sa.update(Carga).where(Carga.id==pg['cargo'].id).values(viagem_id=uuid4()))
        db.rollback()
    assert total(pg,Perfil)==original
    sid=opened(pg)['id']
    with Session(pg['engine']) as db:
        with pytest.raises(IntegrityError):
            db.execute(sa.update(SessaoMonitoramento).where(SessaoMonitoramento.id==UUID(sid)).values(massa_kg=0))
        db.rollback()
    with Session(pg['engine']) as db:
        assert db.get(SessaoMonitoramento,UUID(sid)).massa_kg==Decimal('1000.0000')


def test_pg_04_conflicting_session_creation(pg):
    ok(config(pg))
    responses=race(pg,lambda:start(pg,start_body(pg)),lambda:start(pg,start_body(pg)))
    assert sorted(r.status_code for r in responses)==[201,409]
    assert total(pg,SessaoMonitoramento)==1
    assert total(pg,SessaoMonitoramento,SessaoMonitoramento.estado=='ATIVA')==1
    assert total(pg,EventoMonitoramento)==2


def test_pg_05_simultaneous_same_session_end(pg):
    sid=opened(pg)['id']
    before=total(pg,EventoMonitoramento)
    responses=race(pg,lambda:finish(pg,sid),lambda:finish(pg,sid))
    assert [r.status_code for r in responses]==[200,200]
    with Session(pg['engine']) as db:
        s=db.get(SessaoMonitoramento,UUID(sid))
        assert s.estado=='ENCERRADA' and s.fim is not None
    assert total(pg,EventoMonitoramento)==before+1


def test_pg_06_simultaneous_acquisition_same_key(pg):
    attach_iot(pg); payload={'chave_idempotencia':str(uuid4())}
    responses=race(pg,lambda:sync(pg,payload),lambda:sync(pg,payload))
    assert all(r.status_code in (200,202) for r in responses)
    assert len({r.json()['id'] for r in responses})==1
    assert total(pg,SincronizacaoIoT)==1
    assert total(pg,SincronizacaoIoT,SincronizacaoIoT.estado=='CONCLUIDA')==1
    assert total(pg,RegistroSessaoIoT)==total(pg,LeituraExterna)==total(pg,Medicao)==6


def test_pg_07_deduplication_across_transactions(acquired):
    w=acquired
    responses=race(w,lambda:sync(w),lambda:sync(w))
    assert all(r.status_code in (200,409) for r in responses)
    assert any(r.status_code==200 for r in responses)
    assert total(w,RegistroSessaoIoT)==total(w,LeituraExterna)==total(w,Medicao)==6
    with Session(w['engine']) as db:
        runs=db.scalars(sa.select(SincronizacaoIoT).order_by(SincronizacaoIoT.revisao)).all()
        assert [r.revisao for r in runs]==list(range(1,len(runs)+1))
        assert all(r.estado=='CONCLUIDA' for r in runs)


def test_pg_08_analysis_simultaneous_idempotency_and_snapshot(acquired):
    w=acquired;payload=analysis_body()
    responses=race(w,lambda:estimate(w,payload),lambda:estimate(w,payload))
    a,b=[ok(r) for r in responses]
    assert a==b
    assert total(w,AnaliseEtileno)==1
    assert Decimal(a['resultado']['volume_janela_min_ul'])==700
    assert Decimal(a['resultado']['volume_janela_max_ul'])==9000
    with Session(w['engine']) as db:
        row=db.get(AnaliseEtileno,UUID(a['id']))
        assert row.entrada_snapshot==a['entrada_snapshot'] and row.resultado==a['resultado']
        assert row.hash_entrada==a['hash_entrada'] and row.hash_resultado==a['hash_resultado']
    assert total(w,EventoMonitoramento,EventoMonitoramento.tipo=='ANALISE_ETILENO')==1


def test_pg_09_late_concurrent_complement_and_old_snapshot(acquired):
    w=acquired
    old=ok(estimate(w));ok(finish(w,w['session']['id'],fim=stamp(130)))
    with Session(w['engine']) as db:
        before={r.id:(r.valor,r.medida_em,r.sincronizacao_id) for r in db.scalars(sa.select(RegistroSessaoIoT))}
    w['payload']['feeds'].append(feed(4,100,'15','92'))
    payload=dict(chave_idempotencia=str(uuid4()),complementar_encerrada=True,justificativa='Complemento hipotetico aprovado para teste.')
    responses=race(w,lambda:sync(w,payload,role='GESTOR'),lambda:sync(w,payload,role='GESTOR'))
    assert all(r.status_code in (200,202) for r in responses)
    assert total(w,SincronizacaoIoT)==2
    assert total(w,RegistroSessaoIoT)==8
    with Session(w['engine']) as db:
        assert {r.id:(r.valor,r.medida_em,r.sincronizacao_id) for r in db.scalars(sa.select(RegistroSessaoIoT)) if r.id in before}==before
        row=db.get(AnaliseEtileno,UUID(old['id']))
        assert row.entrada_snapshot==old['entrada_snapshot'] and row.hash_resultado==old['hash_resultado']


def test_pg_10_equivalent_alerts_and_concurrent_decisions(acquired):
    w=acquired;ok(configure(w)); payload=eval_body()
    responses=race(w,lambda:evaluate(w,payload),lambda:evaluate(w,eval_body(corte_aquisicao=payload['corte_aquisicao'])))
    a,b=[ok(r) for r in responses]
    assert set(a['alertas_ids'])==set(b['alertas_ids']) and a['alertas_ids']
    assert total(w,AvaliacaoPreventiva)==2
    assert total(w,AlertaSessao)==len(a['alertas_ids'])
    aid=a['alertas_ids'][0]
    with Session(w['engine']) as db:
        initial=db.scalars(sa.select(DecisaoAlerta).where(DecisaoAlerta.alerta_id==UUID(aid))).all()
        initial_ids={row.id for row in initial}
        assert len(initial)==1 and initial[0].acao=='CRIAR'
    responses=race(w,lambda:decide(w,aid,'RECONHECER',role='GESTOR'),lambda:decide(w,aid,'RESOLVER',role='GESTOR'))
    assert all(r.status_code in (200,409) for r in responses)
    assert any(r.status_code==200 for r in responses)
    with Session(w['engine']) as db:
        assert db.get(Alerta,UUID(aid)).status.value=='RESOLVIDO'
        decisions=db.scalars(sa.select(DecisaoAlerta).where(DecisaoAlerta.alerta_id==UUID(aid))).all()
        assert len(decisions)==len(initial_ids)+sum(r.status_code==200 for r in responses)
        assert initial_ids <= {row.id for row in decisions}
        assert sum(row.acao=='CRIAR' for row in decisions)==1
        assert len({row.chave_idempotencia for row in decisions})==len(decisions)
        assert len({row.ocorrencia_id for row in decisions})==len(decisions)
        assert sum(row.acao=='RESOLVER' for row in decisions)==1
        assert sum(row.acao=='RECONHECER' for row in decisions)==sum(r.status_code==200 for r in responses[:1])


def second_session(w):
    from tests.test_monitoramento_sessoes import BASE
    from app.models.logistica import Viagem,Carga
    from app.models.iot import Dispositivo,Sensor
    from app.models.enums import StatusViagem,StatusCarga,StatusDispositivo,StatusSensor,TipoSensor,ContextoMedicao
    db=w['db']; vehicle=w['trip'].veiculo_id; driver=w['trip'].motorista_id
    trip=Viagem(transportadora_id=w['transport'].id,veiculo_id=vehicle,motorista_id=driver,origem='Fixture',destino='Fixture',saida_em=BASE,inicio_real=BASE,status=StatusViagem.EM_ANDAMENTO)
    db.add(trip);db.flush()
    cargo=Carga(viagem_id=trip.id,produto_id=w['product'].id,produtor_id=w['producer'].id,identificacao='PG-CARGA-2',status=StatusCarga.EM_TRANSITO)
    device=Dispositivo(identificador='PG-ESP-2',viagem_id=trip.id,veiculo_id=vehicle,status=StatusDispositivo.ATIVO)
    db.add_all([cargo,device]);db.flush()
    temp=Sensor(dispositivo_id=device.id,identificador='PG-TEMP-2',tipo=TipoSensor.TEMPERATURA,contexto=ContextoMedicao.AMBIENTE,unidade='C',status=StatusSensor.ATIVO)
    hum=Sensor(dispositivo_id=device.id,identificador='PG-HUM-2',tipo=TipoSensor.UMIDADE,contexto=ContextoMedicao.AMBIENTE,unidade='%',status=StatusSensor.ATIVO)
    db.add_all([temp,hum]);db.commit();db.expunge_all()
    other=w|dict(trip=trip,cargo=cargo,device=device,temp=temp,hum=hum)
    other['session']=opened(other)
    return other


def authorized(w):
    identifier=requested(w)['id'];ok(act(w,identifier,'AUTORIZAR'))
    return identifier


def test_pg_11_two_sessions_start_same_vehicle(pg):
    w=pg;w['session']=opened(w);other=second_session(w)
    a,b=authorized(w),authorized(other)
    responses=race(w,lambda:act(w,a,'INICIAR'),lambda:act(other,b,'INICIAR'))
    assert sorted(r.status_code for r in responses)==[200,409]
    assert total(w,IntervencaoSimulada,IntervencaoSimulada.estado=='EM_EXECUCAO')==1
    assert total(w,AcaoIntervencao)==5


def test_pg_12_stop_while_another_session_starts(pg):
    w=pg;w['session']=opened(w);other=second_session(w)
    a,b=authorized(w),authorized(other);ok(act(w,a,'INICIAR'))
    responses=race(w,lambda:act(w,a,'ENCERRAR'),lambda:act(other,b,'INICIAR'))
    assert responses[0].status_code==200
    assert responses[1].status_code in (200,409)
    with Session(w['engine']) as db:
        assert db.get(IntervencaoSimulada,UUID(a)).estado=='CONCLUIDA'
        expected='EM_EXECUCAO' if responses[1].status_code==200 else 'AUTORIZADA'
        assert db.get(IntervencaoSimulada,UUID(b)).estado==expected
    if responses[1].status_code==409: ok(act(other,b,'INICIAR'))
    assert total(w,IntervencaoSimulada,IntervencaoSimulada.estado=='EM_EXECUCAO')==1
    assert total(w,AcaoIntervencao)==7
