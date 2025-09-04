from __future__ import annotations
from services import SpotifyApiClient, YtDlpClient
from media import Codec, Metadata

def download_playlist_item(item, item_index, total_items, codec: Codec):
  # extract info from api data
  track_name = item["track"]["name"]
  track_artists = [a["name"] for a in item["track"]["artists"]]
  is_not_track = item["track"]["type"] != "track"
  is_local = item["is_local"]
  
  print(f"Downloading track '{track_name}' ({item_index + 1}/{total_items})...")

  # check if track should be downloaded
  if is_local or is_not_track:
    print(f"Download skipped, track is either local or an episode.")
    return 0

  # extract more info
  track_number = item["track"]["track_number"]
  album_name = item["track"]["album"]["name"]
  album_id = item["track"]["album"]["id"]
  disc_number=item["track"]["disc_number"]
  duration_ms = item["track"]["duration_ms"]
  cover_url = item["track"]["album"]["images"][0]["url"]
  release_date = item["track"]["album"]["release_date"]

  # download album cover
  print("Downloading album cover...")
  cover_path, cover_is_fresh = SpotifyApiClient.download_cdn_track_cover(
    url=cover_url,
    album_id=album_id
  )

  # logging
  if not cover_path:
    print("⚠️ Cover download Failed.")
  elif not cover_is_fresh:
    print("⏩ Cover download skipped, cover is already downloaded.")
  else:
    print("✅ Successfully downloaded album cover.")

  # download audio file
  print("Downloading audio...")
  ytdlp_client = YtDlpClient(codec)
  track_path, track_is_fresh = ytdlp_client.download_track(
    number=track_number,
    artists=track_artists,
    name=track_name,
    album=album_name,
    disc_number=disc_number,
    duration_ms=duration_ms
  )

  # check if audio download failed
  if not track_path:
    print("⚠️ Audio download Failed.")
    return -1

  # check if audio download was skipped
  if not track_is_fresh:
    print("⏩ Audio download skipped, file is already downloaded.")
    return 0

  print("✅ Successfully downloaded audio.")

  # add metadata to audio file
  print("Updating audio file metadata...")
  meta = Metadata(
    cover_path=cover_path,
    track_name=track_name,
    track_artists=track_artists,
    album=album_name,
    track_number=track_number,
    disc_number=disc_number,
    release_date=release_date,
    duration_ms=duration_ms
  )
  meta.set_on_flac(track_path)
  print("✅ Updated metadata.")

  # success
  print("✅ Successfully downloaded track.")
  return 1
