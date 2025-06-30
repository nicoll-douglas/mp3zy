import logging, os

logging.basicConfig(
  level=logging.INFO if os.getenv("APP_ENV") == "production" else logging.DEBUG, 
  format="%(levelname)s | %(message)s"
)

from services import SpotifyApiClient
from core import Sync

SPOTIFY_CLIENT = SpotifyApiClient()
SPOTIFY_SYNC = Sync(SPOTIFY_CLIENT)

SPOTIFY_SYNC.trigger()