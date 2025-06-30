import logging, os

logging.basicConfig(
  level=logging.INFO if os.getenv("APP_ENV") == "production" else logging.DEBUG, 
  format="%(levelname)s | %(message)s"
)

from services import SpotifyApiClient, SpotifySync

SPOTIFY_CLIENT = SpotifyApiClient()
SPOTIFY_SYNC = SpotifySync(SPOTIFY_CLIENT)

SPOTIFY_SYNC.sync()