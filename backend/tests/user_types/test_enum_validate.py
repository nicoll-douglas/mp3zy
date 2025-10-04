from user_types import enum_validate
from enum import Enum
import pytest

class MyEnum(Enum):
  VALUE_1 = "value_1"
  VALUE_2 = "value_2"
  VALUE_3 = "value_3"
# END class MyEnum


class EnumValuesAssertion(Enum):
  IS_MISSING = 1
  IS_IN_ENUM = 2
  IS_INVALID = 3
# END class EnumValuesAssertion


@pytest.fixture(params=[
  ("", EnumValuesAssertion.IS_MISSING),
  (None, EnumValuesAssertion.IS_MISSING),
  ("value_1", EnumValuesAssertion.IS_IN_ENUM),
  ("value_3", EnumValuesAssertion.IS_IN_ENUM),
  (513, EnumValuesAssertion.IS_INVALID),
  (["value_1"], EnumValuesAssertion.IS_INVALID)
])
def enum_values_fixture(request):
  return request.param
# END enum_values_fixture


def test_enum_validate(enum_values_fixture):
  value, assertion_type = enum_values_fixture
  result = enum_validate(MyEnum, "my_enum", value)

  if assertion_type is EnumValuesAssertion.IS_INVALID or assertion_type is EnumValuesAssertion.IS_MISSING:
    assert result[0] == False
    assert isinstance(result[1], str)

    if assertion_type is EnumValuesAssertion.IS_INVALID:
      assert result[1] == "Field `my_enum` is invalid."

    elif assertion_type is EnumValuesAssertion.IS_MISSING:
      assert result[1] == "Field `my_enum` is required."
  
  elif assertion_type is EnumValuesAssertion.IS_IN_ENUM:
    assert result[0] == True
    assert result[1] is None
# END test_enum_validate