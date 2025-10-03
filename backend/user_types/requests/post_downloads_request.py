from ..track_artist_names import TrackArtistNames
from ..track_codec import TrackCodec
from ..track_bitrate import TrackBitrate
from ..track_release_date import TrackReleaseDate

class PostDownloadsRequest:
  """Type that represents a validated request body to endpoint POST /downloads.

  Attributes:
    artist_names (TrackArtistNames): Track artist metadata.
    track_name (str): The name of the track.
    album_name (str): Album name metadata.
    codec (TrackCodec): The audio codec to use when saving the track file to disk.
    bitrate (TrackBitrate): The bitrate to use when saving an associated audio file to disk.
    track_number (int | None): Track number metadata.
    disc_number (int | None): Disc number metadata.
    release_date (TrackReleaseDate | None): Track release date metadata.
    url (str): The URL to use as the audio source for the track download.
  """
  
  artist_names: TrackArtistNames
  track_name: str
  album_name: str | None
  codec: TrackCodec
  bitrate: TrackBitrate
  track_number: int | None
  disc_number: int | None
  release_date: TrackReleaseDate | None
  url: str
# END class PostDownloadsRequest