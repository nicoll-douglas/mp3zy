from user_types.reponses import PostDownloadsRestartResponse
from user_types.requests import PostDownloadsRestartRequest
from typing import Any, Literal

class PostDownloadsRestartValidator():
  """Validator class that validates request bodies to the POST /downloads/restart endpoint.

  Attributes:
    _response (PostDownloadsRestartResponse.BadRequest): A response body model instance associated with the endpoint.
    _request (PostDownloadsRestartRequest): A request body model instance associated with the endpoint.
  """
  
  _response: PostDownloadsRestartResponse.BadRequest
  _request: PostDownloadsRestartRequest


  def __init__(self):
    self._response = PostDownloadsRestartResponse.BadRequest()
    self._request = PostDownloadsRestartRequest()
  # END __init__


  def validate(self, body: Any)-> tuple[Literal[False], PostDownloadsRestartResponse.BadRequest] | tuple[Literal[True], PostDownloadsRestartRequest]:
    """Performs full validation on the request body.

    Args:
      body (Any): A request body to validate.

    Returns:
      tuple[Literal[False], PostDownloadsRestartResponse.BadRequest] | tuple[Literal[True], PostDownloadsRestartRequest]: A tuple where on successful validation the first element is True and the second is the sanitized request body, or on failure the first element is False and the second is the response body to send.
    """
    
    bad_request = (False, self._response)
    
    if body is None or not isinstance(body, dict):
      self._response.field = ""
      self._response.message = "Body must be an object."
      return bad_request
    
    self._response.field = "download_id"
    download_id = body.get(self._response.field)

    if download_id is None:
      self._response.message = f"Field `{self._response.field}` is required."
      return bad_request

    if not isinstance(download_id, int):
      self._response.message = f"Field `{self._response.field}` must be an integer."
      return bad_request
      
    if download_id < 1:
      self._response.message = f"Field `{self._response.field}` must be greater than 0."
      return bad_request
    
    self._request.download_id = download_id

    return True, self._request
  # END validate

# END class PostDownloadsRestartValidator