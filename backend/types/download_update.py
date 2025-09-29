from collections import UserDict
from .DownloadStatus import DownloadStatus
from .ArtistNamesMetadata import ArtistNamesMetadata
from .TrackCodec import TrackCodec
from .TrackBitrate import TrackBitrate

class DownloadUpdate(UserDict):
  def __init__(
    self,
    download_id: int,
    status: DownloadStatus,
    downloaded_bytes: int,
    total_bytes: int,
    speed: int | float,
    artist_names: ArtistNamesMetadata,
    track_name: str,
    codec: TrackCodec,
    bitrate: TrackBitrate,
    url: str,
    created_at: str,
    completed_at: str | None = None,
    failed_at: str | None = None,
    eta: int | float | None = None,
    old_status: DownloadStatus | None = None,
  ):
    super.__init__()
    self["download_id"] = download_id
    self["status"] = status.value
    self["downloaded_bytes"] = downloaded_bytes
    self["total_bytes"] = total_bytes
    self["speed"] = speed
    self["artist_names"] = artist_names.data
    self["track_name"] = track_name
    self["codec"] = codec.value
    self["bitrate"] = bitrate.value
    self["url"] = url
    self["created_at"] = created_at
    self["completed_at"] = completed_at
    self["failed_at"] = failed_at
    self["eta"] = eta
    self["old_status"] = None if old_status is None else old_status.value
  # END __init__

# END class DownloadUpdate