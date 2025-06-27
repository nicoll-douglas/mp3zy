import os, glob, logging

STORAGE_DIR = os.getenv("STORAGE_DIR")
TRACKS_DIR = os.path.join(STORAGE_DIR, "tracks")
TRACK_COVERS_DIR = os.path.join(STORAGE_DIR, "track_covers")
PLAYLIST_COVERS_DIR = os.path.join(STORAGE_DIR, "playlist_covers")

def get_cover_id(cover_source: str):
  return cover_source.split("/")[-1]

# get the path to a track
def track_path(track_id: str):
  return os.path.join(TRACKS_DIR, f"{track_id}.mp3")

# gets the path to the cover image stored locally
def cover_path(dir: str, cover_source: str, ext: str | None = None):
  id = get_cover_id(cover_source)
  path_without_ext = os.path.join(dir, id)

  if not ext:
    files = glob.glob(path_without_ext + ".*")
    return files[0]
  
  return os.path.join(dir, id + ext)

# checks if a cover is downloaded
def cover_is_downloaded(dir: str, cover_id: str):
  path_without_ext = os.path.join(dir, cover_id)
  files = glob.glob(path_without_ext + ".*")
  return len(files) > 0

# checks if a track is downloaded
def track_is_downloaded(track_id: str):
  return os.path.exists(track_path(track_id))

# safely create missing directories for the target output directories
def create_dirs():
  logging.debug(f"Creating ouput directories for track downloads: {TRACKS_DIR}")
  os.makedirs(TRACKS_DIR, exist_ok=True)

  logging.debug(f"Creating output directories for track cover downloads: {TRACK_COVERS_DIR}")
  os.makedirs(TRACK_COVERS_DIR, exist_ok=True)

  logging.debug(f"Creating output directories for playlist cover downloads: {PLAYLIST_COVERS_DIR}")
  os.makedirs(PLAYLIST_COVERS_DIR, exist_ok=True)
  logging.debug("Successfully created directories.")