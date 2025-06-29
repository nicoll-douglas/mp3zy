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
    logging.info("Syncing all track files with all track entries in the database...")
    locally_unavailable_tracks = m_track.find_locally_unavailable()
    self._sync_track_files([
      {
        "id": row["id"],
        "name": row["name"],
        "cover_source": row["cover_source"],
        "duration_ms": row["duration_ms"],
        "artists": m_track_artist.find_artists(row["id"])
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
    
    for track in track_data:
      cover_save_path = SpotifyApiClient.download_cdn_image(
        track["cover_source"],
        disk.TrackCover.DIR
      )
      
      track_save_path = ytDlpClient.download_track({
        "id": track["id"],
        "name": track["name"],
        "artists": track["artists"],
        "duration_s": track["duration_ms"] / 1000
      })

      if cover_save_path and track_save_path:
        d_track = disk.Track(path=track_save_path)
        d_track.set_metadata({
          "name": track["name"],
          "artists": [a["name"] for a in track["artists"]],
          "cover": cover_save_path
        })

        m_track.set_locally_available(track["id"])