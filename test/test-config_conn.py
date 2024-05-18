import pytest
from repositories import config_conn


def test_get_connection():
    conn = config_conn.Connection.getConnection()
    assert conn is not None, "La conexión no debería ser None"
    config_conn.Connection.releaseConnection(conn)


def test_get_pool():
    pool = config_conn.Connection.getPool()
    assert pool is not None, "El pool no debería ser None"
