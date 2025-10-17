class DeleteDownloadsRequest:
  """Type that represents a validated request body to endpoint DELETE /downloads.

  Attributes:
    download_ids (list[int]): The IDs of the downloads to delete.
  """
  
  download_ids: list[int]
  
# END class DeleteDownloadsRequest