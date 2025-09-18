import db
from ..Model import Model
from .download_status import DownloadStatus
from .queries import get_downloads
import json

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

  def update_progress(self, id, data: dict):
    params = data.copy()
    params["status"] = "downloading"

    return self.update(
      { "id": id },
      params
    )

  def get_downloading(self):
    query = get_downloads(True)
    self._cur.execute(query, (DownloadStatus.DOWNLOADING.value,))
    rows = self._cur.fetchall()
    return [{**row, "artists": json.loads(row["artists"]) } for row in rows]

  def set_downloading(self, id):
    self.update(
      { "id": id },
      { "status": DownloadStatus.DOWNLOADING.value }
    )
  
  def get_queued(self):
    query = get_downloads(True)
    self._cur.execute(
      f"{query} ORDER BY created_at ASC", 
      (DownloadStatus.QUEUED.value,)
    )
    rows = self._cur.fetchall()
    return [{**row, "artists": json.loads(row["artists"]) } for row in rows]

  def get_completed(self):
    query = get_downloads(True)
    self._cur.execute(
      f"{query} ORDER BY updated_at DESC", 
      (DownloadStatus.COMPLETED.value,)
    )
    rows = self._cur.fetchall()
    return [{**row, "artists": json.loads(row["artists"]) } for row in rows]
  
  def set_failed(self, id):
    self.update(
      { "id": id },
      { "status": DownloadStatus.FAILED.value }
    )

  def get_failed(self):
    query = get_downloads(True)
    self._cur.execute(
      f"{query} ORDER BY updated_at DESC", 
      (DownloadStatus.FAILED.value,)
    )
    rows = self._cur.fetchall()
    return [{**row, "artists": json.loads(row["artists"]) } for row in rows]

  def set_completed(self, id):
    set_clause, set_values = self._build_set({ "status": DownloadStatus.COMPLETED.value })
    where_clause, where_values = self._build_where({ "id": id })
    set_clause += f", completed_at = CURRENT_TIMESTAMP"
    
    self._cur.execute(
      f"UPDATE {self._TABLE} {set_clause} {where_clause}",
      set_values + where_values
    )