import os, glob, logging
from pathlib import Path

STORAGE_DIR = os.getenv("STORAGE_DIR")
TRACKS_DIR = os.path.join(STORAGE_DIR, "tracks")
TRACK_COVERS_DIR = os.path.join(STORAGE_DIR, "track_covers")
PLAYLIST_COVERS_DIR = os.path.join(STORAGE_DIR, "playlist_covers")

def write_b(path: str, buffer):
  logging.debug(f"Writing binary content to disk at: {path}")
  with open(path, "wb") as f:
    f.write(buffer)
  logging.debug("Successfully wrote to disk.")

def cover_id(cover_source: str):
  return cover_source.split("/")[-1]

# get the path to a track
def track_path(track_id: str):
  return os.path.join(TRACKS_DIR, f"{track_id}.mp3")

# gets the path to the cover image stored locally
def cover_path(
  dir: str, 
  cover_source: str | None = None, 
  ext: str | None = None, 
  _cover_id: str | None = None
):
  id = _cover_id or cover_id(cover_source)
  path_without_ext = os.path.join(dir, id)

  if not ext:
    files = glob.glob(path_without_ext + ".*")
    return files[0]
  
  return os.path.join(dir, id + ext)

# checks if a cover is downloaded
def cover_exists(dir: str, _cover_id: str):
  path_without_ext = os.path.join(dir, _cover_id)
  files = glob.glob(path_without_ext + ".*")
  return len(files) > 0

# checks if a track is downloaded
def track_exists(track_id: str):
  return os.path.exists(track_path(track_id))

def delete_track(track_id: str):
  if not track_exists(track_id):
    return False
  
  path = track_path(track_id)
  logging.debug(f"Removing file from disk: {path}")
  os.remove(path)
  logging.debug(f"Successfully removed file.")
  return True

def delete_cover(dir: str, _cover_id: str):
  if not cover_exists(dir, _cover_id):
    return False
  
  path = cover_path(dir=dir, _cover_id=_cover_id)
  logging.debug(f"Removing file from disk: {path}")
  os.remove(path)
  logging.debug(f"Successfully removed file.")
  return True

def delete_tracks(track_ids: tuple[str] | list[str]):
  total = len(track_ids)
  logging.debug(f"Deleting {total} tracks from disk...")
  delete_count = 0
  for track_id in track_ids:
    result = delete_track(track_id)
    delete_count += int(result)
  logging.debug(f"Successfully deleted {delete_count} of {total} files.")
  return delete_count

def delete_covers(dir: str, cover_ids: tuple[str] | list[str]):
  total = len(cover_ids)
  logging.debug(f"Deleting {total} covers from disk...")
  delete_count = 0
  for cover_id in cover_ids:
    result = delete_cover(dir, cover_id)
    delete_count += int(result)
  logging.debug(f"Successfully deleted {delete_count} of {total} files.")
  return delete_count

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

# safely create missing directories for the target output directories
def create_dirs():
  logging.info("Creating necessary directories on disk...")
  logging.debug(f"Creating ouput directories for track downloads: {TRACKS_DIR}")
  os.makedirs(TRACKS_DIR, exist_ok=True)

  logging.debug(f"Creating output directories for track cover downloads: {TRACK_COVERS_DIR}")
  os.makedirs(TRACK_COVERS_DIR, exist_ok=True)

  logging.debug(f"Creating output directories for playlist cover downloads: {PLAYLIST_COVERS_DIR}")
  os.makedirs(PLAYLIST_COVERS_DIR, exist_ok=True)
  logging.info("Successfully created directories.")