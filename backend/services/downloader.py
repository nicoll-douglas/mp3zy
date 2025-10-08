from services import YtDlpClient
from user_types.requests import PostDownloadsRequest
from user_types import TrackBitrate, TrackCodec, TrackReleaseDate, DownloadUpdate, DownloadStatus, TrackArtistNames
import models, db
import threading
from typing import cast, Callable
from sockets import DownloadsSocket

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
      update (DownloadUpdate): Static downloaded update data for the download.

    Returns:
      Callable[[dict], None]: The progress hook function.
    """
    
    def progress_hook(hook_data: dict):
      """Updates the database with the updated downloaded data and emits and update to the downloads web socket.

      Args:
        hook_data (dict): The progress hook data received from the yt-dlp downloader.
      """
      
      with db.connect() as conn:
        models.db.Download(conn).update(update.download_id, {
          "status": DownloadStatus.DOWNLOADING.value,
          "total_bytes": hook_data["total_bytes"],
          "downloaded_bytes": hook_data["downloaded_bytes"],
          "speed": hook_data["speed"],
          "eta": hook_data.get("eta")
        })

      update.status = DownloadStatus.DOWNLOADING
      update.total_bytes = hook_data["total_bytes"]
      update.downloaded_bytes = hook_data["downloaded_bytes"]
      update.speed = hook_data["speed"]
      update.eta = hook_data.get("eta")
      update.terminated_at = None

      DownloadsSocket.instance().send_download_update(update)
    # END progress_hook

    return progress_hook
  # END _create_progress_hook


  @classmethod
  def _thread_target(cls):
    """Defines the thread target to pass to the downloader thread when it is created.
    """
    
    # connect to the database
    with db.connect() as conn:
      # get the next download in the queue
      download_model = models.db.Download(conn)

      # whilst there is a next download, download it
      while (next_download := download_model.get_next_in_queue()):
        # create static download update data
        update = DownloadUpdate()
        update.download_id = next_download["download_id"]
        update.artist_names = TrackArtistNames([next_download["main_artist"], *next_download["other_artists"]])
        update.track_name = next_download["track_name"]
        update.codec = TrackCodec(next_download["codec"])
        update.bitrate = TrackBitrate(next_download["bitrate"])
        update.url = next_download["url"]
        update.created_at = next_download["created_at"]
        update.download_dir = next_download["download_dir"]
        update.error_msg = None

        # get the progress hook to pass to the track download function
        progress_hook = cls._create_progress_hook(update)

        # recreate original request object to pass as track info to the download function
        track_info = PostDownloadsRequest()
        track_info.album_name = next_download["album_name"]
        track_info.track_name = update.track_name
        track_info.artist_names = update.artist_names
        track_info.bitrate = update.bitrate
        track_info.codec = update.codec
        track_info.disc_number = next_download["disc_number"]
        track_info.track_number = next_download["track_number"]
        track_info.url = update.url
        track_info.download_dir = update.download_dir
        track_info.release_date = TrackReleaseDate.from_string(next_download["release_date"]) if next_download["release_date"] else None
        track_info.album_cover_path = next_download["album_cover_path"]

        # here when spotify sync is implemented, we will pass an associated track ID to go in the filename
        is_success, result = YtDlpClient().download_track(track_info, progress_hook)
        
        # add fields to the static download update data with new data
        update.downloaded_bytes = None
        update.total_bytes = None
        update.eta = None
        update.speed = None

        # handle success and failure cases
        if is_success:
          update.status = DownloadStatus.COMPLETED

          track_model = cast(models.disk.Track, result)

          metadata = models.disk.Metadata()
          metadata.track_name = track_info.track_name
          metadata.artist_names = track_info.artist_names
          metadata.album_name = track_info.album_name
          metadata.track_number = track_info.track_number
          metadata.disc_number = track_info.disc_number
          metadata.release_date = track_info.release_date
          metadata.album_cover_path = track_info.album_cover_path

          if track_info.codec is TrackCodec.MP3:
            metadata.set_on_mp3(track_model.path)
          elif track_info.codec is TrackCodec.FLAC:
            metadata.set_on_flac(track_model.path)

          update.terminated_at = download_model.get_current_timestamp()
          download_model.set_completed(update.download_id, update.terminated_at)
        else:
          update.status = DownloadStatus.FAILED
          update.error_msg = cast(str, result)

          update.terminated_at = download_model.get_current_timestamp()
          download_model.set_failed(update.download_id, update.terminated_at, update.error_msg)

        DownloadsSocket.instance().send_download_update(update)
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
      other_artist_ids = models.db.Artist(conn).insert_many([
        { "name": n } 
        for n in track_info.artist_names.get_other_artists()
      ])

      metadata_id = models.db.Metadata(conn).insert({
        "track_name": track_info.track_name,
        "main_artist": track_info.artist_names.get_main_artist(),
        "album_name": track_info.album_name,
        "track_number": track_info.track_number,
        "disc_number": track_info.disc_number,
        "release_date": str(track_info.release_date) if track_info.release_date else None,
        "album_cover_path": track_info.album_cover_path
      })
      metadata_id = cast(int, metadata_id)

      models.db.MetadataArtist(conn).insert_many([
        { "metadata_id": metadata_id, "artist_id": aid }
        for aid in other_artist_ids
      ])

      download_model = models.db.Download(conn)
      created_at = download_model.get_current_timestamp()

      download_id = download_model.insert_as_queued({
        "url": track_info.url,
        "codec": track_info.codec.value,
        "bitrate": track_info.bitrate.value,
        "metadata_id": metadata_id,
        "created_at": created_at,
        "download_dir": track_info.download_dir
      })

    update = DownloadUpdate()
    update.status = DownloadStatus.QUEUED
    update.download_id = download_id
    update.artist_names = track_info.artist_names
    update.track_name = track_info.track_name
    update.codec = track_info.codec
    update.bitrate = track_info.bitrate
    update.url = track_info.url
    update.download_dir = track_info.download_dir
    update.terminated_at = None
    update.created_at = created_at
    update.error_msg = None

    DownloadsSocket.instance().send_download_update(update)

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