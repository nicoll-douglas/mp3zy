from enum import Enum
from typing import Literal

class DownloadStatus(Enum):
  DOWNLOADING = "downloading"
  FAILED = "failed"
  QUEUED = "queued"
  COMPLETED = "completed"

  @classmethod
  def validate(cls, field_name, data) -> tuple[Literal[False], str] | tuple[Literal[True], None]:
    if data is None:
      return False, f"`{field_name}` is required."
    
    has_value = any(data == member.value for member in cls)
    message = None if has_value else f"`{field_name}` is invalid."

    return has_value, message
  # END validate

# END class DownloadStatus