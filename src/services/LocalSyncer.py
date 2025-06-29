from __future__ import annotations
from db import *
import sqlite3, logging
from services import SpotifyApiClient, YtDlpClient
import disk

class LocalSyncer:
  def sync_playlists(
    self,
    db_conn: sqlite3.Connection, 
    spotify_client: SpotifyApiClient
  ):
    logging.info("Syncing playlist data in the database and playlist cover images with the Spotify API...")
    playlist_data = spotify_client.fetch_user_playlists()
    updated_rows = [
      { 
        "id": d["id"],
        "name": d["name"],
        "cover_source": d["cover_source"]
      }
      for d in playlist_data
    ]

    playlist = models.Playlist(db_conn)
    playlist.sync(updated_rows)

    SpotifyApiClient.download_cdn_images(
      [d["cover_source"] for d in updated_rows],
      disk.PlaylistCover.DIR
    )
    logging.info("Finished syncing.")
    
    return playlist_data

  def sync_tracks(
    self,
    db_conn: sqlite3.Connection,
    spotify_client: SpotifyApiClient,
    playlist_data: dict[str],
  ):
    logging.info("Syncing track data from the Spotify API with database...")
    m_track = models.Track(db_conn)
    m_artist = models.Artist(db_conn)
    m_track_artist = models.TrackArtist(db_conn)
    m_playlist_track = models.PlaylistTrack(db_conn)
    
    for playlist in playlist_data:
      # fetch
      track_data = spotify_client.fetch_playlist_tracks(
        playlist["tracks_href"], 
        playlist["name"]
      )

      # start update db
      m_track.sync([
        {
          "id": d["id"],
          "name": d["name"],
          "cover_source": d["cover_source"]
        }
        for d in track_data
      ])

      m_artist.sync([d["artists"] for d in track_data])

      m_playlist_track.sync(
        playlist["id"], 
        [d["id"] for d in track_data]
      )

      for track in track_data:
        m_track_artist.sync(
          track["id"], 
          [d["id"] for d in track["artists"]]
        )
      # finish update db

    logging.info("Finished data syncing.")
    logging.info("Syncing all track files with all track entries in the database...")

    # query entire database and sync tracks
    locally_unavailable_tracks = m_track.find_locally_unavailable()
    self._sync_track_files(db_conn, [
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

  def _sync_track_files(
    self,
    db_conn: sqlite3.Connection,
    track_data: list[dict[str]]
  ):
    ytDlpClient = YtDlpClient()
    m_track = models.Track(db_conn)
    
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