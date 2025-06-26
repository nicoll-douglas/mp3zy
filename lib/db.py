import sqlite3
from . import logger

# connect to the database
def connect():
  db_path = "db/app.db"
  logger.debug(f"Connecting to database `{db_path}`")
  conn = sqlite3.connect(db_path)
  logger.success(f"Successfully connected to database.")
  return conn

# create the database tables in the schema
def create_tables(conn: sqlite3.Connection):
  logger.debug("Creating tables...")
  with open("db/schema.sql", "r") as file:
    db_schema = file.read()
  
  cursor = conn.cursor()
  cursor.executescript(db_schema)
  conn.commit()
  logger.success("Finished creating tables.")

# store data about the user's playlists in the playlists table
def store_user_playlists(
  conn: sqlite3.Connection, 
  playlist_data: list[dict[str, str]]
):
  cursor = conn.cursor()
  playlist_count = len(playlist_data)
  logger.debug(f"Replace-inserting {playlist_count} user playlists into `playlists` table...")

  cursor.executemany(
    "INSERT OR REPLACE INTO playlists (id, name, cover) VALUES (:id, :name, :cover)",
    playlist_data
  )
  conn.commit()
  
  logger.success("Successfully replace-inserted playlists.")

# stores data about tracks in the tracks table
def store_tracks(
  conn: sqlite3.Connection,
  track_data: list[dict[str]]
):
  cursor = conn.cursor()
  track_count = len(track_data)

  logger.debug(f"Ignore-inserting {track_count} tracks into `tracks` table...")
  cursor.executemany(
    "INSERT OR IGNORE INTO tracks (id, name, cover) VALUES (:id, :name, :cover)",
    track_data
  )
  conn.commit()
  logger.success("Successfully ignore-inserted tracks.")

#  stores data about artists in the artists table and track-artist relationships in the track_artist table
def store_track_artists(
  conn: sqlite3.Connection,
  track_data: list[dict[str]]
):
  cursor = conn.cursor()
  logger.debug(f"Ignore-inserting artists into `artists` table and track-artist relationships into the `track_artist` table...")

  for track in track_data:
    cursor.executemany(
      "INSERT OR IGNORE INTO artists (id, name) VALUES (:id, :name)",
      track["artists"]
    )
    conn.commit()
    
    cursor.executemany(
      "INSERT OR IGNORE INTO track_artist (track_id, artist_id) VALUES (?, ?)",
      [(a["id"], track["id"]) for a in track["artists"]]
    )
    conn.commit()

  logger.success("Successfully inserted tracks and track-artist relationships.")

# stores data about playlist-track relationships in the `playlist_track` table
def store_playlist_tracks(
  conn: sqlite3.Connection,
  track_data: list[dict[str]],
  playlist_id: str
):
  logger.debug(f"Ignore-inserting playlist-track relationships into the `playlist_track` table...")
  cursor = conn.cursor()

  cursor.executemany(
    "INSERT OR IGNORE INTO playlist_track (playlist_id, track_id) VALUES (?, ?)",
    [(playlist_id, t["id"]) for t in track_data]
  )

  logger.success("Successfully inserted playlist-track relationships.")

# gets all tracks from the database where `locally_available` is false
# => tracks that haven't been downloaded locally with `yt-dlp` yet
def get_locally_unavailable_tracks(
  conn: sqlite3.Connection,
):
  cursor = conn.cursor()
  logger.debug(f"Selecting all tracks that aren't available locally...")
  cursor.execute(
    "SELECT * FROM tracks WHERE locally_available = ?",
    (False)
  )