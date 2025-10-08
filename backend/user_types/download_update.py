from .download_status import DownloadStatus
from .track_artist_names import TrackArtistNames
from .track_codec import TrackCodec
from .track_bitrate import TrackBitrate

class DownloadUpdate:
  """A class that contains download update data for a track download.

  Attributes:
    download_id (int): The database ID of the download.
    status (DownloadStatus): The current status of the download.
    artist_names (TrackArtistNames): Artist name metadata of the download.
    track_name (str): Track name metadata for the download.
    codec (TrackCodec): The audio codec of the download.
    bitrate (TrackBitrate): The audio bitrate of the download.
    url (str): The YouTube URL being used for the download source.
    created_at (str): Timestamp of when the download record was created in the database
    total_bytes (int | None): The total number of bytes that will be downloaded.
    speed (int | float | None): The speed of the download.
    downloaded_bytes (int | None): THe number of bytes already downloaded.
    terminated_at (str | None): Timestamp of when the download record was set to completed or failed in the database.
    eta (int | None): The amount of time in seconds left for the download.
    download_dir (str): The directory path of where the audio file will be downloaded to.
  """
  
  download_id: int
  status: DownloadStatus
  artist_names: TrackArtistNames
  track_name: str
  codec: TrackCodec
  bitrate: TrackBitrate
  url: str
  download_dir: str
  created_at: str
  total_bytes: int | None
  speed: int | float | None
  downloaded_bytes: int | None
  terminated_at: str | None
  eta: int | None


  def get_serializable(self) -> dict:
    """Returns the class attributes as a serializable dictionary.

    Returns:
      dict: The dictionary of class attributes.
    """

    return {
      **self.__dict__,
      "status": self.status.value,
      "artist_names": self.artist_names.data,
      "codec": self.codec.value,
      "bitrate": self.bitrate.value
    }
  # END get_serializable

# END class DownloadUpdate