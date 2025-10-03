from enum import Enum

class DownloadStatus(Enum):
  """Represents the possible statuses of a download.

  Attributes:
    DOWNLOADING: Represents a download in progress.
    FAILED: Represents a failed download.
    QUEUED: Represents a download in the download queue.
    COMPLETED: Represents a completed download.
  """

  DOWNLOADING = "downloading"
  FAILED = "failed"
  QUEUED = "queued"
  COMPLETED = "completed"

# END class DownloadStatus