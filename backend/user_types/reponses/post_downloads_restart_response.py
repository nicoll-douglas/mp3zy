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
    """

    message: str

    
    def __init__(self):
      self.message = "Your download has been queued and should restart shortly."
    # END __init__
    
  # END class Ok


  class ServerError:
    """Represents the response body for a 500 status code request to a GET /downloads/restart request.

    Attributes:
      message (str): A user-friendly error message.
    """

    message: str

  # END class ServerError

# END class PostDownloadsRestartResponse