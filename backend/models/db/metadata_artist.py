import db
from ..Model import Model

class MetadataArtist(Model):
  _TABLE = "metadata_artists"

  def __init__(self, conn = db.connect()):
    super().__init__(conn)

  def insert_many(self, metadata_id, artist_ids: list[int]):
    self._cur.executemany(
      f"INSERT INTO {self._table} (metadata_id, artist_id) VALUES (?, ?)", 
      [(metadata_id, aid) for aid in artist_ids]
    )