"""The historical IoT migration is applied only to disposable in-memory databases."""
import importlib.util
import io
from pathlib import Path
from uuid import uuid4
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.config import Config
from alembic.script import ScriptDirectory
import pytest
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from app.models.historico_iot import FonteSessaoIoT,SincronizacaoIoT,RegistroSessaoIoT,OcorrenciaIoT
from tests.test_monitoramento_migration import migrated_database

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'alembic/versions/20261028_0007_historico_iot.py'
spec=importlib.util.spec_from_file_location('migration_historico_iot',FILE)
migration=importlib.util.module_from_spec(spec); spec.loader.exec_module(migration)


@pytest.fixture
def iot_migrated(migrated_database):
    connection,cargo,trip_id,cargo_id=migrated_database
    sa.Table('medicoes',sa.MetaData(),sa.Column('id',UUID(as_uuid=True),primary_key=True)).create(connection)
    with Operations.context(MigrationContext.configure(connection)):
        migration.upgrade()
    return connection,cargo,cargo_id


def test_current_head_and_complete_revision_chain():
    cfg=Config(str(ROOT/'alembic.ini')); cfg.set_main_option('script_location',str(ROOT/'alembic'))
    script=ScriptDirectory.from_config(cfg)
    assert len(script.get_heads())==1
    assert script.get_revision('20261028_0007_historico_iot').down_revision=='20261028_0006_monitoramento'
    assert script.get_revision('20261028_0006_monitoramento').down_revision=='20261007_0005_logistica'


def test_no_backfill_or_rewrite_of_legacy_cargo_or_sessions(iot_migrated):
    connection,cargo,cargo_id=iot_migrated
    assert connection.execute(sa.select(cargo.c.id)).scalar_one()==cargo_id
    for name in ('fontes_sessao_iot','sincronizacoes_iot','registros_sessao_iot','ocorrencias_iot'):
        assert connection.execute(sa.text('SELECT COUNT(*) FROM '+name)).scalar_one()==0


@pytest.mark.parametrize('model',[FonteSessaoIoT,SincronizacaoIoT,RegistroSessaoIoT,OcorrenciaIoT])
def test_new_tables_match_models(iot_migrated,model):
    connection,*_=iot_migrated; inspector=sa.inspect(connection); table=model.__table__
    columns={c['name']:c for c in inspector.get_columns(table.name)}
    assert set(columns)==set(table.columns.keys())
    assert all(columns[c.name]['nullable']==c.nullable for c in table.columns)
    assert {c['name'] for c in inspector.get_check_constraints(table.name)}=={c.name for c in table.constraints if isinstance(c,sa.CheckConstraint)}
    assert {i['name'] for i in inspector.get_indexes(table.name)}=={i.name for i in table.indexes}
    assert {c['name'] for c in inspector.get_unique_constraints(table.name)}=={c.name for c in table.constraints if isinstance(c,sa.UniqueConstraint)}
    assert len(inspector.get_foreign_keys(table.name))==len([c for c in table.constraints if isinstance(c,sa.ForeignKeyConstraint)])


def test_downgrade_keeps_previous_tables_and_rows(iot_migrated):
    connection,cargo,cargo_id=iot_migrated
    with Operations.context(MigrationContext.configure(connection)):
        migration.downgrade()
    assert connection.execute(sa.select(cargo.c.id)).scalar_one()==cargo_id
    assert 'sessoes_monitoramento' in sa.inspect(connection).get_table_names()
    assert 'medicoes' in sa.inspect(connection).get_table_names()
    assert 'registros_sessao_iot' not in sa.inspect(connection).get_table_names()


def test_postgresql_offline_ddl_has_expected_constraints_and_no_destructive_updates():
    output=io.StringIO()
    with Operations.context(MigrationContext.configure(dialect_name='postgresql',opts={'as_sql':True,'output_buffer':output})):
        migration.upgrade()
    sql=output.getvalue()
    assert 'JSONB' in sql and "WHERE estado = 'EM_EXECUCAO'" in sql
    assert 'FOREIGN KEY(fonte_id, sessao_id)' in sql
    assert 'FOREIGN KEY(sincronizacao_id, sessao_id)' in sql
    assert 'UPDATE medicoes' not in sql and 'ALTER TABLE sessoes_monitoramento' not in sql
