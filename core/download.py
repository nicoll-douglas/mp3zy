import os, requests, mimetypes, logging
import yt_dlp
from . import app, disk

# download the given track as an mp3 and save it to the target output directory
def track(track_id: str, track_name: str, track_artists: list):
  logging.debug(f"Downloading track: {track_id}")

  if disk.track_is_downloaded(track_id):
    logging.debug("Track is already downloaded, skipping...")
    return disk.get_track_path(track_id), False
    
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
    "outtmpl": os.path.join(disk.TRACKS_DIR, filename_template),
  }
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    search_query = f"ytsearch10:{track_name} {", ".join(track_artists)}"
    info = ydl.extract_info(search_query, download=False)
    entry = info["entries"][0] if "entries" in info else info

    ydl.download([entry["webpage_url"]])

  logging.debug(f"Successfully downloaded track: {track_id}")

  return disk.get_track_path(track_id), True
  
# download an image and save it to disk at the specified path
def cover_image(url: str, target_dir: str):
  logging.debug(f"Downloading cover image: {url}")
  cover_id = disk.get_cover_id(url)

  if disk.cover_is_downloaded(disk.TRACK_COVERS_DIR, cover_id):
    logging.debug("Cover image is already downloaded, skipping...")
    cover_path = disk.get_cover_path(target_dir, url)
    return cover_path, False
  
  response = requests.get(url)
  app.handle_http_response(response, "Cover image request")

  content_type = response.headers.get("Content-Type", "")
  ext = mimetypes.guess_extension(content_type.split(";")[0])

  if not ext:
    ext = "jpg"

  cover_path = disk.get_cover_path(target_dir, url, ext)
  
  logging.debug(f"Saving cover image to disk at: {cover_path}")
  
  with open(cover_path, "wb") as f:
    f.write(response.content)

  logging.debug("Successfully saved image to disk.")

  return cover_path, True
