import logging, os

logging.basicConfig(
  level=logging.DEBUG if os.getenv("DEBUG") == "true" else logging.INFO, 
  format="%(levelname)s | %(message)s"
)

from services import SpotifyApiClient
from core import Sync

SPOTIFY_CLIENT = SpotifyApiClient()
SPOTIFY_SYNC = Sync(SPOTIFY_CLIENT)

SPOTIFY_SYNC.trigger()