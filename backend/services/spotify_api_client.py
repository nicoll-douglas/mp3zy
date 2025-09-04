import os, requests, mimetypes, string, secrets, base64, hashlib, threading, time
import media
from urllib.parse import urlencode

class SpotifyApiClient:
  API_URL = "https://api.spotify.com/v1"
  TOKEN_URL = "https://accounts.spotify.com/api/token"
  AUTH_URL = "https://accounts.spotify.com/authorize"
  CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
  CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
  REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
  WANTED_SCOPES = "playlist-read-private user-library-read playlist-read-collaborative"

  auth_event = threading.Event()
  user_profile = None
  _code_verifier = None
  _access_token = None
  _refresh_token = None
  _access_token_duration = None

  @classmethod
  def _get_code_challenge(cls):
    # create code verifier according to PKCE standard
    possible = string.ascii_letters + string.digits + "_.-~"
    cls._code_verifier = ''.join(secrets.choice(possible) for _ in range(64))

    # hash the code verifier use sha256
    digest = hashlib.sha256(cls._code_verifier.encode("ascii")).digest()

    # calculate base64 representation of the digest (code challenge)
    base64url = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

    return base64url
  
  @classmethod
  def build_auth_url(cls):
    code_challenge = cls._get_code_challenge()

    # query parameters for the auth_url
    params = {
      "client_id": cls.CLIENT_ID,
      "response_type": "code",
      "redirect_uri": cls.REDIRECT_URI,
      "scope": cls.WANTED_SCOPES,
      "code_challenge_method": "S256",
      "code_challenge": code_challenge
    }

    auth_url = cls.AUTH_URL + "?" + urlencode(params)
    return auth_url

  @classmethod
  def request_access_token(cls, auth_code: str):
    # data to send as url encoded
    data = {
      "grant_type": "authorization_code",
      "code": auth_code,
      "redirect_uri": cls.REDIRECT_URI,
      "client_id": cls.CLIENT_ID,
      "code_verifier": cls._code_verifier
    }

    # make POST request for access token
    r = requests.post(cls.TOKEN_URL, data=data)
    r.raise_for_status()
    body = r.json()

    # store tokens
    cls._access_token = body["access_token"]
    cls._refresh_token = body["refresh_token"]
    cls._access_token_duration = body["expires_in"]

  @classmethod
  def refresh_access_token(cls):
    data = {
      "grant_type": "refresh_token",
      "refresh_token": cls._refresh_token,
      "client_id": cls.CLIENT_ID
    }

    r = requests.post(cls.TOKEN_URL, data=data)
    r.raise_for_status()
    body = r.json()

    cls._access_token = body["access_token"]
    cls._access_token_duration = body["expires_in"]

    if "refresh_token" in body:
      cls._refresh_token = body["refresh_token"]

  @classmethod 
  def auto_refresh_access_token(cls, initial_refresh = False):
    def refresh():
      print("Refreshing access token...")
      cls.refresh_access_token()
      print("✅ Successfully refreshed access token.")
    
    if initial_refresh:
      refresh()
      
    while True:
      next_refresh_s = 0.9 * cls._access_token_duration
      next_refresh_m = round(next_refresh_s / 60)
      print(f"{next_refresh_m} minutes until next refresh.")
      time.sleep(next_refresh_s)
      refresh()

  @classmethod
  def fetch_user_profile(cls):
    if cls.user_profile:
      return cls.user_profile
    
    me_url = f"{cls.API_URL}/me"
    r = requests.get(
      url=me_url,
      headers=cls._auth_headers()
    )
    r.raise_for_status()
    body = r.json()

    return body

  @classmethod
  def _auth_headers(cls):
    return {
      "Authorization": f"Bearer {cls._access_token}"
    }
  
  @classmethod
  def _fetch_all_pages(cls, initial: str):
    next = initial
    results = []

    while next:
      r = requests.get(
        next,
        headers=cls._auth_headers()
      )

      r.raise_for_status()
      body = r.json()

      results.extend(body["items"])
      next = body["next"]

    return results

  @classmethod
  def fetch_user_playlists(cls):
    limit = 50
    offset = 0
    initial = f"{cls.API_URL}/users/{cls.user_profile["id"]}/playlists?limit={limit}&offset={offset}"
    return cls._fetch_all_pages(initial)

  @classmethod
  def fetch_playlist_items(cls, url: str):
    fields="next,items(is_local,track(id,name,duration_ms,type,track_number,disc_number,artists(name),album(images(url),release_date,id,name)))"
    limit = 50
    offset = 0
    initial = f"{url}?limit={limit}&offset={offset}&fields={fields}"
    return cls._fetch_all_pages(initial)
  
  @classmethod
  def fetch_liked_tracks(cls):
    limit = 50
    offset = 0
    initial = f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}"
    return cls._fetch_all_pages(initial)
  
  @classmethod
  def playlist_items_url(cls, playlist_id):
    return f"{cls.API_URL}/playlists/{playlist_id}/tracks"
  
  @staticmethod
  def download_cdn_track_cover(url: str, album_id: str):
    cover = media.TrackCover(album_id=album_id)

    # check if the cover is already downloaded
    path = cover.search_and_get_path()
    if path:
      return path, False

    # fetch track cover otherwise
    r = requests.get(url)
    r.raise_for_status()
    
    # get ext from content type (including cases with charset specificed, e.g "image/jpeg; charset=UTF-8")
    content_type = r.headers.get("Content-Type", "")
    ext = mimetypes.guess_extension(content_type.split(";")[0])

    # save cover to disk
    cover.ext = ext
    cover.path = cover.build_path()
    try:
      cover.write(r.content)
      return cover.path, True
    except Exception as e:
      return None, None