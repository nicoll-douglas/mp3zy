from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TRCK, TPOS, TDRC, TLEN
from mutagen.mp3 import MP3
from mutagen.flac import FLAC, Picture
from .track_cover import TrackCover

class Metadata:
  cover_path = None
  track_name = None
  track_artists = None
  album = None
  track_number = None
  disc_number = None
  release_date = None
  duration_ms = None
  
  def __init__(
    self, 
    cover_path = None,
    track_name = None,
    track_artists = None,
    album = None,
    track_number = None,
    disc_number = None,
    release_date = None,
    duration_ms = None
  ):
    self.cover_path = cover_path
    self.track_name = track_name
    self.track_artists = track_artists
    self.album = album
    self.track_number = str(track_number) if track_number else None
    self.disc_number = str(disc_number) if disc_number else None
    self.release_date = release_date
    self.duration_ms = str(duration_ms) if duration_ms else None
  
  def set_on_mp3(self, audio_path):
    audio = MP3(audio_path)

    audio.delete()
    audio.add_tags()      

    audio.tags = ID3()
    audio.tags.add(TIT2(encoding=3, text=self.track_name))
    audio.tags.add(TPE1(encoding=3, text=self.track_artists))
    audio.tags.add(TALB(encoding=3, text=self.album))
    audio.tags.add(TRCK(encoding=3, text=self.track_number))
    audio.tags.add(TPOS(encoding=3, text=self.disc_number))
    audio.tags.add(TDRC(encoding=3, text=self.release_date))
    audio.tags.add(TLEN(encoding=3, text=self.duration_ms))

    if self.cover_path:
      cover = TrackCover(path=self.cover_path)
      mimetype = cover.get_path_mimetype()

      with open(cover, "rb") as img:
        audio.tags.add(
          APIC(
            encoding=3,
            mime=mimetype,
            type=3,
            desc="",
            data=img.read()
          )
        )
    
    audio.save(v2_version=3)

  def set_on_flac(self, audio_path):
    audio = FLAC(audio_path)
    audio.delete()

    audio["title"] = self.track_name
    audio["artist"] = self.track_artists
    audio["album"] = self.album
    audio["tracknumber"] = self.track_number
    audio["discnumber"] = self.disc_number
    audio["date"] = self.release_date

    if self.cover_path:
      p = Picture()
      tc = TrackCover(path=self.cover_path)
      mimetype = tc.get_path_mimetype()

      with open(self.cover_path, "rb") as img:
        p.data = img.read()

      p.type = 3
      p.mime = mimetype

      audio.clear_pictures()
      audio.add_picture(p)

    audio.save()