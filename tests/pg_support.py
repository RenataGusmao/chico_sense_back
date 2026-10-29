"""Opt-in real PostgreSQL support. Never uses DATABASE_URL or the app engine."""
import os
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session
from alembic import command
from alembic.config import Config
from scripts.pg_test_safety import validate_target, open_verified, verify_connection, UnsafeTestDatabase

ROOT=Path(__file__).resolve().parents[1]
HEAD='20261028_0010_exaustao_virtual'


class Database:
    def __init__(self,target,engine,connection):
        self.target,self.engine,self.connection=target,engine,connection
        self.identity=None

    def verify(self):
        self.identity=verify_connection(self.connection,self.target)
        self.connection.commit()

    def migrate(self,direction,revision):
        self.verify()
        cfg=Config(str(ROOT/'alembic.ini'))
        cfg.set_main_option('script_location',str(ROOT/'alembic'))
        cfg.attributes['connection']=self.connection
        from app.core.config import settings
        with patch.object(settings,'database_url',self.target.url.render_as_string(hide_password=False)), patch('logging.config.fileConfig'):
            getattr(command,direction)(cfg,revision)
        self.connection.commit()

    def clear_fixtures(self):
        self.verify()
        from app.core.database import Base
        tables=set(sa.inspect(self.connection).get_table_names(schema='public'))
        expected=set(Base.metadata.tables)|{'alembic_version'}
        if tables != expected:
            raise UnsafeTestDatabase('Unexpected table inventory: refusing TRUNCATE.')
        # No CASCADE: a dependency outside the authorized tables makes this fail closed.
        names=', '.join('public.'+self.engine.dialect.identifier_preparer.quote(n) for n in sorted(Base.metadata.tables))
        self.connection.execute(sa.text('TRUNCATE TABLE '+names))
        self.connection.commit()


@contextmanager
def isolated_database():
    target=validate_target(os.environ)
    if target is None:
        pytest.skip('PostgreSQL real pendente: URL, token descartavel e identidade do servidor ausentes.')
    engine,connection=open_verified(target)
    try:
        # Session lock prevents another invocation from clearing this same database.
        locked=connection.scalar(sa.text('SELECT pg_try_advisory_lock(721844166032)'))
        connection.commit()
        if not locked:
            raise UnsafeTestDatabase('Disposable database is in use by another test run.')
        if connection.scalar(sa.text("SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public'")) or connection.scalar(sa.text("SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public'")) or connection.scalar(sa.text("SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='public'")):
            raise UnsafeTestDatabase('An empty public schema is required; existing data is never erased at startup.')
        # Reject any non-default schema or extension before all migration/cleanup DDL.
        extra=connection.scalars(sa.text("SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname NOT IN ('public','information_schema')")).all()
        extensions=connection.scalars(sa.text("SELECT extname FROM pg_extension WHERE extname <> 'plpgsql'")).all()
        if extra or extensions:
            raise UnsafeTestDatabase('Unexpected schema/extension: isolation unproven.')
        connection.commit()
        db=Database(target,engine,connection)
        db.migrate('upgrade',HEAD)
        yield db
        # Keep database and its identity marker for inspection. No DROP DATABASE.
    finally:
        connection.close()
        engine.dispose()


def race(w,*operations):
    """Hold two actual connections before start; each HTTP request gets one Session."""
    barrier=Barrier(len(operations),timeout=10)
    def worker(operation):
        with w['engine'].connect() as connection:
            pid=connection.scalar(sa.text('SELECT pg_backend_pid()'))
            connection.commit()
            w['local'].connection=connection
            w['local'].pid=pid
            try:
                barrier.wait()
                return pid,operation()
            finally:
                del w['local'].connection
                del w['local'].pid
    with ThreadPoolExecutor(max_workers=len(operations)) as pool:
        futures=[pool.submit(worker,op) for op in operations]
        results=[f.result(timeout=45) for f in futures]
    assert len({pid for pid,_ in results})==len(operations), 'Not independent PostgreSQL backends'
    w['db'].rollback()
    return [r for _,r in results]


def pg_world(database,monkeypatch):
    """The existing business fixtures seed data; requests never share their Session."""
    from fastapi.testclient import TestClient
    from threading import local
    from app.api.deps import get_database_session
    from app.core.config import settings
    from app.core.database import SessionLocal
    from app.main import create_app
    # Static seed code below uses the same hypothetical domain values as SQLite tests.
    from app.models.empresa import Empresa
    from app.models.enums import TipoEmpresa,StatusViagem,StatusCarga,StatusDispositivo,StatusSensor,TipoSensor,ContextoMedicao
    from app.models.usuario import Perfil,Usuario,EmpresaUsuario
    from app.models.produto import Produto
    from app.models.logistica import Veiculo,Motorista,Viagem,Carga
    from app.models.iot import Dispositivo,Sensor
    from tests.test_monitoramento_sessoes import BASE
    database.clear_fixtures()
    monkeypatch.setattr(settings,'secret_key','postgresql-fixture-only-signing-key-at-least-32-bytes')
    db=Session(database.engine,expire_on_commit=False)
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
    db.expunge_all()  # Read-only seed objects must not lazy-load through a shared Session.
    application=create_app()
    thread_local=local()
    # get_database_session is executed in FastAPI's worker, so request context must
    # cross thread boundaries; ContextVar is used by the race client wrapper below.
    from contextvars import ContextVar
    connection_context=ContextVar('pg_test_connection',default=None)
    from fastapi import Request
    def request_db(request:Request):
        bound=connection_context.get() or database.engine
        # Same factory/options as production; only the verified bind is replaced.
        with SessionLocal(bind=bound) as session:
            expected=request.headers.get('X-ChicoSense-Test-Backend-Pid')
            if expected is not None:
                actual=session.scalar(sa.text('SELECT pg_backend_pid()'))
                assert str(actual)==expected, 'HTTP did not use the reserved independent connection'
            yield session
    application.dependency_overrides[get_database_session]=request_db
    client=TestClient(application)
    class Client:
        def __getattr__(self,name):
            original=getattr(client,name)
            if name not in ('get','post','put','patch','delete','request'):
                return original
            def invoke(*args,**kwargs):
                token=connection_context.set(getattr(thread_local,'connection',None))
                if hasattr(thread_local,'pid'):
                    kwargs['headers']=dict(kwargs.get('headers') or {}) | {'X-ChicoSense-Test-Backend-Pid':str(thread_local.pid)}
                try: return original(*args,**kwargs)
                finally: connection_context.reset(token)
            return invoke
    w=dict(db=db,client=Client(),application=application,cargo=cargo,trip=trip,
           transport=transport,outsider=outsider,producer=producer,product=product,
           temp=temp,hum=hum,device=device,users=users,engine=database.engine,local=thread_local)
    try:
        with client: yield w
    finally:
        db.close()


def attach_iot(w):
    """Actual acquisition client and mapper, provider HTTP replaced by fake feed."""
    import httpx
    from app.modules.integracoes.thingspeak.client import ThingSpeakClient
    from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
    from app.modules.integracoes.thingspeak.schemas import ThingSpeakChannelConfig,ThingSpeakMappingConfig,ThingSpeakFieldMapping
    from app.modules.integracoes.thingspeak.service import ThingSpeakService
    from app.modules.monitoramento.historico_routes import thingspeak_service
    from tests.test_monitoramento_sessoes import opened
    from tests.test_historico_iot import feed
    w['session']=opened(w)
    w['payload']={'channel':{'id':12345},'feeds':[feed(1,10,'13','92'),feed(2,70,'20','92'),feed(3,130,'20','92')]}
    def factory():
        # New AsyncClient per request; never share event-loop-bound HTTP state.
        http=httpx.AsyncClient(base_url='https://api.thingspeak.com',transport=httpx.MockTransport(lambda request:httpx.Response(200,json=w['payload'])))
        mapping=ThingSpeakMappingConfig(fields={
            'field4':ThingSpeakFieldMapping(sensor_id=w['temp'].id,tipo='TEMPERATURA',contexto='AMBIENTE',unidade='C'),
            'field7':ThingSpeakFieldMapping(sensor_id=w['hum'].id,tipo='UMIDADE',contexto='AMBIENTE',unidade='%')})
        return http,ThingSpeakService(ThingSpeakChannelConfig(base_url='https://api.thingspeak.com',channel_id='12345',timeout_seconds=1),
                                    ThingSpeakClient('https://api.thingspeak.com',read_api_key='PG_FAKE_KEY',http_client=http),ThingSpeakFieldMapper(mapping))
    async def service():
        http,svc=factory()
        try: yield svc
        finally: await http.aclose()
    w['application'].dependency_overrides[thingspeak_service]=service
