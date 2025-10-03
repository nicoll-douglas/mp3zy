class PostDownloadsResponse:
  """Class that contains nested classes to be used as models for responses to the POST /downloads endpoint.
  """

  class BadRequest:
    """Represents the response body for a 400 status code response to a POST /downloads request.

    Attributes:
      field (str): The first field that failed request validation; will match a key in the JSON request body.
      message (str): A user-friendly message indicating the validation error.
    """
    
    field: str
    message: str


    def __init__(self, field: str, message: str):
      self.field = field
      self.message = message
    # END __init__

  # END class BadRequest


  class Ok:
    """Represents the response body for a 200 status code response to a POST /downloads request.

    Attributes:
      download_id (int): The database ID of the download that was freshly queued and inserted into the database.
      message (str): A user-friendly message.
    """

    download_id: int
    message: str = "Your download has been queued and should start shortly."


    def __init__(self, download_id: int):
      self.download_id = download_id
    # END __init__
    
  # END class Ok

# END class PostDownloadsResponse