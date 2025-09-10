from __future__ import annotations
from .store_playlist import store_playlist
from .download_all_playlist_items import download_all_playlist_items
from models.disk import Codec

def download_playlist(pl, pl_index, total_pl, codec: Codec):
  pl_name = pl["name"]

  print(f"Downloading playlist '{pl_name}' ({pl_index + 1}/{total_pl})...")

  results = download_all_playlist_items(pl, codec)
  pl_items = results["items"]

  store_playlist(pl_name, pl_items)

  print(f"✅ Finished downloading playlist '{pl_name}'.")

  return results