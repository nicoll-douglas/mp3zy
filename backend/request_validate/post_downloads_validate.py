from user_types import TrackArtistNames, TrackCodec, TrackBitrate, TrackReleaseDate, enum_validate
from typing import Any, Literal
from user_types.requests import PostDownloadsRequest
from user_types.reponses import PostDownloadsResponse

def post_downloads_validate(body: Any) -> tuple[Literal[False], PostDownloadsResponse.BadRequest] | tuple[Literal[True], PostDownloadsRequest]:
  """Validates the body of a request made to the POST /downloads endpoint.

  Args:
    body (Any): The body of the request.

  Returns:
    tuple[Literal[False], PostDownloadsResponse.BadRequest] | tuple[Literal[True], PostDownloadsRequest]: A tuple where on successful validation the first element is True and the second is the sanitized request body, or on failure the first element is False and the second is the response body.
  """

  res = PostDownloadsResponse.BadRequest()
  
  if body is None or not isinstance(body, dict):
    res.field = ""
    res.message = "Body must be an object."
    return False, res
  
  res.field = "artist_names"
  artist_names = TrackArtistNames(res.field, body.get(res.field))
  
  if not artist_names.validation_passed:
    res.message = artist_names.validation_message
    return False, res
  
  res.field = "track_name"
  track_name = body.get(res.field)

  if track_name is None:
    res.message = f"Field `{res.field}` is required."
    return False, res
  
  if not isinstance(track_name, str):
    res.message = f"Field `{res.field}` must be a string."
    return False, res
  
  res.field = "album_name"
  album_name = body.get(res.field)

  if album_name is not None and not isinstance(album_name, str):
    res.message = f"Field `{res.field}` must be a string or null."
    return False, res
  
  res.field = "codec"
  codec = body.get(res.field)
  codec_valid, codec_validation_message = enum_validate(TrackCodec, res.field, codec)

  if not codec_valid:
    res.message = codec_validation_message
    return False, res
  
  codec = TrackCodec(codec)
  res.field = "bitrate"
  bitrate = body.get(res.field)
  bitrate_valid, bitrate_validation_message = enum_validate(TrackBitrate, res.field, bitrate)

  if not bitrate_valid:
    res.message = bitrate_validation_message
    return False, res

  bitrate = TrackBitrate(bitrate)
  res.field = "track_number"
  track_number = body.get(res.field)

  if track_number is not None:
    if not isinstance(track_number, int):
      res.message = f"Field `{res.field}` must be an integer."
      return False, res

    if track_number < 1:
      res.message = f"Field `{res.field}` must be greater than 0."
      return False, res
  
  res.field = "disc_number"
  disc_number = body.get(res.field)

  if disc_number is not None:
    if not isinstance(disc_number, int):
      res.message = f"Field `{res.field}` must be an integer."
      return False, res
    
    if disc_number < 1:
      res.message = f"Field `{res.field}` must be greater than 0."
      return False, res

  res.field = "release_date"
  release_date = body.get(res.field)

  if release_date is not None:
    release_date = TrackReleaseDate(res.field, release_date)

    if not release_date.validation_passed:
      res.message = release_date.validation_message
      return False, res
    
  res.field = "url"
  url = body.get(res.field)

  if url is None:
    res.message = f"Field `{res.field}` is required."
    return False, res
  
  if not isinstance(url, str):
    res.message = f"Field `{res.field}` must be a string."
    return False, res
  
  req = PostDownloadsRequest()
  req.artist_names = artist_names
  req.track_name = track_name
  req.album_name = album_name
  req.codec = codec
  req.bitrate = bitrate
  req.track_number = track_number
  req.disc_number = disc_number
  req.release_date = release_date
  req.url = url
  
  return True, req
# END post_downloads_validate