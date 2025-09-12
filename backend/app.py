from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from flask import Flask, request, jsonify
import os, threading
from services import YtDlpClient
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

  try:
    status = "success"
    results = YtDlpClient().query_youtube(artist, track)
  except Exception as e:
    status = "error"
    results = []
      
  return jsonify({ "status": status, "results": results })

@app.route("/download", methods=["POST"])
@auth
def download():
  data = request.get_json()
  result = start_track_download(socketio, data)
  return jsonify(result)

@socketio.on("subscribe")
def subscribe(data):
  room_id = data["room_id"]
  join_room(room_id)
  emit("subscribed", { "room_id": room_id })

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8888, debug=False)