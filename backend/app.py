from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
import os
from flask import Flask, request, jsonify
from services import YtDlpClient
import os
from api import start_track_download

app = Flask(os.getenv("VITE_APP_NAME") + " Backend")

allowed_origins = [
  os.getenv("VITE_APP_URL"),
  "file://*",
  "app://*"
]

CORS(app, resources={r"/*": {"origins": allowed_origins}})

socketio = SocketIO(app, cors_allowed_origins=allowed_origins)

def auth(f):
  def wrapper(*args, **kwargs):
    token = request.headers.get("X-Electron-Auth")
    if token != os.getenv("ELECTRON_AUTH_KEY"):
      return jsonify({ "error": "Unauthorized" }), 401
    
    return f(*args, **kwargs)
  
  wrapper.__name__ = f.__name__
  return wrapper

@app.route("/ping")
@auth
def ping():
  return jsonify({ "message": "Pong from Python" })

@app.route("/audio-search/yt-dlp", methods=["GET"])
@auth
def audio_search():
  artist = request.args.get("artist")
  track = request.args.get("track")
  results = YtDlpClient().query_youtube(artist, track)
  return jsonify(results)

@app.route("/download", methods=["POST"])
@auth
def download():
  data = request.get_json()
  task_id = start_track_download(socketio, data)
  return jsonify({ "taskId": task_id })

@socketio.on("subscribe")
def subscribe(data):
  task_id = data["task_id"]
  join_room(task_id)
  emit("subscribed", { "taskId": task_id })

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8888, debug=False)