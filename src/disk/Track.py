import os, logging
from .File import File
from mutagen.id3 import ID3, APIC, TIT2, TPE1, error
from mutagen.mp3 import MP3

class Track(File):
  DIR: str = os.path.join(os.getenv("STORAGE_DIR"), "tracks")
  
  def __init__(
    _id: str | None = None,
    path: str | None = None
  ):
    super().__init__(
      _id=_id,
      ext=".mp3",
      path=path
    )
    
  def ytdtl_download_path(self) -> str:
    if not self._id:
      logging.warning(f"You may be attempting to download a track without knowing it's target filename.")
      return ""
      
    filename_template = f"{self._id}.%(ext)s"
    return os.path.join(self.DIR, filename_template),

  def set_metadata(self, metadata: dict[str]):
    logging.debug(f"Updating metadata for: {self._path}")

    audio = MP3(self._path)
    cover_img_mimetype = metadata["cover"].mimetype() or "application/octet-stream"

    try:
      audio.delete()
    except error:
      pass

    audio.tags = ID3()
    audio.tags.add(TIT2(encoding=3, text=metadata["name"]))
    audio.tags.add(TPE1(encoding=3, text=metadata["artists"]))

    with open(metadata["cover"].get_path(), "rb") as img:
      audio.tags.add(
        APIC(
          encoding=3,
          mime=cover_img_mimetype,
          type=3,
          desc="",
          data=img.read()
        )
      )
    
    audio.save(v2_version=3)

    logging.debug("Successfully updated metadata.")