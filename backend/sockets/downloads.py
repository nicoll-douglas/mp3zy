from flask_socketio import Namespace
from user_types import DownloadUpdate, DownloadStatus, TrackArtistNames, TrackCodec, TrackBitrate
import models, db
from typing import Self
import sqlite3

class DownloadsSocket(Namespace):
  """Socket namespace that deals with downloads.

  Attributes:
    DOWNLOAD_UPDATE_EVENT (str): The name of the event for download upates.
    DOWNLOAD_INIT_EVENT (str): The name of the event for sending all downloads (downloads initialization).
    _db_conn (sqlite3.Connection | None): A singleton database connection instance used by the app.
    _instance (DownloadsSocket | None): A singleton instance of the class to use throughout the rest of the app.
  """

  DOWNLOAD_UPDATE_EVENT = "download_update"
  DOWNLOAD_INIT_EVENT = "download_init"
  NAMESPACE = "/downloads"

  _db_conn: sqlite3.Connection | None
  _instance: Self | None = None


  def __init__(self, db_conn: sqlite3.Connection | None = None):
    """Stores the database connection as well as the current instance in the class as a singleton instance.
    """
    
    super().__init__(self.NAMESPACE)
    self._db_conn = db_conn
    DownloadsSocket._instance = self
  # END __init__


  @classmethod
  def instance(cls) -> Self:
    """Gets the singleton class instance to use throughout the rest of the app.

    Returns:
      DownloadsSocket: The instsance.

    Raises:
      RuntimeError: If the instance was not yet created.
    """
    
    if cls._instance is None:
      raise RuntimeError("DownloadsSocket instance was accessed before it was created")

    return cls._instance
  # END instance


  def on_connect(self):
    """Sends a list of all downloads when a client connects to the namespace.
    """

    self.get_and_send_all_downloads()
  # END on_connect


  def on_disconnect(self):
    pass
  # END on_disconnect


  def get_and_send_all_downloads(self):
    """Gets and sends a list of all downloads.
    """
    
    db_conn = self._db_conn
    created_conn = False

    if not db_conn:
      db_conn = db.connect()
      created_conn = True

    dl = models.db.Download(db_conn)
    downloads = dl.get_all_downloads()

    download_updates = []

    for d in downloads:
      d_update = DownloadUpdate()
      d_update.download_id = d["download_id"]
      d_update.status = DownloadStatus(d["status"])
      d_update.artist_names = TrackArtistNames([d["main_artist"], *d["other_artists"]])
      d_update.track_name = d["track_name"]
      d_update.codec = TrackCodec(d["codec"])
      d_update.bitrate = TrackBitrate(d["bitrate"])
      d_update.url = d["url"]
      d_update.download_dir = d["download_dir"]
      d_update.created_at = d["created_at"]
      d_update.total_bytes = d["total_bytes"]
      d_update.downloaded_bytes = d["downloaded_bytes"]
      d_update.speed = d["speed"]
      d_update.eta = d["eta"]
      d_update.terminated_at = d["terminated_at"]
      d_update.error_msg = d["error_msg"]

      download_updates.append(d_update)

    self.send_all_downloads(download_updates)

    if created_conn:
      db_conn.close()
  # END get_and_send_all_downloads


  def send_all_downloads(self, downloads: list[DownloadUpdate]):
    """Emits the `downloads_init` event sending a list of downloads.

    Args:
      downloads (list[DownloadUpdate]): The list of downloads to send.
    """
    
    self.emit(self.DOWNLOAD_INIT_EVENT, {
      "downloads": [d.get_serializable() for d in downloads]
    })
  # END send_all_downloads


  def send_download_update(self, update: DownloadUpdate):
    """Emits the `download_update` event sending a download update.

    Args:
      update (DownloadUpdate): The download update.
    """

    self.emit(self.DOWNLOAD_UPDATE_EVENT, update.get_serializable())
  # END send_download_update
  
# END class DownloadsSocket