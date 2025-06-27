import sqlite3, logging

class Playlist:
  _conn: sqlite3.Connection
  __TABLE = "playlists"

  def __init__(self, conn: sqlite3.Connection):
    self._conn = conn

  def insert_many(self, playlists: list[dict[str, str]]):
    cursor = self._conn.cursor()
    playlist_count = len(playlists)

    logging.debug(f"Replace-inserting {playlist_count} user playlists into `{self.__TABLE}` table...")

    cursor.executemany(
      f"INSERT OR REPLACE INTO {self.__TABLE} (id, name, cover_source) VALUES (:id, :name, :cover_source)",
      playlists
    )
    self._conn.commit()
    
    logging.debug("Successfully replace-inserted playlists.")

  def find_all(self):
    self._conn.row_factory = sqlite3.Row
    cursor = self._conn.cursor()

    logging.debug(f"Selecting all playlists from the `{self.__TABLE}` table...")

    cursor.execute(f"SELECT * FROM {self.__TABLE}")
    rows = cursor.fetchall()

    logging.debug("Successfully selected playlists.")

    self._conn.row_factory = None

    return rows