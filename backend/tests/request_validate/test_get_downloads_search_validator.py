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

    assert isinstance(test_result, tuple)
    assert len(test_result) == 2

    is_valid_flag, validation_result_data = test_result
    
    if isinstance(assertion_type, BadRequestParamsAssertion):
      assert is_valid_flag is False
      assert isinstance(validation_result_data, GetDownloadsSearchResponse.BadRequest)
      assert hasattr(validation_result_data, "message")
      assert hasattr(validation_result_data, "parameter")
      assert isinstance(validation_result_data.message, str)

      if assertion_type is BadRequestParamsAssertion.BOTH_MISSING:
        assert validation_result_data.parameter == "main_artist" or validation_result_data.parameter == "track_name"

      elif assertion_type is BadRequestParamsAssertion.MAIN_ARTIST_MISSING:
        assert validation_result_data.parameter == "main_artist"

      elif assertion_type is BadRequestParamsAssertion.TRACK_NAME_MISSING:
        assert validation_result_data.parameter == "track_name"
        
    elif isinstance(assertion_type, GoodRequestParamsAssertion):
      assert is_valid_flag is True
      assert isinstance(validation_result_data, GetDownloadsSearchRequest)
      assert hasattr(validation_result_data, "main_artist")
      assert hasattr(validation_result_data, "track_name")
      assert validation_result_data.main_artist == "Queen"
      assert validation_result_data.track_name == "Radio Ga Ga"
    
    else:
      raise ValueError("Unknown assertion type")
  # END test_validate

# END class TestGetDownloadsSearchValidator