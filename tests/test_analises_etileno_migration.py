"""Only disposable SQLite and offline PostgreSQL DDL; never remote migrations."""
import importlib.util
import io
from pathlib import Path
import pytest
import sqlalchemy as sa
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from app.models.analises_etileno import AnaliseEtileno
from tests.test_monitoramento_migration import migrated_database
from tests.test_historico_iot_migration import iot_migrated

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('migration_analises',ROOT/'alembic/versions/20261028_0008_analises_etileno.py')
migration=importlib.util.module_from_spec(spec); spec.loader.exec_module(migration)


@pytest.fixture
def migrated(iot_migrated):
    connection,*_=iot_migrated
    with Operations.context(MigrationContext.configure(connection)): migration.upgrade()
    return iot_migrated


def test_single_head_and_stable_parent_chain():
    config=Config(str(ROOT/'alembic.ini')); config.set_main_option('script_location',str(ROOT/'alembic'))
    script=ScriptDirectory.from_config(config)
    assert len(script.get_heads())==1
    assert script.get_revision('20261028_0008_analises_etileno').down_revision=='20261028_0007_historico_iot'
    assert script.get_revision('20261028_0007_historico_iot').down_revision=='20261028_0006_monitoramento'


def test_upgrade_columns_types_and_constraints_match_model(migrated):
    connection,*_=migrated; inspector=sa.inspect(connection); table=AnaliseEtileno.__table__
    columns={c['name']:c for c in inspector.get_columns(table.name)}
    assert set(columns)==set(table.columns.keys())
    assert all(columns[c.name]['nullable']==c.nullable for c in table.columns)
    assert columns['massa_kg']['type'].precision==12 and columns['massa_kg']['type'].scale==4
    assert columns['intervalo_maximo_s']['type'].scale==3
    assert {c['name'] for c in inspector.get_check_constraints(table.name)}=={c.name for c in table.constraints if isinstance(c,sa.CheckConstraint)}
    assert {c['name'] for c in inspector.get_unique_constraints(table.name)}=={c.name for c in table.constraints if isinstance(c,sa.UniqueConstraint)}
    assert {i['name'] for i in inspector.get_indexes(table.name)}=={i.name for i in table.indexes}
    assert {tuple(c['referred_columns'])+tuple(c['constrained_columns']) for c in inspector.get_foreign_keys(table.name)}=={('id','sessao_id'),('id','usuario_id')}


def test_no_backfill_and_downgrade_preserves_previous_data(migrated):
    connection,cargo,cargo_id=migrated
    assert connection.execute(sa.select(cargo.c.id)).scalar_one()==cargo_id
    assert connection.execute(sa.text('SELECT COUNT(*) FROM analises_etileno')).scalar_one()==0
    with Operations.context(MigrationContext.configure(connection)): migration.downgrade()
    names=sa.inspect(connection).get_table_names()
    assert 'analises_etileno' not in names
    assert all(n in names for n in ('sessoes_monitoramento','registros_sessao_iot','medicoes','cargas'))
    assert connection.execute(sa.select(cargo.c.id)).scalar_one()==cargo_id


def test_postgresql_offline_upgrade_and_downgrade():
    output=io.StringIO()
    with Operations.context(MigrationContext.configure(dialect_name='postgresql',opts={'as_sql':True,'output_buffer':output})):
        migration.upgrade(); migration.downgrade()
    sql=output.getvalue()
    assert 'JSONB' in sql and 'NUMERIC(12, 4)' in sql and 'NUMERIC(12, 3)' in sql
    assert 'uq_analise_sessao_chave' in sql and 'ck_analise_janela' in sql
    assert 'FOREIGN KEY(sessao_id) REFERENCES sessoes_monitoramento (id)' in sql
    assert 'DROP TABLE analises_etileno' in sql
    assert 'ALTER TABLE sessoes_monitoramento' not in sql and 'UPDATE ' not in sql
