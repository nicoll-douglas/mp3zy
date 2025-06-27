import logging, sqlite3

class TrackArtist:
  conn: sqlite3.Connection
  __TABLE = "track_artist"

  def __init__(self, conn: sqlite3.Connection):
    self._conn = conn

  def insert_many(self, track_id: str, artist_ids: list[str]):
    cursor = self.conn.cursor()
    logging.debug(f"Ignore-inserting track-artist relationships into the `{self.__TABLE}` table...")

    cursor.executemany(
      f"INSERT OR IGNORE INTO {self.__TABLE} (track_id, artist_id) VALUES (:track_id, :artist_id)",
      [{ "track_id": track_id, "artist_id": id } for id in artist_ids]
    )
    self.conn.commit()

    logging.debug("Successfully inserted track-artist relationships.")
  
  def find_all(self, track_id: str) -> list[str]:
    cursor = self.conn.cursor()
  
    query = """
SELECT a.name
FROM track_artist AS ta
JOIN artists AS a ON ta.artist_id = a.id
WHERE ta.track_id = ?
"""
    
    logging.debug(f"Selecting all track artists from `{self.__TABLE}` table for track: {track_id}")
    cursor.execute(query, (track_id,))
    rows = cursor.fetchall()
    logging.debug("Successfully selected all track artists.")

    # return artist names as a list
    return [artist[0] for artist in rows]