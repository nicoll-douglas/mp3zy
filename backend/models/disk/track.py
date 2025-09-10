from __future__  import annotations
import os, glob, mimetypes
from platformdirs import user_data_dir
from pathvalidate import sanitize_filename
from .codec import Codec
from utils import File

class Track:  
  PARENT_DIR = os.path.join(File.save_path(), "tracks")

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
      os.makedirs(self.get_save_dir(), exist_ok=True)
  
  def get_output_template(self) -> str:
    stem = self.build_stem()
    template = f"{stem}.%(ext)s"
    return os.path.join(self.PARENT_DIR, self.codec.value, template)

  def build_stem(self):
    raw_filename = f"{self.artist} - {self.name}"
    return sanitize_filename(raw_filename)

  def get_ext(self):
    return "." + self.codec.value
  
  def get_save_dir(self):
    return os.path.join(self.PARENT_DIR, self.codec.value)

  def build_path(self):
    return os.path.join(self.get_save_dir(), self.build_stem() + self.get_ext())

  def exists(self):
    return os.path.exists(self.path)
  
  def search(self):
    stem = self.build_stem()
    file_path = os.path.join(self.get_save_dir(), glob.escape(stem)) + self.get_ext()
    return glob.glob(file_path)
  
  def search_and_get_path(self):
    results = self.search()
    path = results[0] if results else None
    return path

  def get_path_mimetype(self):
    file_mimetype, _ = mimetypes.guess_type(self.path)
    return file_mimetype