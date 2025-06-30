import os, logging
from .File import File
from mutagen.id3 import ID3, APIC, TIT2, TPE1, error
from mutagen.mp3 import MP3
from .TrackCover import TrackCover
from pathlib import Path

class Track(File):  
  DIR: str = os.path.join(os.getenv("STORAGE_DIR"), "tracks")
  EXT: str = ".mp3"
  
  def __init__(
    self,
    _id: str | None = None,
    path: str | None = None
  ):
    super().__init__(
      _id=_id,
      ext=self.EXT,
      path=path
    )
    
  def get_outtmpl(self) -> str:
    if not self._id:
      logging.warning(f"You may be attempting to download a track without knowing it's target filename.")
      return ""
      
    filename_template = f"{self._id}.%(ext)s"
    return os.path.join(self.DIR, filename_template)

  def set_metadata(self, metadata: dict[str], track_id: str):
    logging.debug(f"Updating metadata for: {self._path}")
    audio = MP3(self._path)

    try:
      audio.delete()
    except error:
      pass

    audio.tags = ID3()
    audio.tags.add(TIT2(encoding=3, text=metadata["name"]))
    audio.tags.add(TPE1(encoding=3, text=metadata["artists"]))

    if metadata["cover"]:
      t_cov = TrackCover(path=metadata["cover"])
      cover_img_mimetype = t_cov.get_mimetype() or "application/octet-stream"

      with open(metadata["cover"], "rb") as img:
        audio.tags.add(
          APIC(
            encoding=3,
            mime=cover_img_mimetype,
            type=3,
            desc="",
            data=img.read()
          )
        )
    else:
      logging.warning(f"Track {track_id} doesn't have its cover set in its metadata.")
    
    audio.save(v2_version=3)

    logging.debug("Successfully updated metadata.")

  @classmethod
  def get_all(cls):
    p = Path(cls.DIR)
    return [cls(path=path.resolve()) for path in p.iterdir()]