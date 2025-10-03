from ..download_search_result import DownloadSearchResult

class GetDownloadsSearchResponse:
  """Class that contains nested classes to be used as models for responses to the GET /downloads/search endpoint.
  """

  class BadRequest:
    """Represents the response body for a 400 status code response to a GET /downloads/search request.

    Attributes:
      parameter (str): The first parameter that failed validation; will match one of the request parameter names.
      message (str): A user-friendly message indicating the validation error.
    """
    
    parameter: str
    message: str


    def __init__(self, parameter: str, message: str):
      self.parameter = parameter
      self.message = message
    # END __init__

  # END class BadRequest


  class Ok:
    """Represents the response body for a 200 status code response to a GET /downloads/search request.

    Attributes:
      results (list[DownloadSearchResult]): A list of download search results.
    """

    results: list[DownloadSearchResult]


    def __init__(self, results: list[DownloadSearchResult]):
      self.results = results
    # END __init__


    def get_serializable(self):
      """Returns the class attributes as a serializable dictionary.

      Returns:
        dict: The dictionary of class attributes.
      """
      
      return {
        "results": [r.__dict__ for r in self.results]
      }
    # END get_serializable
    
  # END class Ok

# END class GetDownloadsSearchResponse