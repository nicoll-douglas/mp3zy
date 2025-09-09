from flask import Flask, request, render_template, redirect, url_for, jsonify, Response, json
from services import SpotifyApiClient, YtDlpClient
import threading, os
from helpers import download_all_playlists
from media import Codec

app = Flask(os.getenv("VITE_APP_NAME") + " Backend")

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
  if not data:
    return jsonify({ "error": "Invalid or missing JSON request body." }), 400

@app.route("/spotify/callback")
def spotify_callback():
    error = request.args.get("error")
    if error:
      return jsonify({ "error": error }), 500

    auth_code = request.args.get("code")
    if not auth_code:
      return jsonify({ "error": "Error: No auth code received."  }), 500
    
    print("✅ Successfully received authorization code.")

    # need to handle HTTP errors here
    print("Exchanging authorization code for an access token...")
    SpotifyApiClient.request_access_token(auth_code)
    print("✅ Successfully obtained access token.")
    
    print("Fetching user profile...")
    SpotifyApiClient.user_profile = SpotifyApiClient.fetch_user_profile()
    print("✅ Successfully fetched user profile.")

    threading.Thread(target=SpotifyApiClient.auto_refresh_access_token).start()

    return render_template("spotify/callback.html")

@app.route("/spotify/sync")
def spotify_sync():
  if not SpotifyApiClient.user_profile:
    return redirect(url_for("index"))

  threading.Thread(target=download_all_playlists, args=(Codec.FLAC,)).start()
  return "Downloading all playlists, check the CLI..."