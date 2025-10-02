from .download_status import DownloadStatus
from .track_artist_names import TrackArtistNames
from .track_codec import TrackCodec
from .track_bitrate import TrackBitrate

class DownloadUpdate:
  download_id: int
  status: DownloadStatus
  artist_names: TrackArtistNames
  track_name: str
  codec: TrackCodec
  bitrate: TrackBitrate
  url: str
  created_at: str
  total_bytes: int | None
  speed: int | float | None
  downloaded_bytes: int | None
  completed_at: str | None
  failed_at: str | None
  eta: int | float | None
  old_status: DownloadStatus | None

  def get_serializable(self):
    return {
      **self.__dict__,
      "status": self.status.value,
      "artist_names": self.artist_names.data,
      "codec": self.codec.value,
      "bitrate": self.bitrate.value,
      "old_status": None if self.old_status is None else self.old_status.value
    }
  # END get_serializable

# END class DownloadUpdate