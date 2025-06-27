from mutagen.id3 import ID3, APIC, TIT2, TPE1, error
from mutagen.mp3 import MP3
import mimetypes
import logger

# adds the track title, artists and cover image to the mp3 file
def add_mp3_metadata(
  mp3_file_path: str, 
  track_name: str, 
  track_artists: list[str],
  cover_img_path: str
):
  logger.debug(f"Updating metadata for: {mp3_file_path}")

  audio = MP3(mp3_file_path, ID3=ID3)
  cover_img_mimetype, _ = mimetypes.guess_type(cover_img_path)
  cover_img_mimetype = cover_img_mimetype or "application/octet-stream"

  try:
    audio.delete()
  except error:
    pass

  audio.add_tags()
  audio.tags.add(TIT2(encoding=3, text=track_name))
  audio.tags.add(TPE1(encoding=3, text=track_artists))

  with open(cover_img_path, "rb") as img:
    audio.tags.add(
      APIC(
        encoding=3,
        mime=cover_img_mimetype,
        type=3,
        desc="Cover",
        data=img.read()
      )
    )
  
  audio.save()

  logger.success("Successfully update metadata.")