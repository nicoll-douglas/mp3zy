from .Cover import Cover
import os

class TrackCover(Cover):  
  DIR: str = os.path.join(os.getenv("STORAGE_DIR"), "track_covers")

  def __init__(
    self, 
    _id: str | None = None,
    ext: str | None = None, 
    source: str | None = None, 
    path: str | None = None
  ):
    super().__init__(
      _id=_id, 
      ext=ext, 
      source=source, 
      path=path, 
    )