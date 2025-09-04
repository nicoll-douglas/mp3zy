from __future__  import annotations
import os, glob, mimetypes
from platformdirs import user_data_dir
from pathvalidate import sanitize_filename
from .codec import Codec
from utils import File

class Track:  
  PARENT_DIR = os.path.join(File.save_path(), "tracks")

  number = None
  artists = None
  name = None
  album = None
  disc_number = None
  path = None
  codec: Codec = None

  def __init__(
    self, 
    number = None, 
    artists = None, 
    name = None, 
    album = None, 
    disc_number = None,
    path = None,
    codec: Codec = None
  ):
    self.number = number
    self.artists = artists
    self.name = name
    self.album = album
    self.disc_number = disc_number
    self.path = path
    self.codec = codec
    self._safe_create_dir()
  
  def _safe_create_dir(self):
    if self.codec:
      os.makedirs(os.path.join(self.PARENT_DIR, self.codec.value), exist_ok=True)
  
  def get_output_template(self) -> str:
    stem = self.build_stem()
    template = f"{stem}.%(ext)s"
    return os.path.join(self.SAVE_DIR, template)

  def build_stem(self):
    file_disk_num = str(self.disc_number).zfill(3)
    file_track_num = str(self.number).zfill(3)
    raw_filename = f"{file_disk_num}-{file_track_num} - {self.artists[0]} - {self.album} - {self.name}"
    
    return sanitize_filename(raw_filename)

  def get_ext(self):
    return "." + self.codec.value
  
  def get_save_dir(self):
    return os.path.join(self.PARENT_DIR, self.codec.value)

  def build_path(self):
    return os.path.join(self.SAVE_DIR, self.codec.value, self.build_stem() + self.get_ext())

  def exists(self):
    return os.path.exists(self.path)
  
  def search(self):
    stem = self.build_stem()
    file_path = os.path.join(f"{self.SAVE_DIR}", self.codec.value, glob.escape(stem)) + self.get_ext()
    return glob.glob(file_path)
  
  # search for and get the path of a track on disk based on track info (if it exists)
  def search_and_get_path(self, codec: Codec):
    results = self.search(codec)
    path = results[0] if results else None
    return path

  def get_path_mimetype(self):
    file_mimetype, _ = mimetypes.guess_type(self.path)
    return file_mimetype