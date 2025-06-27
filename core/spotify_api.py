import requests, os, logging
from . import  app

API_URL = "https://api.spotify.com/v1"
AUTH_URL = "https://accounts.spotify.com/api/token"
USER_ID = os.getenv("SPOTIFY_USER_ID")

# helper to return the necessary auth headers for an API call
def get_auth_header(access_token: str):
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

  response = requests.post(
    url, 
    data=data, 
    headers=headers, 
    auth=(client_id, client_secret)
  )

  if (response.status_code != 200):
    raise RuntimeError(f"Access token request failed with status code {response.status_code}.\nResponse body:\n{response.text}")    

  logging.debug("Access token request succeeded.")
  response_body = response.json()
  
  return response_body["access_token"]

# request user playlists
def request_user_playlists(access_token: str):
  user_playlists_url = f"{API_URL}/users/{USER_ID}/playlists?limit=50"

  logging.debug(f"Requesting user playlist data from {user_playlists_url}")

  response = requests.get(
    user_playlists_url,
    headers=get_auth_header(access_token)
  )

  if (response.status_code != 200):
    raise RuntimeError(f"User playlist request failed with status code {response.status_code}.\nResponse body:\n{response.text}")    

  logging.debug("User playlist request succeeded.")
  response_body = response.json()

  return [
    {
      "id": p["id"],
      "name": p["name"],
      "cover_source": p["images"][0]["url"],
      "tracks_href": p["tracks"]["href"]
    }
    for p in response_body["items"]
  ]

# gets all tracks in a playlist
def request_playlist_tracks(access_token: str, url: str):
  headers = get_auth_header(access_token)
  fields="next,offset,items(track(id,name,duration_ms,artists(id,name),album(images(url))))"

  next = f"{url}?limit=50&offset=0&fields={fields}"
  all_tracks = []

  while next:
    logging.debug(f"Requesting playlist tracks from {next}")
    response = requests.get(
      next,
      headers=headers
    )

    if response.status_code != 200:
      logging.warning("Playlist track request failed, data for this run may be partial or incomplete.")
      return all_tracks

    response_body = response.json()
    all_tracks.extend([
      {
        "id": t["track"]["id"],
        "name": t["track"]["name"],
        "artists": t["track"]["artists"],
        "cover_source": t["track"]["album"]["images"][0]["url"],
        "duration_ms": t["track"]["duration_ms"]
      }
      for t in response_body["items"]
    ])
    next = response_body["next"]

  return all_tracks