import sqlite3, logging
from ..Model import Model

class Playlist(Model):
  def __init__(self, conn: sqlite3.Connection):
    super().__init__(conn, "playlists")
  
  def update_many(self, params_list: list[dict[str, str]]):
    item_count = len(params_list)
    cursor = self._CONN.cursor()
    
    logging.debug(f"Updating {item_count} items in the {self._TABLE} table...")

    self._CONN.execute("BEGIN")
    cursor.executemany(
      f"UPDATE {self._TABLE} SET name = :name, cover_source = :cover_source WHERE id = :id", 
      params_list
    )
    self._CONN.commit()

    logging.debug("Successfully updated items.")

  def delete_many(self, params_list: list[str]):
    cursor = self._CONN.cursor()
    item_count = len(params_list)
    
    logging.debug(f"Deleting {item_count} items from the {self._TABLE} table...")

    self._CONN.execute("BEGIN")
    cursor.executemany(
      f"DELETE FROM {self._TABLE} WHERE id = ?", 
      params_list
    )
    self._CONN.commit()

    logging.debug("Successfully deleted items")
  
  def sync(self, new_table: list[dict[str]]):
    logging.info("Syncing database with new playlist data...")
    logging.debug(f"Computing and applying table diff for table {self._TABLE}...")

    rows = self.select_all()

    row_map = {row["id"]: row for row in rows}
    new_table_map = {row["id"]: row for row in new_table}

    db_ids = set(row_map.keys())
    updated_ids = set(new_table_map.keys())

    self.update_many([
      new_table_map[_id]
      for _id in (db_ids & updated_ids)
      if row_map[_id] != new_table_map[_id]
    ])

    self.delete_many([_id for _id in db_ids - updated_ids])

    self.insert_many([
      new_table_map[_id]
      for _id in updated_ids - db_ids
    ])

    logging.debug(f"Successfully applied table diff.")
    logging.info("Successfully synced database.")