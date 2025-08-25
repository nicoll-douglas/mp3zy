import os, glob, mimetypes
from platformdirs import user_data_dir
from pathvalidate import sanitize_filename

class Track:  
  SAVE_DIR = os.path.join(user_data_dir(os.getenv("APP_NAME")), "tracks")

  number = None
  artists = None
  name = None
  album = None
  disc_number = None
  path = None
  ext = None

  def __init__(
    self, 
    number = None, 
    artists = None, 
    name = None, 
    album = None, 
    disc_number = None,
    path = None,
    ext = None
  ):
    self.safe_create_dir()
    self.number = number
    self.artists = artists
    self.name = name
    self.album = album
    self.disc_number = disc_number
    self.path = path
    self.ext = ext
  
  @classmethod
  def safe_create_dir(cls):
    os.makedirs(cls.SAVE_DIR, exist_ok=True)
  
  def get_output_template(self) -> str:
    stem = self.build_stem()
    template = f"{stem}.%(ext)s"
    return os.path.join(self.SAVE_DIR, template)

  def build_stem(self):
    file_disk_num = str(self.disc_number).zfill(3)
    file_track_num = str(self.number).zfill(3)
    raw_filename = f"{file_disk_num}-{file_track_num} - {self.artists[0]} - {self.album} - {self.name}"
    
    return sanitize_filename(raw_filename)

  def build_path(self):
    return os.path.join(self.SAVE_DIR, self.build_stem() + self.ext)

  def exists(self):
    return os.path.exists(self.path)
  
  def search(self):
    stem = self.build_stem()
    return glob.glob(f"{self.SAVE_DIR}/{stem}.*")
  
  # search for and get the path of a track on disk based on track info (if it exists)
  def search_and_get_path(self):
    results = self.search()
    path = results[0] if results else None
    return path

  def get_path_mimetype(self):
    file_mimetype, _ = mimetypes.guess_type(self.path)
    return file_mimetype