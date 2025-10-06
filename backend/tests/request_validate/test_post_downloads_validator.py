from enum import Enum
import pytest
from request_validate import PostDownloadsValidator
from typing import Any, Literal

class ValidationCase(Enum):
  """Represents test case assertions for validator function results.

  Attributes:
    VALID: Represents the case where validation passes for a validator.
    INVALID: Represents the case where valdation does not pass for a validator.
  """
  
  VALID = 1
  INVALID = 2
# END class ValidationCase


@pytest.fixture(params=[
  # (body test value, assertion type)
  (None, ValidationCase.INVALID),
  ([], ValidationCase.INVALID),
  ("{}", ValidationCase.INVALID),
  ({}, ValidationCase.VALID),
  ({ "key": "value" }, ValidationCase.VALID)
])
def validate_body_fixture(request: pytest.FixtureRequest) ->  tuple[Any, ValidationCase]:
  """Parametrized fixture providing test cases for the test_validate_body method.
  
  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[Any, ValidationCase]: The parameter; is a tuple containing the mock HTTP request body and the assertion type of the test case.
  """

  return request.param
# END validate_body_fixture


@pytest.fixture(params=[
  # (body test value, assertion type)
  ({}, ValidationCase.INVALID),
  ({ "track_name": None }, ValidationCase.INVALID),
  ({ "track_name": "" }, ValidationCase.INVALID),
  ({ "track_name": 343 }, ValidationCase.INVALID),
  ({ "track_name": ["abcd"] }, ValidationCase.INVALID),
  ({ "track_name": "abcd" }, ValidationCase.VALID)
])
def validate_track_name_fixture(request: pytest.FixtureRequest) -> tuple[dict, ValidationCase]:
  """Parametrized fixture providing test cases for the test_validate_track method.
  
  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[dict, ValidationCase]: The parameter; is a tuple containing the mock HTTP request body and the assertion type of the test case.
  """
  
  return request.param
# END validate_track_name_fixture


@pytest.fixture(params=[
  # (body test value, assertion type)
  ({}, ValidationCase.INVALID),
  ({ "url": None }, ValidationCase.INVALID),
  ({ "url": "" }, ValidationCase.INVALID),
  ({ "url": 343 }, ValidationCase.INVALID),
  ({ "url": ["abcd"] }, ValidationCase.INVALID),
  ({ "url": "abcd" }, ValidationCase.VALID)
])
def validate_url_fixture(request: pytest.FixtureRequest) -> tuple[dict, ValidationCase]:
  """Parametrized fixture providing test cases for the test_validate_url method.
  
  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[dict, ValidationCase]: The parameter; is a tuple containing the mock HTTP request body and the assertion type of the test case.
  """
  
  return request.param
# END validate_url_fixture


@pytest.fixture(params=[
  # (body test value, assertion type)
  ({}, ValidationCase.VALID),
  ({ "album_name": None }, ValidationCase.VALID),
  ({ "album_name": "" }, ValidationCase.VALID),
  ({ "album_name": 324 }, ValidationCase.INVALID),
  ({ "album_name": ["abcd"] }, ValidationCase.INVALID),
  ({ "album_name": "abcd" }, ValidationCase.VALID)
])
def validate_album_name_fixture(request: pytest.FixtureRequest) -> tuple[dict, ValidationCase]:
  """Parametrized fixture providing test cases for the test_validation_album_name method.
  
  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[dict, ValidationCase]: The parameter; is a tuple containing the mock HTTP request body and the assertion type of the test case.
  """
  
  return request.param
# END validate_album_name_fixture


@pytest.fixture(params=[
  # (field name test value, body test value, assertion type)
  ("track_number", {}, ValidationCase.VALID),
  ("disc_number", { "disc_number": None }, ValidationCase.VALID),
  ("track_number", { "track_number": "234" }, ValidationCase.INVALID),
  ("disc_number", { "disc_number": ["4256"] }, ValidationCase.INVALID),
  ("track_number", { "track_number": -1 }, ValidationCase.INVALID),
  ("disc_number", { "disc_number": 0 }, ValidationCase.INVALID),
  ("track_number", { "track_number": 1 }, ValidationCase.VALID),
  ("disc_number", { "disc_number": 42 }, ValidationCase.VALID),
])
def validate_track_or_disc_number_fixture(request: pytest.FixtureRequest) -> tuple[Literal["track_number", "disc_number"], dict, ValidationCase]:
  """Parametrized fixture providing test cases for the test_validate_track_or_disc_number method.
  
  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[Literal["track_number", "disc_number"], dict, ValidationCase]: The parameter; is a tuple containing the mock field name, the mock HTTP request body and the assertion type of the test case.
  """
  
  return request.param
# END validate_track_or_disc_number_fixture


class TestPostDownloadsValidator:
  """Unit tests for methods of the PostDownloadsValidator class.
  """

  def test__validate_body(self, validate_body_fixture: tuple[Any, ValidationCase]):
    """Verifies that the _validate_body method validates the HTTP request body correctly for a valid request body.

    Args:
      validate_body_fixture (tuple[Any, ValidationCase]): The parametrized fixture value containing the request body test case and the assertion type.
    """
    
    body_test_value, assertion = validate_body_fixture
    validator = PostDownloadsValidator()
    validation_result = validator._validate_body(body_test_value)

    if assertion is ValidationCase.INVALID:
      assert validation_result is False
      assert hasattr(validator._response, "field")
      assert hasattr(validator._response, "message")
      assert isinstance(validator._response.field, str)
      assert isinstance(validator._response.message, str)

    elif assertion is ValidationCase.VALID:
      assert isinstance(validation_result, dict)
          
    else:
      raise ValueError("Unknown assertion type")
  # END test__validate_body


  def test__validate_track_name(self, validate_track_name_fixture: tuple[dict, ValidationCase]):
    """Verifies that the _validate_track_name method validates the HTTP request body correctly with respect to a track name field.

    Args:
      validate_track_name_fixture (tuple[dict, ValidationCase]): The parametrized fixture value containing the request body test case and the assertion type.
    """
    
    body_test_value, assertion = validate_track_name_fixture
    validator = PostDownloadsValidator()
    validation_result = validator._validate_track_name(body_test_value)

    if assertion is ValidationCase.INVALID:
      assert validation_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == "track_name"
      assert hasattr(validator._response, "message")
      assert isinstance(validator._response.message, str)

    elif assertion is ValidationCase.VALID:
      assert isinstance(validation_result, str)    

    else:
      raise ValueError("Unknown assertion type")
  # test__validate_track_name


  def test__validate_url(self, validate_url_fixture: tuple[dict, ValidationCase]):
    """Verifies that the _validate_url method validates the HTTP request body correctly with respect to a URL field.

    Args:
      validate_url_fixture (tuple[dict, ValidationCase]): The parametrized fixture value containing the request body test case and the assertion type.
    """
    
    body_test_value, assertion = validate_url_fixture
    validator = PostDownloadsValidator()
    validation_result = validator._validate_url(body_test_value)

    if assertion is ValidationCase.INVALID:
      assert validation_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == "url"
      assert hasattr(validator._response, "message")
      assert isinstance(validator._response.message, str)

    elif assertion is ValidationCase.VALID:
      assert isinstance(validation_result, str)
          
    else:
      raise ValueError("Unknown assertion type")
  # test__validate_url


  def test__validate_album_name(self, validate_album_name_fixture: tuple[dict, ValidationCase]):
    """Verifies that the _validate_album_name method validates the HTTP request body correctly with respect to an album name field.

    Args:
      validate_album_name_fixture (tuple[dict, ValidationCase]): The parametrized fixture value containing the request body test case and the assertion type.
    """
    
    body_test_value, assertion = validate_album_name_fixture
    validator = PostDownloadsValidator()
    validation_result = validator._validate_album_name(body_test_value)

    if assertion is ValidationCase.INVALID:
      assert validation_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == "album_name"
      assert hasattr(validator._response, "message")
      assert isinstance(validator._response.message, str)

    elif assertion is ValidationCase.VALID:
      assert validation_result is None or isinstance(validation_result, str)          

    else:
      raise ValueError("Unknown assertion type")
  # test__validate_album_name


  def test__validate_track_or_disc_number(self, validate_track_or_disc_number_fixture: tuple[Literal["track_number", "disc_number"], dict, ValidationCase]):
    """Verifies that the _validate_track_or_disc_number method validates the HTTP request body correctly with respect to the "disc_number" or "track_number" field.

    Args:
      validate_track_or_disc_number_fixture (tuple[Literal["track_number", "disc_number"], dict, ValidationCase]): The parametrized fixture value containing the field name test case, request body test case and the assertion type.
    """

    field_name_test_value, body_test_value, assertion = validate_track_or_disc_number_fixture
    validator = PostDownloadsValidator()
    validation_result = validator._validate_track_or_disc_number(body_test_value, field_name_test_value)

    if assertion is ValidationCase.INVALID:
      assert validation_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == field_name_test_value
      assert hasattr(validator._response, "message")
      assert isinstance(validator._response.message, str)

    elif assertion is ValidationCase.VALID:
      assert validation_result is None or isinstance(validation_result, int)

    else:
      raise ValueError("Unknown assertion type")
  # test__validate_track_or_disc_number

# END class TestPostDownloadsValidator