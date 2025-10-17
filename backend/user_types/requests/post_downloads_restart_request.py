class PostDownloadsRestartRequest:
  """Type that represents a validated request body to endpoint POST /downloads/restart.

  Attributes:
    download_ids (list[int]): The IDs of the downloads to restart.
  """
  
  download_ids: list[int]
  
# END class PostDownloadsRestartRequest