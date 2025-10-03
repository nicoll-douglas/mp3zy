from enum import Enum

class TrackBitrate(Enum):
  """Represents the acceptable bitrates for a track download.

  Attributes:
    _320: Represents a bitrate of 320kbps.
    _192: Represents a bitrate of 192kbps.
    _128: Represents a bitrate of 128kbps.
  """
  
  _320 = 320
  _192 = 192
  _128 = 128
  
# END class TrackBitrate