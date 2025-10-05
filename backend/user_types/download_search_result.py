class DownloadSearchResult:
  """A class that contains app-relevant data retrieved from a YouTube download search result.

  Attributes:
    title (str | None): The title of the YouTube video.
    channel (str | None): The channel of the YouTube video.
    url (str): The URL fo the YouTube video; can be passed to the app downloader in order to download.
    thumbnail (str | None): The URL of the YouTube video thumbnail.
  """
  
  title: str | None
  channel: str | None
  url: str
  duration: int | float | None
  thumbnail: str | None
  
# END class DownloadSearchResult