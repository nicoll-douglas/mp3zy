from request_validate import GetDownloadsSearchValidator
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
  # (params test value, assertion type)
  (MultiDict(), BadRequestParamsAssertion.BOTH_MISSING),
  (MultiDict({ "track_name": "", "main_artist": "" }), BadRequestParamsAssertion.BOTH_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga" }), BadRequestParamsAssertion.MAIN_ARTIST_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga", "main_artist": "" }), BadRequestParamsAssertion.MAIN_ARTIST_MISSING),
  (MultiDict({ "main_artist": "Queen" }), BadRequestParamsAssertion.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "" }), BadRequestParamsAssertion.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "Radio Ga Ga" }), GoodRequestParamsAssertion.SINGLE_PARAMS),
  (MultiDict([["main_artist", "Queen"], ["main_artist", "Led Zeppelin"], ["track_name", "Radio Ga Ga"], ["track_name", "Kashmir"]]), GoodRequestParamsAssertion.LIST_PARAMS)
])
def validate_fixture(request):
  return request.param
# END validate_fixture


class TestGetDownloadsSearchValidator:
  
  def test_validate(self, validate_fixture):
    params_test_value, assertion_type = validate_fixture
    test_result = GetDownloadsSearchValidator().validate(params_test_value)

    if isinstance(assertion_type, BadRequestParamsAssertion):
      assert test_result[0] is False
      assert isinstance(test_result[1], GetDownloadsSearchResponse.BadRequest)
      assert hasattr(test_result[1], "message")
      assert hasattr(test_result[1], "parameter")

      if assertion_type is BadRequestParamsAssertion.BOTH_MISSING:
        assert test_result[1].parameter == "main_artist" or test_result[1].parameter == "track_name"

      elif assertion_type is BadRequestParamsAssertion.MAIN_ARTIST_MISSING:
        assert test_result[1].parameter == "main_artist"

      elif assertion_type is BadRequestParamsAssertion.TRACK_NAME_MISSING:
        assert test_result[1].parameter == "track_name"
        
    elif isinstance(assertion_type, GoodRequestParamsAssertion):
      assert test_result[0] is True
      assert isinstance(test_result[1], GetDownloadsSearchRequest)
      assert hasattr(test_result[1], "main_artist")
      assert hasattr(test_result[1], "track_name")
      assert test_result[1].main_artist == "Queen"
      assert test_result[1].track_name == "Radio Ga Ga"
    
    else:
      raise ValueError("Unknown assertion type")
  # END test_validate

# END class