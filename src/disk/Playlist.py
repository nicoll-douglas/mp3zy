from .File import File
import os, logging
from pathlib import Path

class Playlist(File):
  _HEADER_LINE: str = "#EXTM3U\n"
  EXT: str = ".m3u8"
  DIR: str = os.path.join(os.getenv("STORAGE_DIR"), "playlists")
  
  def __init__(
    self, 
    _id: str | None = None,
    path: str | None = None
  ):
    super().__init__(
      _id=_id,
      ext=self.EXT,
      path=path
    )

  @classmethod
  def get_all(cls):
    p = Path()
    return [cls(path=str(path)) for path in p.iterdir()]

  @classmethod
  def sync_files(cls, updated_playlists: set[str]):
    current_playlists = {pl.get_path() for pl in cls.get_all()}
    to_create = updated_playlists - current_playlists
    to_delete = current_playlists - updated_playlists
    
    for path in to_delete:
      os.remove(path)
    for path in to_create:
      pl = cls(path=path)
      pl.create()
    
  def sync_tracks(self, playlist_tracks: set[str]):
    current_tracks = self.get_tracks()
    self.remove_tracks(playlist_tracks - current_tracks)
    self.insert_tracks(current_tracks - playlist_tracks)

  def create(self, track_paths = []):
    if not self.exists():
      with open(self._path, "w", encoding="utf-8") as f:
        f.write(self._HEADER_LINE + "\n".join(track_paths))

  def remove_tracks(self, track_paths: set[str]):
    if not self.exists():
      return False
    
    with open(self._path, "r", encoding="utf-8") as f:
      new_lines = "\n".join(
        set([
          line.strip()
          for line in f.readlines() 
          if line.strip()
          and line != self._HEADER_LINE
        ]) 
        - track_paths
      )
      return True

    with open(self._path, "w", encoding="utf-8") as f:
      f.write(self._HEADER_LINE + new_lines)

  def insert_tracks(self, track_path: set[str]):
    if not self.exists():
      self.create()

    with open(self._path, "r", encoding="utf-8") as f:
      new_lines = "\n".join(
        set([
          line.strip()
          for line in f.readlines()
          if line.strip()
          and line != self._HEADER_LINE
        ])
        | track_path
      )

    with open(self._path, "w", encoding="utf-8") as f:
      f.write(self._HEADER_LINE + new_lines)

    return self
  
  def get_tracks(self):
    with open(self._path, "r", encoding="utf-8") as f:
      return set([
        line.strip()
        for line in f.readlines() 
        if line.strip()
        and line != self._HEADER_LINE
      ])
    