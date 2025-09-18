import db
import sqlite3

class Model:
  _conn: sqlite3.Connection
  _cur: sqlite3.Cursor
  _TABLE: str

  def __init__(self, conn):
    self._conn = conn
    self._cur = self._conn.cursor()

  def _build_where(self, params: dict):
    statement = "WHERE " + "AND ".join(f"{k}=?" for k in params.keys())
    values = tuple(params.values())
    return statement, values

  def _build_set(self, params: dict):
    statement = "SET " + ", ".join([f"{k}=?" for k in params.keys()])
    values = tuple(params.values())
    return statement, values

  def _build_select(self, fields: list | str | None = None):
    if fields is None or fields == "*":
      fields_str = "*"
    else:
      fields_str = ", ".join(fields)

    return "SELECT " + fields_str + " FROM " + self._TABLE
    
  def insert(self, data: dict):
    fields = ", ".join(k for k in data.keys())
    values = tuple(data.values())
    placeholders = ", ".join("?" * len(values))

    self._cur.execute(
      f"INSERT INTO {self._TABLE} ({fields}) VALUES ({placeholders})",
      values
    )

    return self._cur.lastrowid
  
  def update(self, where: dict, data: dict):
    set_clause, set_values = self._build_set(data)
    where_clause, where_values = self._build_where(where)

    self._cur.execute(
      f"UPDATE {self._TABLE} {set_clause} {where_clause}",
      set_values + where_values
    )

  def select(self, fields: list | str | None = None, where: dict = None):
    select_clause = self._build_select(fields)
    where_clause, where_values = self._build_where(where)

    self._cur.execute(f"{select_clause} {where_clause}", where_values)
    return [dict(row) for row in self._cur.fetchall()]
  
  def delete(self, where: dict):
    where_clause, where_values = self._build_where(where)
    self._cur.execute(f"DELETE FROM {self._TABLE} {where_clause}", where_values)