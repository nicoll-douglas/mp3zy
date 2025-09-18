from enum import Enum

class DownloadStatus(Enum):
  DOWNLOADING = "downloading"
  COMPLETED = "completed"
  QUEUED = "queued"
  FAILED = "failed"