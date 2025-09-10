from .track import Track
import os
from pathlib import Path
from platformdirs import user_data_dir
from pathvalidate import sanitize_filename
from utils import File

class Playlist:
  EXT = ".m3u"
  DESKTOP_PL_DIR = os.path.join(File.save_path(), "playlists", "desktop")

  path = None
  name = None
  directory = None

  def __init__(self, path = None, name = None, directory = None):
    self.safe_create_dirs()
    self.path = path
    self.name = name
    self.directory = directory

  @classmethod
  def safe_create_dirs(cls):
    os.makedirs(cls.DESKTOP_PL_DIR, exist_ok=True)

  def build_path(self):
    filename = sanitize_filename(self.name)
    return os.path.join(self.directory, filename + self.EXT)

  def write(self, playlist_items):
    paths = []

    # get all file paths on disk that line up with tracks in the spotify playlist
    for pl_item in playlist_items:
      is_local = pl_item["is_local"]
      is_not_track = pl_item["track"]["type"] != "track"

      if is_local or is_not_track:
        continue

      track_name = pl_item["track"]["name"]
      track_number = pl_item["track"]["track_number"]      
      track_artists = [a["name"] for a in pl_item["track"]["artists"]]
      album_name = pl_item["track"]["album"]["name"]
      disc_number=pl_item["track"]["disc_number"]
      
      t = Track(
        number=track_number,
        artists=track_artists,
        name=track_name,
        album=album_name,
        disc_number=disc_number,
      )

      path = t.search_and_get_path()
      if path:
        paths.append(path)

    # write file paths to the file path
    with open(self.path, "w", encoding="utf-8") as f:
      f.write("\n".join(paths))

  def create(self, playlist_items):
    if not self.exists():
      self.write(playlist_items)

  def exists(self):
    return os.path.exists(self.path)
  
  def get_all(self):
    d = Path(self.directory)
    return [f for f in d.iterdir() if f.is_file()]