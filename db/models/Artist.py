from core import logging
import sqlite3

class Artist:
  conn: sqlite3.Connection
  __TABLE = "artists"

  def __init__(self, conn: sqlite3.Connection):
    self._conn = conn

  def insert_many(self, artists: list[dict[str, str]]):
    cursor = self.conn.cursor()
    logging.debug(f"Ignore-inserting artists into `{self.__TABLE}` table...")

    cursor.executemany(
      f"INSERT OR IGNORE INTO {self.__TABLE} (id, name) VALUES (:id, :name)",
      artists
    )
    self.conn.commit()

    logging.debug("Successfully inserted artists.")