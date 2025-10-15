from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TRCK, TPOS, TDRC, TYER, TDAT
from mutagen.mp3 import MP3
from mutagen.flac import FLAC, Picture
from .album_cover import AlbumCover
from user_types import TrackArtistNames, TrackReleaseDate

class Metadata:
  """A model class that interfaces with metadata of a music file on disk

  Attributes:
    album_cover_path (str | None): The path to an image file on disk that can be used as album cover metadata.
    track_name (str): Track name metadata.
    artist_names (TrackArtistNames): Artist name metadata.
    album_name (str | None): Album name metadata.
    track_number (int | None): Track number metadata.
    disc_number (int | None): Disc number metadata.
    release_date (TrackReleaseDate | None): Track release date metadata.
  """
  
  album_cover_path: str | None
  track_name: str
  artist_names: TrackArtistNames
  album_name: str | None
  track_number: int | None
  disc_number: int | None
  release_date: TrackReleaseDate | None
  

  def set_on_mp3(self, file_path: str):
    """Sets the metadata onto an MP3 file.

    Args:
      file_path (str): The path to the MP3 file.
    """
    
    audio = MP3(file_path)
    audio.tags = ID3()

    audio.tags.add(TIT2(encoding=3, text=self.track_name))
    audio.tags.add(TPE1(encoding=3, text=self.artist_names.data))

    if self.album_name:
      audio.tags.add(TALB(encoding=3, text=self.album_name))

    if self.track_number is not None:
      audio.tags.add(TRCK(encoding=3, text=str(self.track_number)))

    if self.disc_number is not None:
      audio.tags.add(TPOS(encoding=3, text=str(self.disc_number)))

    if self.release_date is not None:
      audio.tags.add(TYER(encoding=3, text=str(self.release_date.year)))

      if self.release_date.month is not None and self.release_date.day is not None:
        tdat_value = str(self.release_date.day).zfill(2) + str(self.release_date.month).zfill(2)
        audio.tags.add(TDAT(encoding=3, text=tdat_value))

    if self.album_cover_path:
      cover = AlbumCover(self.album_cover_path)
      mimetype = cover.get_mimetype()

      if cover.exists():
        audio.tags.add(
          APIC(
            encoding=3,
            mime=mimetype,
            type=3,
            desc="",
            data=cover.read()
          )
        )
  
    # need to add try catch here
    audio.save(v2_version=3)
  # END set_on_mp3


  def set_on_flac(self, file_path: str):
    """Sets the metadata onto a FLAC file.

    Args:
      file_path (str): The path to the FLAC file.
    """
    
    audio = FLAC(file_path)
    audio.delete()

    audio["TITLE"] = self.track_name
    audio["ARTIST"] = self.artist_names.data
    
    if self.album_name:
      audio["ALBUM"] = self.album_name

    if self.track_number is not None:      
      audio["TRACKNUMBER"] = str(self.track_number)

    if self.disc_number is not None:      
      audio["DISCNUMBER"] = str(self.disc_number)
    
    if self.release_date is not None:
      audio["DATE"] = str(self.release_date)

    if self.album_cover_path:
      p = Picture()
      cover = AlbumCover(self.album_cover_path)
      mimetype = cover.get_mimetype()

      try:
        p.data = cover.read()
        p.type = 3
        p.mime = mimetype

        audio.clear_pictures()
        audio.add_picture(p)
      except OSError:
        pass
      
    audio.save()
  # END set_on_flac

# END class Metadata