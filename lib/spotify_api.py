import requests
import os
from . import logger, app

URL = "https://api.spotify.com/v1"
USER_ID = os.getenv("SPOTIFY_USER_ID")

# helper to return the necessary auth headers for an API call
def get_auth_headers(access_token: str):
  return  {
    "Authorization": f"Bearer {access_token}"
  }

# request client credentials from API
def request_access_token() -> str:
  client_id = os.getenv("CLIENT_ID")
  client_secret = os.getenv("CLIENT_SECRET")

  url = "https://accounts.spotify.com/api/token"
  data = {
    "grant_type": "client_credentials"
  }
  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }

  logger.debug("Requesting access token from Spotify API with given client ID and secret...")

  response = requests.post(
    url, 
    data=data, 
    headers=headers, 
    auth=(client_id, client_secret)
  )

  app.handle_http_response(response, "Access token request")

  token_data = response.json()
  return token_data["access_token"]

# request user playlists
def request_user_playlists(access_token: str):
  user_playlists_url = f"{URL}/users/{USER_ID}/playlists?limit=50"

  logger.debug(f"Requesting user playlist data from {user_playlists_url}")

  response = requests.get(
    user_playlists_url,
    headers=get_auth_headers(access_token)
  )

  app.handle_http_response(response, "User playlists request")
  response_body = response.json()

  return [
    {
      "id": p["id"],
      "name": p["name"],
      "cover": p["images"][0]["url"],
      "tracks_href": p["tracks"]["href"]
    }
    for p in response_body["items"]
  ]

# gets all tracks in a playlist
def request_playlist_tracks(access_token: str, url: str):
  headers = get_auth_headers(access_token)
  fields="next,offset,items(track(id,name,artists(id,name),album(images(url))))"

  next = f"{url}?limit=50&offset=0&fields={fields}"
  all_tracks = []

  while next:
    logger.debug(f"Requesting playlist tracks from {next}")
    response = requests.get(
      next,
      headers=headers
    )
    app.handle_http_response(response, "Playlist tracks request")

    response_body = response.json()
    all_tracks.extend([
      {
        "id": t["track"]["id"],
        "name": t["track"]["name"],
        "artists": t["track"]["artists"],
        "cover": t["track"]["album"]["images"][0]["url"]
      }
      for t in response_body["items"]
    ])
    next = response_body["next"]

  return all_tracks