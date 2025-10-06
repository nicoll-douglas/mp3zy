import pytest
from app import create_app
from flask_socketio import SocketIOTestClient

@pytest.fixture
def socketio_test_client_fixture() -> callable:
  app, socketio = create_app()

  clients: list[tuple[SocketIOTestClient, str]] = []

  def _make_client(namespace = "/") -> SocketIOTestClient:
    client = socketio.test_client(app, namespace=namespace)
    clients.append((client, namespace))
    return client

  yield _make_client

  # Cleanup: disconnect all created clients
  for client, ns in clients:
    client.disconnect(namespace=ns)  
# END socketio_test_client_fixture