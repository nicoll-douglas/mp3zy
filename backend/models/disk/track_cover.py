import os, mimetypes, glob
from utils import File

class TrackCover:
  SAVE_DIR = os.path.join(File.CACHE_DIR, "covers")

  album_id = None
  path = None
  ext = None

  def __init__(
    self, 
    album_id = None,
    path = None,
    ext = None
  ):
    self.album_id = album_id
    self.path = path
    self.ext = ext
    self._safe_create_dir()

  @classmethod
  def _safe_create_dir(cls):
    os.makedirs(cls.SAVE_DIR, exist_ok=True)
  
  def write(self, buffer):    
    with open(self.path, "wb") as f:
      f.write(buffer)

  def exists(self):
    return os.path.exists(self.path)

  def get_path_mimetype(self):
    file_mimetype, _ = mimetypes.guess_type(self.path)
    return file_mimetype
  
  # build the fully correct path of a track cover's save location from the associated album id and extension
  def build_path(self):
    return os.path.join(self.SAVE_DIR, self.album_id + self.ext)
  
  # search for a track cover on disk based on the album id
  def search(self):
    return glob.glob(os.path.join(self.SAVE_DIR, f"{self.album_id}.*"))
  
  # search for and get the path of a track cover on disk based on album id (if it exists)
  def search_and_get_path(self):
    results = self.search()
    path = results[0] if results else None
    return path

