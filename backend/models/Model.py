import db
import sqlite3

class Model:
  _conn: sqlite3.Connection
  _cur: sqlite3.Cursor
  _TABLE: str

  def __init__(self, conn):
    self._conn = conn
    self._cur = self._conn.cursor()

  def insert(self, data: dict):
    fields = ", ".join(k for k in data.keys())
    values = tuple(data.values())
    placeholders = ", ".join("?" * len(values))

    self._cur.execute(
      f"INSERT INTO {self._table} ({fields}) VALUES ({placeholders})",
      values
    )

    return self._cur.lastrowid
  
  def update(self, where: dict, data: dict):
    assignments = ", ".join([f"{k}=?" for k in data.keys()])
    where_clause = " AND ".join(f"{k}=?" for k in where.keys())
    values = list(data.values()) + list(where.values())

    self._cur.execute(f"UPDATE {self._table} SET {assignments} WHERE {where_clause}", values)