import pytest
from enum import Enum
from user_types import TrackArtistNames

class ValidateAssertion(Enum):
  VALID = 1
  INVALID = 2
# END ValidateAssertion


@pytest.fixture(params=[
  # (data test value, assertion type)
  (None, ValidateAssertion.INVALID),
  ("", ValidateAssertion.INVALID),
  ({}, ValidateAssertion.INVALID),
  ([], ValidateAssertion.INVALID),
  ([2345, {}, ""], ValidateAssertion.INVALID),
  (["", "abcd"], ValidateAssertion.INVALID),
  (["ab"], ValidateAssertion.VALID),
  (["ab", "abcd"], ValidateAssertion.VALID)
])
def validate_fixture(request):
  return request.param
# END validate_fixture


class TestTrackArtistNames:

  def test__validate(self, validate_fixture):
    data_test_value, assertion_type = validate_fixture

    if assertion_type is ValidateAssertion.INVALID:
      with pytest.raises(ValueError) as excinfo:
        TrackArtistNames(data_test_value)
      assert excinfo.value.args[0] != ""

    elif assertion_type is ValidateAssertion.VALID:
      track_artist_names = TrackArtistNames(data_test_value)
      assert track_artist_names.data == data_test_value
      
    else:
      raise ValueError("Unknown assertion type")
