CREATE TABLE IF NOT EXISTS playlists (
  id TEXT PRIMARY KEY,
  name TEXT,
  cover TEXT
);

CREATE TABLE IF NOT EXISTS tracks (
  id TEXT PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS artists (
  id TEXT PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS track_artist (
  track_id TEXT,
  artist_id TEXT,
  PRIMARY KEY (track_id, artist_id),
  FOREIGN KEY (track_id) REFERENCES tracks(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id)
);