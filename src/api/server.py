from flask import Flask, request
from services import SpotifyApiClient

app = Flask(__name__)

@app.route("/spotify/callback")
def spotify_callback():
    error = request.args.get("error")
    if error:
      return f"Error: {error}"

    auth_code = request.args.get("code")
    SpotifyApiClient.request_access_token(auth_code)

    # resume main thread execution once access token obtained (authorization is complete)
    SpotifyApiClient.auth_event.set()
    
    return f"Authentication successful. You can close this window."

def serve():
  app.run(port=8888)