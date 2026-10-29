"""Migration tests are disposable SQLite and offline PostgreSQL only."""
import importlib.util
import io
from pathlib import Path
import pytest
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from app.models.preventivo import ConfiguracaoAmbiental,AvaliacaoPreventiva,AlertaSessao,EvidenciaPreventiva,DecisaoAlerta
from tests.test_monitoramento_migration import migrated_database
from tests.test_historico_iot_migration import iot_migrated
from tests.test_analises_etileno_migration import migrated as analyses_migrated

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('migration_preventivo',ROOT/'alembic/versions/20261028_0009_preventivo.py')
migration=importlib.util.module_from_spec(spec); spec.loader.exec_module(migration)
MODELS=(ConfiguracaoAmbiental,AvaliacaoPreventiva,AlertaSessao,EvidenciaPreventiva,DecisaoAlerta)


@pytest.fixture
def migrated(analyses_migrated):
    connection,*_=analyses_migrated
    for name in ('alertas','ocorrencias'):
        sa.Table(name,sa.MetaData(),sa.Column('id',UUID(as_uuid=True),primary_key=True)).create(connection)
    with Operations.context(MigrationContext.configure(connection)): migration.upgrade()
    return analyses_migrated


def test_single_incremental_head():
    cfg=Config(str(ROOT/'alembic.ini')); cfg.set_main_option('script_location',str(ROOT/'alembic'))
    script=ScriptDirectory.from_config(cfg)
    assert len(script.get_heads())==1
    assert script.get_revision('20261028_0009_preventivo').down_revision=='20261028_0008_analises_etileno'


@pytest.mark.parametrize('model',MODELS)
def test_model_and_migration_constraints_agree(migrated,model):
    c,*_=migrated; i=sa.inspect(c); t=model.__table__
    cols={x['name']:x for x in i.get_columns(t.name)}
    assert set(cols)==set(t.columns.keys())
    assert all(cols[x.name]['nullable']==x.nullable for x in t.columns)
    assert {x['name'] for x in i.get_check_constraints(t.name)}=={x.name for x in t.constraints if isinstance(x,sa.CheckConstraint)}
    assert {x['name'] for x in i.get_unique_constraints(t.name)}=={x.name for x in t.constraints if isinstance(x,sa.UniqueConstraint)}
    assert {x['name'] for x in i.get_indexes(t.name)}=={x.name for x in t.indexes}
    actual={(tuple(x['constrained_columns']),x['referred_table'],tuple(x['referred_columns'])) for x in i.get_foreign_keys(t.name)}
    expected={(tuple(e.parent.name for e in x.elements),x.elements[0].column.table.name,tuple(e.column.name for e in x.elements)) for x in t.constraints if isinstance(x,sa.ForeignKeyConstraint)}
    assert actual==expected


def test_upgrade_downgrade_preserves_old_rows_and_tables(migrated):
    c,cargo,cargo_id=migrated
    for m in MODELS: assert c.execute(sa.text('SELECT count(*) FROM '+m.__tablename__)).scalar_one()==0
    with Operations.context(MigrationContext.configure(c)): migration.downgrade()
    names=sa.inspect(c).get_table_names()
    assert all(m.__tablename__ not in names for m in MODELS)
    assert all(x in names for x in ('alertas','ocorrencias','analises_etileno','sessoes_monitoramento','registros_sessao_iot'))
    assert c.execute(sa.select(cargo.c.id)).scalar_one()==cargo_id


def test_postgresql_offline_ddl_has_composite_guards_without_legacy_changes():
    output=io.StringIO()
    with Operations.context(MigrationContext.configure(dialect_name='postgresql',opts={'as_sql':True,'output_buffer':output})):
        migration.upgrade(); migration.downgrade()
    sql=output.getvalue()
    assert 'JSONB' in sql and 'UUID' in sql
    assert 'FOREIGN KEY(avaliacao_id, sessao_id)' in sql
    assert 'FOREIGN KEY(alerta_id, sessao_id)' in sql
    assert 'uq_alerta_sessao_identidade' in sql
    assert 'ALTER TABLE alertas' not in sql and 'ALTER TYPE' not in sql
    assert 'DROP TABLE alertas;' not in sql and 'DROP TABLE ocorrencias;' not in sql
    assert 'UPDATE ' not in sql
