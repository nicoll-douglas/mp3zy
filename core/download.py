import os, requests, mimetypes, logging
import yt_dlp
from . import disk

# download the given track as an mp3 and save it to the target output directory
def track(track_info: dict[str]):
  logging.debug(f"Downloading track: {track_info["id"]} ({track_info["name"]})")

  if disk.track_exists(track_info["id"]):
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
    search_query = f"ytsearch5:{track_info["name"]} {", ".join(track_info["artists"])}"

    # try to search
    try:
      info = ydl.extract_info(search_query, download=False)
      
      # try to get candidates
      logging.debug("Finding best track candidate...")
      best_entries = get_best_track_candidates(info["entries"], track_info)
      
      # throw if no candidates / get entries
      if not best_entries:
        raise RuntimeError(f"Failed to find downloadable entries for track: {track_info["id"]} ({track_info["name"]})")

    # log and skip if failed to get entries
    except Exception as e:
      logging.error(f"An error occurred: {e}")
      return None, None


    # download best candidate
    try:
      logging.debug("Found best track candidate. Download starting...")
      ydl.download([best_entries[0]["webpage_url"]])
      logging.debug(f"Successfully downloaded track: {track_info["id"]}")
      return disk.track_path(track_info["id"]), True

    # log if failed to download
    except Exception as e:
      logging.error(f"An error occurred: {e}")
      logging.warning(f"Failed to download best entry for {track_info["id"]} ({track_info["name"]})")

    # try next candidate if there is one
    try:
      if len(best_entries) > 1:
        logging.info(f"Trying next best entry...")
        ydl.download([best_entries[1]["webpage_url"]])
        logging.debug(f"Successfully downloaded track: {track_info["id"]}")
        return disk.track_path(track_info["id"]), True

    # log if failed to download
    except Exception as e:
      logging.error(f"An error occurred: {e}")

    # no more entries to try so skip
    logging.warning("No more entries to try, skipping...")
    return None, None
  
def tracks(track_info_list: list[str]) -> list[str]:
  total = len(track_info_list)
  dl_count = 0
  already_dl_count = 0
  fail_count = 0
  downloaded = []
  
  logging.info(f"Downloading {total} tracks...")
  for index, item in enumerate(track_info_list):
    current_num = index + 1
    
    logging.info(f"Downloading track {current_num} of {total}...")
    mp3_file_path, track_is_fresh = track(item)

    if not track_is_fresh:
      logging.info("Track already downloaded so skipped.")
      already_dl_count += 1

    if mp3_file_path and track_is_fresh:
      logging.info(f"Successfully downloaded track {current_num} of {total}.")
      downloaded.append(mp3_file_path)
      dl_count += 1
      
    if not mp3_file_path:
      logging.warning(f"Track download {current_num} of {total} failed. ({item["id"], item["name"]})")
      fail_count += 1

  logging.info(f"{already_dl_count} tracks already downloaded. Successfully downloaded {dl_count} of {total - already_dl_count}. {fail_count} failed.")
  return downloaded
  
# download an image and save it to disk at the specified path
def cover_image(url: str, target_dir: str):
  logging.debug(f"Downloading cover image: {url}")
  cover_id = disk.cover_id(url)

  if disk.cover_exists(target_dir, cover_id):
    logging.debug("Cover image is already downloaded, skipping...")
    cover_path = disk.cover_path(dir=target_dir, _cover_id=cover_id)
    return cover_path, False
  
  response = requests.get(url)
  if response.status_code != 200:
    logging.error("Cover image request failed.")
    return None, None

  content_type = response.headers.get("Content-Type", "")
  ext = mimetypes.guess_extension(content_type.split(";")[0])

  if not ext:
    ext = "jpg"

  cover_path = disk.cover_path(dir=target_dir, cover_source=url, ext=ext)
  
  logging.debug(f"Saving cover image to disk at: {cover_path}")
  disk.write_b(cover_path, response.content)
  logging.debug("Successfully saved image to disk.")

  return cover_path, True

def cover_images(urls: list[str] | tuple[str], target_dir: str) -> list[str]:
  total = len(urls)
  dl_count = 0
  already_dl_count = 0
  fail_count = 0
  downloaded = []
  
  logging.info(f"Downloading {total} cover images...")
  for index, url in enumerate(urls):
    current_num = index + 1
    
    logging.info(f"Downloading cover image {current_num} of {total}...")
    cover_path, cover_is_fresh = cover_image(url, target_dir)

    if not cover_is_fresh:
      logging.info("Cover image already downloaded so skipped.")
      already_dl_count += 1

    if cover_path and cover_is_fresh:
      logging.info(f"Successfully downloaded cover image {current_num} of {total}.")
      downloaded.append(cover_path)
      dl_count += 1
      
    if not cover_path:
      logging.warning(f"Cover image download {current_num} of {total} failed. ({url})")
      fail_count += 1

  logging.info(f"{already_dl_count} cover images already downloaded. Successfully downloaded {dl_count} of {total - already_dl_count}. {fail_count} failed.")
  return downloaded

def get_best_track_candidates(entries: list[dict[str]], track: dict[str]):  
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

  return sorted(entries, key=score, reverse=True)[:2]
