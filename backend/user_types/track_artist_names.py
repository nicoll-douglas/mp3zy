from collections import UserList
from typing import Any

class TrackArtistNames(UserList):
  """A class validates, contains, and works with track artist name metadata associated with a track.

  Attributes:
    _field_name (str): The name of an associated form field to raw data being validated.
    _raw_data (Any): The raw artist name data to be validated.
    validation_passed (bool): True if the raw data passed validation, False otherwise.
    validation_message (str | None): Contains a validation message if validation failed, None otherwise.
  """
  
  _raw_data: Any
  field_name: str
  validation_passed: bool
  validation_message: str | None


  def __init__(self, field_name: str, data: Any):
    """Initializes TrackArtistNames, validating the data passed.

    Copies over the raw data into the `data` attribute on successful validation or assigns validation attributes otherwise (`validation_passed`, `validation_message`).

    Args:
      field_name (str): Assigned to `_field_name`.
      data (Any): Assigned to `_raw_data`
    """
    
    super.__init__()
    self.field_name = field_name
    self._raw_data = data

    if not self._validate():
      return
    
    self.data = list(self.raw_data)
    self.validation_message = None
    self.validation_passed = True
  # END __init__


  def _validate(self):
    """Validates the raw data against constraints.

    Assigns validation class attributes on failure.

    Returns:
      bool: False if validation fails, True otherwise.
    """
    
    if self._raw_data is None:
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


  def get_main_artist(self) -> str:
    """Gets the name of the main artist from the metadata.

    Returns:
      str: The name of the main artist.
    """
    
    return self[0]
  # END get_main_artist
  

  def get_other_artists(self) -> list[str]:
    """Gets the name of the other artists (artists that aren't the main artist) from the metadata.

    Returns:
      list[str]: A list of the artist names.
    """
    
    return list(self[1:])
  # END get_other_artists

# END class TrackArtistNames