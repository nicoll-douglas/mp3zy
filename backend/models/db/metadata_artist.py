import db
from ..Model import Model

class MetadataArtist(Model):
  _TABLE = "metadata_artists"

  def __init__(self, conn = db.connect()):
    super().__init__(conn)

  def insert_many(self, metadata_id, artist_ids: list[int]):
    self._cur.executemany(
      f"INSERT INTO {self._TABLE} (metadata_id, artist_id) VALUES (?, ?)", 
      [(metadata_id, aid) for aid in artist_ids]
    )

  def get_artists(self, metadata_id):
    sql = """
SELECT a.name, a.id
FROM metadata_artists ma
JOIN artists a ON ma.artist_id = a.id
WHERE ma.metadata_id = ?
"""
    self._cur.execute(sql, (metadata_id,))
    return [dict(row) for row in self._cur.fetchall()]