import pytest
from app import create_app
from flask_socketio import SocketIOTestClient
from typing import Generator, Callable
import sqlite3

@pytest.fixture
def socketio_test_client(in_memory_db_conn: sqlite3.Connection) -> Generator[Callable[[str], SocketIOTestClient], None, None]:
  """Fixture that provides a function for creating a SocketIO test client with a given namespace.

  Args:
    in_memory_db_conn (sqlite3.Connection): An in-memory database connection provided by the in_memory_db_conn fixture.

  Returns:
    Generator[Callable[[str], SocketIOTestClient], None, None]: Yields a callable that can create a test client under the given SocketIO namespace.

  Notes:
    - On cleanup it will disconnect all created clients.
  """
  
  app, socketio = create_app(in_memory_db_conn)

  clients: list[tuple[SocketIOTestClient, str]] = []

  def _make_client(namespace = "/") -> SocketIOTestClient:
    client = socketio.test_client(app, namespace=namespace)
    clients.append((client, namespace))
    return client

  yield _make_client

  for client, ns in clients:
    client.disconnect(namespace=ns)  
# END socketio_test_client