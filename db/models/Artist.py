import logging, sqlite3
from db.Model import Model

class Artist(Model):
  def __init__(self, conn: sqlite3.Connection):
    super().__init__(conn, "artists")

  def apply_table_diff(self, updated_rows: list[dict[str, str]]):
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