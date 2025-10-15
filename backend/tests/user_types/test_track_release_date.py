import pytest
from user_types import TrackReleaseDate
from tests.test_utils import ValidationCase
from typing import Any

@pytest.fixture(params=[
  # (data test value, field name test value, assertion type, (year value, month value, day value))
  (None, None, ValidationCase.INVALID, None),
  (None, "abcd", ValidationCase.INVALID, None),
  ([], None, ValidationCase.INVALID, None),
  ({}, "abcd", ValidationCase.INVALID, None),
  ({ "year": None }, None, ValidationCase.INVALID, None),
  ({ "year": [2025] }, "abcd", ValidationCase.INVALID, None),
  ({ "year": 13.5 }, None, ValidationCase.INVALID, None),
  ({ "year": -1 }, "abcd", ValidationCase.INVALID, None),
  ({ "year": 24034 }, None, ValidationCase.INVALID, None),
  ({ "year": 2025, "month": "6" }, "abcd", ValidationCase.INVALID, None),
  ({ "year": 2025, "month": [7] }, "", ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 5.5 }, None, ValidationCase.INVALID, None),
  ({ "year": 2025, "month": -1 }, "abcd", ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 0 }, "", ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 13 }, None, ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 5, "day": "4" }, None, ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 5, "day": 16.2 }, "", ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 5, "day": -1 }, None, ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 5, "day": 32 }, "abcd", ValidationCase.INVALID, None),
  ({ "year": 2025, "month": 5, "day": 0 }, "", ValidationCase.INVALID, None),
  ({ "year": 2025 }, "abcd", ValidationCase.VALID, (2025, None, None)),
  ({ "year": 2025, "day": 5 }, None, ValidationCase.VALID, (2025, None, None)),
  ({ "year": 2025, "month": 6 }, "abcd", ValidationCase.VALID, (2025, 6, None)),
  ({ "year": 2025, "month": 12, "day": 1 }, "", ValidationCase.VALID, (2025, 12, 1)),
  ({ "year": 2025, "month": 1, "day": 31 }, None, ValidationCase.VALID, (2025, 1, 31)),
  ({ "year": 9999, "month": None, "day": 31 }, "", ValidationCase.VALID, (9999, None, None)),
  ({ "year": 0, "month": 3, "day": None }, "abcd", ValidationCase.VALID, (0, 3, None)),
])
def init_fixture(request: pytest.FixtureRequest) -> tuple[
  Any, 
  str | None, 
  ValidationCase, 
  tuple[int, int | None, int | None] | None
]:
  """Parametrized fixture providing test cases for the test_init method.

  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[Any, str | None, ValidationCase, tuple[int, int | None, int | None] | None]: A tuple containing the test release date data, the test field name, the assertion type, and a tuple (or None) of the expected values.
  """
  
  return request.param
# END init_fixture


class TestTrackReleaseDate:
  """Contains a unit test for the constructor of the TrackReleaseDate class.
  """

  def test_init(self, init_fixture: tuple[Any, str | None, ValidationCase, tuple[int, int | None, int | None] | None]):
    """Tests that the constructor correctly performs validation and raises any necessary errors or initializes its fields.

    Args:
      init_fixture (tuple[Any, str | None, ValidationCase, tuple[int, int | None, int | None] | None]): The parametrized fixture value containing the test case data.
    """
    
    data_test_value, field_name_test_value, assertion, expected_release_date = init_fixture

    if assertion is ValidationCase.INVALID:
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

    elif assertion is ValidationCase.VALID:
      track_release_date = TrackReleaseDate(data_test_value)
      expected_year, expected_month, expected_day = expected_release_date
      assert hasattr(track_release_date, "year")
      assert hasattr(track_release_date, "month")
      assert hasattr(track_release_date, "day")
      assert track_release_date.year is None if expected_year is None else track_release_date.year == expected_year
      assert track_release_date.month is None if expected_month is None else track_release_date.month == expected_month
      assert track_release_date.day is None if expected_day is None else track_release_date.day == expected_day

    else:
      raise ValueError("Unknown assertion type")
  # END test_init

# END class TestTrackReleaseDate
