from dotenv import load_dotenv
load_dotenv()

import traceback
import sys
from lib import spotify_api, db, logger

current_step = 1

def attempt(name, handler):
  global current_step
  logger.step_start(current_step, name)

  try:
    handler()
  except Exception:
    logger.error("An error ocurred:")
    traceback.print_exc()
    logger.step_fail(current_step)
    logger.debug("\nExiting...")
    sys.exit(1)

  logger.step_success(current_step)
  current_step += 1

conn = None
def step_1():
  global conn
  conn = db.connect()
  db.create_tables(conn)

attempt("Database Setup", step_1)

access_token = None
def step_2():
  global access_token
  access_token = spotify_api.request_access_token()

attempt("Obtain Access Token", step_2)

user_playlists = None
def step_3():
  global user_playlists
  user_playlists = spotify_api.request_user_playlists(access_token)
  db.store_user_playlists(conn, user_playlists)

attempt("Save User Playlists", step_3)

def step_4():
  for playlist in user_playlists:
    tracks = spotify_api.request_playlist_tracks(
      access_token, 
      playlist["tracks_href"]
    )

    db.store_tracks(conn, tracks)
    db.store_track_artists(conn, tracks)
    db.store_playlist_tracks(conn, tracks, playlist["id"])

attempt("Save Track Data", step_4)