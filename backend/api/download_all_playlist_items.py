from __future__ import annotations
from services import SpotifyApiClient
from .download_playlist_item import download_playlist_item
from models.disk import Codec

def download_all_playlist_items(pl, codec: Codec):
  # extract info from api data
  pl_name = pl["name"]
  pl_id = pl["id"]
  pl_items_url = SpotifyApiClient.playlist_items_url(pl_id)

  # get playlist items from api with url
  print(f"Fetching playlist tracks...")
  pl_items = SpotifyApiClient.fetch_playlist_items(pl_items_url)
  print("✅ Fetched playlist tracks.")

  print(f"Downloading playlist tracks for playlist '{pl_name}'...")

  final_result = {
    "success_count": 0,
    "skip_count": 0,
    "failed_tracks": {},
    "items": pl_items
  }
  
  # loop over playlist items and download
  for pl_item_index, pl_item in enumerate(pl_items):
    result = download_playlist_item(
      item=pl_item, 
      item_index=pl_item_index, 
      total_items=len(pl_items),
      codec=codec
    )
    track_id = pl_item["track"]["id"]

    # update final download results
    if result == 0:
      final_result["skip_count"] += 1
    elif result == -1:
      already_failed = track_id in final_result["failed_tracks"]
      if not already_failed:
        final_result["failed_tracks"][track_id] = pl_item
    else:
      final_result["success_count"] += 1

  print(f"✅ Finished downloading playlist tracks for playlist '{pl_name}' ({final_result["success_count"]} successful, {final_result["skip_count"]} skipped, {len(final_result["failed_tracks"])} failed).")

  return final_result