import sqlite3
from core import logging

class PlaylistTrack:
  conn: sqlite3.Connection
  __TABLE = "playlist_track"

  def __init__(self, conn: sqlite3.Connection):
    self.conn = conn
  
  # stores data about playlist-track relationships in the `playlist_track` table
  def insert_many(self, playlist_id: str, track_ids: list[str]):
    logging.debug(f"Ignore-inserting playlist-track relationships into the `{self.__TABLE}` table...")
    cursor = self.conn.cursor()

    cursor.executemany(
      f"INSERT OR IGNORE INTO {self.__TABLE} (playlist_id, track_id) VALUES (:playlist_id, :track_id)",
      [{ "playlist_id": playlist_id, "track_id": id } for id in track_ids]
    )
    self.conn.commit()

    logging.debug("Successfully inserted playlist-track relationships.")