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
      "INSERT OR REPLACE INTO playlists (id, name, cover_source) VALUES (:id, :name, :cover_source)",
      playlists
    )
    self._conn.commit()
    
    logging.debug("Successfully replace-inserted playlists.")