import db
from ..Model import Model

class Download(Model):
  _TABLE = "downloads"

  def __init__(self, conn = db.connect()):
    super().__init__(conn)

  def queue(self, data: dict):
    params = data.copy()
    params["status"] = "queued"
    return self.insert(params)

  def is_in_progress(self):
    self._cur.execute(f"SELECT EXISTS(SELECT 1 FROM {self._TABLE} WHERE status = ?)", ("downloading",))
    return bool(self._cur.fetchone()[0])

  def set_failed(self, id, error):
    self._cur.execute(
      f"UPDATE {self._TABLE} SET status=?, error=? WHERE id=?", 
      ("failed", error, id)
    )

  def update_progress(self, id, data: dict):
    params = data.copy()
    params["status"] = "downloading"

    return self.update(
      { "id": id },
      params
    )

  def get_downloading(self):
    self._cur.execute(f"SELECT * FROM {self._TABLE} WHERE status = ?", ("downloading",))
    return dict(self._cur.fetchone())