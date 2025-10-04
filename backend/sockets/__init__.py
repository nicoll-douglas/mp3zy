from .downloads import DownloadsNamespace
from flask_socketio import SocketIO

def register_sockets(socketio: SocketIO):
  """Registers the SocketIO namespaces for the application.

  Args:
    socketio (SocketIO): The SocketIO instance.
  """

  socketio.on_namespace(DownloadsNamespace("/downloads"))
# END register_sockets