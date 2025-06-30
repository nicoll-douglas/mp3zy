from .FtpClient import FtpClient
import os, logging
import disk

class FtpMusicManager(FtpClient):
  __STORAGE_DIR = os.getenv("FTP_MUSIC_STORAGE_DIR")
  __TRACKS_DIR = os.path.join(os.getenv("FTP_MUSIC_STORAGE_DIR"), "tracks")
  __PLAYLISTS_DIR = os.path.join(os.getenv("FTP_MUSIC_STORAGE_DIR"), "playlists")
  
  def __init__(self):
    super().__init__()
    self.connect()
    self.mkdir_p(self.__TRACKS_DIR)
    self.mkdir_p(self.__PLAYLISTS_DIR)
    self.__cd_storage()

  def __cd_storage(self):
    self._ftp_instance.cwd(self.__STORAGE_DIR)

  def __cd_tracks(self):
    self._ftp_instance.cwd(self.__TRACKS_DIR)

  def __cd_playlists(self):
    self._ftp_instance.cwd(self.__PLAYLISTS_DIR)

  @staticmethod
  def get_track_id(track_filename: str):
    return track_filename.split(disk.Track.EXT)[0]

  @staticmethod
  def get_playlist_id(playlist_filename: str):
    return playlist_filename.split(disk.Playlist.EXT)[0]

  @staticmethod
  def get_track_filename(track_id: str):
    return track_id + disk.Track.EXT

  @staticmethod
  def get_playlist_filename(playlist_name: str):
    return playlist_name + disk.Playlist.EXT

  @classmethod
  def path_to_track_from_playlist(cls, track_id: str):
    return "../tracks/" + cls.get_track_filename(track_id)
  
  def insert_track(self, track_id: str):
    track = disk.Track(track_id)
    path = track.get_path()

    if path and track.exists():
      self.write(
        path, 
        self.__TRACKS_DIR + self.get_track_filename(track_id)
      )

  def remove_track(self, track_filename: str):
    self.__cd_tracks()
    if self.exists_here(track_filename):
      self.rm(track_filename)
    self.__cd_storage()

  def insert_playlist(self, playlist_name: str):
    playlist = disk.MobilePlaylist(playlist_name)
    path = playlist.get_path()

    if path and playlist.exists():
      self.write(
        path, 
        self.__PLAYLISTS_DIR + self.get_playlist_filename(playlist_name)
      )

  def remove_playlist(self, playlist_filename: str):
    self.__cd_playlists()
    if self.exists_here(playlist_filename):
      self.rm(playlist_filename)
    self.__cd_storage()

  def get_all_tracks(self):
    self.__cd_tracks()
    tracks = self.ls()
    self.__cd_storage()
    return tracks

  def get_all_playlists(self):
    self.__cd_playlists()
    playlists = self.ls()
    self.__cd_storage()
    return playlists
  
  def sync_tracks(self, updated_track_ids: set[str]):
    current_tracks = self.get_all_tracks()

    to_delete = {
      self.get_track_filename(t) 
      for t in updated_track_ids
    } - set(current_tracks)
    to_insert = {
      self.get_track_id(t)
      for t in current_tracks
    } - updated_track_ids

    self.__cd_tracks()
    for filename in to_delete:
      self.remove_track(filename)
    for track_id in to_insert:
      self.insert_track(track_id)
    self.__cd_storage()

  def sync_playlists(self, updated_playlist_names: set[str]):
    self.log("info", "Syncing playlist data...")
    current_playlists = self.get_all_playlists()

    to_delete = {
      self.get_playlist_filename(t)
      for t in updated_playlist_names
    } - set(current_playlists)
    to_insert = {
      self.get_playlist_id(t)
      for t in current_playlists
    } - updated_playlist_names

    self.__cd_playlists()
    self.log("debug", "Deleting diffed playlists...")
    for filename in to_delete:
      self.remove_playlist(filename)
    self.log("debug", "Inserting diffed playlists")
    for playlist_name in to_insert:
      self.insert_playlist(playlist_name)

    self.__cd_storage()
    self.log("info", "Playlist data synced successfully.")