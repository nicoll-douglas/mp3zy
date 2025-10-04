from werkzeug.datastructures import MultiDict
from user_types.reponses import GetDownloadsSearchResponse
from user_types.requests import GetDownloadsSearchRequest
from typing import Literal

def get_downloads_search_validate(params: MultiDict[str, str]) -> tuple[Literal[False], GetDownloadsSearchResponse.BadRequest] | tuple[Literal[True], GetDownloadsSearchRequest]:
  """Validates the parameters of a request made to the GET /downloads/search endpoint.

  Args:
    params (MultiDict[str, str]): The params of the request.

  Returns:
    tuple[Literal[False], PostDownloadsResponse.BadRequest] | tuple[Literal[True], PostDownloadsRequest]: A tuple where on successful validation the first element is True and the second are the sanitized params, or on failure the first element is False and the second is the response body to send.
  """
  
  res = GetDownloadsSearchResponse.BadRequest()
  res.parameter = "main_artist"
  main_artist = params.get(res.parameter)

  if not main_artist:
    res.message = f"Parameter `{res.parameter}` is required."
    return False, res
  
  res.parameter = "track_name"
  track_name = params.get(res.parameter)

  if not track_name:
    res.message = f"Parameter `{res.parameter}` is required."
    return False, res

  req = GetDownloadsSearchRequest()
  req.main_artist = main_artist
  req.track_name = track_name

  return True, req
# END get_downloads_search_validate