from mutagen.id3 import ID3, APIC, TIT2, TPE1, error
from mutagen.mp3 import MP3
import mimetypes, logging

# adds the track title, artists and cover image to the mp3 file
def set_mp3(mp3_file_path: str, track_data: dict):
  logging.debug(f"Updating metadata for: {mp3_file_path}")

  audio = MP3(mp3_file_path)
  cover_img_mimetype, _ = mimetypes.guess_type(track_data["cover_path"])
  cover_img_mimetype = cover_img_mimetype or "application/octet-stream"

  try:
    audio.delete()
  except error:
    pass

  audio.tags = ID3()
  audio.tags.add(TIT2(encoding=3, text=track_data["name"]))
  audio.tags.add(TPE1(encoding=3, text=track_data["artists"]))

  with open(track_data["cover_path"], "rb") as img:
    audio.tags.add(
      APIC(
        encoding=3,
        mime=cover_img_mimetype,
        type=3,
        desc="Cover",
        data=img.read()
      )
    )
  
  audio.save(v2_version=3)

  logging.debug("Successfully updated metadata.")