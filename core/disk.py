import os, glob, logging
from pathlib import Path

STORAGE_DIR = os.getenv("STORAGE_DIR")
TRACKS_DIR = os.path.join(STORAGE_DIR, "tracks")
TRACK_COVERS_DIR = os.path.join(STORAGE_DIR, "track_covers")
PLAYLIST_COVERS_DIR = os.path.join(STORAGE_DIR, "playlist_covers")


def compute_cover_diff(dir: str, updated_cover_ids: tuple[str] | list[str]):
  logging.debug("Computing a cover diff for files on disk...")
  dir_obj = Path(dir)
  cover_ids = [f.stem for f in dir_obj.iterdir() if f.is_file()]
  updates = {
    "insert": [_id for _id in updated_cover_ids if _id not in cover_ids],
    "delete": [_id for _id in cover_ids if _id not in updated_cover_ids],
  }
  return updates

def compute_track_diff(updated_track_ids: tuple[str] | list[str]):
  logging.debug("Computing a track diff for files on disk...")
  directory = Path(TRACKS_DIR)
  track_ids = [f.stem for f in directory.iterdir() if f.is_file()]
  updates = {
    "insert": [_id for _id in updated_track_ids if _id not in track_ids],
    "delete": [_id for _id in track_ids if _id not in updated_track_ids],
  }
  return updates