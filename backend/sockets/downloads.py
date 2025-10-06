from flask_socketio import Namespace
from user_types import DownloadUpdate

DOWNLOADS_NAMESPACE = "/downloads"

class DownloadsSocket(Namespace):
  """Socket namespace that deals with downloads.

  Attributes:
    DOWNLOAD_UPDATE_EVENT (str): The name of the event for download upates.
    DOWNLOAD_INIT_EVENT (str): The name of the event for sending all downloads (downloads initialization).
  """

  DOWNLOAD_UPDATE_EVENT = "download_update"
  DOWNLOAD_INIT_EVENT = "download_init"


  def on_connect(self):
    pass
  # END on_connect


  def on_disconnect(self):
    pass
  # END on_disconnect


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

downloads_socket = DownloadsSocket(DOWNLOADS_NAMESPACE)