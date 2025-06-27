import os
import yt_dlp
from . import logger

OUTPUT_DIR = os.getenv("DL_OUTPUT_DIR")
TRACKS_DIR = os.path.join(OUTPUT_DIR, "tracks")
TRACK_COVERS_DIR = os.path.join(OUTPUT_DIR, "track_covers")
PLAYLIST_COVERS_DIR = os.path.join(OUTPUT_DIR, "playlist_covers")

# get the path to a track
def get_track_path(track_id: str):
  return os.path.join(TRACKS_DIR, f"{track_id}.mp3")

# checks if a track is downloaded
def track_is_downloaded(track_id: str):
  return os.path.exists(get_track_path(track_id))

# checks if a track cover is downloaded based on the full path stored in the database
def track_cover_is_downloaded(full_cover_path: str):
  return os.path.exists(full_cover_path)

# safely create missing directories for the target output directories
def create_output_dirs():
  logger.debug(f"Creating ouput directories for track downloads: {TRACKS_DIR}")
  os.makedirs(TRACKS_DIR, exist_ok=True)
  logger.success("Successfully created directories.")

  logger.debug(f"Creating output directories for track cover downloads: {TRACK_COVERS_DIR}")
  os.makedirs(TRACK_COVERS_DIR, exist_ok=True)
  logger.success("Successfully created directories.")

  logger.debug(f"Creating output directories for playlist cover downloads: {PLAYLIST_COVERS_DIR}")
  os.makedirs(PLAYLIST_COVERS_DIR, exist_ok=True)
  logger.success("Successfully created directories.")

# download the given track as an mp3 and save it to the target output directory
def download_track(track_name: str, track_artists: tuple, track_id: str):
  if track_is_downloaded(track_id):
    logger.debug(f"Track {track_id} is already downloaded, skipping...")
    return
  
  filename_template = f"{track_id}.%(ext)s"

  ydl_opts = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "postprocessors": [{
      "key": "FFmpegExtractAudio",
      "preferredcodec": "mp3",
      "preferredquality": "192",
    }],
    "outtmpl": os.path.join(OUTPUT_DIR, filename_template),
  }
  
  logger.debug(f"Downloading track: {track_id}")

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    search_query = f"ytsearch1:{", ".join(track_artists)} - {track_name}"
    info = ydl.extract_info(search_query, download=False)
    entry = info["entries"][0] if "entries" in info else info

    ydl.download([entry["webpage_url"]])

  logger.success(f"Successfully downloaded track: {track_id}")
  