"""Fail-closed guard for opt-in, disposable PostgreSQL tests. No .env loading."""
from dataclasses import dataclass
import re
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool

PREFIX = 'chicosense_test_'
ROLE = 'chicosense_test_user'
KEYS = ('CHICOSENSE_TEST_DATABASE_URL', 'CHICOSENSE_TEST_DISPOSABLE_TOKEN',
        'CHICOSENSE_TEST_SYSTEM_IDENTIFIER')


class UnsafeTestDatabase(ValueError):
    pass


@dataclass(frozen=True)
class Target:
    url: object
    token: str
    system_identifier: str


def validate_target(environ):
    """None means not requested; partial/malformed configuration is an error."""
    values = [environ.get(k, '') for k in KEYS]
    if not any(values):
        return None
    raw, token, identity = values
    if not all(values) or not re.fullmatch(r'[a-f0-9]{32}', token):
        raise UnsafeTestDatabase('Explicit disposable token and server identity required.')
    if not re.fullmatch(r'[0-9]{10,20}', identity):
        raise UnsafeTestDatabase('Invalid expected server identity.')
    try:
        url = make_url(raw)
        allowed = (url.drivername == 'postgresql+psycopg'
                   and url.host in ('127.0.0.1', '::1')
                   and url.port is not None and 1024 <= url.port <= 65535
                   and url.database == PREFIX + token
                   and url.username == ROLE and bool(url.password)
                   and not url.query)
    except Exception:
        raise UnsafeTestDatabase('Invalid test target; URL omitted.') from None
    if not allowed:
        raise UnsafeTestDatabase('Only explicit loopback disposable PostgreSQL is allowed.')
    return Target(url, token, identity)


def validate_identity(target, identity):
    """Must run on the same locked connection used for destructive DDL."""
    if not (identity['database'] == PREFIX + target.token
            and identity['role'] == ROLE and identity['owner'] == ROLE
            and identity['marker'] == 'chicosense-disposable:' + target.token
            and str(identity['system_identifier']) == target.system_identifier
            and not identity['recovery'] and identity['server_port'] is not None
            and int(identity['version']) >= 140000):
        raise UnsafeTestDatabase('Server/database ownership, identity or marker mismatch.')


def verify_connection(connection, target):
    row = connection.execute(text('''
        SELECT current_database() AS database, current_user AS role,
               pg_get_userbyid(d.datdba) AS owner,
               shobj_description(d.oid, 'pg_database') AS marker,
               (SELECT system_identifier::text FROM pg_control_system()) AS system_identifier,
               pg_is_in_recovery() AS recovery, inet_server_port() AS server_port,
               current_setting('server_version_num')::int AS version
        FROM pg_database d WHERE d.datname=current_database()
    ''')).mappings().one()
    validate_identity(target, row)
    return dict(row)


def open_verified(target):
    engine = create_engine(target.url, poolclass=NullPool, hide_parameters=True,
                           connect_args={'hostaddr': target.url.host, 'connect_timeout': 5, 'application_name': 'chicosense_disposable_tests',
                                         'options': '-c search_path=public -c lock_timeout=5000 -c statement_timeout=15000'})
    connection = None
    try:
        connection = engine.connect()
        verify_connection(connection, target)
        connection.commit()
        return engine, connection
    except Exception:
        if connection is not None:
            connection.close()
        engine.dispose()
        raise UnsafeTestDatabase('Test PostgreSQL unavailable or identity unverified; no DDL executed.') from None
