import models
import db
from utils import get_track_string

def get_downloads(status):
  conn = db.connect()
  dl = models.db.Download(conn)

  if status == models.db.DownloadStatus.COMPLETED.value:
    downloads = dl.get_completed()
  elif status == models.db.DownloadStatus.FAILED.value:
    downloads = dl.get_failed()
  elif status == models.db.DownloadStatus.QUEUED.value:
    downloads = dl.get_queued()
  else:
    downloads = dl.get_downloading()

  data = [
    {
      "trackStr": get_track_string(d["artists"], d["track"]),
      "codec": d["codec"],
      "bitrate": d["bitrate"],
      "error": d["error"],
      "createdAt": d["created_at"],
      "completedAt": d["completed_at"],
      "updatedAt": d["updated_at"]
    }
    for d in downloads
  ]

  return data
