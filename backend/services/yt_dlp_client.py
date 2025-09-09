from __future__ import annotations
import media
import yt_dlp

class YtDlpClient:
  def query_youtube(self, artist_name, track_name):
    search_query = f"ytsearch10:{artist_name} {track_name}"
    
    info = yt_dlp.YoutubeDL({
      "noplaylist": True,
      "extract_flat": True
    }).extract_info(search_query, download=False)

    return self.order_entries(
      entries=info["entries"] or [],
      track_name=track_name,
      track_artists=[artist_name]
    )

  def download_track(
    self, 
    number = None, 
    artists: list = None, 
    name = None, 
    album = None, 
    disc_number = None,
    duration_ms = None
  ):
    track = media.Track(number, artists, name, album, disc_number)

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

  def _get_download_link(self, entry):
    return entry["url"]
        
  def order_entries(self, entries, track_name, track_artists: list, track_duration_s = None):
    def score(entry):
      video_title = entry.get("title", "").lower()
      video_channel = entry.get("channel", "").lower()
      video_duration_s = entry.get("duration", 0)
      view_count = entry.get("view_count", 0)
      duration_diff = abs(video_duration_s - track_duration_s) if track_duration_s != None else None

      score_value = 0

      if track_name in video_title:
        score_value += 5
      if "official audio" in video_title:
        score_value += 20
      if " - topic" in video_channel:
        score_value += 100
      if any(artist == video_channel for artist in track_artists):
        score_value += 5
      if duration_diff != None and duration_diff <= 15:
        score_value += 5
      if any(artist in video_title for artist in track_artists):
        score_value += 5
      
      score_value += min(view_count // 100_000, 10)

      return score_value

    return sorted(entries, key=score, reverse=True)

