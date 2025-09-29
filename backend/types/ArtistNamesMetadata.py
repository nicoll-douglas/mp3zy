from collections import UserList
from typing import Any

class ArtistNamesMetadata(UserList):
  field_name: str
  raw_data: Any
  validation_passed: bool
  validation_message: str | None


  def __init__(self, field_name, data):
    super.__init__()
    self.field_name = field_name
    self.raw_data = data

    if not self._validate():
      return
    
    self.data = list(self.raw_data)
    self.validation_message = None
    self.validation_passed = True
  # END __init__


  def _validate(self):
    if self.raw_data is None:
      self.validation_message = f"`{self.field_name}` is required."
      self.validation_passed = False
      return False

    if not isinstance(self.raw_data, list):
      self.validation_message = f"`{self.field_name}` must be an array."
      self.validation_passed = False
      return False
    
    if len(self.raw_data) == 0:
      self.validation_message = f"`{self.field_name}` must be of at least length 1."
      self.validation_passed = False
      return False
    
    if not all(isinstance(item, str) for item in self.raw_data):
      self.validation_message = f"`{self.field_name}` must be a string array."
      self.validation_passed = False
      return False
        
    return True
  # END _validate

# END class ArtistNamesMetadata