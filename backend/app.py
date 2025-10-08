from flask_cors import CORS
from flask import Flask
import os, sqlite3
from routes import register_routes
from sockets import register_sockets
import config, db
from flask_socketio import SocketIO

def create_app(db_conn: sqlite3.Connection = db.connect()) -> tuple[Flask, SocketIO]:
  """Sets up and creates the application and returns it.

  Returns:
    tuple[Flask, SocketIO]: A tuple containing the Flask application and the SocketIO instance.
  """

  db.setup(db_conn)

  app_name = os.getenv("APP_NAME") or ""
  flask_app_name = app_name + (" " if app_name else "") + "Desktop Backend API"
  
  app = Flask(flask_app_name)
  CORS(app, resources={ r"/*": { "origins": config.CORS_ALLOWED_ORIGINS } })
  socketio = SocketIO(app, cors_allowed_origins=config.CORS_ALLOWED_ORIGINS)

  register_routes(app)
  register_sockets(socketio, db_conn)

  return app, socketio
# END create_app

if __name__ == "__main__":
  app, socketio = create_app()
  socketio.run(app, host="127.0.0.1", port=8888, debug=False)