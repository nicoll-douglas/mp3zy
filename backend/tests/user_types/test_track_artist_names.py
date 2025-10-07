import pytest
from user_types import TrackArtistNames
from ..test_utils import ValidationCase
from typing import Any

@pytest.fixture(params=[
  # (data test value, field name test value, assertion type)
  (None, None, ValidationCase.INVALID),
  ("", "abcd", ValidationCase.INVALID),
  ({}, None, ValidationCase.INVALID),
  ([], "abcd", ValidationCase.INVALID),
  ([2345, {}, ""], None, ValidationCase.INVALID),
  (["", "abcd"], "abcd", ValidationCase.INVALID),
  (["ab"], None, ValidationCase.VALID),
  (["ab", "abcd"], "abcd", ValidationCase.VALID)
])
def init_fixture(request: pytest.FixtureRequest) -> tuple[Any, str | None, ValidationCase]:
  """Parametrized fixture providing test cases for the test_init method.

  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[Any, str | None, ValidationCase]: A tuple containing the test artist names data, the test field name, and the assertion type.
  """
  
  return request.param
# END init_fixture


class TestTrackArtistNames:
  """Contains a unit test for the constructor of the TrackArtistNames class.
  """

  def test_init(self, init_fixture):
    """Tests that the constructor correctly performs validation and raises any necessary errors or initializes its fields.

    Args:
      init_fixture (tuple[Any, str | None, ValidationCase, tuple[int, int | None, int | None] | None]): The parametrized fixture value containing the test case data.
    """
    
    data_test_value, field_name_test_value, assertion = init_fixture

    if assertion is ValidationCase.INVALID:
      with pytest.raises(ValueError) as excinfo:
        TrackArtistNames(data_test_value, field_name_test_value)

      assert len(excinfo.value.args) == 1
      assert isinstance(excinfo.value.args[0], str)
      assert excinfo.value.args[0] != ""

    elif assertion is ValidationCase.VALID:
      track_artist_names = TrackArtistNames(data_test_value, field_name_test_value)
      assert track_artist_names.data == data_test_value
      
    else:
      raise ValueError("Unknown assertion type")
  # END test_init

# END class TestTrackArtistNames
