import sqlite3

class Model:
  _CONN: sqlite3.Connection
  _TABLE: str

  def __init__(self, conn: sqlite3.Connection, table: str):
    self._CONN = conn
    self._TABLE = table