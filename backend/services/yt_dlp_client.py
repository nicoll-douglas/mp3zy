import models
import yt_dlp
from user_types.requests import PostDownloadsRequest, GetDownloadsSearchRequest
from user_types import DownloadSearchResult
from typing import Callable, Literal
from yt_dlp.utils import DownloadError, ExtractorError, UnsupportedError

class YtDlpClient:
  """Service class that interfaces with yt-dlp.
  """
  
  def query_youtube(self, query: GetDownloadsSearchRequest) -> tuple[Literal[False], str] | tuple[Literal[True], list[DownloadSearchResult]]:
    """Scrapes and aggregates search results of YouTube videos that may be downloaded as an audio source based on the query.

    Args:
      query (GetDownloadsSearchRequest): The search query containing the main artist and name of the track.

    Returns:
      tuple[Literal[False], str] | tuple[Literal[True], list[DownloadSearchResult]]: On failure the first element is False and the second is a user-friendly error message, otherwise the first element is True and the second is the search results.
    """
    
    search_query = f"ytsearch5:{query.main_artist} {query.track_name}"
    
    try:
      info = yt_dlp.YoutubeDL({
        "skip_download": True,
        "extract_flat": True
      }).extract_info(search_query, download=False)
    except DownloadError as e:
      return False, "Unable to fetch video data."
    except ExtractorError as e:
      return False, "Failed to extract video metadata."
    except UnsupportedError as e:
      return False, "Video search URL is not supported."
    except Exception as e:
      return False, "An unexpected error occurred."

    entries = info.get("entries", [])
    ordered_entries = self._order_entries(entries, query)
    search_results: list[DownloadSearchResult] = []

    for entry in ordered_entries:
      url = entry.get("url")

      if url:
        result = DownloadSearchResult()
        result.title = entry.get("title")
        result.url = url
        result.channel = entry.get("uploader") or entry.get("channel")
        result.duration = entry.get("duration")
        thumbnails = entry.get("thumbnails")

        if isinstance(thumbnails, list) and thumbnails and isinstance(thumbnails[0], dict) and thumbnails[0].get("url"):
          result.thumbnail = thumbnails[0].get("url")
        else:
          id = entry.get("id")
          result.thumbnail = f"https://i.ytimg.com/vi/{id}/hqdefault.jpg" if id else None

        search_results.append(result)

    return True, search_results
  # END query_youtube

  
  def download_track(self,
    track_info: PostDownloadsRequest,
    progress_hook: Callable[[dict], None],
    save_dir: str | None = None,
    track_id: str | None = None
  ) -> models.disk.Track:
    """Uses the yt-dlp downloader to download the associated track.

    Args:
      track_info (PostDownloadsRequest): Contains all information about the track.
      progress_hook (Callable[[dict], None]): The progress hook function to be passed to the downloader.
      save_dir (str | None): The preferred root directory that the track will be saved under.
      track_id (str | None): A unique identifier that will go in the downloaded track filename.

    Returns:
      models.disk.Track: A disk model track instance.
    """

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
  # END download_track


  def _order_entries(self, entries: list, query: GetDownloadsSearchRequest) -> list[dict]:
    """Orders search result entries based on how well they align with the search query.

    Args:
      entries (list): The search results entries.
      query (GetDownloadsSearchRequest): The search query.

    Returns:
      list: The orderered list of entries.
    """
    
    def score(entry: dict):
      video_title = entry.get("title")
      video_channel = entry.get("uploader") or entry.get("channel")
      view_count = entry.get("view_count")
      score_value = 0

      if video_title:
        if query.track_name.lower() in video_title.lower():
          score_value += 5
        if "official audio" in video_title:
          score_value += 20
        if query.main_artist.lower() in video_title.lower():
          score_value += 5

      if video_channel:
        if " - topic" in video_channel.lower():
          score_value += 100
        if query.main_artist.lower() == video_channel.lower():
          score_value += 5
      
      if view_count is not None:
        score_value += min(view_count // 100_000, 10)
      
      return score_value
    # END score

    return sorted(entries, key=score, reverse=True)
  # END _order_entries

# END class YtDlpClient