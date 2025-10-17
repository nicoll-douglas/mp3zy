class PostDownloadsRestartResponse():
  class BadRequest:
    """Represents the response body for a 400 status code response to a POST /downloads/restart request.

    Attributes:
      field (str): The first field that failed request validation; will match a key in the JSON request body.
      message (str): A user-friendly message indicating the validation error.
    """
  
    field: str
    message: str

  # END class BadRequest


  class Ok:
    """Represents the response body for a 200 status code response to a POST /downloads/restart request.

    Attributes:
      message (str): A user-friendly message.
      restart_count (int): The number of downloads restarted.
    """

    message: str
    restart_count: int
    
  # END class Ok

# END class PostDownloadsRestartResponse