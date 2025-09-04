from services import SpotifyApiClient
from .download_playlist import download_playlist

def download_all_playlists(codec):
  print("Downloading all user playlists, this may take a while...")
  
  print("Fetching user playlists...")
  user_playlists = SpotifyApiClient.fetch_user_playlists()
  print("✅ Fetched user playlists.")

  final_results = {
    "success_count": 0,
    "skip_count": 0,
    "failed_tracks": []
  }

  for pl_index, pl in enumerate(user_playlists):
    results = download_playlist(pl, pl_index, len(user_playlists), codec)

    # update  final results
    final_results["success_count"] += results["success_count"]
    final_results["skip_count"] += results["skip_count"]
    final_results["failed_tracks"].append(results["failed_tracks"])
    
  print("✅ Finished downloading all playlists.")

  # log failed tracks
  print(f"Tracks that failed ({len(final_results["failed_tracks"])}):")
  for tr in results["failed_tracks"].values():
    artist_string = ", ".join([a["name"] for a in tr["track"]["artists"]])
    track_name = tr["track"]["name"]
    print(f"- {artist_string} - {track_name}")