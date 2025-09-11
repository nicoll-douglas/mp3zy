from __future__ import annotations
import models.disk as disk
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
  
  def download_track(self, url, task_id, codec, bitrate, progress_hook):
    track = disk.Track(codec=disk.Codec(codec))
    output_template = track.get_output_template(task_id)
    ydl_opts = {
      "format": "bestaudio/best",
      "progress_hooks": [progress_hook],
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": codec,
        "preferredquality": bitrate,
      }],
      "outtmpl": output_template
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])

    return track
            
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

