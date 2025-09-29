from collections import UserDict
from typing import Any, cast

class TrackReleaseDate(UserDict):
  field_name: str
  raw_data: Any
  failed_field: str | None
  validation_passed: bool
  validation_message: str | None


  def __init__(self, field_name, data):
    super.__init__()
    self.field_name = field_name
    self.raw_data = data

    if not self._validate_object():
      return
    
    raw_data = cast(dict, self.raw_data)
    year = raw_data.get("year")

    if not self._validate_year(year):
      return
      
    month = raw_data.get("month")

    if month is None:
      self["year"] = year
      self["month"] = None
      self["day"] = None
      self.failed_field = None
      self.validation_message = None
      self.validation_passed = True
      return
    
    if not self._validate_month(month):
      return
  
    day = raw_data.get("day")

    if day is None:
      self["year"] = year
      self["month"] = month
      self["day"] = None
      self.failed_field = None
      self.validation_message = None
      self.validation_passed = True
      return
    
    if not self._validate_day(day):
      return
    
    self["year"] = year
    self["month"] = month
    self["day"] = day
    self.failed_field = None
    self.validation_message = None
    self.validation_passed = True
  # END __init__

  def _validate_object(self) -> bool:
    if self.raw_data is None:
      self.failed_field = self.field_name
      self.validation_message = f"`{self.failed_field}` is required."
      self.validation_passed = False
      return False

    if not isinstance(self.raw_data, dict):
      self.failed_field = self.field_name
      self.validation_message = f"`{self.failed_field}` must be an object."
      self.validation_passed = False
      return False
        
    return True
  # END _validate_is_object


  def _validate_year(self, year) -> bool:
    field = f"{self.field_name}.year"
    
    if year is None:
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` is required."
      self.validation_passed = False
      return False
  
    if not isinstance(year, int):
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be an integer."
      self.validation_passed = False
      return False
    
    if year < 0:
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be greater than 0."
      self.validation_passed = False
      return False
    
    if year > 9999:
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be no greater than 9999."
      self.validation_passed = False
      return False
    
    return True
  # END _validate_year


  def _validate_month(self, month) -> bool:
    field = f"{self.field_name}.month"
    
    if not isinstance(month, int):
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be an integer or null."
      self.validation_passed = False
      return False
    
    if month < 1:
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be greater than 0."
      self.validation_passed = False
      return False
    
    if month > 12:
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be no greater than 12."
      self.validation_passed = False
      return False
    
    return True
  # END _validate_month


  def _validate_day(self, day) -> bool:
    field = f"{self.field_name}.day"
    
    if not isinstance(day, int):
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be an integer or null."
      self.validation_passed = False
      return False
    
    if day < 1:
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be greater than 0."
      self.validation_passed = False
      return False
    
    if (day > 31):
      self.failed_field = field
      self.validation_message = f"`{self.failed_field}` must be no greater than 31."
      self.validation_passed = False
      return False
    
    return True
  # END _validate_day


  def __str__(self) -> str:
    if not self.validation_passed:
      return self.validation_message

    value = ""
    value += str(self["year"]).zfill(4)

    if self["month"] is not None:
      value += f"-{str(self["month"]).zfill(2)}"

      if self.day is not None:
        value += f"-{str(self["day"]).zfill(2)}"

    return value
  # END __str__

# END class TrackReleaseDate