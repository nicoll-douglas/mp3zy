class PostDownloadsResponse:
  class BadRequest:
    field: str
    message: str

    def __init__(self, field: str, message: str):
      self.field = field
      self.message = message
    # END __init__
  # END class BadRequest

  class Ok:
    download_id: int
    message: str = "Your download has been queued and should start shortly."

    def __init__(self, download_id: int):
      self.download_id = download_id
    # END __init__

# END class PostDownloadsResponse