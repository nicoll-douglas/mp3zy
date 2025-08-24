from __future__ import annotations
import disk
import yt_dlp

class YtDlpClient:
  codec = None
  
  def __init__(
    self, 
    codec: disk.Codec
  ):
    self.codec = codec

  def download_track(
    self, 
    number = None, 
    artists: list = None, 
    name = None, 
    album = None, 
    disc_number = None,
    duration_ms = None
  ):
    track = disk.Track(number, artists, name, album, disc_number)

    # check if track is already downloaded
    path = track.search_and_get_path()
    if path:
      return path, False
    
    output_template = track.get_output_template()
    ydl_opts = self._get_dl_opts(output_template)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      # find download link
      link = self._get_download_link(ydl, name, artists, duration_ms)

      # check for link
      if not link:
        return None, None
      
      # download
      ydl.download([link])
    
    # build and return path
    track.ext = "." + self.codec.value
    return track.build_path(), True

  def _get_dl_opts(
    self, 
    output_template,
  ):
    return {
      "format": "bestaudio/best",
      "noplaylist": True,
      "quiet": True,
      "no_warnings": True,
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": self.codec.value,
        "preferredquality": "320",
      }],
      "outtmpl": output_template
    }

  # queries youtube and gets the download link
  def _get_download_link(
    self, 
    ydl: yt_dlp.YoutubeDL, 
    track_name,
    track_artists: list,
    track_duration_ms
  ):
    search_query = f"ytsearch10:{", ".join(track_artists)} - {track_name}"

    try:
      info = ydl.extract_info(search_query, download=False)
      
      entry = self._get_best_track_candidate(
        info.get("entries", []) if info else [], 
        track_name,
        track_artists,
        round(track_duration_ms / 1000)
      )

      return entry["webpage_url"]
    except Exception as e:
      return None
    
  def _get_best_track_candidate(self, entries, track_name, track_artists: list, track_duration_s):
    if not entries:
      return None

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
        score_value += 20
      if " - topic" in video_channel:
        score_value += 100
      if any(artist == video_channel for artist in track_artists):
        score_value += 5
      if duration_diff <= 15:
        score_value += 5
      if any(artist in video_title for artist in track_artists):
        score_value += 5
      
      score_value += min(view_count // 100_000, 10)

      return score_value

    return sorted(entries, key=score, reverse=True)[0]

