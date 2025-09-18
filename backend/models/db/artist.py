import db
from ..Model import Model

class Artist(Model):
  _TABLE = "artists"

  def __init__(self, conn = db.connect()):
    super().__init__(conn)

  def insert_many(self, artists: list[str]):
    ids = []
    
    for a in artists:
      self._cur.execute(
        f"INSERT INTO {self._TABLE} (name) VALUES (?) RETURNING id", 
        (a,)
      )
      ids.append(self._cur.fetchone()[0])

    return ids