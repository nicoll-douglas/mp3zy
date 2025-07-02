import logging, os, time, sys
from datetime import datetime

logging.basicConfig(
  level=logging.DEBUG if os.getenv("DEBUG") == "true" else logging.INFO, 
  format="%(levelname)s | %(message)s"
)

from services import SpotifyApiClient
from ftp_server import MusicManager
from core import Sync
import time

def main():
  logging.info(f"🟡 NEW SYNC STARTED AT {datetime.now()} 🟡")
  spotify_client = SpotifyApiClient()
  ftp_music_manager = MusicManager()
  spotify_sync = Sync(spotify_client, ftp_music_manager)
  spotify_sync.trigger()
  logging.info(f"🟢 SYNC FINISHED AT {datetime.now()} 🟢")
  ftp_music_manager.quit()

try:
  while True:
    main()
    sync_interval = os.getenv("SYNC_INTERVAL") or 12
    logging.info(f"🔴 SLEEPING FOR {sync_interval} HOURS BEFORE NEXT SYNC 🔴")
    time.sleep(int(sync_interval) * 60 * 60)
except Exception as e:
  logging.critical(e)
  logging.critical("Failed to sync.")
  sys.exit(1)