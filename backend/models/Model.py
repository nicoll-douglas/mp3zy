import sqlite3

class Model:
  """An extensible model class representing a database model/table.

  Attributes:
    _conn (sqlite3.Connection): A connection to the application database.
    _cur (sqlite3.Cursor): The connection's cursor.
    _TABLE (str): The name of the model's table in the database.
  """

  _conn: sqlite3.Connection
  _cur: sqlite3.Cursor
  _TABLE: str

  def __init__(self, conn: sqlite3.Connection):
    self._conn = conn
    self._cur = self._conn.cursor()
  # END __init__
    
  def insert(self, data: dict) -> int | None:
    """Inserts a row into the model's table.

    Args:
      data (dict): Key-value pairs representing the column names and values to insert for them.

    Returns:
      int | None: The ID of the row that was inserted if the table has an integer primary key, else None.
    """
    fields = ", ".join(k for k in data.keys())
    params = tuple(data.values())
    placeholders = ", ".join("?" * len(params))

    self._cur.execute(
      f"INSERT INTO {self._TABLE} ({fields}) VALUES ({placeholders})",
      params
    )
    self._conn.commit()

    return self._cur.lastrowid
  # END insert

# END class Model