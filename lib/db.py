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
  logger.debug("Setting up database...")
  with open("db/schema.sql", "r") as file:
    db_schema = file.read()
  
  cursor = conn.cursor()
  cursor.executescript(db_schema)
  conn.commit()
  logger.success("Database setup finished.")

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

# 1. stores data about tracks in the tracks table
# 2. stores data about artists in the artists table
# 3. stores track-artist relationships in the track_artist table
def store_tracks(
  conn: sqlite3.Connection,
  track_data: list[dict[str]]
):
  cursor = conn.cursor()

  # 1
  track_count = len(track_data)
  logger.debug(f"Ignore-inserting {track_count} tracks into `tracks` table...")
  cursor.executemany(
    "INSERT OR IGNORE INTO tracks (id, name, cover) VALUES (:id, :name, :cover)",
    track_data
  )
  conn.commit()
  logger.success("Successfully ignore-inserted tracks.")

  # 2, 3
  logger.debug(f"Ignore-inserting tracks into `tracks` table and track-artist relationships into the `track_artist` table...")
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