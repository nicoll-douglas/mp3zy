import os, requests, mimetypes, logging
import yt_dlp
from . import app, disk

# download the given track as an mp3 and save it to the target output directory
def track(track_info: dict):
  logging.debug(f"Downloading track: {track_info["id"]}")

  if disk.track_is_downloaded(track_info["id"]):
    logging.debug("Track is already downloaded, skipping...")
    return disk.track_path(track_info["id"]), False
    
  filename_template = f"{track_info["id"]}.%(ext)s"

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
    search_query = f"ytsearch20:{track_info["name"]} {", ".join(track_info["artists"])}"
    info = ydl.extract_info(search_query, download=False)
    entry = best_track_candidate(info["entries"], track_info)

    if not entry:
      raise RuntimeError(f"Failed to find downloadable entries for track: {track_info["id"]} ({track_info["name"]})")

    ydl.download([entry["webpage_url"]])

  logging.debug(f"Successfully downloaded track: {track_info["id"]}")

  return disk.track_path(track_info["id"]), True
  
# download an image and save it to disk at the specified path
def cover_image(url: str, target_dir: str):
  logging.debug(f"Downloading cover image: {url}")
  cover_id = disk.get_cover_id(url)

  if disk.cover_is_downloaded(disk.TRACK_COVERS_DIR, cover_id):
    logging.debug("Cover image is already downloaded, skipping...")
    cover_path = disk.cover_path(target_dir, url)
    return cover_path, False
  
  response = requests.get(url)
  app.handle_http_response(response, "Cover image request")

  content_type = response.headers.get("Content-Type", "")
  ext = mimetypes.guess_extension(content_type.split(";")[0])

  if not ext:
    ext = "jpg"

  cover_path = disk.cover_path(target_dir, url, ext)
  
  logging.debug(f"Saving cover image to disk at: {cover_path}")
  
  with open(cover_path, "wb") as f:
    f.write(response.content)

  logging.debug("Successfully saved image to disk.")

  return cover_path, True

def best_track_candidate(entries: list[dict[str]], track: dict[str]):
  track_name = track["name"].lower()
  track_artists = [t.lower() for t in track["artists"]]
  track_duration_s = track["duration_s"]

  def score(entry):
    video_title = entry.get("title", "").lower()
    video_channel = entry.get("channel", "").lower()
    video_duration_s = entry.get("duration", 0)
    view_count = entry.get("view_count", 0)
    duration_diff = abs(video_duration_s - track_duration_s)

    score_value = 0

    if track_name in video_title:
      score_value += 5
    if "official audio" in video_title:
      score_value += 30
    if " - topic" in video_channel:
      score_value += 20
    if any(artist == video_channel for artist in track_artists):
      score_value += 20
    if duration_diff <= 15:
      score_value += 5
    if any(artist in video_title for artist in track_artists):
      score_value += 5
    
    score_value += min(view_count // 100_000, 10)

    return score_value

  return max(entries, key=score, default=None)
