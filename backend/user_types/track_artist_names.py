from collections import UserList
from typing import Any

class TrackArtistNames(UserList):
  """A that class validates, contains, and works with track artist name metadata associated with a track.
  """

  def __init__(self, data: Any, field_name: str | None = None):
    """Initializes TrackArtistNames, validating the data passed.

    Args:
      field_name (str | None): The name of a field associated with the incoming data.
      data (Any): The data to instantiate from.

    Raises:
      ValueError: If validation fails.
    """
    
    self._validate(data, field_name)
    super().__init__(data)
  # END __init__


  def _validate(self, data: Any, field_name: str | None = None):
    """Validates the incoming data against constraints.

    Args:
      data (Any): The data being passed to the class to validate.
      field_name (str | None): The name of a field associated with the incoming data.

    Raises:
      ValueError: If validation fails.
    """
    
    if data is None:
      raise ValueError(
        f"Field `{field_name}` is required." if field_name else "Expected non-empty value, got None"
      )

    if not isinstance(data, list):
      raise ValueError(
        f"Field `{field_name}` must be an array." if field_name else f"Expected list, got {data!r}"
      )
    
    if len(data) == 0:
      raise ValueError(
        f"Field `{field_name}` must be of at least length 1." if field_name else f"Expected list of at least 1, got list of length 0"
      )
    
    if not all(isinstance(item, str) for item in data):
      raise ValueError(
        f"Field `{field_name}` must be a string array." if field_name else f"Expected list of strings, got {data!r}"
      )
    
    if not all(len(item) > 0 for item in data):
      raise ValueError(
        f"Field `{field_name}` must be a string array of non-empty strings." if field_name else f"Expected list of non-empty strings, got {data!r}"
      )
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
    
    return list(self)[1:]
  # END get_other_artists

# END class TrackArtistNames