import sqlite3, logging

class Model:
  _CONN: sqlite3.Connection
  _TABLE: str

  def __init__(self, conn: sqlite3.Connection, table: str):
    self._CONN = conn
    self._TABLE = table

  def insert_many(self, new_rows: list[dict[str]]):
    cursor = self._CONN.cursor()
    item_count = len(new_rows)
    
    logging.debug(f"Ignore-inserting {item_count} items into the {self._TABLE} table...")

    columns = ", ".join([d["id"] for d in new_rows])
    params = ", ".join([f":{d["id"]}" for d in new_rows])

    self._CONN.execute("BEGIN")
    cursor.executemany(
      f"INSERT OR IGNORE INTO {self._TABLE} ({columns}) VALUES ({params})",
      new_rows
    )
    self._CONN.commit()

    logging.debug("Successfully inserted items.")

  def select_all(
    self, 
    columns: tuple[str] | str = "*", 
    row_factory = sqlite3.Row
  ):
    if row_factory:
      self._CONN.row_factory = row_factory
    
    cursor = self._CONN.cursor()
    columns_clause = columns if columns == "*" else ", ".join(columns)

    logging.debug(f"Selecting {columns_clause} from the {self._TABLE} table...")

    cursor.execute(f"SELECT {columns_clause} FROM {self._TABLE}")
    rows = cursor.fetchall()

    if row_factory:
      self._CONN.row_factory = None

    logging.debug("Successfully selected playlists.")
    return rows