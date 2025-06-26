from dotenv import load_dotenv
load_dotenv()

from lib import spotify_api, db, logger

ACCESS_TOKEN = spotify_api.request_access_token()

user_playlists = spotify_api.request_user_playlists(ACCESS_TOKEN)

conn = db.connect()
db.create_tables(conn)

db.store_user_playlists(conn, user_playlists)

for playlist in user_playlists:
  tracks = spotify_api.request_playlist_tracks(
    ACCESS_TOKEN, 
    playlist["tracks_href"]
  )
  db.store_tracks(conn, tracks)