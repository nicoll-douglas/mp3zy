import db
from ..Model import Model

class Artist(Model):
  _TABLE = "artists"

  def __init__(self, conn = db.connect()):
    super().__init__(conn)

  def insert_many(self, artists: list[str]):
    self._cur.executemany(
      f"INSERT INTO {self._table} (name) VALUES (?) RETURNING id", 
      [(a,) for a in artists]
    )
    return [row[0] for row in self._cur.fetchall()]