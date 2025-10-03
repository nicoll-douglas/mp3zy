class DownloadSearchResult:
  """A class that contains app-relevant data retrieved from a YouTube download search result.

  Attributes:
    title (str): The title of the YouTube video.
    channel (str): The channel of the YouTube video.
    duration (float | int): The duration of the YouTube video.
    url (str): The URL fo the YouTube video; can be passed to the app downloader in order to download.
  """
  
  title: str
  channel: str
  duration: int
  url: str
  
# END class DownloadSearchResult