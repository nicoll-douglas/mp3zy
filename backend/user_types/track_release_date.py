from typing import Any, cast

class TrackReleaseDate:
  """A class that validates, contains, and works with track release date metadata associated with a track.

  Attributes:
    year (int): The year of the release date.
    month (int | None): The month of the release date.
    day (int | None): The day of the release date.
  """
  
  year: int
  month: int | None
  day: int | None


  def __init__(self, data: Any, field_name: str | None = None):
    """Initializes TrackReleaseDate, validating the data passed.

    Constructs the effective release date values (`year`, `month`, `day`) from the data.

    Args:
      data (Any): The data being passed to the class to validate and instantiate from.
      field_name (str | None): The name of a field associated with the incoming data.

    Raises:
      ValueError: If validation fails.
    """

    year, month, day = self._validate(data, field_name)

    self.year = year
    self.month = month
    self.day = day
  # END __init__


  def _build_field_name(self, root_field_name: str, property: str) -> str:
    """Build the full field name for a property with respect to an incoming field name.

    Args:
      root_field_name (str): The root field name (e.g `"release_date"`).
      property (str): The property name (e.g `"year"`).

    Returns:
      str: The full field name.
    """
    
    return f"{root_field_name}.{property}"
  # END _build_field_name


  def _validate(self, data: Any, field_name: str | None = None) -> tuple[int, None, None] | tuple[int, int, int | None]:
    """Validates the incoming data against constraints.

    Args:
      data (Any): The data being passed to the class to validate.
      field_name (str | None): The name of a field associated with the incoming data.

    Returns:
      tuple[int, None, None] | tuple[int, int, int | None]: A tuple containing the effective year, month, and date values of the release date.

    Raises:
      ValueError: If validation fails.
    """

    self._validate_object(data, field_name)

    validated_data = cast(dict, data)
    key = "year"
    year = validated_data.get(key)

    self._validate_year(year, self._build_field_name(field_name, key) if field_name else None)

    validated_year = cast(int, year)
    key = "month"
    month = validated_data.get(key)

    self._validate_month(month, self._build_field_name(field_name, key) if field_name else None)
          
    validated_month = cast(int | None, month)

    if validated_month is None:
      return validated_year, None, None

    key = "day"
    day = validated_data.get(key)

    self._validate_day(day, self._build_field_name(field_name, key) if field_name else None)

    validate_day = cast(int | None , day)

    return validated_year, validated_month, validate_day
  # END _validate


  def _validate_object(self, data: Any, field_name: str | None = None):
    """Validates that incoming data is a dictionary.

    Args:
      data (Any): The data to pass to the class to validate.
      field_name (str | None): The name of a field associated with the incoming data.

    Raises:
      ValueError: If validation fails.
    """
    
    args = []
    
    if data is None:
      if field_name:
        args.append(f"Field `{field_name}` is required.")
        args.append(field_name)
      else:
        args.append("Expected non-empty value, got None")

      raise ValueError(*args)

    if not isinstance(data, dict):
      if field_name:
        args.append(f"Field `{field_name}` must be an object.")
        args.append(field_name)
      else:
        args.append(f"Expected dict, got {data!r}")
      
      raise ValueError(*args)
  # END _validate_object


  def _validate_year(self, year: Any, field_name: str | None = None):
    """Validates the year against constraints.

    Args:
      year (Any): The year property extracted from the incoming data.
      field_name (str | None): The name of the year field associated with the incoming data.

    Raises:
      ValueError: If validation fails.
    """
    
    args = []
    
    if year is None:
      if field_name:
        args.append(f"Field `{field_name}` is required.")
        args.append(field_name)
      else:
        args.append(f"Expected non-empty property `year`, got {year!r}")

      raise ValueError(*args)
  
    if not isinstance(year, int):
      if field_name:
        args.append(f"Field `{field_name}` must be an integer.")
        args.append(field_name)
      else:
        args.append(f"Expected integer property `year`, got {year!r}")
      
      raise ValueError(*args)
    
    if year < 0:
      if field_name:
        args.append(f"Field `{field_name}` must be greater than or equal to 0.")
        args.append(field_name)
      else:
        args.append(f"Expected integer property `year` greater than or equal 0, got {year!r}")

      raise ValueError(*args)
    
    if year > 9999:
      if field_name:
        args.append(f"Field `{field_name}` must be no greater than 9999.")
        args.append(field_name)
      else:
        args.append(f"Expected integer property `year` no greater than 9999, got {year!r}")

      raise ValueError(*args)
  # END _validate_year


  def _validate_month(self, month: Any, field_name: str | None = None):
    """Validates the month against constraints.

    Args:
      month (Any): The month property extracted from the incoming data.
      field_name (str | None): The name of the month field associated with the incoming data.

    Raises:
      ValueError: If validation fails.
    """

    if month is None:
      return
    
    args = []
    
    if not isinstance(month, int):
      if field_name:
        args.append(f"Field `{field_name}` must be an integer or null.")
        args.append(field_name)
      else:
        args.append(f"Expected integer or empty property `month`, got {month!r}")

      raise ValueError(*args)
    
    if month < 1:
      if field_name:
        args.append(f"Field `{field_name}` must be greater than 0.")
        args.append(field_name)
      else:
        args.append(f"Expected integer greater than 0 or empty property `month`, got {month!r}")

      raise ValueError(*args)
    
    if month > 12:
      if field_name:
        args.append(f"Field `{field_name}` must be no greater than 12.")
        args.append(field_name)
      else:
        args.append(f"Expected integer no greater than 12 or empty property `month`, got {month!r}")

      raise ValueError(*args)
  # END _validate_month


  def _validate_day(self, day: Any, field_name: str | None = None):
    """Validates the day against constraints.

    Args:
      day (Any): The day property extracted from the incoming data.
      field_name (str | None): The name of the day field associated with the incoming data.

    Raises:
      ValueError: If validation fails.
    """

    if day is None:
      return

    args = []
    
    if not isinstance(day, int):
      if field_name:
        args.append(f"Field `{field_name}` must be an integer or null.")
        args.append(field_name)
      else:
        args.append(f"Expected integer or empty property `day`, got {day!r}")

      raise ValueError(*args)        

    if day < 1:
      if field_name:
        args.append(f"Field `{field_name}` must be greater than 0.")
        args.append(field_name)
      else:
        args.append(f"Expected integer greater than 0 or empty property `day`, got {day!r}")

      raise ValueError(*args)
    
    if day > 31:
      if field_name:
        args.append(f"Field `{field_name}` must be no greater than 31.")
        args.append(field_name)
      else:
        args.append(f"Expected integer no greater than 31 or empty property `day`, got {day!r}")

      raise ValueError(*args)
  # END _validate_day


  def __str__(self) -> str:
    """
    Returns:
      str: The string representation of the release date.
    """

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

    Raises:
      ValueError: If the year, month, or day in the release date string cannot be parsed as integers or if validation fails when instantiating the class.
    """

    segments = value.split("-")
    data = {}

    if len(segments) > 0:
      data["year"] = int(segments[0])

    if len(segments) > 1:
      data["month"] = int(segments[1])

    if len(segments) > 2:
      data["day"] = segments[2]

    return cls(data)
  # END from_string

# END class TrackReleaseDate