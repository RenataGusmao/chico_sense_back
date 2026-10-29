"""Only disposable SQLite and offline PostgreSQL DDL, including vehicle exclusion."""
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
from app.models.exaustao_simulada import IntervencaoSimulada,AcaoIntervencao
from tests.test_monitoramento_migration import migrated_database
from tests.test_historico_iot_migration import iot_migrated
from tests.test_analises_etileno_migration import migrated as analyses_migrated
from tests.test_preventivo_migration import migrated as preventive_migrated

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('migration_exaustao',ROOT/'alembic/versions/20261028_0010_exaustao_virtual.py')
migration=importlib.util.module_from_spec(spec); spec.loader.exec_module(migration)
MODELS=(IntervencaoSimulada,AcaoIntervencao)


@pytest.fixture
def migrated(preventive_migrated):
    connection,*_=preventive_migrated
    sa.Table('veiculos',sa.MetaData(),sa.Column('id',UUID(as_uuid=True),primary_key=True)).create(connection)
    with Operations.context(MigrationContext.configure(connection)): migration.upgrade()
    return preventive_migrated


def test_single_head_and_previous_revisions_unchanged():
    cfg=Config(str(ROOT/'alembic.ini')); cfg.set_main_option('script_location',str(ROOT/'alembic'))
    script=ScriptDirectory.from_config(cfg)
    assert script.get_heads()==['20261028_0010_exaustao_virtual']
    assert script.get_revision(script.get_current_head()).down_revision=='20261028_0009_preventivo'


@pytest.mark.parametrize('model',MODELS)
def test_migration_matches_model_constraints_and_precision(migrated,model):
    c,*_=migrated; inspector=sa.inspect(c); t=model.__table__
    columns={x['name']:x for x in inspector.get_columns(t.name)}
    assert set(columns)==set(t.columns.keys())
    assert all(columns[x.name]['nullable']==x.nullable for x in t.columns)
    assert {x['name'] for x in inspector.get_check_constraints(t.name)}=={x.name for x in t.constraints if isinstance(x,sa.CheckConstraint)}
    assert {x['name'] for x in inspector.get_unique_constraints(t.name)}=={x.name for x in t.constraints if isinstance(x,sa.UniqueConstraint)}
    assert {x['name'] for x in inspector.get_indexes(t.name)}=={x.name for x in t.indexes}
    actual={(tuple(x['constrained_columns']),x['referred_table'],tuple(x['referred_columns'])) for x in inspector.get_foreign_keys(t.name)}
    expected={(tuple(e.parent.name for e in x.elements),x.elements[0].column.table.name,tuple(e.column.name for e in x.elements)) for x in t.constraints if isinstance(x,sa.ForeignKeyConstraint)}
    assert actual==expected
    if model is IntervencaoSimulada:
        assert columns['duracao_planejada_s']['type'].scale==3 and columns['duracao_registrada_s']['type'].scale==6
        idx=next(x for x in inspector.get_indexes(t.name) if x['name']=='uq_exaustor_virtual_executando')
        assert idx['unique'] and "estado = 'EM_EXECUCAO'" in str(idx['dialect_options']['sqlite_where'])


def test_upgrade_and_downgrade_preserve_previous_tables_and_data(migrated):
    c,cargo,cargo_id=migrated
    assert c.execute(sa.select(cargo.c.id)).scalar_one()==cargo_id
    for m in MODELS: assert c.execute(sa.text('SELECT COUNT(*) FROM '+m.__tablename__)).scalar_one()==0
    with Operations.context(MigrationContext.configure(c)): migration.downgrade()
    names=sa.inspect(c).get_table_names()
    assert all(m.__tablename__ not in names for m in MODELS)
    assert all(n in names for n in ('alertas','ocorrencias','analises_etileno','avaliacoes_preventivas','sessoes_monitoramento'))
    assert c.execute(sa.select(cargo.c.id)).scalar_one()==cargo_id


def test_postgresql_offline_ddl_has_exclusion_and_no_hardware_or_legacy_mutation():
    output=io.StringIO()
    with Operations.context(MigrationContext.configure(dialect_name='postgresql',opts={'as_sql':True,'output_buffer':output})):
        migration.upgrade(); migration.downgrade()
    sql=output.getvalue()
    assert "CREATE UNIQUE INDEX uq_exaustor_virtual_executando ON intervencoes_simuladas (veiculo_id) WHERE estado = 'EM_EXECUCAO'" in sql
    assert 'JSONB' in sql and 'NUMERIC(20, 6)' in sql
    assert 'FOREIGN KEY(intervencao_id, sessao_id)' in sql
    assert 'FOREIGN KEY(alerta_id, sessao_id)' in sql
    assert 'ALTER TABLE alertas' not in sql and 'ALTER TYPE' not in sql and 'UPDATE ' not in sql
    assert 'DROP TABLE alertas;' not in sql and 'DROP TABLE ocorrencias;' not in sql
    assert 'mqtt' not in sql.lower() and 'api_key' not in sql.lower()
