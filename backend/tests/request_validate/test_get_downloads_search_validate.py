from request_validate import get_downloads_search_validate
from werkzeug.datastructures import MultiDict
from user_types.reponses import GetDownloadsSearchResponse
from user_types.requests import GetDownloadsSearchRequest
import pytest
from enum import Enum

class BadRequestParamsAssertions(Enum):
  BOTH_MISSING = 1
  MAIN_ARTIST_MISSING = 2
  TRACK_NAME_MISSING = 3
# END class BadRequestParamsAssertions

class GoodRequestParamsAssertions(Enum):
  SINGLE_PARAMS = 1
  LIST_PARAMS = 2
# END class GoodRequestParamsAssertions


@pytest.fixture(params=[
  # (params value, assertion type)
  (MultiDict(), BadRequestParamsAssertions.BOTH_MISSING),
  (MultiDict({ "track_name": "", "main_artist": "" }), BadRequestParamsAssertions.BOTH_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga" }), BadRequestParamsAssertions.MAIN_ARTIST_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga", "main_artist": "" }), BadRequestParamsAssertions.MAIN_ARTIST_MISSING),
  (MultiDict({ "main_artist": "Queen" }), BadRequestParamsAssertions.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "" }), BadRequestParamsAssertions.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "Radio Ga Ga" }), GoodRequestParamsAssertions.SINGLE_PARAMS),
  (MultiDict([["main_artist", "Queen"], ["main_artist", "Led Zeppelin"], ["track_name", "Radio Ga Ga"], ["track_name", "Kashmir"]]), GoodRequestParamsAssertions.LIST_PARAMS)
])
def request_params_fixture(request):
  return request.param
# END request_params_fixture


def test_get_downloads_search_validate(request_params_fixture):
  """Ensures that request params are validated correctly for all fixture cases.
  """
  
  params, assertion_type = request_params_fixture
  
  result = get_downloads_search_validate(params)

  if isinstance(assertion_type, BadRequestParamsAssertions):
    assert result[0] == False
    assert isinstance(result[1], GetDownloadsSearchResponse.BadRequest)

    if assertion_type is BadRequestParamsAssertions.BOTH_MISSING or assertion_type is BadRequestParamsAssertions.MAIN_ARTIST_MISSING:
      assert result[1].parameter == "main_artist"
      assert result[1].message == "Parameter `main_artist` is required."

    elif assertion_type is BadRequestParamsAssertions.TRACK_NAME_MISSING:
      assert result[1].parameter == "track_name"
      assert result[1].message == "Parameter `track_name` is required."
      
  elif isinstance(assertion_type, GoodRequestParamsAssertions):
    assert result[0] == True
    assert isinstance(result[1], GetDownloadsSearchRequest)

    if assertion_type is GoodRequestParamsAssertions.SINGLE_PARAMS or assertion_type is GoodRequestParamsAssertions.LIST_PARAMS:
      assert result[1].main_artist == "Queen"
      assert result[1].track_name == "Radio Ga Ga"
# END test_get_downloads_search_validate


