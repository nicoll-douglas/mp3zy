from ..track_artist_names import TrackArtistNames
from ..track_codec import TrackCodec
from ..track_bitrate import TrackBitrate
from ..track_release_date import TrackReleaseDate

class PostDownloadsRequest:
  artist_names: TrackArtistNames
  track_name: str
  album_name: str | None
  codec: TrackCodec
  bitrate: TrackBitrate
  track_number: int | None
  disc_number: int | None
  release_date: TrackReleaseDate | None
  url: str
# END post_downloads_request