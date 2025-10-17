CREATE TABLE IF NOT EXISTS downloads (
  id INTEGER PRIMARY KEY,
  url TEXT NOT NULL,
  codec TEXT NOT NULL,
  bitrate TEXT NOT NULL,
  metadata_id INTEGER,
  status TEXT NOT NULL,
  downloaded_bytes INTEGER,
  download_dir TEXT NOT NULL,
  total_bytes INTEGER,
  speed REAL,
  eta REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  terminated_at TIMESTAMP,
  error_msg TEXT,
  FOREIGN KEY (metadata_id) REFERENCES metadata(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS artists (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS metadata (
  id INTEGER PRIMARY KEY,
  track_name TEXT NOT NULL,
  main_artist TEXT NOT NULL,
  album_name TEXT,
  track_number INTEGER,
  disc_number INTEGER,
  release_date TEXT,
  album_cover_path TEXT
);

CREATE TABLE IF NOT EXISTS metadata_artists (
  metadata_id INTEGER NOT NULL,
  artist_id INTEGER NOT NULL,
  FOREIGN KEY (metadata_id) REFERENCES metadata(id) ON DELETE CASCADE,
  FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
  PRIMARY KEY (metadata_id, artist_id)
);