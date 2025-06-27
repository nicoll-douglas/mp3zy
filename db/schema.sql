CREATE TABLE IF NOT EXISTS playlists (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  cover_source TEXT NOT NULL,
  cover_local TEXT
);

CREATE TABLE IF NOT EXISTS tracks (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  cover_source TEXT NOT NULL,
  mobile_available BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS artists (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS track_artist (
  track_id TEXT,
  artist_id TEXT,
  PRIMARY KEY (track_id, artist_id),
  FOREIGN KEY (track_id) REFERENCES tracks(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE IF NOT EXISTS playlist_track (
  track_id TEXT,
  playlist_id TEXT,
  PRIMARY KEY (track_id, playlist_id),
  FOREIGN KEY (track_id) REFERENCES tracks(id),
  FOREIGN KEY (playlist_id) REFERENCES playlists(id)
);