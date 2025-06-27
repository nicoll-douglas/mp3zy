from dotenv import load_dotenv
load_dotenv()

from lib import spotify_api, db, app, download, metadata
import os

conn = None
def step_0():
  global conn
  conn = db.connect()
  db.create_tables(conn)

app.attempt("Setup", step_0, 0)

access_token = None
def step_1():
  global access_token
  access_token = spotify_api.request_access_token()

app.attempt("Obtain Access Token", step_1, 1)

user_playlists = None
def step_2():
  global user_playlists
  user_playlists = spotify_api.request_user_playlists(access_token)
  db.store_user_playlists(conn, user_playlists)

app.attempt("Save User Playlists", step_2, 2)

def step_3():
  for playlist in user_playlists:
    tracks = spotify_api.request_playlist_tracks(
      access_token, 
      playlist["tracks_href"]
    )

    db.store_tracks(conn, tracks)
    db.store_track_artists(conn, tracks)
    db.store_playlist_tracks(conn, tracks, playlist["id"])

app.attempt("Save Track Data", step_3, 3)

def step_4():
  all_tracks = db.get_all_tracks(conn)
  download.create_output_dirs()

  for track in all_tracks:
    track_artists = db.get_all_track_artists(conn, track["id"])
    mp3_file_path, track_is_fresh = download.download_track(
      track["name"], 
      track_artists, track["id"]
    )

    cover_img_path_without_ext = os.path.join(
      download.TRACK_COVERS_DIR, 
      track["id"]
    )
    cover_img_path, cover_img_is_fresh = download.download_cover_image(
      track["cover_source"],
      cover_img_path_without_ext
    )

    if (track_is_fresh or cover_img_is_fresh):
      metadata.add_mp3_metadata(
        mp3_file_path,
        track["name"],
        track_artists,
        cover_img_path
      )

app.attempt("Download All Undownloaded Tracks", step_4, 4)