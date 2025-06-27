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

def download_playlist_covers():
  total = len(PLAYLISTS)
  logging.info(f"Downloading user playlist covers (~{total}).")
  success_count = 0

  for index, item in enumerate(PLAYLISTS):
    current_num = index + 1
    
    logging.info(f"Downloading {current_num} of ~{total}")
    cover_img_path, cover_img_is_fresh = download.cover_image(
      item["cover_source"],
      disk.PLAYLIST_COVERS_DIR
    )

    if not cover_img_is_fresh:
      logging.info("Already downloaded so skipped.")
      continue

    if not cover_img_path:
      logging.warning(f"Playlist cover download {current_num} of {total} failed. ({item["id"], item["name"]})")
      continue

    success_count += 1
    logging.info(f"Download {current_num} of ~{total} succeeded.")

  logging.info(f"Successfully downloaded {success_count} of {total} new covers.")

app.attempt("Download Playlist Covers", download_playlist_covers, 3)

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

app.attempt("Retrieve Track Data", retrieve_track_data, 4)

def download_undownloaded():
  disk.create_dirs()
  track = Track(DB_CONN)
  track_artist = TrackArtist(DB_CONN)

  logging.info("Finding all locally unavailable tracks...")
  locally_unavailable_tracks = track.find_all_locally_unavailable()
  total = len(locally_unavailable_tracks)
  success_count = 0

  logging.info(f"Downloading {total} locally unavailable tracks...")
  for index, item in enumerate(locally_unavailable_tracks):
    current_num = index + 1
    
    logging.info(f"Downloading {current_num} of {total}...")
    track_artists = track_artist.find_all(item["id"])

    mp3_file_path, track_is_fresh = download.track({
      "id": item["id"],
      "name": item["name"],
      "artists": track_artists,
      "duration_s": item["duration_ms"] / 1000
    })

    cover_img_path, cover_img_is_fresh = download.cover_image(
      item["cover_source"],
      disk.TRACK_COVERS_DIR
    )

    if not mp3_file_path or not cover_img_path:
      logging.warning(f"Track download {current_num} of {total} failed. ({item["id"], item["name"]})")
      continue

    if (track_is_fresh or cover_img_is_fresh) and (mp3_file_path and cover_img_path):
      metadata.set_mp3(
        mp3_file_path,
        {
          "name": item["name"],
          "artists": track_artists,
          "cover_path": cover_img_path
        }
      )
      track.set_locally_available(item["id"])

    success_count += 1
    logging.info(f"Download {current_num} of {total} succeeded.")
    
  logging.info(f"Successfully finished downloading {success_count} of {total}.")

app.attempt("Download All Undownloaded Tracks", download_undownloaded, 5)