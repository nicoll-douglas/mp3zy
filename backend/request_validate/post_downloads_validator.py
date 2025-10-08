from user_types import TrackArtistNames, TrackCodec, TrackBitrate, TrackReleaseDate, enum_validate
from typing import Any, Literal, Callable
from user_types.requests import PostDownloadsRequest
from user_types.reponses import PostDownloadsResponse
import copy

class PostDownloadsValidator:
  """Validator class that validates request bodies to the POST /downloads endpoint.

  Attributes:
    _response (PostDownloadsResponse.BadRequest): A response body model instance associated with the endpoint.
    _request (PostDownloadsRequest): A request body model instance associated with the endpoint.
  """
  
  _response: PostDownloadsResponse.BadRequest
  _request: PostDownloadsRequest


  def __init__(self):
    self._response = PostDownloadsResponse.BadRequest()
    self._request = PostDownloadsRequest()
  # END __init__
  

  def _validate_body(self, body: Any)-> Literal[False] | dict:
    """Helper that validates a raw request body.

    Args:
      body (Any): A request body to validate.

    Returns:
      bool: False is the body is invalid, a copy of the raw body otherwise.
    """
    
    if body is None or not isinstance(body, dict):
      self._response.field = ""
      self._response.message = "Body must be an object."
      return False
    
    return copy.deepcopy(body)
  # END _validate_body


  def _validate_artist_names(self, body: dict) -> Literal[False] | TrackArtistNames:
    """Helper that validates the `artist_names` field of the request body.

    Args:
      body (dict): The request body.

    Returns:
      Literal[False] | TrackArtistNames: False if the field is invalid, a TrackArtistNames instance otherwise.
    """
    
    self._response.field = "artist_names"
    
    try:
      artist_names = TrackArtistNames(body.get(self._response.field), self._response.field)
    except ValueError as e:
      self._response.message = str(e)
      return False
    
    return artist_names
  # END _validate_artist_names


  def _validate_track_name(self, body: dict) -> Literal[False] | str:
    """Helper that validates the `track_name` field of the request body.

    Args:
      body (dict): The request body.

    Returns:
      Literal[False] | str: False if the field is invalid, the validated field value otherwise.
    """

    self._response.field = "track_name"
    track_name = body.get(self._response.field)

    if not track_name:
      self._response.message = f"Field `{self._response.field}` is required."
      return False
    
    if not isinstance(track_name, str):
      self._response.message = f"Field `{self._response.field}` must be a string."
      return False
    
    return track_name
  # END _validate_track_name


  def _validate_url(self, body: dict) -> Literal[False] | str:
    """Helper that validates the `url` field of the request body.

    Args:
      body (dict): The request body.

    Returns:
      Literal[False] | str: False is the field is invalid, the validated field value otherwise.
    """

    self._response.field = "url"
    url = body.get(self._response.field)

    if not url:
      self._response.message = f"Field `{self._response.field}` is required."
      return False
    
    if not isinstance(url, str):
      self._response.message = f"Field `{self._response.field}` must be a string."
      return False
    
    return url
  # END _validate_url


  def _validate_codec(self, body: dict) -> Literal[False] | TrackCodec:
    """Helper that validates the `codec` field of the request body.

    Args:
      body (dict): The request body.

    Returns:
      Literal[False] | TrackCodec: False is the field is invalid, a TrackCodec instance otherwise.
    """
    
    self._response.field = "codec"
    codec = body.get(self._response.field)
    codec_valid, codec_validation_message = enum_validate(TrackCodec, self._response.field, codec)

    if not codec_valid:
      self._response.message = codec_validation_message
      return False
    
    return TrackCodec(codec)
  # END _validate_codec


  def _validate_bitrate(self, body: dict) -> Literal[False] | TrackBitrate:
    """Helper that validates the `bitrate` field of the request body.

    Args:
      body (dict): The request body.

    Returns:
      Literal[False] | TrackBitrate: False is the field is invalid, a TrackBitrate instance otherwise.
    """
    
    self._response.field = "bitrate"
    bitrate = body.get(self._response.field)
    bitrate_valid, bitrate_validation_message = enum_validate(TrackBitrate, self._response.field, bitrate)

    if not bitrate_valid:
      self._response.message = bitrate_validation_message
      return False

    return TrackBitrate(bitrate)
  # END _validate_bitrate
  

  def _validate_album_name(self, body: dict) -> Literal[False] | str | None:
    """Helper that validates the `album_name` field of the request body.

    Args:
      body (dict): The request body.

    Returns:
      Literal[False] | str | None: False is the field is invalid, the validated field's value otherwise.
    """
    
    self._response.field = "album_name"
    album_name = body.get(self._response.field)

    if album_name is not None and not isinstance(album_name, str):
      self._response.message = f"Field `{self._response.field}` must be a string or null."
      return False
    
    return album_name
  # END _validate_album_name


  def _validate_track_or_disc_number(self, body: dict, field_name: str) -> Literal[False] | int | None:
    """Helper that validates the `track_number` or `disc_number` field of the request body.

    Args:
      body (dict): The request body.
      field_name (str): The name of the field.

    Returns:
      Literal[False] | int | None: False is the field is invalid, the validated field's value otherwise.
    """
    
    self._response.field = field_name
    value = body.get(self._response.field)

    if value is not None:
      if not isinstance(value, int):
        self._response.message = f"Field `{self._response.field}` must be an integer or null."
        return False
      
      if value < 1:
        self._response.message = f"Field `{self._response.field}` must be greater than 0."
        return False
      
      if value > 99:
        self._response.message = f"Field `{self._response.field} must not be greater than 99."
        return False
      
    return value
  # END _validate_track_or_disc_number


  def _validate_release_date(self, body: dict) -> Literal[False] | TrackReleaseDate:
    """Helper that validates the `release_date` field of the request body.

    Args:
      body (dict): The request body.

    Returns:
      Literal[False] | TrackReleaseDate: False is the field is invalid, a TrackReleaseDate instance otherwise.
    """
    
    self._response.field = "release_date"
    release_date = body.get(self._response.field)

    if release_date is not None:
      try:
        release_date = TrackReleaseDate(release_date, self._response.field)
      except ValueError as e:
        message, field_name = e.args
        self._response.field = field_name
        self._response.message = message
        return False
      
    return release_date
  # END _validate_release_date


  def validate(self, body: Any) -> tuple[Literal[False], PostDownloadsResponse.BadRequest] | tuple[Literal[True], PostDownloadsRequest]:
    """Performs full validation on the request body.

    Args:
      body (Any): The request body.

    Returns:
      tuple[Literal[False], PostDownloadsResponse.BadRequest] | tuple[Literal[True], PostDownloadsRequest]: A tuple where on successful validation the first element is True and the second is the sanitized request body, or on failure the first element is False and the second is the response body to send.
    """

    bad_request = (False, self._response)
    validated_body = self._validate_body(body)

    if validated_body is False:
      return bad_request
    
    validators: list[tuple[Callable[[dict], Literal[False] | Any], str]] = [
      # (validator function, attribute name on self._request)
      (self._validate_artist_names, "artist_names"),
      (self._validate_track_name, "track_name"),
      (self._validate_url, "url"),
      (self._validate_codec, "codec"),
      (self._validate_bitrate, "bitrate"),
      (self._validate_album_name, "album_name"),
      (lambda: validated_body, self._validate_track_or_disc_number(validated_body, "track_number"), "track_number"),
      (lambda: validated_body, self._validate_track_or_disc_number(validated_body, "disc_number"), "disc_number"),
      (self._validate_release_date, "release_date")
    ]

    for validator_func, request_attr_name in validators:
      result = validator_func(validated_body)

      if result is False:
        return bad_request
      
      setattr(self._request, request_attr_name, result)
    
    return True, self._request
  # END validate

# END class PostDownloadsValidator