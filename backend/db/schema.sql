CREATE TABLE downloads (
  id TEXT PRIMARY KEY,           -- UUID or unique task ID
  url TEXT NOT NULL,             -- Source URL
  codec TEXT NOT NULL,
  bitrate TEXT NOT NULL,
  metadata_id INTEGER NOT NULL,  -- Metadata ID           
  status TEXT NOT NULL,          -- queued | downloading | postprocessing | completed | failed
  
  error TEXT,                    -- Error message if failed
  
  downloaded_bytes INTEGER,      -- Progress so far
  total_bytes INTEGER,           -- Final size if known
  speed INTEGER,                 -- Bytes per second
  eta INTEGER,                   -- Seconds remaining
  elapsed REAL,                  -- Seconds since start
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,        -- Filled when status = completed

  FOREIGN KEY (metadata_id) REFERENCES metadata(id)
);

CREATE TABLE artists (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE metadata (
  id INTEGER PRIMARY KEY,
  track TEXT NOT NULL,
  album TEXT,
  track_number INTEGER,
  disc_number INTEGER,
  release_date TEXT
);

CREATE TABLE metadata_artists (
  metadata_id INTEGER NOT NULL,
  artist_id INTEGER NOT NULL,
  FOREIGN KEY (metadata_id) REFERENCES metadata(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id),
  PRIMARY KEY (metadata_id, artist_id)
);