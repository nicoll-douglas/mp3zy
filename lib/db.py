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