import pytest
from enum import Enum
from user_types import TrackArtistNames

class ValidateAssertion(Enum):
  VALID = 1
  INVALID = 2
# END ValidateAssertion


@pytest.fixture(params=[
  # (data test value, field name test value assertion type)
  (None, None, ValidateAssertion.INVALID),
  ("", "abcd", ValidateAssertion.INVALID),
  ({}, None, ValidateAssertion.INVALID),
  ([], "abcd", ValidateAssertion.INVALID),
  ([2345, {}, ""], None, ValidateAssertion.INVALID),
  (["", "abcd"], "abcd", ValidateAssertion.INVALID),
  (["ab"], None, ValidateAssertion.VALID),
  (["ab", "abcd"], "abcd", ValidateAssertion.VALID)
])
def init_fixture(request):
  return request.param
# END init_fixture


class TestTrackArtistNames:

  def test_init(self, init_fixture):
    data_test_value, field_name_test_value, assertion_type = init_fixture

    if assertion_type is ValidateAssertion.INVALID:
      with pytest.raises(ValueError) as excinfo:
        TrackArtistNames(data_test_value, field_name_test_value)

      assert len(excinfo.value.args) == 1
      assert isinstance(excinfo.value.args[0], str)
      assert excinfo.value.args[0] != ""

    elif assertion_type is ValidateAssertion.VALID:
      track_artist_names = TrackArtistNames(data_test_value, field_name_test_value)
      assert track_artist_names.data == data_test_value
      
    else:
      raise ValueError("Unknown assertion type")
  # END test_init

# END class TestTrackArtistNames
