import glob, os, mimetypes, logging
from __future__ import annotations
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
    self._ext = ext
    self._id = _id
    self._path = path
    os.makedirs(self.DIR, exist_ok=True)
    self.build_path()
    
  def exists(self):
    if not self._path:
      return False
    return os.path.exists(self._path)
  
  def write(self, buffer):
    logging.debug(f"Writing binary content to disk at: {self._path}")

    if not self._path:
      raise RuntimeError("Failed to write binary content to path for a `File` object, property `_path` is not set.")
    
    with open(self._path, "wb") as f:
      f.write(buffer)
    
    logging.debug("Successfully wrote to disk.")

  def delete(self):
    logging.debug(f"Removing file from disk: {self._path}")
    
    if not self.exists():
      logging.debug("File doesn't exist, nothing removed.")
      return False

    os.remove(self._path)
    logging.debug(f"Successfully removed file.")
    
    return True
  
  def mimetype(self):
    if not self._path:
      return False
    file_mimetype, _ = mimetypes.guess_type(self._path)
    return file_mimetype or False
  
  def get_path(self):
    return self._path
  
  def set_ext(self, ext: str):
    self._ext = ext
    return self
  
  def build_path(self):
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
    
    return self
  
  @staticmethod
  def delete_many(covers: list[File]):
    total = len(covers)
    logging.debug(f"Deleting {total} files from disk...")
    delete_count = 0

    for cover in covers:
      result = cover.delete()
      delete_count += int(result)

    logging.debug(f"Successfully deleted {delete_count} of {total} files. {total - delete_count} failed.")
    return delete_count
  