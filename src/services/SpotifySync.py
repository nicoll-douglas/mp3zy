from __future__ import annotations
from db import *
import sqlite3, logging
from services import SpotifyApiClient, YtDlpClient
import disk

class SpotifySync:
  _DB_CONN: sqlite3.Connection
  _SPOTIFY_CLIENT: SpotifyApiClient
  
  def __init__(
    self,
    db_conn: sqlite3.Connection, 
    spotify_client: SpotifyApiClient
  ):
    self._DB_CONN = db_conn
    self._SPOTIFY_CLIENT = spotify_client
  
  def sync_playlists(self):
    logging.info("Syncing playlist data from the Spotify API with database...")

    playlist_data = self._SPOTIFY_CLIENT.fetch_user_playlists()
    updated_rows = [
      { 
        "id": d["id"],
        "name": d["name"],
        "cover_source": d["cover_source"]
      }
      for d in playlist_data
    ]

    playlist = models.Playlist(self._DB_CONN)
    playlist.sync(updated_rows)
    
    logging.info("Finished data syncing.")
    logging.info("Syncing all playlist cover image files with updated entries...")

    SpotifyApiClient.download_cdn_images(
      [d["cover_source"] for d in playlist_data],
      disk.PlaylistCover.DIR
    )
    
    logging.info("Finished file syncing.")
    
    return playlist_data

  def sync_tracks(
    self,
    playlist_data: list[dict[str, str]],
  ):
    m_track = models.Track(self._DB_CONN)
    m_track_artist = models.TrackArtist(self._DB_CONN)

    logging.info("Syncing track data from the Spotify API with database...")
    self._sync_track_data(playlist_data)
    logging.info("Finished data syncing.")

    # query entire database and sync tracks
    logging.info("Syncing all track files and covers...")
    locally_unavailable_tracks = m_track.find_locally_unavailable()
    self._sync_track_files([
      {
        "id": row["id"],
        "name": row["name"],
        "cover_source": row["cover_source"],
        "duration_ms": row["duration_ms"],
        "artists": [
          a["name"]
          for a in m_track_artist.find_artists(row["id"])
        ]
      }
      for row in locally_unavailable_tracks
    ])

    logging.info("Finished file syncing.")

  def _sync_track_data(
    self,
    playlist_data: list[dict[str, str]],
  ):
    logging.info("Syncing track data...")
    
    m_track = models.Track(self._DB_CONN)
    m_artist = models.Artist(self._DB_CONN)
    m_track_artist = models.TrackArtist(self._DB_CONN)
    m_playlist_track = models.PlaylistTrack(self._DB_CONN)

    for playlist in playlist_data:
      track_data = self._SPOTIFY_CLIENT.fetch_playlist_tracks(
        playlist["tracks_href"], 
        playlist["name"]
      )

      m_track.sync([
        {
          "id": d["id"],
          "name": d["name"],
          "cover_source": d["cover_source"],
          "duration_ms": d["duration_ms"]
        }
        for d in track_data
      ])

      m_artist.sync([
        a
        for t in track_data
        for a in t["artists"]
      ])

      m_playlist_track.sync(
        playlist["id"], 
        [d["id"] for d in track_data]
      )

      m_track_artist.sync([
        {
          "track_id": t["id"],
          "artist_id": a["id"]
        }
        for t in track_data
        for a in t["artists"]
      ])

    logging.info("Synced successfully.")

  def _sync_track_files(
    self,
    track_data: list[dict[str]]
  ):
    ytDlpClient = YtDlpClient()
    m_track = models.Track(self._DB_CONN)
    
    total = len(track_data)
    success_count = 0
    fail_count = 0

    try:
      logging.info(f"Syncing files for {total} tracks...")
      for index, track in enumerate(track_data):
        current_num = index + 1
        track_label = f"{", ".join(track['artists'])} - {track['name']}"
        logging.info(f"Syncing track {current_num} of {total} ({track_label})...")
        
        # download cover image
        logging.info("Downloading cover image...")
        cover_save_path, cover_is_fresh = SpotifyApiClient.download_cdn_image(
          track["cover_source"],
          disk.TrackCover.DIR
        )

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

        # sync status
        track_is_in_sync = cover_save_path and track_save_path

        # log and act based on results
        if track_is_in_sync:
          d_track = disk.Track(path=track_save_path)
          d_track.set_metadata({
            "name": track["name"],
            "artists": track["artists"],
            "cover": cover_save_path
          })
          m_track.set_locally_available(track["id"])
          logging.info("Successfully synced track.")
          success_count += 1
        else:
          logging.info("Failed to sync track.")
          fail_count += 1
    except Exception as e:
      raise e
    finally:
      logging.info(f"Successfully synced {success_count} of {total}. {fail_count} failed.")

