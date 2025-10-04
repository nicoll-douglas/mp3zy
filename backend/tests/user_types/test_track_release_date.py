import pytest
from enum import Enum
from user_types import TrackReleaseDate

class ValidateAssertion(Enum):
  VALID = 1
  INVALID = 2
# END ValidateAssertion


@pytest.fixture(params=[
  # (data test value, field name test value, assertion type, (year value, month value, day value))
  (None, None, ValidateAssertion.INVALID, ()),
  (None, "abcd", ValidateAssertion.INVALID, ()),
  ([], None, ValidateAssertion.INVALID, ()),
  ({}, "abcd", ValidateAssertion.INVALID, ()),
  ({ "year": None }, None, ValidateAssertion.INVALID, ()),
  ({ "year": [2025] }, "abcd", ValidateAssertion.INVALID, ()),
  ({ "year": 13.5 }, None, ValidateAssertion.INVALID, ()),
  ({ "year": -1 }, "abcd", ValidateAssertion.INVALID, ()),
  ({ "year": 24034 }, None, ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": "6" }, "abcd", ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": [7] }, "", ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 5.5 }, None, ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": -1 }, "abcd", ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 0 }, "", ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 13 }, None, ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 5, "day": "4" }, None, ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 5, "day": 16.2 }, "", ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 5, "day": -1 }, None, ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 5, "day": 32 }, "abcd", ValidateAssertion.INVALID, ()),
  ({ "year": 2025, "month": 5, "day": 0 }, "", ValidateAssertion.INVALID, ()),
  ({ "year": 2025 }, "abcd", ValidateAssertion.VALID, (2025, None, None)),
  ({ "year": 2025, "day": 5 }, None, ValidateAssertion.VALID, (2025, None, None)),
  ({ "year": 2025, "month": 6 }, "abcd", ValidateAssertion.VALID, (2025, 6, None)),
  ({ "year": 2025, "month": 12, "day": 1 }, "", ValidateAssertion.VALID, (2025, 12, 1)),
  ({ "year": 2025, "month": 1, "day": 31 }, None, ValidateAssertion.VALID, (2025, 1, 31)),
  ({ "year": 2025, "month": None, "day": 31 }, "", ValidateAssertion.VALID, (2025, None, None)),
  ({ "year": 2025, "month": 3, "day": None }, "abcd", ValidateAssertion.VALID, (2025, 3, None)),
])
def init_fixture(request):
  return request.param
# END init_fixture


class TestTrackReleaseDate:

  def test_init(self, init_fixture):
    data_test_value, field_name_test_value, assertion_type, expected_release_date = init_fixture

    if assertion_type is ValidateAssertion.INVALID:
      with pytest.raises(ValueError) as excinfo:
        TrackReleaseDate(data_test_value, field_name_test_value)
      
      if field_name_test_value:
        assert len(excinfo.value.args) == 2
        assert isinstance(excinfo.value.args[1], str)
        assert excinfo.value.args[1] != ""
      else:
        assert len(excinfo.value.args) == 1
        
      assert isinstance(excinfo.value.args[0], str)
      assert excinfo.value.args[0] != ""

    elif assertion_type is ValidateAssertion.VALID:
      track_release_date = TrackReleaseDate(data_test_value)
      expected_year, expected_month, expected_day = expected_release_date
      assert track_release_date.year is None if expected_year is None else track_release_date.year == expected_year
      assert track_release_date.month is None if expected_month is None else track_release_date.month == expected_month
      assert track_release_date.day is None if expected_day is None else track_release_date.day == expected_day

    else:
      raise ValueError("Unknown assertion type")
  # END test_init

# END class TestTrackReleaseDate
