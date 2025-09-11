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
    self._cur.execute("SELECT EXISTS(SELECT 1 FROM tasks WHERE status = ?)", ("downloading",))
    return bool(self._cur.fetchone()[0])

  def set_failed(self, task_id, error):
    self._cur.execute(
      f"UPDATE {self._TABLE} SET status=?, error=? WHERE id=?", 
      ("failed", error, task_id)
    )

  def update_progress(self, task_id, data: dict):
    params = data.copy()
    params["status"] = "downloading"

    return self.update(
      { "id": task_id },
      params
    )
