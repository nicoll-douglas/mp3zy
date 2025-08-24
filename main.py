from dotenv import load_dotenv
load_dotenv()

import threading
from services import SpotifyApiClient, YtDlpClient
from disk import Codec, Playlist, Metadata
import api

def main():
  if __name__ == "__main__":
    threading.Thread(target=api.serve, daemon=True).start()

  auth_url = SpotifyApiClient.build_auth_url()
  print("👉 Open this URL in your browser:", auth_url)

  print("⏳ Waiting for user to authenticate...")
  SpotifyApiClient.auth_event.wait()
  print("✅ Authentication successful.")

  print("⬇️ Fetching user ID...")
  user_id = SpotifyApiClient.fetch_user_id()
  SpotifyApiClient.user_id = user_id
  print("✅ Fetched user ID.")

  print("⬇️ Fetching user playlists...")
  user_playlists = SpotifyApiClient.fetch_user_playlists()
  print("✅ Fetched user playlists.")

  ytdlp_client = YtDlpClient(Codec.FLAC)

  total_playlists = len(user_playlists)

  for pl_index, pl in enumerate(user_playlists):
    playlist_name = pl["name"]
    playlist_id = pl["id"]
    playlist_items_url = SpotifyApiClient.playlist_items_url(playlist_id)

    print(f"⬇️ Fetching playlist tracks for playlist '{playlist_name}' ({pl_index + 1}/{total_playlists})...")
    playlist_items = SpotifyApiClient.fetch_playlist_items(playlist_items_url)
    print("✅ Fetched playlist tracks.")

    total_tracks = len(playlist_items)
    skip_count = 0
    success_count = 0
    fail_count = 0
    
    for pl_item_index, pl_item in enumerate(playlist_items):
      track_name = pl_item["track"]["name"]
      is_not_track = pl_item["track"]["type"] != "track"
      is_local = pl_item["is_local"]
      
      print(f"⬇️ Downloading track '{track_name}' ({pl_item_index + 1}/{total_tracks})...")

      if is_local or is_not_track:
        print(f"⏩ Download skipped, track is either local or an episode.")
        skip_count += 1
        continue

      track_number = pl_item["track"]["track_number"]      
      track_artists = [a["name"] for a in pl_item["track"]["artists"]]
      album_name = pl_item["track"]["album"]["name"]
      album_id = pl_item["track"]["album"]["id"]
      disc_number=pl_item["track"]["disc_number"]
      duration_ms = pl_item["track"]["duration_ms"]
      cover_url = pl_item["track"]["album"]["images"][0]["url"]
      release_date = pl_item["track"]["album"]["release_date"]

      cover_path, _ = SpotifyApiClient.download_cdn_track_cover(
        url=cover_url,
        album_id=album_id
      )

      track_path, track_is_fresh = ytdlp_client.download_track(
        number=track_number,
        artists=track_artists,
        name=track_name,
        album=album_name,
        disc_number=disc_number,
        duration_ms=duration_ms
      )

      if not track_path:
        print("⚠️ Download Failed.")
        fail_count += 1
        continue

      if not track_is_fresh:
        print("⏩ Download skipped, track is already downloaded.")
        skip_count += 1
        continue

      print("✅ Successfully downloaded track.")

      print("🔁 Updating track metadata...")
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
      success_count += 1
      print("✅ Updated metadata.")

    print(f"✅ Finished downloading playlist tracks ({success_count} successful, {skip_count} skipped, {fail_count} failed).")

    print(f"🔁 Creating playlist file for playlist '{playlist_name}'...")
    p = Playlist(
      name=playlist_name,
      directory=Playlist.DESKTOP_PL_DIR
    )
    p.path = p.build_path()
    p.write(playlist_items)
    print("✅ Playlist file created.")
    print("ℹ️ Finished downloading playlist")
    
main()