import sqlite3, logging
from ..Model import Model

class PlaylistTrack(Model):
  def __init__(self, conn: sqlite3.Connection):
    super().__init__(conn, "playlist_track")

  def find_playlist(self, playlist_id: str):
    logging.debug(f"Selecting track_id from the {self._TABLE} table based on playlist_id...")
    
    cursor = self._CONN.cursor()
    cursor.execute(
      f"SELECT track_id FROM {self._TABLE} WHERE playlist_id = ?",
      (playlist_id,)
    )
    rows = cursor.fetchall()

    logging.debug("Successfully selected rows.")

    return rows

  def delete_many(self, params_list: list[tuple[str]]):
    cursor = self._CONN.cursor()
    item_count = len(params_list)
    
    logging.debug(f"Deleting {item_count} items from the {self._TABLE} table...")
    
    cursor.execute("BEGIN")
    cursor.executemany(
      f"DELETE FROM {self._TABLE} WHERE playlist_id = ? AND track_id = ?", 
      params_list
    )
    self._CONN.commit()

    logging.debug("Successfully deleted items.")

  def sync(
    self, 
    playlist_id: str,
    track_ids: list[str]
  ):
    logging.debug(f"Applying table diff for table {self._TABLE}...")

    rows = self.find_playlist(playlist_id)
    
    db_pairs = {(playlist_id, track_id) for (track_id) in rows}
    updated_pairs = {(playlist_id, track_id) for track_id in track_ids }

    self.delete_many([
      (playlist_id, track_id)
      for (playlist_id, track_id) in db_pairs - updated_pairs
    ])

    self.insert_many([
      {"playlist_id": playlist_id, "track_id": track_id }
      for (playlist_id, track_id) in updated_pairs - db_pairs
    ])

    logging.debug("Successfully applied table diff.")