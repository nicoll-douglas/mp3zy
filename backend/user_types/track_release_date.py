from typing import Any, cast

class TrackReleaseDate:
  """A class validates, contains, and works with track release date metadata associated with a track.

  Attributes:
    _field_name (str): The name of an associated form field to raw data being validated.
    _raw_data (Any): The raw release date data to be validated.
    validation_passed (bool): True if the raw data passed validation, False otherwise.
    validation_message (str | None): Contains a validation message if validation failed, None otherwise.
    year (int): The effective `year` field in the raw data if successfully validated.
    month (int | None): The effective `month` field in the raw data if successfully validated.
    day (int | None): The effective `day` field in the raw data if successfully validated. 
  """
  
  _field_name: str
  _raw_data: Any
  failed_field: str | None
  validation_passed: bool
  validation_message: str | None
  year: int
  month: int | None
  day: int | None


  def __init__(self, field_name: str, data: Any):
    """Initializes TrackReleaseDate, validating the data passed.

    Constructs the effective values (`year`, `month`, `day`) of the data's fields on successful validation or validation attributes otherwise (`validation_passed`, `validation_message`).

    Args:
      field_name (str): Assigned to `_field_name`.
      data (Any): Assigned to `_raw_data`
    """
    
    self._field_name = field_name
    self._raw_data = data

    if not self._validate_object():
      return
    
    raw_data = cast(dict, self._raw_data)
    year = raw_data.get("year")

    if not self._validate_year(year):
      return
      
    year = cast(int, year)
    month = raw_data.get("month")

    if month is None:
      self.year = year
      self.month = None
      self.day = None
      self.failed_field = None
      self.validation_message = None
      self.validation_passed = True
      return
    
    if not self._validate_month(month):
      return

    month = cast(int, month)
    day = raw_data.get("day")

    if day is None:
      self.year = year
      self.month = month
      self.day = None
      self.failed_field = None
      self.validation_message = None
      self.validation_passed = True
      return
    
    if not self._validate_day(day):
      return
    
    day = cast(int, day)
    
    self.year = year
    self.month = month
    self.day = day
    self.failed_field = None
    self.validation_message = None
    self.validation_passed = True
  # END __init__


  def _validate_object(self) -> bool:
    """Validates that the raw data is a dictionary.

    Assigns validation class attributes on failure.

    Returns:
      bool: False if validation fails, True otherwise.
    """
    
    if self._raw_data is None:
      self.failed_field = self._field_name
      self.validation_message = f"Field `{self.failed_field}` is required."
      self.validation_passed = False
      return False

    if not isinstance(self._raw_data, dict):
      self.failed_field = self._field_name
      self.validation_message = f"Field `{self.failed_field}` must be an object."
      self.validation_passed = False
      return False
        
    return True
  # END _validate_object


  def _validate_year(self, year) -> bool:
    """Validates the `year` field in the raw data against constraints.

    Assigns validation class attributes on failure.

    Returns:
      bool: False if validation fails, True otherwise.
    """
    
    field = f"{self._field_name}.year"
    
    if year is None:
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` is required."
      self.validation_passed = False
      return False
  
    if not isinstance(year, int):
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be an integer."
      self.validation_passed = False
      return False
    
    if year < 0:
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be greater than 0."
      self.validation_passed = False
      return False
    
    if year > 9999:
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be no greater than 9999."
      self.validation_passed = False
      return False
        
    return True
  # END _validate_year


  def _validate_month(self, month) -> bool:
    """Validates the `month` field in the raw data against constraints.

    Assigns validation class attributes on failure.

    Returns:
      bool: False if validation fails, True otherwise.
    """
    
    field = f"{self._field_name}.month"
    
    if not isinstance(month, int):
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be an integer or null."
      self.validation_passed = False
      return False
    
    if month < 1:
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be greater than 0."
      self.validation_passed = False
      return False
    
    if month > 12:
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be no greater than 12."
      self.validation_passed = False
      return False
    
    return True
  # END _validate_month


  def _validate_day(self, day) -> bool:
    """Validates the `day` field in the raw data against constraints.

    Assigns validation class attributes on failure.

    Returns:
      bool: False if validation fails, True otherwise.
    """
    
    field = f"{self._field_name}.day"
    
    if not isinstance(day, int):
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be an integer or null."
      self.validation_passed = False
      return False
    
    if day < 1:
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be greater than 0."
      self.validation_passed = False
      return False
    
    if (day > 31):
      self.failed_field = field
      self.validation_message = f"Field `{self.failed_field}` must be no greater than 31."
      self.validation_passed = False
      return False
    
    return True
  # END _validate_day


  def __str__(self) -> str:
    """
    Returns:
      str: The validation message if validation failed, the string representation of the release date otherwise.
    """

    if not self.validation_passed:
      return self.validation_message

    value = ""
    value += str(self.year).zfill(4)

    if self.month is not None:
      value += f"-{str(self.month).zfill(2)}"

      if self.day is not None:
        value += f"-{str(self.day).zfill(2)}"

    return value
  # END __str__


  @classmethod
  def from_string(cls, value: str):
    """Returns an instance of the class constructed from a stringified release date value.

    Args:
      value (str): The stringified value.

    Returns:
      TrackReleaseDate: The instance constructed.
    """

    segments = value.split("-")
    data = {
      "year": segments[0]
    }

    if len(segments) > 1:
      data["month"] = segments[0]

    if len(segments) > 2:
      data["day"] = segments[1]

    return cls("", data)
  # END from_string

# END class TrackReleaseDate