# Spotify Downloader Project

## Goals

- Create a script to run on PC that can request playlist data from the Spotify API and download all tracks as MP3s to physical mobile storage.
- Set up syncing so that tracks on phone stay up to date with tracks on Spotify

## Steps

### 1. Spotify API Requests

- Request only the needed playlist data from Spotify API for all playlists
- Store the results in a local database if not already in the database

#### Needed data:

- Song name (fetch from Spotify)
- Artist names (fetch from Spotify)
- Album cover link (fetch from Spotify)
- MP3 locally available on PC (from local database, default `false`)
- MP3 available on mobile (from local database, default `false`)

#### Technologies:

- Python (HTTP module/lib, database interaction module)
- SQLite (to store fetch results)

### 2. Download Tracks as MP3s

- Query the database for all items that have `locally_available` set to false
- Use `yt-dlp` to search for and download the songs (by song name and artists from the query)
- Save downloaded files to Syncthing directory on HDD in order to back up
- On successful download, update database to set `locally_available` to `true`
- Set MP3 track metadata to match the data in the database (track name, artists, album cover)

#### Technologies:

- `yt-dlp`
- Python
- SQLite
- Bash?

### 3. Mobile FTP Server

- Set up mobile FTP to listen for requests from PC that will be transferring the MP3s
- Store the received MP3s in a common location and according to playlist if possible
- Make sure FTP port(s) are open if necessary

#### Technologies:

- FTP server app?

### 4. Transferring Files via FTP

- After all necessary MP3s have been downloaded, query database to find all tracks that have`mobile_available` set to `false` (default)
- Send those tracks to mobile FTP server (via FTP naturally)
- On successful send, set `mobile_available` to `true`

#### Technologies

- Python (FTP module/lib)

### 4. Music Listening App

- Download a music listening app that can display the saved tracks in their folders as playlists

### 5. Syncing

- Set up a CRON job to run the script periodically (e.g every 24 hours) to keep the mobile playlists up to date with the Spotify playlists
