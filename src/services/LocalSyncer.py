from __future__ import annotations
from db import *
import sqlite3, logging
from services import SpotifyApiClient
import disk

class LocalSyncer:
  def sync_playlists(
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

  def sync_playlist_tracks(
    db_conn: sqlite3.Connection,
    spotify_client: SpotifyApiClient,
    playlist_data: dict[str],
  ):
    logging.info("Syncing track data in the database and track cover images with the Spotify API...")
    m_track = models.Track(db_conn)
    m_artist = models.Artist(db_conn)
    m_track_artist = models.TrackArtist(db_conn)
    m_playlist_track = models.PlaylistTrack(db_conn)
    
    for playlist in playlist_data:
      track_data = spotify_client.fetch_playlist_tracks(
        playlist["tracks_href"], 
        playlist["name"]
      )

      updated_track_rows = [
        {
          "id": d["id"],
          "name": d["name"],
          "cover_source": d["cover_source"]
        }
        for d in track_data
      ]
      m_track.sync(updated_track_rows)

      m_playlist_track.sync(
        playlist["id"], 
        [d["id"] for d in track_data]
      )

      m_artist.sync([d["artists"] for d in track_data])

      for track in track_data:
        m_track_artist.sync(
          track["id"], 
          [d["id"] for d in track["artists"]]
        )
      
      SpotifyApiClient.download_cdn_images(
        [d["cover_source"] for d in track_data], 
        disk.TrackCover.DIR
      )

    logging.info("Finished syncing.")