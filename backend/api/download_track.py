from services import YtDlpClient

def extract_data(request_body: dict):
  year = request_body.get("year")
  month = request_body.get("month")
  day = request_body.get("day")
  disc_number = request_body.get("discNumber")
  track_number = request_body.get("trackNumber")

  disc_number = int(disc_number) if disc_number else None
  track_number = int(track_number) if track_number else None

  release_date = None
  if year:
    release_date = year
    if month:
      release_date += f"-{month}"
      if day:
        release_date += f"-{day}"
  
  return {
    "artists": request_body["artists"],
    "track": request_body["track"],
    "album": request_body.get("album"),
    "codec": request_body["codec"],
    "bitrate": request_body["bitrate"],
    "track_number": track_number,
    "disc_number": disc_number,
    "release_date": release_date,
    "download_url": request_body["download_url"]
  }

def download_track(request_body: dict):
  data = extract_data(request_body)
  yt_dlp = YtDlpClient()
  return yt_dlp.download_track(data)
  