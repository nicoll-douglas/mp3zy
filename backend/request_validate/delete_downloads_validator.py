from user_types.reponses import DeleteDownloadsResponse
from user_types.requests import DeleteDownloadsRequest
from typing import Any, Literal

class DeleteDownloadsValidator():
  """Validator class that validates request bodies to the DELETE /downloads endpoint.

  Attributes:
    _response (DeleteDownloadsResponse.BadRequest): A response body model instance associated with the endpoint.
    _request (DeleteDownloadsRequest): A request body model instance associated with the endpoint.
  """
  
  _response: DeleteDownloadsResponse.BadRequest
  _request: DeleteDownloadsRequest


  def __init__(self):
    self._response = DeleteDownloadsResponse.BadRequest()
    self._request = DeleteDownloadsRequest()
  # END __init__


  def validate(self, body: Any)-> tuple[Literal[False], DeleteDownloadsResponse.BadRequest] | tuple[Literal[True], DeleteDownloadsRequest]:
    """Performs full validation on the request body.

    Args:
      body (Any): A request body to validate.

    Returns:
      tuple[Literal[False], DeleteDownloadsResponse.BadRequest] | tuple[Literal[True], DeleteDownloadsRequest]: A tuple where on successful validation the first element is True and the second is the sanitized request body, or on failure the first element is False and the second is the response body to send.
    """
    
    bad_request = (False, self._response)
    
    if body is None or not isinstance(body, dict):
      self._response.field = ""
      self._response.message = "Body must be an object."
      return bad_request
    
    self._response.field = "download_ids"
    download_ids = body.get(self._response.field)

    if download_ids is None:
      self._response.message = f"Field `{self._response.field}` is required."
      return bad_request
    
    if not isinstance(download_ids, list):
      self._response.message = f"Field `{self._response.field}` must be an array."
      return bad_request

    if len(list) == 0:
      self._response.message = f"Field `{self._response.field}` must be of at least length 1."
      return bad_request

    if not all(isinstance(id, int) for id in download_ids):
      self._response.message = f"Field `{self._response.field}` must be an array of integers."
      return bad_request
      
    if not all(id > 0 for id in download_ids):
      self._response.message = f"Field `{self._response.field}` must be an array of integers greater than 0."
      return bad_request
    
    self._request.download_ids = download_ids

    return True, self._request
  # END validate

# END class DeleteDownloadsValidator