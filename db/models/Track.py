import sqlite3, logging

class Track:
  _conn: sqlite3.Connection
  __TABLE = "tracks"
  
  def __init__(self, conn: sqlite3.Connection):
    self._conn = conn

  def insert_many(self, tracks: list[dict[str, str]]):
    cursor = self._conn.cursor()
    track_count = len(tracks)

    logging.debug(f"Ignore-inserting {track_count} tracks into `{self.__TABLE}` table...")
    cursor.executemany(
      f"INSERT OR IGNORE INTO {self.__TABLE} (id, name, cover_source) VALUES (:id, :name, :cover_source)",
      tracks
    )
    self._conn.commit()

    logging.debug("Successfully ignore-inserted tracks.")
  
  def find_all_locally_unavailable(self) -> list[dict[str]]:
    self._conn.row_factory = sqlite3.Row
    cursor = self._conn.cursor()

    logging.debug("Selecting all tracks where `locally_available` is `false`...")
    cursor.execute(f"SELECT * FROM {self.__TABLE} WHERE locally_available = ?", (0,))
    rows = cursor.fetchall()

    logging.debug("Successfully selected tracks.")

    self._conn.row_factory = None
    
    return rows

  def set_locally_available(self, track_id: str):
    cursor = self._conn.cursor()
    
    logging.debug(f"Setting `locally_available` to `true` for track: {track_id}")
    cursor.execute(
      f"UPDATE {self.__TABLE} SET locally_available = ? WHERE id = ?",
      (1, track_id)
    )
    self._conn.commit()
    logging.debug(f"Successfully updated track.")