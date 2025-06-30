from .Client import Client
import os
import disk

class MusicManager(Client):
  __TRACKS_DIR: str = os.path.join(os.getenv("FTP_STORAGE_DIR"), "tracks")
  __PLAYLISTS_DIR: str = os.path.join(os.getenv("FTP_STORAGE_DIR"), "playlists")
  __INTERNAL_STORAGE_ROOT: str = "/storage/emulated/0/"
  
  def __init__(self):
    super().__init__()
    self.connect()
    self.mkdir_p(self.__TRACKS_DIR)
    self.mkdir_p(self.__PLAYLISTS_DIR)

  def __cd_tracks(self):
    self.log("debug", f"cd'ing to {self.__TRACKS_DIR}")
    self.cwd(self.__TRACKS_DIR)

  def __cd_playlists(self):
    self.log("debug", f"cd'ing to {self.__PLAYLISTS_DIR}")
    self.cwd(self.__PLAYLISTS_DIR)

  @staticmethod
  def get_track_id(track_filename: str):
    return track_filename.split(disk.models.Track.EXT)[0]

  @staticmethod
  def get_playlist_id(playlist_filename: str):
    return playlist_filename.split(disk.models.Playlist.EXT)[0]

  @staticmethod
  def get_track_filename(track_id: str):
    return track_id + disk.models.Track.EXT

  @staticmethod
  def get_playlist_filename(playlist_name: str):
    return playlist_name + disk.models.Playlist.EXT

  @classmethod
  def get_absolute_track_path(cls, track_id: str):
    return os.path.join(
      cls.__INTERNAL_STORAGE_ROOT, 
      cls.__TRACKS_DIR.strip("/"),
      cls.get_track_filename(track_id)
    )
  
  def write_track(self, track_id: str):
    self.log("debug", f"Transfering track to server: {track_id}")
    original_dir = self.pwd()
    self.__cd_tracks()

    track_filename = self.get_track_filename(track_id)

    if self.exists_here(track_filename):
      self.log("debug", "File already exists, skipping...")
      self.log("debug", f"cd'ing back to {original_dir}")
      self.cwd(original_dir)
      return

    track = disk.models.Track(track_id)
    if track.exists():
      path = track.get_path()
      self.write(path, track_filename)
      self.log("debug", f"Successfully transferred.")
    else:
      self.log("File does not exist on client.")
    
    self.log("debug", f"cd'ing back to {original_dir}")
    self.cwd(original_dir)

  def remove_track(self, track_filename: str):
    self.log("debug", f"Removing track: {track_filename}")
    original_dir = self.pwd()
    self.__cd_tracks()
    if self.exists_here(track_filename):
      self.rm(track_filename)
    self.log("debug", "Successfully removed.")
    self.log("debug", f"cd'ing back to {original_dir}")
    self.cwd(original_dir)

  def write_playlist(self, playlist_name: str):
    self.log("debug", f"Transferring playlist to server: {playlist_name}")
    playlist = disk.models.MobilePlaylist(playlist_name)

    if playlist.exists():
      original_dir = self.pwd()
      self.__cd_playlists()
      self.write(
        playlist.get_path(), 
        self.get_playlist_filename(playlist_name)
      )
      self.log("debug", "Successfully transferred.")
      self.log("debug", f"cd'ing back to {original_dir}")
      self.cwd(original_dir)
    else:
      self.log("File does not exist on client.")

  def remove_playlist(self, playlist_filename: str):
    self.log("debug", f"Removing playlist: {playlist_filename}")
    original_dir = self.pwd()
    self.__cd_playlists()
    if self.exists_here(playlist_filename):
      self.rm(playlist_filename)
    self.log("debug", "Successfully removed.")
    self.log("debug", f"cd'ing back to {original_dir}")
    self.cwd(original_dir)

  def list_tracks(self):
    original_dir = self.pwd()
    self.__cd_tracks()
    tracks = self.nlst()
    self.cwd(original_dir)
    return tracks

  def list_playlists(self):
    original_dir = self.pwd()
    self.__cd_playlists()
    playlists = self.nlst()
    self.cwd(original_dir)
    return playlists
  
  def sync_tracks(self, incoming_tracks: set[str]):
    self.log("info", "Syncing client track files to server...")
    current_tracks = self.list_tracks()

    to_delete = {
      self.get_track_filename(_id)
      for _id in incoming_tracks
    } - set(current_tracks)
    to_write = {
      self.get_track_id(filename)
      for filename in current_tracks
    } - incoming_tracks

    self.log("debug", "Deleting diffed tracks...")
    for filename in to_delete:
      self.remove_track(filename)
    self.log("debug", "Inserting diffed tracks...")
    for track_id in to_write:
      self.write_track(track_id)

    self.log("info", "Client track files synced successfully.")    

  def sync_playlists(self, updated_playlist_names: set[str]):
    self.log("info", "Syncing client playlist files to server...")
    current_playlists = self.list_playlists()

    to_delete = set(current_playlists) - {
      self.get_playlist_filename(t)
      for t in updated_playlist_names
    }
    to_write = updated_playlist_names - {
      self.get_playlist_id(file) 
      for file in to_delete
    }

    self.log("debug", "Deleting diffed playlists...")
    for filename in to_delete:
      self.remove_playlist(filename)
    self.log("debug", "Inserting diffed playlists...")
    for playlist_name in to_write:
      self.write_playlist(playlist_name)

    self.log("info", "Client playlist files synced successfully.")    