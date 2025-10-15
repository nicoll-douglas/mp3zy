from .downloads import DownloadsSocket
from flask_socketio import SocketIO
import sqlite3

def register_sockets(socketio: SocketIO, db_conn: sqlite3.Connection | None = None):
  """Registers the SocketIO namespaces for the application.

  Args:
    socketio (SocketIO): The SocketIO instance.
    db_conn (sqlite3.Connection | None): A database connection to inject into any sockets.
  """

  socketio.on_namespace(DownloadsSocket(db_conn))
# END register_sockets