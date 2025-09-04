from flask import Flask, request, render_template, redirect, url_for, jsonify, Response, json
from services import SpotifyApiClient
import threading
from helpers import download_all_playlists
from disk import Codec

app = Flask(__name__)

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

@app.route("/ping")
def ping():
  return jsonify({ "message": "Pong from Python" })
