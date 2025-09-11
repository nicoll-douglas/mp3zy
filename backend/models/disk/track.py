from __future__  import annotations
import os, glob, mimetypes
from pathvalidate import sanitize_filename
from .codec import Codec
from utils import File

class Track:  
  artist = None
  name = None
  path = None
  codec: Codec = None

  def __init__(
    self, 
    artist = None, 
    name = None, 
    path = None,
    codec: Codec = None
  ):
    self.artist = artist
    self.name = name
    self.path = path
    self.codec = codec
    self._safe_create_dir()
  
  def _safe_create_dir(self):
    if self.codec:
      os.makedirs(self.get_collection_dir(), exist_ok=True)
  
  def get_output_template(self, task_id) -> str:
    template = f"{task_id}.%(ext)s"
    return os.path.join(self.get_collection_dir(), template)

  def build_stem(self):
    raw_filename = f"{self.artist} - {self.name}"
    return sanitize_filename(raw_filename)

  def get_ext(self):
    return "." + self.codec.value
  
  def get_collection_dir(self):
    return File.collection_dir(self.codec.value)

  def set_name(self, task_id):
    download_path = os.path.join(self.get_collection_dir(), task_id + self.get_ext())
    os.rename(download_path, self.build_path())
  
  def build_path(self):
    return os.path.join(self.get_collection_dir(), self.build_stem() + self.get_ext())

  def exists(self):
    return os.path.exists(self.path)
  
  def search(self):
    stem = self.build_stem()
    file_path = os.path.join(self.get_collection_dir(), glob.escape(stem)) + self.get_ext()
    return glob.glob(file_path)
  
  def search_and_get_path(self):
    results = self.search()
    path = results[0] if results else None
    return path

  def get_path_mimetype(self):
    file_mimetype, _ = mimetypes.guess_type(self.path)
    return file_mimetype