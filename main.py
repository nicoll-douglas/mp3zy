from __future__ import annotations

# bootstrap
import bootstrap

# imports

from db import *
from services import SpotifyApiClient, SpotifySync
from utils.helpers import attempt_step

# Step 1: Set up database and authenticate with Spotify API
# Expected Results:
#   - A database connection and tables created
#   - A Spotify client object authenticated with an access token

def setup():
  db = Db()
  conn = db.connect()
  db.setup(conn)

  spotify_client = SpotifyApiClient()

  return conn, spotify_client

DB_CONN, SPOTIFY_CLIENT = attempt_step(("Setup", 1), setup)

# Step 2: Query Spotify API and sync user playlist data (not tracks) in the database and on disk
# Pseudocode:
#   - FOREACH incoming.playlists UPDATE db.playlist IF IN incoming.playlists
#   - FOREACH incoming.playlists INSERT incoming.playlist IF NOT IN db.playlists
#   - FOREACH db.playlists DELETE db.playlist IF NOT IN incoming.playlists
#   - FOREACH db.playlists DOWNLOAD db.playlist.cover IF NOT IN disk.playlist_covers
# Notes:
#   - If some cover downloads fail then the images on disk will not be synced with the expected from the database

def sync_user_playlist_data():
  syncer = SpotifySync(DB_CONN, SPOTIFY_CLIENT)
  playlist_data = syncer.sync_playlists()
  return playlist_data

playlist_data = attempt_step(
  ("Sync User Playlist Data", 2), 
  sync_user_playlist_data
)

# Step 3: Query Spotify API and sync playlist track data in the database and on disk
# Pseudocode:
#   - FOREACH incoming.tracks INSERT incoming.track IF NOT IN db.tracks
#   - FOREACH incoming.tracks INSERT incoming.track.artists IF NOT IN db.artists
#   - FOREACH incoming.tracks INSERT incoming.track.track_artists IF NOT IN db.track_artists
#   - FOREACH db.playlist_tracks DELETE db.playlist_track IF NOT IN incoming.playlist_tracks
#   - FOREACH incoming.playlist_tracks INSERT incoming.playlist_track IF NOT IN db.playlist_tracks
#   - FIND tracks IN db.tracks WHERE db.track.is_locally_unavailable (no cover or no mp3)
#   - FOREACH track DOWNLOAD track.cover IF NOT IN disk.track_covers
#   - FOREACH track DOWNLOAD track IF NOT IN disk.tracks
#   - FOREACH track IF track.downloaded AND track.cover.downloaded SET track.locally_available
# Notes:
#   - If some downloads fail then the images and track files on disk will not be synced with the database
#   - Only if both track and cover downloads succeed then track metadata is set and locally_available is set to true

def sync_playlist_track_data():
  syncer = SpotifySync(DB_CONN, SPOTIFY_CLIENT)
  syncer.sync_tracks(playlist_data)

attempt_step(
  ("Sync Playlist Track Data", 3),
  sync_playlist_track_data
)