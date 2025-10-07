from services import YtDlpClient
from user_types.requests import PostDownloadsRequest
from user_types import TrackBitrate, TrackCodec, TrackReleaseDate, DownloadUpdate, DownloadStatus, TrackArtistNames
import models, db
import threading
from typing import cast, Callable
from sockets import downloads_socket

class Downloader:
  """A singleton class that acts as the controller for track downloads in the application.

  Attributes:
    _thread (threading.Thread | None): The thread where downloads run.
  """
  
  _thread: threading.Thread | None = None


  @staticmethod
  def _create_progress_hook(update: DownloadUpdate) -> Callable[[dict], None]:
    """Creates a progress hook function to be passed to the yt-dlp client instance when downloading.

    Args:
      update (DownloadUpdate): The download update to be emitted via web socket in the progress hook.

    Returns:
      Callable[[dict], None]: The progress hook function.
    """
    
    def progress_hook(hook_data: dict):
      with db.connect() as conn:
        models.db.Download(conn).update(update.download_id, {
          "status": update.status.value,
          "total_bytes": hook_data["total_bytes"],
          "downloaded_bytes": hook_data["downloaded_bytes"],
          "speed": hook_data["speed"],
          "eta": hook_data["eta"]
        })

      update.total_bytes = hook_data["total_bytes"]
      update.downloaded_bytes = hook_data["downloaded_bytes"]
      update.speed = hook_data["speed"]
      update.eta = hook_data["eta"]

      downloads_socket.send_download_update(update)
    # END progress_hook

    return progress_hook
  # END _create_progress_hook


  @classmethod
  def _thread_target(cls):
    """Defines the thread target to pass to the downloader thread when it is created.
    """
    
    with db.connect() as conn:
      next_download = models.db.Download(conn).get_next_in_queue()

      while next_download:
        artist_names = TrackArtistNames(next_download["artist_names"])
        track_name = next_download["track_name"]
        codec = TrackCodec(next_download["codec"])
        bitrate = TrackBitrate(next_download["bitrate"])
        
        update = DownloadUpdate()
        update.status = DownloadStatus.DOWNLOADING
        update.download_id = next_download["download_id"]
        update.artist_names = artist_names
        update.track_name = track_name
        update.codec = codec
        update.bitrate = bitrate
        update.url = next_download["url"]
        update.completed_at = next_download["completed_at"]
        update.failed_at = next_download["failed_at"]
        update.created_at = next_download["created_at"]

        progress_hook = cls._create_progress_hook(update)

        track_info = PostDownloadsRequest()
        track_info.album_name = next_download["album_name"]
        track_info.track_name = track_name
        track_info.artist_names = artist_names
        track_info.bitrate = bitrate
        track_info.codec = codec
        track_info.disc_number = next_download["disc_number"]
        track_info.track_number = next_download["track_number"]
        track_info.release_date = TrackReleaseDate.from_string(next_download["release_date"])

        # here when spotify sync is implemented, we will pass an associated save dir and track id retrieved from the database
        # we will also have to implement a try catch here; on failure update the download in db to failed and emit this update to the socket
        track_model = YtDlpClient().download_track(track_info, progress_hook)

        # on success here we have to update the metadata of the track using the track model to get the path
        # then we have to set the download to completed in the db then emit this update to the socket
        
        next_download = models.db.Download(conn).get_next_in_queue()
  # END _thread_target


  @staticmethod
  def queue(track_info: PostDownloadsRequest) -> int:
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

      # need to query for created_at here

    update = DownloadUpdate()
    update.status = DownloadStatus.QUEUED
    update.download_id = download_id
    update.artist_names = track_info.artist_names
    update.track_name = track_info.track_name
    update.codec = track_info.codec
    update.bitrate = track_info.bitrate
    update.url = track_info.url
    update.terminated_at = None
    # assign created_at to the update here

    downloads_socket.send_download_update(update)

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

    cls._thread = threading.Thread(target=cls._thread_target)
    cls._thread.start()
    return True
  # END start

# END class Downloader