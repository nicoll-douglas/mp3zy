from .Playlist import Playlist
import os

class LocalPlaylist(Playlist):
  DIR: str = os.path.join(os.getenv("STORAGE_DIR"), "playlists", "local")
  
  def __init__(
    self, 
    _id: str | None = None,
    path: str | None = None
  ):
    super().__init__(_id=_id, path=path)