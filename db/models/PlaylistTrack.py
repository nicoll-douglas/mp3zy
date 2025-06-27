import sqlite3, logging

class PlaylistTrack:
  _conn: sqlite3.Connection
  __TABLE = "playlist_track"

  def __init__(self, conn: sqlite3.Connection):
    self._conn = conn
  
  # stores data about playlist-track relationships in the `playlist_track` table
  def insert_many(self, playlist_id: str, track_ids: list[str]):
    logging.debug(f"Ignore-inserting playlist-track relationships into the `{self.__TABLE}` table...")
    cursor = self._conn.cursor()

    cursor.executemany(
      f"INSERT OR IGNORE INTO {self.__TABLE} (playlist_id, track_id) VALUES (:playlist_id, :track_id)",
      [{ "playlist_id": playlist_id, "track_id": id } for id in track_ids]
    )
    self._conn.commit()

    logging.debug("Successfully inserted playlist-track relationships.")