class DeleteDownloadsResponse():
  class BadRequest:
    """Represents the response body for a 400 status code response to a DELETE /downloads request.

    Attributes:
      field (str): The first field that failed request validation; will match a key in the JSON request body.
      message (str): A user-friendly message indicating the validation error.
    """
  
    field: str
    message: str

  # END class BadRequest


  class Ok:
    """Represents the response body for a 200 status code response to a DELETE /downloads request.

    Attributes:
      message (str): A user-friendly message.
      delete_count (int): The number of downloads deleted.
    """

    message: str
    delete_count: int
    
  # END class Ok

# END class DeleteDownloadsResponse