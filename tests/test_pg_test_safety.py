"""Safety gate tests: pure local data, no database connection."""
import pytest
from scripts.pg_test_safety import KEYS, ROLE, UnsafeTestDatabase, validate_target, validate_identity

TOKEN='a'*32
IDENTITY='7123456789012345678'


def environment(**changes):
    return dict(zip(KEYS, [f'postgresql+psycopg://{ROLE}:fake-only@127.0.0.1:35432/chicosense_test_{TOKEN}', TOKEN, IDENTITY])) | changes


def identity(**changes):
    return dict(database='chicosense_test_'+TOKEN, role=ROLE, owner=ROLE,
                marker='chicosense-disposable:'+TOKEN, system_identifier=IDENTITY,
                recovery=False, server_port=5432, version=170000) | changes


def test_no_opt_in_ignores_even_production_database_url():
    assert validate_target({'DATABASE_URL':'postgresql://production.invalid/live'}) is None


@pytest.mark.parametrize('url', [
    'postgresql+psycopg://chicosense_test_user:fake@remote.invalid:35432/chicosense_test_'+TOKEN,
    'postgresql+psycopg://chicosense_test_user:fake@localhost:35432/chicosense_test_'+TOKEN,
    'postgresql+psycopg://chicosense_test_user:fake@127.0.0.1:35432/production',
    'postgresql+psycopg://postgres:fake@127.0.0.1:35432/chicosense_test_'+TOKEN,
    'postgresql+psycopg://chicosense_test_user:fake@127.0.0.1/chicosense_test_'+TOKEN,
    'postgresql+psycopg://chicosense_test_user:fake@127.0.0.1:35432/chicosense_test_'+TOKEN+'?host=remote.invalid',
    'postgresql+psycopg://chicosense_test_user:fake@127.0.0.1:35432/chicosense_test_'+TOKEN+'?service=production',
    'postgresql+psycopg://chicosense_test_user:fake@127.0.0.1:35432/chicosense_test_'+TOKEN+'?options=-csearch_path=production',
    'sqlite:///test.db', 'invalid',
])
def test_unsafe_urls_rejected_before_connection(url):
    with pytest.raises(UnsafeTestDatabase):
        validate_target(environment(CHICOSENSE_TEST_DATABASE_URL=url))


@pytest.mark.parametrize('key',KEYS)
def test_partial_configuration_is_error(key):
    env=environment(); del env[key]
    with pytest.raises(UnsafeTestDatabase): validate_target(env)


def test_allowed_target_and_identity():
    target=validate_target(environment())
    validate_identity(target,identity())
    assert target.url.host=='127.0.0.1'


@pytest.mark.parametrize('changes',[
    {'database':'production'}, {'role':'postgres'}, {'owner':'someone_else'},
    {'marker':None}, {'marker':'chicosense-disposable:'+'b'*32},
    {'system_identifier':'9123456789012345678'}, {'recovery':True},
    {'server_port':None}, {'version':130000},
])
def test_wrong_server_or_database_identity_blocks_destruction(changes):
    with pytest.raises(UnsafeTestDatabase):
        validate_identity(validate_target(environment()),identity(**changes))


@pytest.mark.parametrize('key,value',[(KEYS[1],'not-a-token'),(KEYS[2],'not-a-server-id')])
def test_invalid_markers_rejected(key,value):
    with pytest.raises(UnsafeTestDatabase): validate_target(environment(**{key:value}))


def test_alembic_uses_supplied_connection_without_opening_default_engine(monkeypatch):
    """Regression for the test runner's connection injection; no DDL/database."""
    import runpy
    from pathlib import Path
    from unittest.mock import Mock,MagicMock
    from alembic import context
    from alembic.config import Config
    import sqlalchemy
    config=Config()
    connection=object()
    config.attributes['connection']=connection
    monkeypatch.setattr(context,'config',config,raising=False)
    monkeypatch.setattr(context,'is_offline_mode',lambda:False)
    configure=Mock();run=Mock()
    monkeypatch.setattr(context,'configure',configure)
    monkeypatch.setattr(context,'run_migrations',run)
    monkeypatch.setattr(context,'begin_transaction',MagicMock())
    engine_factory=Mock(side_effect=AssertionError('Default/remote engine must never be opened'))
    monkeypatch.setattr(sqlalchemy,'engine_from_config',engine_factory)
    runpy.run_path(str(Path(__file__).resolve().parents[1]/'alembic/env.py'))
    engine_factory.assert_not_called()
    assert configure.call_args.kwargs['connection'] is connection
    run.assert_called_once_with()
