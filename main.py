from dotenv import load_dotenv
load_dotenv()

import logging, os

APP_ENV = os.getenv("APP_ENV")
LOGGING_LEVEL = logging.INFO if APP_ENV == "production" else logging.DEBUG
LOGGING_FORMAT = "%(levelname)s | %(message)s"

logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)

from core import spotify_api, app, download, metadata, disk
from db.Db import Db
from db.models.Track import Track
from db.models.Playlist import Playlist
from db.models.TrackArtist import TrackArtist
from db.models.PlaylistTrack import PlaylistTrack
from db.models.Artist import Artist

def setup():
  DB = Db()
  conn = DB.connect()
  DB.setup(conn)
  return conn

DB_CONN = app.attempt("Setup", setup, 0)

def get_access_token():
  logging.info("Requesting an access token from the Spotify API...")
  access_token = spotify_api.request_access_token()
  logging.info("Successfully obtained an access token.")
  return access_token

ACCESS_TOKEN = app.attempt("Obtain Access Token", get_access_token, 1)

def retrieve_user_playlists():
  logging.info("Retrieving user playlist data from the Spotify API")
  playlist_data = spotify_api.request_user_playlists(ACCESS_TOKEN)
  logging.info("Successfully retrieved playlist data.")
  
  playlist = Playlist(DB_CONN)

  logging.info("Inserting playlist data into the database...")
  playlist.insert_many([
    { k: v for k, v in d.items() if k != "tracks_href" }
    for d in playlist_data
  ])
  logging.info("Successfully inserted playlist data.")

  return playlist_data

PLAYLISTS = app.attempt("Retrieve User Playlists", retrieve_user_playlists, 2)

def retrieve_track_data():
  track = Track(DB_CONN)
  track_artist = TrackArtist(DB_CONN)
  playlist_track = PlaylistTrack(DB_CONN)
  artist = Artist(DB_CONN)

  logging.info("Batch requesting track data for each playlist from the Spotify API and inserting into the database...")
  for playlist in PLAYLISTS:
    track_data = spotify_api.request_playlist_tracks(
      ACCESS_TOKEN, 
      playlist["tracks_href"]
    )

    track.insert_many([
      { k: v for k, v in d.items() if k != "artists" }
      for d in track_data
    ])

    for t in track_data:
      artist.insert_many(t["artists"])
      
      track_artist.insert_many(t["id"], [
        a["id"] for a in t["artists"]
      ])
    
    playlist_track.insert_many(playlist["id"], [
      t["id"] for t in track_data      
    ])
  logging.info("Successfully retrieved and inserted track data.")

app.attempt("Retrieve Track Data", retrieve_track_data, 3)

logging.info("Database is now filled with all necessary data.")

def download_undownloaded():
  disk.create_dirs()
  track = Track(DB_CONN)
  track_artist = TrackArtist(DB_CONN)
  logging.info("Find all locally unavailable tracks...")
  locally_unavailable_tracks = track.find_all_locally_unavailable()

  logging.info("Downloading all locally unavailable tracks, this may take some time....")
  for t in locally_unavailable_tracks:
    track_artists = track_artist.find_all(t["id"])

    mp3_file_path, track_is_fresh = download.track({
      "id": t["id"],
      "name": t["name"],
      "artists": track_artists,
      "duration_s": t["duration_ms"] / 1000
    })

    cover_img_path, cover_img_is_fresh = download.cover_image(
      t["cover_source"],
      disk.TRACK_COVERS_DIR
    )

    if not mp3_file_path:
      continue

    if (track_is_fresh or cover_img_is_fresh):
      metadata.set_mp3(
        mp3_file_path,
        {
          "name": t["name"],
          "artists": track_artists,
          "cover_path": cover_img_path
        }
      )
      track.set_locally_available(t["id"])
  logging.info("Successfully finished downloading. All tracks in the database are now locally available.")

app.attempt("Download All Undownloaded Tracks", download_undownloaded, 4)