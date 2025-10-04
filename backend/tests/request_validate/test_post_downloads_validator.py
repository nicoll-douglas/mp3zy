from enum import Enum
import pytest
from request_validate import PostDownloadsValidator

class ValidateAssertion(Enum):
  VALID = 1
  INVALID = 2
# END ValidateAssertion


@pytest.fixture(params=[
  # (body test value, assertion type)
  (None, ValidateAssertion.INVALID),
  ([], ValidateAssertion.INVALID),
  ("{}", ValidateAssertion.INVALID),
  ({}, ValidateAssertion.VALID),
  ({ "key": "value" }, ValidateAssertion.VALID)
])
def validate_body_fixture(request):
  return request.param
# END request_body_fixture


@pytest.fixture(params=[
  # (body test value, assertion type)
  ({}, ValidateAssertion.INVALID),
  ({ "track_name": None }, ValidateAssertion.INVALID),
  ({ "track_name": "" }, ValidateAssertion.INVALID),
  ({ "track_name": 343 }, ValidateAssertion.INVALID),
  ({ "track_name": ["abcd"] }, ValidateAssertion.INVALID),
  ({ "track_name": "abcd" }, ValidateAssertion.VALID)
])
def validate_track_name_fixture(request):
  return request.param
# END validate_track_name_fixture


@pytest.fixture(params=[
  # (body test value, assertion type)
  ({}, ValidateAssertion.INVALID),
  ({ "url": None }, ValidateAssertion.INVALID),
  ({ "url": "" }, ValidateAssertion.INVALID),
  ({ "url": 343 }, ValidateAssertion.INVALID),
  ({ "url": ["abcd"] }, ValidateAssertion.INVALID),
  ({ "url": "abcd" }, ValidateAssertion.VALID)
])
def validate_url_fixture(request):
  return request.param
# END validate_url_fixture


@pytest.fixture(params=[
  # (body test value, assertion type)
  ({}, ValidateAssertion.VALID),
  ({ "album_name": None }, ValidateAssertion.VALID),
  ({ "album_name": "" }, ValidateAssertion.VALID),
  ({ "album_name": 324 }, ValidateAssertion.INVALID),
  ({ "album_name": ["abcd"] }, ValidateAssertion.INVALID),
  ({ "album_name": "abcd" }, ValidateAssertion.VALID)
])
def validate_album_name_fixture(request):
  return request.param
# END validate_album_name_fixture


@pytest.fixture(params=[
  # (field name test value, body test value, assertion type)
  ("track_number", {}, ValidateAssertion.VALID),
  ("disc_number", { "disc_number": None }, ValidateAssertion.VALID),
  ("track_number", { "track_number": "234" }, ValidateAssertion.INVALID),
  ("disc_number", { "disc_number": ["4256"] }, ValidateAssertion.INVALID),
  ("track_number", { "track_number": -1 }, ValidateAssertion.INVALID),
  ("disc_number", { "disc_number": 0 }, ValidateAssertion.INVALID),
  ("track_number", { "track_number": 1 }, ValidateAssertion.VALID),
  ("disc_number", { "disc_number": 42 }, ValidateAssertion.VALID),
])
def validate_track_or_disc_number_fixture(request):
  return request.param
# END validate_track_or_disc_number_fixture


class TestPostDownloadsValidator:

  def test__validate_body(self, validate_body_fixture):
    body_test_value, assertion_type = validate_body_fixture
    validator = PostDownloadsValidator()
    test_result = validator._validate_body(body_test_value)

    if assertion_type is ValidateAssertion.INVALID:
      assert test_result is False
      assert hasattr(validator._response, "field")
      assert hasattr(validator._response, "message")

    elif assertion_type is ValidateAssertion.VALID:
      assert isinstance(test_result, dict)
          
    else:
      raise ValueError("Unknown assertion type")
  # END test__validate_body


  def test__validate_track_name(self, validate_track_name_fixture):
    body_test_value, assertion_type = validate_track_name_fixture
    validator = PostDownloadsValidator()
    test_result = validator._validate_track_name(body_test_value)

    if assertion_type is ValidateAssertion.INVALID:
      assert test_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == "track_name"
      assert hasattr(validator._response, "message")

    elif assertion_type is ValidateAssertion.VALID:
      assert isinstance(test_result, str)    

    else:
      raise ValueError("Unknown assertion type")
  # test__validate_track_name


  def test__validate_url(self, validate_url_fixture):
    body_test_value, assertion_type = validate_url_fixture
    validator = PostDownloadsValidator()
    test_result = validator._validate_url(body_test_value)

    if assertion_type is ValidateAssertion.INVALID:
      assert test_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == "url"
      assert hasattr(validator._response, "message")

    elif assertion_type is ValidateAssertion.VALID:
      assert isinstance(test_result, str)
          
    else:
      raise ValueError("Unknown assertion type")
  # test__validate_url


  def test__validate_album_name(self, validate_album_name_fixture):
    body_test_value, assertion_type = validate_album_name_fixture
    validator = PostDownloadsValidator()
    test_result = validator._validate_album_name(body_test_value)

    if assertion_type is ValidateAssertion.INVALID:
      assert test_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == "album_name"
      assert hasattr(validator._response, "message")

    elif assertion_type is ValidateAssertion.VALID:
      assert test_result is None or isinstance(test_result, str)          

    else:
      raise ValueError("Unknown assertion type")
  # test__validate_album_name


  def test__validate_track_or_disc_number(self, validate_track_or_disc_number_fixture):
    field_name_test_value, body_test_value, assertion_type = validate_track_or_disc_number_fixture
    validator = PostDownloadsValidator()
    test_result = validator._validate_track_or_disc_number(body_test_value, field_name_test_value)

    if assertion_type is ValidateAssertion.INVALID:
      assert test_result is False
      assert hasattr(validator._response, "field")
      assert validator._response.field == field_name_test_value
      assert hasattr(validator._response, "message")

    elif assertion_type is ValidateAssertion.VALID:
      assert test_result is None or isinstance(test_result, int)

    else:
      raise ValueError("Unknown assertion type")
  # test__validate_track_or_disc_number

# END class TestPostDownloadsValidator