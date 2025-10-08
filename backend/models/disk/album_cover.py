import os, mimetypes
from .cache import Cache
from typing import Any

class AlbumCover:
  """A model class for interfacing with album cover files on disk

  Attributes:
    DIR (str): The path of the directory where album covers ares saved.
    path (str): The path to an album cover file.
  """
  
  DIR = os.path.join(Cache.DIR, "covers")

  path: str


  def __init__(self, path = None):
    self.path = path

    self._safe_create_dir()
  # END __init__


  @classmethod
  def _safe_create_dir(cls):
    """Safely creates the directory where album covers are saved if it doesn't exist yet.
    """

    os.makedirs(cls.DIR, exist_ok=True)
  # END _safe_create_dir


  def read(self) -> bytes:
    """Reads the contents of the album cover file into bytes.

    Returns:
      bytes: The contents of the album cover file.
    """

    with open(self.path, "rb") as img:
      return img.read()
  # END read
  

  def write(self, buffer: Any):    
    """Writes a readable buffer to the album cover file.

    Args:
      buffer (Any): A readable buffer.
    """
    
    with open(self.path, "wb") as file:
      file.write(buffer)
  # END write


  def exists(self) -> bool:
    """Checks whether the album cover file exists.

    Returns:
      bool: True if it exists, false otherwise.
    """
    
    return os.path.exists(self.path)
  # END exists
  

  def get_mimetype(self) -> str | None:
    """Guesses the mimetype of the album cover file.

    Returns:
      str | None: The mimetype if it could be guessed, None otherwise.
    """
    
    file_mimetype, _ = mimetypes.guess_type(self.path)

    return file_mimetype
  # END get_mimetype

# END class AlbumCover
