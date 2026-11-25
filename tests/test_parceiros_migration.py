"""New migration runs locally; previous domain migrations are never rewritten."""
import importlib.util
import io
from pathlib import Path
from uuid import uuid4
import pytest
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from alembic.migration import MigrationContext
from alembic.operations import Operations
from app.models.parceiro_comercial import ParceiroComercial

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('migration_partners',ROOT/'alembic/versions/20261124_0011_parceiros_comerciais.py')
migration=importlib.util.module_from_spec(spec);spec.loader.exec_module(migration)


def test_upgrade_constraints_and_downgrade_preserve_other_tables():
    engine=sa.create_engine('sqlite://')
    with engine.begin() as c:
        c.exec_driver_sql('PRAGMA foreign_keys=ON')
        metadata=sa.MetaData()
        companies=sa.Table('empresas',metadata,sa.Column('id',UUID(as_uuid=True),primary_key=True))
        users=sa.Table('usuarios',metadata,sa.Column('id',UUID(as_uuid=True),primary_key=True))
        metadata.create_all(c)
        carrier,partner,actor=uuid4(),uuid4(),uuid4()
        c.execute(companies.insert(),[dict(id=carrier),dict(id=partner)]);c.execute(users.insert(),dict(id=actor))
        with Operations.context(MigrationContext.configure(c)):migration.upgrade()
        table=ParceiroComercial.__table__
        assert set(sa.inspect(c).get_columns(table.name)[0])  # inspect actual DDL
        assert {r['name'] for r in sa.inspect(c).get_columns(table.name)}==set(table.columns.keys())
        body=dict(id=uuid4(),transportadora_id=carrier,empresa_id=partner,ativo=True,
            aprovado_por_id=actor,atualizado_por_id=actor,justificativa='Teste')
        c.execute(table.insert(),body)
        with pytest.raises(sa.exc.IntegrityError):
            with c.begin_nested():c.execute(table.insert(),body|dict(id=uuid4()))
        with pytest.raises(sa.exc.IntegrityError):
            with c.begin_nested():c.execute(table.insert(),body|dict(id=uuid4(),empresa_id=carrier))
        with pytest.raises(sa.exc.IntegrityError):
            with c.begin_nested():c.execute(table.insert(),body|dict(id=uuid4(),empresa_id=uuid4()))
        with Operations.context(MigrationContext.configure(c)):migration.downgrade()
        assert not sa.inspect(c).has_table(table.name)
        assert c.scalar(sa.select(sa.func.count()).select_from(companies))==2
        assert c.scalar(sa.select(sa.func.count()).select_from(users))==1
    engine.dispose()


def test_postgresql_offline_sql_only_adds_new_table():
    output=io.StringIO()
    context=MigrationContext.configure(dialect_name='postgresql',opts=dict(as_sql=True,output_buffer=output))
    with Operations.context(context):migration.upgrade()
    sql=output.getvalue()
    assert 'CREATE TABLE parceiros_comerciais' in sql
    assert 'uq_parceiro_transportadora_empresa' in sql and 'ck_parceiro_empresas_distintas' in sql
    assert 'ALTER TABLE' not in sql and 'DROP TABLE' not in sql
