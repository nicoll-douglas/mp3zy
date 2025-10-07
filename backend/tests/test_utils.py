from enum import Enum

class ValidationCase(Enum):
  """Represents test case assertions for validator function results.

  Attributes:
    VALID: Represents the case where validation passes for a validator.
    INVALID: Represents the case where valdation does not pass for a validator.
  """
  
  VALID = 1
  INVALID = 2
# END class ValidationCase