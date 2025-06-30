from .File import File
import os, logging

class TrackCover(File):
  _source: str | None
  DIR: str = os.path.join("/data", "track_covers")

  def __init__(
    self, 
    _id: str | None = None,
    ext: str | None = None, 
    source: str | None = None, 
    path: str | None = None
  ):
    self._source = source

    if not _id and self._source:
      _id = self._source.split("/")[-1]

    super().__init__(
      _id=_id,
      ext=ext,
      path=path
    )

  def set_ext(self, ext: str):
    self._ext = ext
    return self

  def write(self, buffer):
    logging.debug(f"Writing binary content to disk at: {self._path}")

    if not self._path:
      raise RuntimeError("Failed to write binary content to path for a `File` object, property `_path` is not set.")
    
    with open(self._path, "wb") as f:
      f.write(buffer)
    
    logging.debug("Successfully wrote to disk.")