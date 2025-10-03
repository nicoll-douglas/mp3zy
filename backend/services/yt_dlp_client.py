import models
import yt_dlp
from user_types.requests import PostDownloadsRequest, GetDownloadsSearchRequest

class YtDlpClient:
  
  def query_youtube(self, query: GetDownloadsSearchRequest) -> list:
    """Scrapes and aggregates search results based on the query for YouTube videos that may be downloaded as an audio source.

    Args:
      query (GetDownloadsSearchRequest): The search query containing the main artist and name of the track.

    Returns:
      list: The search results.
    """
    
    search_query = f"ytsearch10:{query.main_artist} {query.track_name}"
    
    info = yt_dlp.YoutubeDL({
      "noplaylist": True,
      "extract_flat": True
    }).extract_info(search_query, download=False)

    return self._order_entries(info["entries"] or [], query)
  # END query_youtube

  
  def download_track(self,
    track_info: PostDownloadsRequest,
    progress_hook,
    save_dir: str | None = None,
    track_id: str | None = None
  ) -> models.disk.Track:
    track = models.disk.Track(track_info, save_dir, track_id)
    ydl_opts = {
      "format": "bestaudio/best",
      "progress_hooks": [progress_hook],
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": track_info.codec.value,
        "preferredquality": track_info.bitrate.value,
      }],
      "outtmpl": track.build_output_template()
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([track_info.url])

    return track
            
  def _order_entries(self, entries: list, query: GetDownloadsSearchRequest) -> list:
    """Orders search result entries based on how well they aligm with the search query.

    Args:
      entries (list): The search results entries.
      query (GetDownloadsSearchRequest): The search query.

    Returns:
      list: The orderered list of entries.
    """
    
    def score(entry: dict):
      video_title = entry.get("title", "").lower()
      video_channel = entry.get("channel", "").lower()
      view_count = entry.get("view_count", 0)
      score_value = 0

      if query.track_name.lower() in video_title:
        score_value += 5
      if "official audio" in video_title:
        score_value += 20
      if " - topic" in video_channel:
        score_value += 100
      if query.main_artist.lower() == video_channel:
        score_value += 5
      if query.main_artist.lower() in video_title:
        score_value += 5
      
      score_value += min(view_count // 100_000, 10)

      return score_value
    # END score

    return sorted(entries, key=score, reverse=True)
  # END _order_entries

