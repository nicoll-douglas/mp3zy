from enum import Enum

class TrackCodec(Enum):
  """Represents the acceptable audio codecs for a track download.

  Attributes:
    MP3: Represents the MP3 (mpeg-3) codec.
    FLAC: Represents the FLAC codec.
  """
  
  MP3 = "mp3"
  FLAC = "flac"

# END class TrackCodec