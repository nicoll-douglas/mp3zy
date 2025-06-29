import logging, sqlite3
from ..Model import Model

class TrackArtist(Model):
  def __init__(self, conn: sqlite3.Connection):
    super().__init__(conn, "track_artist")
  
  def find_artists(self, track_id: str):
    logging.debug(f"Finding all artists associated with {track_id} from tables {self._TABLE} and artists...")
    self._CONN.row_factory = sqlite3.Connection
    cursor = self._CONN.cursor()
    
    query = f"""
SELECT a.name, a.id
FROM {self._TABLE} AS ta
JOIN artists AS a ON ta.artist_id = a.id
WHERE ta.track_id = ?
"""
    cursor.execute(query, (track_id,))
    rows = cursor.fetchall()

    self._CONN.row_factory = None
    logging.debug("Successfully selected artists.")

    return rows
  
  def sync(self, updated_rows: list[dict[str, str]]):
    logging.debug(f"Applying table diff for table {self._TABLE}...")

    rows = self.select_all()

    db_pairs = {
      (row["track_id"], row["artist_id"]) 
      for row in rows
    }
    updated_pairs = {
      (row["track_id"], row["artist_id"]) 
      for row in updated_rows 
    }

    self.insert_many([
      {"artist_id": a_id, "track_id": t_id}
      for (t_id, a_id) in updated_pairs - db_pairs
    ])
    
    logging.debug(f"Successfully applied table diff.")