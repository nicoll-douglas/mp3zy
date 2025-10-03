from typing import Literal, Any
from enum import Enum

def enum_validate(enum: Enum, field_name: str, data: Any) -> tuple[Literal[False], str] | tuple[Literal[True], None]:
  """Validates that an enum contains a certain value.

  Args:
    enum (Enum): The enum to to check against.
    field_name (str): The name of an associated form field to the tested value.
    data (Any): The value to check for in the enum.

  Returns:
    tuple[Literal[False], str] | tuple[Literal[True], None]: Returns a tuple with the first element being False if the value is not in the enum and the second being a string validation message, or True and None otherwise.
  """
  
  if data is None:
    return False, f"`{field_name}` is required."
  
  has_value = any(data == member.value for member in enum)
  message = None if has_value else f"`{field_name}` is invalid."

  return has_value, message
# END enum_validate