import logging, sqlite3
from db.Model import Model

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
  
  def apply_table_diff(
    self,
    track_id: str,
    artists_ids: list[str]
  ):
    logging.debug(f"Applying table diff for table {self._TABLE}...")

    rows = self.find_artists(track_id)

    db_pairs = {(track_id, row["id"]) for row in rows}
    updated_pairs = {(track_id, artist_id) for artist_id in artists_ids }

    self.insert_many([
      {"artist_id": artist_id, "track_id": track_id}
      for (artist_id, track_id) in updated_pairs - db_pairs
    ])
    
    logging.debug(f"Successfully applied table diff.")