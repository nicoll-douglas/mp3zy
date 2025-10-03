from services import YtDlpClient
from user_types.requests import PostDownloadsRequest
from user_types import TrackBitrate, TrackCodec, TrackReleaseDate
import models, db
import threading
from typing import cast

class Downloader:
  """A singleton class that acts as the controller for track downloads in the application.

  Attributes:
    _thread (threading.Thread | None): The thread where downloads run.
  """
  
  _thread: threading.Thread | None = None


  @classmethod
  def _progress_hook():
    pass


  @classmethod
  def queue(cls, track_info: PostDownloadsRequest) -> int:
    """Inserts the track info into the database and inserts a download row as queued.

    Args:
      track_info (PostDownloadsRequest): Metadata and details about a track that is to be downloaded.

    Returns:
      int: The ID of the newly inserted download.
    """

    with db.connect() as conn:
      artist_ids = models.db.Artist(conn).insert_many([
        { "name": n } 
        for n in track_info.artist_names
      ])

      metadata_id = models.db.Metadata(conn).insert({
        "track_name": track_info.track_name,
        "album_name": track_info.album_name,
        "track_number": track_info.track_number,
        "disc_number": track_info.disc_number,
        "release_date": str(track_info.release_date)
      })
      metadata_id = cast(int, metadata_id)

      models.db.MetadataArtist(conn).insert_many([
        { "metadata_id": metadata_id, "artist_id": aid }
        for aid in artist_ids
      ])

      download_id = models.db.Download(conn).insert_as_queued({
        "url": track_info.url,
        "codec": track_info.codec.value,
        "bitrate": track_info.bitrate.value,
        "metadata_id": metadata_id
      })

    return download_id
  # END queue


  @classmethod
  def start(cls) -> bool:
    """Starts the downloader in a new thread if not already running.

    Returns:
      bool: True if the downloader thread was freshly started and not already running, False otherwise.
    """

    if cls._thread is not None and cls._thread.is_alive():
      return False
    
    def target():
      with db.connect() as conn:
        yt_dlp_client = YtDlpClient()
        next_download = models.db.Download(conn).get_next_in_queue()

        while next_download:
          track_info = PostDownloadsRequest()
          track_info.album_name = next_download["album_name"]
          track_info.track_name = next_download["track_name"]
          track_info.artist_names = next_download["artist_names"]
          track_info.bitrate = TrackBitrate(next_download["bitrate"])
          track_info.codec = TrackCodec(next_download["codec"])
          track_info.disc_number = next_download["disc_number"]
          track_info.track_number = next_download["track_number"]
          track_info.release_date = TrackReleaseDate.from_string(next_download["release_date"])

          yt_dlp_client.download_track(track_info)
          next_download = models.db.Download(conn).get_next_in_queue()
    # END target

    cls._thread = threading.Thread(target=target)
    cls._thread.start()
    return True
  # END start

# END class Downloader