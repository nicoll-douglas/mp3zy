from __future__ import annotations
import logging, traceback
import disk
import yt_dlp

class YtDlpClient:
  def download_track(self, track_info: dict[str]):
    logging.debug(f"Downloading track: {track_info["id"]} ({track_info["name"]})")

    track = disk.Track(track_info["id"])

    if track.exists():
      logging.debug("Track is already downloaded, skipping...")
      return track.get_path(), False
      
    ydl_opts = self._get_dl_opts(track_info["id"])
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      first, second = self._query_youtube(ydl, track_info)

      # check for entries
      if not first:
        logging.warning("Found no downloadable entries to try, skipping....")
        return None, None
      
      # helper
      def try_entry(entry: dict[str], number: int):
        try:
          logging.debug(f"Found entry ({number}). Download starting...")
          ydl.download([entry["webpage_url"]])
          logging.debug(f"Successfully downloaded track: {track_info["id"]}")
          return True

        # log if failed to download
        except Exception as e:
          logging.error(f"An error occurred: {e}")
          logging.warning(f"Failed to download track: {track_info["id"]} ({track_info["name"]})")
          return False

      # try entries
      if try_entry(first, 1) or (second and try_entry(second, 2)):
        return track.get_path(), True

      logging.warning("No more entries to try, skipping...")
      return None, None
      
  def download_tracks(self, track_info_list: list[dict[str]]):
    total = len(track_info_list)
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    logging.info(f"Downloading {total} tracks...")
    for index, item in enumerate(track_info_list):
      current_num = index + 1
      
      logging.info(f"Downloading track {current_num} of {total}...")
      save_path, track_is_fresh = self.download_track(item)

      if not save_path:
        logging.warning(f"Track download {current_num} of {total} failed. ({item["id"], item["name"]})")
        fail_count += 1
        continue

      if not track_is_fresh:
        logging.info("Track already downloaded so skipped.")
        skip_count += 1
        continue

      logging.info(f"Successfully downloaded track {current_num} of {total}.")
      success_count += 1

    logging.info(
      f"{skip_count} tracks already downloaded. Successfully downloaded {success_count} of {total - skip_count}. {fail_count} failed."
    )

  def _get_dl_opts(self, track_id: str):
    return {
      "format": "bestaudio/best",
      "noplaylist": True,
      "quiet": True,
      "no_warnings": True,
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
      }],
      "outtmpl": disk.Track(track_id).ytdtl_download_path()
    }

  def _query_youtube(
    self, 
    ydl: yt_dlp.YoutubeDL, 
    track_info: dict[str]
  ):
    track_name = track_info["name"]
    track_artists = ", ".join(track_info["artists"]) 
    search_query = f"ytsearch5:{track_name} {track_artists}"
    logging.debug(f"Finding entries for query: {search_query}")

    try:
      info = ydl.extract_info(search_query, download=False)
      
      logging.debug("Finding best track candidate...")
      best_entries = self._get_best_track_candidates(
        info.get("entries", []) if info else [], 
        track_info
      )

      return best_entries
    except Exception as e:
      logging.error(f"An error occurred: {e}")
      return [None, None]
    
  def _get_best_track_candidates(
    self,
    entries: list[dict[str]], 
    track_info: dict[str]
  ):
    track_name = track_info["name"].lower()
    track_artists = [t.lower() for t in track_info["artists"]]
    track_duration_s = track_info["duration_s"]

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

    results = sorted(entries, key=score, reverse=True)[:2]

    match len(results):
      case 2:
        return results
      case 1:
        return [results[0], None]
      case 0:
        return [None, None]