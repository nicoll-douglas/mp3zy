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

  def download_track(self, track_data):
    artists = track_data["artists"]
    track_name = track_data["track"]
    codec = track_data["codec"]

    track = media.Track(
      artist=artists[0], 
      name=track_name,
      codec=media.Codec(codec)
    )

    path = track.search_and_get_path()
    if path:
      return path, False
    
    bitrate = track_data["bitrate"]
    
    output_template = track.get_output_template()
    ydl_opts = self._get_dl_opts(output_template, codec, bitrate)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      link = track_data["download_url"]
      ydl.download([link])
    
    return track.build_path(), True

  def _get_dl_opts(self, output_template, codec, bitrate):
    return {
      "format": "bestaudio/best",
      "quiet": True,
      "no_warnings": True,
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": codec,
        "preferredquality": bitrate,
      }],
      "outtmpl": output_template
    }
        
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

