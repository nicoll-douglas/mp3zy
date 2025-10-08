import os, mimetypes
from pathvalidate import sanitize_filename
from .settings import Settings
from user_types.requests import PostDownloadsRequest

class Track:
  """A model class for interfacing with an audio/track file path on disk.

  Attributes:
    track_info (PostDownloadsRequest): Metadata about the track.
    save_dir (str): The preferred root directory under which the track file should be stored, defaults to the user's preference in the application settings file.
    track_id (str | None): A unique ID associated with the track that will go in the file name if not None.
    ext (str): The extension (including the ".") of the track file associated with the codec in the track info.
    mimetype (str): The mimetype of the track file.
    output_template (str): The output filepath template for `yt_dlp` to know where to download the track to.
  """

  track_info: PostDownloadsRequest
  save_dir: str
  track_id: str | None
  ext: str
  mimetype: str
  path: str
  output_template: str


  def __init__(self, track_info: PostDownloadsRequest, save_dir: str | None = None, track_id: str | None = None):
    """Initializes Track.

    Will assign the appropriate save directory to `save_dir` and create the track file path's directories if they don't exist.
    """
    
    self.track_info = track_info
    self.track_id = track_id
    self.ext = "." + self.track_info.codec.value
    self.mimetype = mimetypes.types_map[self.ext]
    self.path = self._build_path()
    self.output_template = self._build_output_template()

    if save_dir is None:
      settings = Settings()
      settings.load()
      self.save_dir = settings.download_dir
    else:
      self.save_dir = save_dir

    os.makedirs(self.path, exist_ok=True)
  # END __init__
  

  def _build_path(self) -> str:
    """Builds the full path of where the track should be stored.

    Returns:
      str: The file path.
    """

    return os.path.join(
      self.save_dir, 
      self._build_relative_dir(), 
      self._build_stem() + self.ext
    )
  # END _build_path
  

  def _build_output_template(self) -> str:
    """Builds the output filepath template for `yt_dlp` to know where to download the track to.

    Returns:
      str: The output filepath template.
    """

    return os.path.join(
      self.save_dir,
      self._build_relative_dir(),
      f"{self._build_stem()}.%(ext)s"
    )
  # END _build_output_template

  
  def _build_relative_dir(self) -> str:
    """Builds the path of the directory the track file should be stored in relative to `save_dir`.

    Returns:
      str: A relative path.
    """

    segments = []
    artist_folder = sanitize_filename(self.track_info.artist_names.get_main_artist())
    segments.append(artist_folder)

    if self.track_info.album_name:
      album_folder = sanitize_filename(self.track_info.album_name)
      segments.append(album_folder)

    return os.path.join(*segments)
  # END _build_relative_dir


  def _build_stem(self) -> str:
    """Builds the stem of the track filename and returns it sanitized.

    Returns:
      str: The stem.
    """
    
    stem = ""

    if self.track_info.album_name:
      if self.track_info.track_number is not None:
        stem += str(self.track_info.track_number).zfill(2) + " - "

        if self.track_info.disc_number is not None:
          stem = str(self.track_info.disc_number).zfill(2) + "-" + stem

    stem += self.track_info.track_name
    other_artists = self.track_info.artist_names.get_other_artists()

    if len(other_artists) > 0:
      stem += " - " + ", ".join(other_artists)

    if self.track_id:
      stem += " - " + self.track_id

    return sanitize_filename(stem)
  # END _build_stem
  

  def exists(self) -> bool:
    """Checks whether the track file exists.

    Returns:
      bool: True if it exists, false otherwise.
    """

    return os.path.exists(self.path)
  # END exists

# END class Track