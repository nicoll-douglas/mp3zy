from __future__ import annotations
import logging, os
import disk
import ftp_server
from services import SpotifyApiClient, YtDlpClient

class Sync:
  _SPOTIFY_CLIENT: SpotifyApiClient
  _FTP_MUSIC_MANAGER: ftp_server.MusicManager
  
  def __init__(
    self, 
    spotify_client: SpotifyApiClient
  ):
    self._SPOTIFY_CLIENT = spotify_client
    self._FTP_MUSIC_MANAGER = ftp_server.MusicManager()
  
  def trigger(self):
    logging.info("Syncing data from the Spotify API for the user...")
    playlist_data = self._SPOTIFY_CLIENT.fetch_user_playlists()
    self._sync_disk_playlists(playlist_data)

    all_tracks = []
    for playlist in playlist_data:
      playlist_tracks = self._sync_disk_playlist_tracks(playlist)
      all_tracks.extend(playlist_tracks)

    self._FTP_MUSIC_MANAGER.sync_playlists({
      d["name"] for d in playlist_data
    })

    self._sync_tracks(all_tracks)

    logging.info("Finished syncing.")
    self._FTP_MUSIC_MANAGER.quit()

  def _sync_disk_playlists(self, incoming_playlists: list[dict[str]]):
    logging.info("Syncing incoming playlist data with playlist state on disk...")

    logging.debug("Syncing local playlist state on disk...")
    updated_playlists = {
      disk.models.LocalPlaylist(d["name"]).get_path() 
      for d in incoming_playlists
    }
    disk.models.LocalPlaylist.sync_files(updated_playlists)
    logging.debug("Synced local playlist state.")

    logging.debug("Syncing mobile playlist state on disk...")
    updated_playlists = {
      disk.models.MobilePlaylist(d["name"]).get_path() 
      for d in incoming_playlists
    }
    disk.models.MobilePlaylist.sync_files(updated_playlists)
    logging.debug("Synced mobile playlist state.")
    
    logging.info("Successfully synced playlists on disk.")

  def _sync_disk_playlist_tracks(self, playlist: dict[str]):
    logging.info(f"Syncing playlist tracks for playlist '{playlist["name"]}' with playlist files on disk...")
    tracks = self._SPOTIFY_CLIENT.fetch_playlist_tracks(
      playlist["tracks_href"],
      playlist["name"]
    )

    logging.debug("Syncing local playlists on disk...")
    local_pl = disk.models.LocalPlaylist(playlist["name"])
    local_pl.sync_tracks({
      disk.models.Track(t["id"]).get_path() 
      for t in tracks
    })
    logging.debug("Synced local playlists.")

    logging.debug("Syncing mobile playlists on disk...")
    mobile_pl = disk.models.MobilePlaylist(playlist["name"])
    mobile_pl.sync_tracks({
      ftp_server.MusicManager.get_absolute_track_path(t["id"])
      for t in tracks
    })
    logging.debug("Synced mobile playlists")

    logging.info("Successfully synced playlist files.")
    return tracks

  def _sync_tracks(self, incoming_tracks: list[dict[str]]):
    ytDlpClient = YtDlpClient()   
    total = len(incoming_tracks)
    logging.info(f"Syncing tracks on disk and on FTP server for {total} incoming tracks...")

    # delete necessary tracks on ftp
    current_track_filenames = self._FTP_MUSIC_MANAGER.list_tracks()
    incoming_track_filenames = {
      ftp_server.MusicManager.get_track_filename(t["id"])
      for t in incoming_tracks
    }
    logging.info(f"Removing {len(to_delete)} tracks from FTP server...")
    to_delete = current_track_filenames - incoming_track_filenames
    for filename in to_delete:
      self._FTP_MUSIC_MANAGER.remove_track(filename)
    logging.info("Finished removing.")

    # delete necessary tracks on disk
    logging.info(f"Removing {len(to_delete)} tracks from disk...")
    current_track_paths = {t.get_path() for t in disk.models.Track.get_all()}
    incoming_track_paths = {
      disk.models.Track(d["id"]).get_path() 
      for d in incoming_tracks
    }
    incoming_track_map = {
      track["id"]: track
      for track in incoming_tracks
    }
    to_delete = current_track_paths - incoming_track_paths
    to_insert = incoming_track_paths - current_track_paths
    for path in to_delete:
      os.remove(path)
    logging.info("Finished removing.")

    # write necessary tracks to disk and FTP
    success_count = 0
    fail_count = 0
    to_insert_total = len(to_insert)

    logging.info(f"Writing {to_insert_total} tracks to disk and FTP server...")
    try:
      for index, track_id in enumerate(to_insert):
        track = incoming_track_map[track_id]
        current_num = index + 1
        track_label = f"{', '.join(track['artists'])} - {track['name']}"

        logging.info(f"Syncing track {current_num} of {to_insert_total} ({track_label})...")

        cover_save_path, _ = SpotifyApiClient.download_cdn_track_cover(track["cover_source"])

        track_save_path, _ = ytDlpClient.download_track({
          "id": track["id"],
          "name": track["name"],
          "artists": track["artists"],
          "duration_s": track["duration_ms"] / 1000
        })

        if track_save_path:
          d_track = disk.models.Track(path=track_save_path)
          d_track.set_metadata({
            "name": track["name"],
            "artists": track["artists"],
            "cover": cover_save_path
          }, track["id"])
          self._FTP_MUSIC_MANAGER.write_track(track["id"])
          
          logging.info("Successfully wrote track to disk and FTP server.")
          success_count += 1
        else:
          logging.info("Failed to sync disk track.")
          fail_count += 1
    except Exception as e:
      raise e
    finally:
      logging.info("Finished syncing tracks.")
      logging.info(f"Successfully synced {success_count} of {to_insert_total} tracks. {fail_count} failed.")