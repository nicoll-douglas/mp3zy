import requests
import sys
import os
from . import logger

URL = "https://api.spotify.com/v1"
USER_ID = os.getenv("SPOTIFY_USER_ID")

# log results of API calles and sys.exit on failure
def handle_api_response(response: requests.Response, request_name: str | None):
  if response.status_code != 200:
    logger.error(f"{request_name or "Request"} failed with status code {response.status_code}.")
    logger.info(f"Response body:\n{response.text}")
    sys.exit(1)
  else:
    logger.success(f"{request_name or "Request"} succeeded.")

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

  handle_api_response(response, "Access token request")

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

  handle_api_response(response, "User playlists request")
  response_body = response.json()

  return [
    {
      "id": p["id"],
      "name": p["name"],
      "cover": p["images"][0]["url"],
      "tracks_url": p["tracks"]["href"]
    }
    for p in response_body["items"]
  ]


# from playlist request
# items[i]["track"]["id"] string
# items[i]["track"]["name"] string
# items[i]["track"]["artists"][j]["id"]
# items[i]["track"]["artists"][j]["name"]
# def request_user_playlist_tracks(access_token: str, url: str):
#   logger.debug(f"Requesting user playlist tracks from {url}")

#   response = requests.get(
#     url,
#     headers=get_auth_headers(access_token)
#   )

#   handle_api_response(response, "User playlist tracks")
#   response_body