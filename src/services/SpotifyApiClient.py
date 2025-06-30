import os, logging, requests, mimetypes, sys
import disk

class SpotifyApiClient:
  __API_URL = "https://api.spotify.com/v1"
  __API_AUTH_HEADERS = None
  __AUTH_URL = "https://accounts.spotify.com/api/token"
  __USER_ID = os.getenv("SPOTIFY_USER_ID")
  __CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
  __CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

  def __init__(self):
    logging.info("Requesting an access token from the Spotify API...")

    data = { "grant_type": "client_credentials" }
    headers = { "Content-Type": "application/x-www-form-urlencoded" }

    response = requests.post(
      self.__AUTH_URL, 
      data=data,
      headers=headers, 
      auth=(self.__CLIENT_ID, self.__CLIENT_SECRET)
    )

    if (response.status_code != 200):
      logging.critical(f"Access token request failed with status code {response.status_code}.")
      logging.debug(f"Response body: {response.text}")
      sys.exit(1)

    response_body = response.json()
    self.__API_AUTH_HEADERS = {
      "Authorization": f"Bearer {response_body["access_token"]}"
    }

    logging.info("Successfully obtained an access token.")

  # request user playlists
  def fetch_user_playlists(self):
    logging.info("Retrieving all user playlists from the Spotify API...")

    user_playlists_url = f"{self.__API_URL}/users/{self.__USER_ID}/playlists?limit=50"
    response = requests.get(
      user_playlists_url,
      headers=self.__API_AUTH_HEADERS
    )

    if (response.status_code != 200):
      logging.error(
        f"Request failed with status code {response.status_code}."
      )
      logging.debug(f"Response body: {response.text}")
      return []

    response_body = response.json()
    logging.info("Successfully retrieved playlist data.")

    return [
      {
        "name": p["name"],
        "tracks_href": p["tracks"]["href"]
      }
      for p in response_body["items"]
    ]

  # gets all tracks in a playlist
  def fetch_playlist_tracks(self, url: str, playlist_name: str):
    logging.info(f"Retrieving playlist tracks for playlist '{playlist_name}'...")
    fields="next,offset,items(track(id,name,duration_ms,artists(id,name),album(images(url))))"

    next = f"{url}?limit=50&offset=0&fields={fields}"
    all_tracks = []

    while next:
      response = requests.get(
        next,
        headers=self.__API_AUTH_HEADERS
      )

      logging.debug(f"Request: GET {next}")
      if response.status_code != 200:
        logging.error("Failed to retrieve all playlist tracks.")
        logging.warning("Data for this run may be partial or incomplete.")
        return all_tracks

      response_body = response.json()
      all_tracks.extend([
        {
          "id": t["track"]["id"],
          "name": t["track"]["name"],
          "artists": [a["name"] for a in t["track"]["artists"]],
          "cover_source": t["track"]["album"]["images"][0]["url"],
          "duration_ms": t["track"]["duration_ms"]
        }
        for t in response_body["items"]
      ])
      next = response_body["next"]

    logging.info("Successfully retrieved all track data.")
    return all_tracks
  
  @staticmethod
  def download_cdn_track_cover(url: str):
    logging.info(f"Downloading cover image...")
    cover = disk.models.TrackCover(source=url)

    if cover.exists():
      logging.info("Cover image is already downloaded.")
      return cover.get_path(), False

    response = requests.get(url)
    if response.status_code != 200:
      logging.error("Cover image request failed.")
      logging.warning("Data for this run may be partial or incomplete.")
      return None, None

    # get ext from content type (including cases ~ "image/jpeg; charset=UTF-8")
    content_type = response.headers.get("Content-Type", "")
    ext = mimetypes.guess_extension(content_type.split(";")[0]) or ".jpg"

    # build and get path now that we know the extension
    save_path = cover.set_ext(ext).normalise().get_path()
    
    logging.debug(f"Saving cover image to disk at: {save_path}")

    # don't worry about write failure, not critical
    try:
      cover.write(response.content)
      logging.info("Successfully downloaded cover image.")
      return save_path, True
    except Exception as e:
      logging.error(e)
      logging.warning("Failed to save cover image to disk.")
      logging.warning("Data for this run may be partial or incomplete.")
      return None, None