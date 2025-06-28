# bootstrap
import bootstrap

# imports
from __future__ import annotations

from db import *
from services import SpotifyApiClient, LocalSyncer
from utils.helpers import attempt_step

# Step 1: Set up database and authenticate with Spotify API
def setup():
  db = Db()
  conn = db.connect()
  db.setup(conn)

  spotify_client = SpotifyApiClient()

  return conn, spotify_client

DB_CONN, SPOTIFY_CLIENT = attempt_step(("Setup", 1), setup)

# Step 2: Query Spotify API and sync user playlist data in the database and on disk
def sync_user_playlist_data():
  syncer = LocalSyncer()
  playlist_data = syncer.sync_playlists(DB_CONN, SPOTIFY_CLIENT)
  return playlist_data

playlist_data = attempt_step(
  ("Sync User Playlist Data", 2), 
  sync_user_playlist_data
)

# Step 3: Query Spotify API and sync playlist track data in the database and on disk
def sync_playlist_track_data():
  syncer = LocalSyncer()
  syncer.sync_playlist_tracks(DB_CONN, SPOTIFY_CLIENT, playlist_data)

attempt_step(
  ("Sync Playlist Track Data", 3),
  sync_playlist_track_data
)