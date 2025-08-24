# Roadmap

Rough roadmap for this project

## Features

- Option to select app working directory (~)
- Download track to ~/tracks
- Track filename format: Artist - Year - Album - Track# - Title.mp3
- Create playlists for PC and mobile under ~/playlists.windows, ~/playlists.linux and ~/playlists.android
- Use Syncthing to sync ~/tracks and ~/playlists.android to mobile

## Settings / Setup flow / Dashboard

- select primary folder where music is downloaded to, default to user/music

## Downloader

- Desktop app with Python web backend running on user machine
- Cross platform so Electron GUI for frontend
- Purpose: downloading mp3s easily and neatly with yt-dlp package
- Search YouTube, show results of which to select, query Spotify, prefill reasonable mp3 metadata with Spotify data
- Option to select audio quality / bitrate

## Spotify Syncer

- Have authentication flow with Spotify to have access to all playlist data and liked songs for user
- Download tracks in Spotify playlists to files and convert playlists to .m3u8 files
- Have a button to sync from Spotify
- Check all files for UFID to see if downloaded, download otherwise and always refresh playlists

## Deployment

- GitHub/Gitea actions to bundle into cross-platform installers/downloadables
- Make downloads available on GitHub releases
- Add app download link on website and privacy policy

## Web Routes

### GET /

Output:

- text/html
- page with link to /download and /spotify-sync

### GET /download

Inputs:

?artist=_&track=_

Output:

- text/html
- Page with form accepting track name and artist name (action = /download, method = GET)
- Download form with inputs
- mp3 metadata prefilled in form and YouTube results ranked best to worst (action = /download, method = POST)

### POST /download

Input:

form data { ...mp3_metadata, youtube_result, bitrate }

Output:

- 301 GET /downloads/{id}

### GET /downloads/{id}

Inputs:

- {id}

Output:

- text/html
- Page with progress updates
- Live updates on download progress with web sockets
- Button to cancel which will remove anything saved to disk and cancel download
- On error follow cancel process
- Link to start new download

### GET /downloads

Output:

- Download queue with live download updates via ws://
- Links to invidivual download progress (/downloads/{id})

### GET /spotify-sync

- prompt auth flow if not auth'd
- after auth, make button available for sync
- show time since last sync
