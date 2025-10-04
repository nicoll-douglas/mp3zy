from werkzeug.datastructures import MultiDict
from user_types.reponses import GetDownloadsSearchResponse
from user_types.requests import GetDownloadsSearchRequest
from typing import Literal

class GetDownloadsSearchValidator:
  """Validator class that validates request parameters of requests made to the GET /downloads/search endpoint.

  Attributes:
    _response (GetDownloadsSearchResponse.BadRequest): A response body model instance associated with the endpoint.
    _request (GetDownloadsSearchRequest): A request parameters model instance associated with the endpoint.
  """
  
  _response: GetDownloadsSearchResponse.BadRequest
  _request: GetDownloadsSearchRequest


  def __init__(self):
    self._response = GetDownloadsSearchResponse.BadRequest()
    self._request = GetDownloadsSearchRequest()
  # END __init__


  def validate(self, params: MultiDict[str, str]) -> tuple[Literal[False], GetDownloadsSearchResponse.BadRequest] | tuple[Literal[True], GetDownloadsSearchRequest]:
    """Performs full validation on the request parameters.

    Args:
      params (MultiDict[str, str]): The request parameters.

    Returns:
      tuple[Literal[False], PostDownloadsResponse.BadRequest] | tuple[Literal[True], PostDownloadsRequest]: A tuple where on successful validation the first element is True and the second are the sanitized params, or on failure the first element is False and the second is the response body to send.
    """
    
    bad_request = (False, self._response)
    self._response.parameter = "main_artist"
    main_artist = params.get(self._response.parameter)

    if not main_artist:
      self._response.message = f"Parameter `{self._response.parameter}` is required."
      return bad_request
    
    self._response.parameter = "track_name"
    track_name = params.get(self._response.parameter)

    if not track_name:
      self._response.message = f"Parameter `{self._response.parameter}` is required."
      return bad_request

    self._request.main_artist = main_artist
    self._request.track_name = track_name

    return True, self._request
  # END validate

# END class GetDownloadsSearchValidator