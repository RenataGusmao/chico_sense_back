"""The new migration is exercised only on disposable in-memory SQLite or offline SQL."""
import importlib.util
import io
from pathlib import Path
from uuid import uuid4

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
import pytest
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from app.models.sessoes_monitoramento import CargaMonitoramento, EventoMonitoramento, SessaoMonitoramento

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'alembic/versions/20261028_0006_sessoes_monitoramento.py'
spec=importlib.util.spec_from_file_location('migration_monitoramento',FILE)
migration=importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)


@pytest.fixture
def migrated_database():
    engine=sa.create_engine('sqlite://')
    @sa.event.listens_for(engine,'connect')
    def enforce(connection,record):
        connection.execute('PRAGMA foreign_keys=ON')
    metadata=sa.MetaData()
    for name in ('usuarios','viagens','sensores'):
        sa.Table(name,metadata,sa.Column('id',UUID(as_uuid=True),primary_key=True))
    cargo=sa.Table('cargas',metadata,sa.Column('id',UUID(as_uuid=True),primary_key=True),
                   sa.Column('viagem_id',UUID(as_uuid=True),sa.ForeignKey('viagens.id'),nullable=False))
    metadata.create_all(engine)
    with engine.begin() as connection:
        trip_id,cargo_id=uuid4(),uuid4()
        connection.execute(metadata.tables['viagens'].insert().values(id=trip_id))
        connection.execute(cargo.insert().values(id=cargo_id,viagem_id=trip_id))
        context=MigrationContext.configure(connection)
        with Operations.context(context):
            migration.upgrade()
        yield connection,cargo,trip_id,cargo_id
    engine.dispose()


def test_revision_has_single_expected_parent_and_head():
    config=Config(str(ROOT/'alembic.ini'))
    config.set_main_option('script_location',str(ROOT/'alembic'))
    script=ScriptDirectory.from_config(config)
    assert len(script.get_heads()) == 1
    assert script.get_revision('20261028_0006_monitoramento').down_revision == '20261007_0005_logistica'
    assert '20261028_0006_monitoramento' in {rev.revision for rev in script.walk_revisions()}


def test_sqlite_upgrade_preserves_legacy_rows_without_backfill(migrated_database):
    connection,cargo,trip_id,cargo_id=migrated_database
    assert connection.execute(sa.select(cargo.c.id)).scalar_one() == cargo_id
    assert connection.execute(sa.text('SELECT COUNT(*) FROM cargas_monitoramento')).scalar_one() == 0
    assert connection.execute(sa.text('SELECT COUNT(*) FROM sessoes_monitoramento')).scalar_one() == 0
    assert set(sa.inspect(connection).get_table_names()) == {
        'usuarios','viagens','sensores','cargas','cargas_monitoramento','sessoes_monitoramento','eventos_monitoramento',
    }


@pytest.mark.parametrize('model',[CargaMonitoramento,SessaoMonitoramento,EventoMonitoramento])
def test_migration_columns_checks_and_indexes_match_models(migrated_database,model):
    connection,*_=migrated_database
    inspector=sa.inspect(connection)
    columns={col['name']:col for col in inspector.get_columns(model.__tablename__)}
    assert set(columns) == set(model.__table__.columns.keys())
    for column in model.__table__.columns:
        assert columns[column.name]['nullable'] == column.nullable
    actual_checks={c['name'] for c in inspector.get_check_constraints(model.__tablename__)}
    expected_checks={c.name for c in model.__table__.constraints if isinstance(c,sa.CheckConstraint)}
    assert actual_checks == expected_checks
    assert {i['name'] for i in inspector.get_indexes(model.__tablename__)} == {i.name for i in model.__table__.indexes}
    expected_unique={c.name for c in model.__table__.constraints if isinstance(c,sa.UniqueConstraint)}
    assert {c['name'] for c in inspector.get_unique_constraints(model.__tablename__)} == expected_unique


def test_local_downgrade_preserves_existing_cargo(migrated_database):
    connection,cargo,_,cargo_id=migrated_database
    with Operations.context(MigrationContext.configure(connection)):
        migration.downgrade()
    assert connection.execute(sa.select(cargo.c.id)).scalar_one() == cargo_id
    assert 'sessoes_monitoramento' not in sa.inspect(connection).get_table_names()
    assert 'uq_cargas_id_viagem_monitoramento' not in {i['name'] for i in sa.inspect(connection).get_indexes('cargas')}


def test_postgresql_ddl_compiles_offline_without_loading_database_settings():
    output=io.StringIO()
    context=MigrationContext.configure(dialect_name='postgresql',opts={'as_sql':True,'output_buffer':output})
    with Operations.context(context):
        migration.upgrade()
    sql=output.getvalue()
    assert 'CREATE TABLE sessoes_monitoramento' in sql
    assert 'JSONB' in sql
    assert "WHERE estado = 'ATIVA'" in sql
    assert 'FOREIGN KEY(carga_id, viagem_id) REFERENCES cargas (id, viagem_id)' in sql
    assert 'UPDATE cargas ' not in sql
