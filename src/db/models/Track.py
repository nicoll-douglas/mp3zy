import sqlite3, logging
from ..Model import Model

class Track(Model):
  def __init__(self, conn: sqlite3.Connection):
    super().__init__(conn, "tracks")
  
  def find_locally_unavailable(self):
    self._CONN.row_factory = sqlite3.Row
    cursor = self._CONN.cursor()

    logging.debug("Selecting all tracks where `locally_available` is `false`...")
    cursor.execute(f"SELECT * FROM {self._TABLE} WHERE locally_available = ?", (0,))
    rows = cursor.fetchall()

    logging.debug("Successfully selected tracks.")

    self._CONN.row_factory = None
    
    return rows

  def set_locally_available(self, track_id: str):
    cursor = self._CONN.cursor()
    
    logging.debug(f"Setting `locally_available` to `true` for track: {track_id}")
    cursor.execute(
      f"UPDATE {self._TABLE} SET locally_available = ? WHERE id = ?",
      (1, track_id)
    )
    self._CONN.commit()
    logging.debug(f"Successfully updated track.")
    
  def sync(self, updated_rows: list[dict[str]]):
    logging.debug(f"Applying table diff for table {self._TABLE}...")

    rows = self.select_all(("id"))
    updated_row_map = {row["id"]: row for row in updated_rows}

    db_ids = {row["id"] for row in rows}
    updated_ids = set(updated_row_map.keys())

    self.insert_many([
      updated_row_map[_id]
      for _id in updated_ids - db_ids
    ])
    
    logging.debug(f"Successfully applied table diff.")