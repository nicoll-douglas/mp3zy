from request_validate import GetDownloadsSearchValidator
from werkzeug.datastructures import MultiDict
from user_types.reponses import GetDownloadsSearchResponse
from user_types.requests import GetDownloadsSearchRequest
import pytest
from enum import Enum

class BadRequestParamsCase(Enum):
  """Represents different cases of invalid HTTP request parameters that can be supplied to the validate method of GetDownloadsSearchValidator.

  Attributes:
    BOTH_MISSING: Represents the case where both the `main_artist` and `track_name` parameters are missing.
    MAIN_ARTIST_MISSING: Represents the case where the `main_artist` parameter is missing.
    TRACK_NAME_MISSING: Represents the case where the `track_name` parameter is missing.
  """
  
  BOTH_MISSING = 1
  MAIN_ARTIST_MISSING = 2
  TRACK_NAME_MISSING = 3
# END class BadRequestParamsCase


class GoodRequestParamsCase(Enum):
  """Represents different cases of valid HTTP request parameters supplied to the validate method of GetDownloadsSearchValidator.

  Attributes:
    SINGLE_PARAMS: Represents the case where both the `main_artist` and `track_name` parameters are present as single parameters.
    LIST_PARAMS: Represents the case where both `main_artist` or `track_name` or both parameters are present as a list of values.
  """
  
  SINGLE_PARAMS = 1
  LIST_PARAMS = 2
# END class GoodRequestParamsCase


@pytest.fixture(params=[
  # (params test value, assertion type)
  (MultiDict(), BadRequestParamsCase.BOTH_MISSING),
  (MultiDict({ "track_name": "", "main_artist": "" }), BadRequestParamsCase.BOTH_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga" }), BadRequestParamsCase.MAIN_ARTIST_MISSING),
  (MultiDict({ "track_name": "Radio Ga Ga", "main_artist": "" }), BadRequestParamsCase.MAIN_ARTIST_MISSING),
  (MultiDict({ "main_artist": "Queen" }), BadRequestParamsCase.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "" }), BadRequestParamsCase.TRACK_NAME_MISSING),
  (MultiDict({ "main_artist": "Queen", "track_name": "Radio Ga Ga" }), GoodRequestParamsCase.SINGLE_PARAMS),
  (MultiDict([["main_artist", "Queen"], ["main_artist", "Led Zeppelin"], ["track_name", "Radio Ga Ga"], ["track_name", "Kashmir"]]), GoodRequestParamsCase.LIST_PARAMS)
])
def validate_fixture(request: pytest.FixtureRequest) -> tuple[MultiDict, BadRequestParamsCase | GoodRequestParamsCase]:
  """Parametrized fixture providing test cases for the test_validate method.
  
  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[MultiDict, BadRequestParamsCase | GoodRequestParamsCase]: The parameter; is a tuple containing mock Flask HTTP request parameters and the assertion type of the test case.
  """
  
  return request.param
# END validate_fixture


class TestGetDownloadsSearchValidator:
  """Unit tests for methods of the GetDownloadsSearchValidator class.
  """
  
  def test_validate(self, validate_fixture: tuple[MultiDict, BadRequestParamsCase | GoodRequestParamsCase]):
    """Verifies that the validate method validates request paramters correctly and returns the correct result.

    Args:
      validate_fixture (tuple[MultiDict, BadRequestParamsCase | GoodRequestParamsCase]): The parametrized fixture value containing the request parameters test case and the assertion type.
    """
    
    params_test_value, assertion = validate_fixture
    validation_result = GetDownloadsSearchValidator().validate(params_test_value)

    assert isinstance(validation_result, tuple)
    assert len(validation_result) == 2

    is_valid_flag, validation_result_data = validation_result
    
    if isinstance(assertion, BadRequestParamsCase):
      assert is_valid_flag is False
      assert isinstance(validation_result_data, GetDownloadsSearchResponse.BadRequest)
      assert hasattr(validation_result_data, "message")
      assert hasattr(validation_result_data, "parameter")
      assert isinstance(validation_result_data.message, str)

      if assertion is BadRequestParamsCase.BOTH_MISSING:
        assert validation_result_data.parameter == "main_artist" or validation_result_data.parameter == "track_name"

      elif assertion is BadRequestParamsCase.MAIN_ARTIST_MISSING:
        assert validation_result_data.parameter == "main_artist"

      elif assertion is BadRequestParamsCase.TRACK_NAME_MISSING:
        assert validation_result_data.parameter == "track_name"
        
    elif isinstance(assertion, GoodRequestParamsCase):
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