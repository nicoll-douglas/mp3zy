from __future__ import annotations
import logging, os
import disk
import ftp_server
from services import SpotifyApiClient, YtDlpClient

class Sync:
  _SPOTIFY_CLIENT: SpotifyApiClient
  _FTP_MUSIC_MANAGER: ftp_server.MusicManager
  
  def __init__(self, spotify_client: SpotifyApiClient):
    self._SPOTIFY_CLIENT = spotify_client
    self._FTP_MUSIC_MANAGER = ftp_server.MusicManager()
  
  def trigger(self):
    logging.info("Syncing playlist data from the Spotify API for the user...")
    # fetch updated playlist data
    playlist_data = self._SPOTIFY_CLIENT.fetch_user_playlists()
  
    # delete any playlist paths in local if not in updated
    # insert any playlist paths in updated if not in local
    updated_playlists = {disk.models.LocalPlaylist(d["name"]).get_path() for d in playlist_data}
    disk.models.LocalPlaylist.sync_files(updated_playlists)

    # delete any playlist paths in playlists/mobile if not in updated
    # insert any playlist paths in updated if not in playlists/mobile
    updated_playlists = {disk.models.MobilePlaylist(d["name"]).get_path() for d in playlist_data}
    disk.models.MobilePlaylist.sync_files(updated_playlists)

    all_tracks = []

    logging.info("Syncing playlist tracks from the Spotify API for the user...")
    for playlist in playlist_data:
      # fetch updated track data
      tracks = self._SPOTIFY_CLIENT.fetch_playlist_tracks(
        playlist["tracks_href"],
        playlist["name"]
      )

      # delete any track paths in local if not in updated
      # insert any track paths in updated if not in local
      local_pl = disk.models.LocalPlaylist(playlist["name"])
      local_pl.sync_tracks({
        disk.models.Track(t["id"]).get_path() 
        for t in tracks
      })

      # delete any track paths in local if not in updated
      # insert any track paths in updated if not in local
      mobile_pl = disk.models.MobilePlaylist(playlist["name"])
      mobile_pl.sync_tracks({
        ftp_server.MusicManager.get_absolute_track_path(t["id"])
        for t in tracks
      })

      all_tracks.extend(tracks)

    # delete any playlist paths in ftp/playlists if not in updated
    # insert any playlist paths in updated if not in ftp/playlists
    self._FTP_MUSIC_MANAGER.sync_playlists({d["name"] for d in playlist_data})

    # sync tracks
    self._sync_track_files(all_tracks)
    self._FTP_MUSIC_MANAGER.sync_tracks({d["id"] for d in all_tracks})
    
    logging.info("Finished data syncing.")
    self._FTP_MUSIC_MANAGER.quit()

  def _sync_track_files(
    self,
    track_data: list[dict[str]]
  ):
    ytDlpClient = YtDlpClient()    
    total = len(track_data)
    success_count = 0
    fail_count = 0
    
    current_tracks = {t.get_path() for t in disk.models.Track.get_all()}
    incoming_tracks = {
      disk.models.Track(d["id"]).get_path() 
      for d in track_data
    }
    to_delete = current_tracks - incoming_tracks

    for path in to_delete:
      os.remove(path)

    try:
      logging.info(f"Syncing files for {total} tracks...")
      for index, track in enumerate(track_data):
        current_num = index + 1
        track_label = f"{', '.join(track['artists'])} - {track['name']}"
        logging.info(f"Syncing track {current_num} of {total} ({track_label})...")
        
        # download cover image
        logging.info("Downloading cover image...")
        cover_save_path, cover_is_fresh = SpotifyApiClient.download_cdn_track_cover(track["cover_source"])

        # cover download states
        cover_skipped = (not cover_is_fresh) and cover_save_path
        cover_success = cover_is_fresh and cover_save_path
        cover_fail = not cover_save_path

        # log for cover image download status
        if cover_skipped:
          logging.info("Cover image already downloaded.")
        if cover_success:
          logging.info("Successfully downloaded cover image.")
        if cover_fail:
          logging.error("Failed to download cover image.")

        # download track
        logging.info("Downloading track...")
        track_save_path, track_is_fresh = ytDlpClient.download_track({
          "id": track["id"],
          "name": track["name"],
          "artists": track["artists"],
          "duration_s": track["duration_ms"] / 1000
        })

        # track download status
        track_skipped = (not track_is_fresh) and track_save_path
        track_success = track_is_fresh and track_save_path
        track_fail = not track_save_path

        # log for track download status
        if track_skipped:
          logging.info("Track already downloaded.")
        if track_success:
          logging.info("Successfully downloaded track.")
        if track_fail:
          logging.info("Failed to download track.")

        # log and set metadata if there is a save path
        if track_save_path:
          d_track = disk.models.Track(path=track_save_path)
          d_track.set_metadata({
            "name": track["name"],
            "artists": track["artists"],
            "cover": cover_save_path
          }, track["id"])
          
          self._FTP_MUSIC_MANAGER.insert_track(track["id"])
          
          logging.info("Successfully synced track.")
          success_count += 1
        else:
          logging.info("Failed to sync track.")
          fail_count += 1

    except Exception as e:
      raise e
    finally:
      logging.info(f"Successfully synced {success_count} of {total}. {fail_count} failed.")

