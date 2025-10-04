from request_validate import get_downloads_search_validate
from werkzeug.datastructures import MultiDict
from user_types.reponses import GetDownloadsSearchResponse
from user_types.requests import GetDownloadsSearchRequest
import pytest
from enum import Enum

class BadRequestParamsAssertion(Enum):
  BOTH_MISSING = 1
  MAIN_ARTIST_MISSING = 2
  TRACK_NAME_MISSING = 3
# END class BadRequestParamsAssertion


class GoodRequestParamsAssertion(Enum):
  SINGLE_PARAMS = 1
  LIST_PARAMS = 2
# END class GoodRequestParamsAssertion


@pytest.fixture(params=[
  # (params value, assertion type)
  (MultiDict(), BadRequestParamsAssertion.BOTH_MISSING),
  (MultiDict({ "track_name": "", "main_artist": "" }), BadRequestParamsAssertion.BOTH_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga" }), BadRequestParamsAssertion.MAIN_ARTIST_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga", "main_artist": "" }), BadRequestParamsAssertion.MAIN_ARTIST_MISSING),
  (MultiDict({ "main_artist": "Queen" }), BadRequestParamsAssertion.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "" }), BadRequestParamsAssertion.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "Radio Ga Ga" }), GoodRequestParamsAssertion.SINGLE_PARAMS),
  (MultiDict([["main_artist", "Queen"], ["main_artist", "Led Zeppelin"], ["track_name", "Radio Ga Ga"], ["track_name", "Kashmir"]]), GoodRequestParamsAssertion.LIST_PARAMS)
])
def request_params_fixture(request):
  return request.param
# END request_params_fixture


def test_get_downloads_search_validate(request_params_fixture):
  """Ensures that request params are validated correctly for all fixture cases.
  """
  
  params, assertion_type = request_params_fixture
  
  result = get_downloads_search_validate(params)

  if isinstance(assertion_type, BadRequestParamsAssertion):
    assert result[0] == False
    assert isinstance(result[1], GetDownloadsSearchResponse.BadRequest)

    if assertion_type is BadRequestParamsAssertion.BOTH_MISSING or assertion_type is BadRequestParamsAssertion.MAIN_ARTIST_MISSING:
      assert result[1].parameter == "main_artist"
      assert result[1].message == "Parameter `main_artist` is required."

    elif assertion_type is BadRequestParamsAssertion.TRACK_NAME_MISSING:
      assert result[1].parameter == "track_name"
      assert result[1].message == "Parameter `track_name` is required."
      
  elif isinstance(assertion_type, GoodRequestParamsAssertion):
    assert result[0] == True
    assert isinstance(result[1], GetDownloadsSearchRequest)

    if assertion_type is GoodRequestParamsAssertion.SINGLE_PARAMS or assertion_type is GoodRequestParamsAssertion.LIST_PARAMS:
      assert result[1].main_artist == "Queen"
      assert result[1].track_name == "Radio Ga Ga"
# END test_get_downloads_search_validate


