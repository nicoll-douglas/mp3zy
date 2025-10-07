from user_types import enum_validate
from enum import Enum
import pytest
from typing import Any

class EnumValueAssertion(Enum):
  """Represents test case assertions for validating whether a value exists in an enum.

  Attributes:
    IS_MISSING: Represents the case where an empty value was provided for validation.
    IS_IN_ENUM: Represents the case where the value is in the enum.
    IS_INVALID: Represents the case where the value is not in the enum (is an invalid enum value).
  """
  
  IS_MISSING = 1
  IS_IN_ENUM = 2
  IS_INVALID = 3
# END class EnumValueAssertion


@pytest.fixture
def sample_enum() -> Enum:
  """Fixture providing a mock enum with data for testing.

  Returns:
    Enum: The enum.
  """
  
  class MyEnum(Enum):
    VALUE_1 = "value_1"
    VALUE_2 = "value_2"
    VALUE_3 = "value_3"
  # END class MyEnum

  return MyEnum
# END sample_enum


@pytest.fixture(params=[
  # (test value, assertion type)
  ("", EnumValueAssertion.IS_MISSING),
  (None, EnumValueAssertion.IS_MISSING),
  ("value_1", EnumValueAssertion.IS_IN_ENUM),
  ("value_3", EnumValueAssertion.IS_IN_ENUM),
  (513, EnumValueAssertion.IS_INVALID),
  (["value_1"], EnumValueAssertion.IS_INVALID)
])
def enum_values_fixture(request) -> tuple[Any, EnumValueAssertion]:
  """Parametrized fixture providing test cases for the test_enum_validate function.

  Args:
    request (pytest.FixtureRequest): Provides the current parameter.
  
  Returns:
    tuple[Any, EnumValueAssertion]: A tuple containing the test case value and the assertion type.
  """
  
  return request.param
# END enum_values_fixture


def test_enum_validate(enum_values_fixture: tuple[Any, EnumValueAssertion], sample_enum: Enum):
  """Tests that the enum_validate function correctly validates a value against the given enum.

  Args:
    enum_values_fixture (tuple[Any, EnumValueAssertion]): The parametrized fixture value from enum_values_fixture containing the test case data.
    sample_enum (Enum): The test enum provided by the sample_enum fixture.
  """
  
  test_value, assertion = enum_values_fixture
  has_value, message = enum_validate(sample_enum, "my_enum", test_value)

  if assertion is EnumValueAssertion.IS_INVALID or assertion is EnumValueAssertion.IS_MISSING:
    assert has_value is False
    assert isinstance(message, str)
  
  elif assertion is EnumValueAssertion.IS_IN_ENUM:
    assert has_value is True
    assert message is None

  else:
    raise ValueError("Unknown assertion type")
# END test_enum_validate