import os, logging, requests, mimetypes
from disk import Cover

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
      raise RuntimeError(f"Access token request failed with status code {response.status_code}.\nResponse body:\n{response.text}")    

    response_body = response.json()
    self.__API_AUTH_HEADERS = {
      "Authorization": f"Bearer {response_body["access_token"]}"
    }

    logging.info("Successfully obtained an access token.")

  # request user playlists
  def fetch_user_playlists(self):
    logging.info("Retrieving user playlist data from the Spotify API...")

    user_playlists_url = f"{self.__API_URL}/users/{self.__USER_ID}/playlists?limit=50"
    response = requests.get(
      user_playlists_url,
      headers=self.__API_AUTH_HEADERS
    )

    if (response.status_code != 200):
      raise RuntimeError(f"User playlist request failed with status code {response.status_code}.\nResponse body:\n{response.text}")    

    response_body = response.json()

    logging.info("Successfully retrieved playlist data.")

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
  def fetch_playlist_tracks(self, url: str, playlist_name: str):
    logging.info(f"Requesting track data for playlist '{playlist_name}'...")
    fields="next,offset,items(track(id,name,duration_ms,artists(id,name),album(images(url))))"

    next = f"{url}?limit=50&offset=0&fields={fields}"
    all_tracks = []

    while next:
      logging.debug(f"Requesting playlist tracks from {next}")
      response = requests.get(
        next,
        headers=self.__API_AUTH_HEADERS
      )

      if response.status_code != 200:
        logging.error("Playlist track request failed.")
        logging.warning("Data for this run may be partial or incomplete.")
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

    logging.info("Successfully retrieved all track data.")
    return all_tracks
  
  @staticmethod
  def download_cdn_image(url: str, target_dir: str):
    logging.debug(f"Downloading cover image: {url}")
    cover = Cover(source=url, _dir=target_dir)

    if cover.exists():
      logging.debug("Cover image is already downloaded, skipping...")
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
    save_path = cover.set_ext(ext).build_path().get_path()
    
    logging.debug(f"Saving cover image to disk at: {save_path}")

    # don't worry about write failure, not critical
    try:
      cover.write(response.content)
      logging.debug("Successfully saved image to disk.")
      return save_path, True
    except Exception as e:
      logging.error(e)
      return None, None
    
  @classmethod
  def download_cdn_images(cls, incoming_hrefs: list[str], target_dir: str):
    total = len(incoming_hrefs)
    success_count = 0
    fail_count = 0
    skip_count = 0

    logging.info(f"Downloading {total} cover images...")
    for index, url in enumerate(incoming_hrefs):
      logging.info(f"Downloading cover image {current_num} of {total}...")
      save_path, cover_is_fresh = cls.download_cdn_image(url, target_dir)
      current_num = index + 1

      if not save_path:
        logging.warning(f"Cover image download {current_num} of {total} failed. ({url})")
        fail_count += 1
        continue
      
      if not cover_is_fresh:
        logging.info("Cover image already downloaded so skipped.")
        skip_count += 1
      
      logging.info(f"Successfully downloaded cover image {current_num} of {total}.")
      success_count += 1

    logging.info(f"{skip_count} cover images already downloaded. Successfully downloaded {success_count} of {total - skip_count}. {fail_count} failed.")
