from __future__ import annotations
import glob, os, mimetypes, logging
from pathlib import Path
class File:
  DIR: str | None
  _ext: str | None
  _id: str | None
  _path: str | None

  def __init__(
    self,
    _id: str | None = None,
    ext: str | None = None, 
    path: str | None = None
  ):
    self._id = _id
    self._ext = ext
    self._path = path
    os.makedirs(self.DIR, exist_ok=True)
    self.normalise()
    
  def exists(self):
    if not self._path:
      return False
    return os.path.exists(self._path)

  def delete(self):
    logging.debug(f"Removing file from disk: {self._path}")
    
    if not self.exists():
      logging.debug("File doesn't exist, nothing removed.")
      return False

    os.remove(self._path)
    logging.debug(f"Successfully removed file.")
    
    return True
  
  def get_mimetype(self):
    if not self._path:
      return False
    file_mimetype, _ = mimetypes.guess_type(self._path)
    return file_mimetype or False
  
  def get_path(self):
    return self._path

  def get_ext(self):
    return self._ext
  
  def normalise(self):
    if self._id:
      path_without_ext = os.path.join(self.DIR, self._id)
      files = glob.glob(path_without_ext + ".*")

      if len(files) > 0:
        self._path = files[0]
        self._ext = mimetypes.guess_extension(files[0])
      elif self._ext:
        self._path = os.path.join(self.DIR, self._id + self._ext)

    elif self._path:
      p = Path(self._path)
      self._id = p.stem
      self._ext = p.suffix
    
    return self