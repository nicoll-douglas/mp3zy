import logging, os, time
from datetime import datetime

logging.basicConfig(
  level=logging.DEBUG if os.getenv("DEBUG") == "true" else logging.INFO, 
  format="%(levelname)s | %(message)s"
)

from services import SpotifyApiClient
from core import Sync
import time

def main():
  logging.info(f"🟡 NEW SYNC STARTED AT {datetime.now()} 🟡")
  SPOTIFY_CLIENT = SpotifyApiClient()
  SPOTIFY_SYNC = Sync(SPOTIFY_CLIENT)
  SPOTIFY_SYNC.trigger()
  logging.info(f"🟢 SYNC FINISHED AT {datetime.now()} 🟢")

while True:
  main()
  sync_interval = os.getenv("SYNC_INTERVAL") or 12
  logging.info(f"🔴 SLEEPING FOR {sync_interval} HOURS BEFORE NEXT SYNC 🔴")
  time.sleep(sync_interval * 60 * 60)