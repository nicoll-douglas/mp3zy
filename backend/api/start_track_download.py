from __future__ import annotations
from utils import create_task_id
from flask_socketio import SocketIO
from services import YtDlpClient
import threading
import db, models

def get_progress_hook(socket: SocketIO, task_id):
  def hook(d: dict):
    dl = models.db.Download()
    dl.update_progress(task_id, {
      "downloaded_bytes": d.get("downloaded_bytes"),
      "total_bytes": d.get("total_bytes"),
      "eta": d.get("total_bytes"),
      "speed": d.get("speed"),
      "elapsed": d.get("elapsed"),
    })

    socket.emit("progress", {
      "taskId": task_id,
      "status": d.get("status"),
      "downloaded_bytes": d.get("downloaded_bytes"),
      "total_bytes": d.get("total_bytes"),
      "eta": d.get("total_bytes"),
      "speed": d.get("speed"),
      "elapsed": d.get("elapsed"),
    })

  return hook

def extract_data(data: dict):
  year = data.get("year")
  month = data.get("month")
  day = data.get("day")
  release_date = None

  if year:
    release_date = year
    if month:
      release_date += f"-{month}"
      if day:
        release_date += f"-{day}"
  
  disc_number = data.get("discNumber")
  track_number = data.get("trackNumber")

  fields = {
    "codec": data["codec"],
    "bitrate": data["bitrate"],
    "download_url": data["downloadUrl"],
    "artists": data["artists"],
    "track": data["track"],
    "album": data.get("album"),
    "release_date": release_date,
    "disc_number": int(disc_number) if disc_number else None,
    "track_number": int(track_number) if track_number else None
  }
  return fields

def start_track_download(socket: SocketIO, data: dict):  
  data = extract_data(data)
  conn = db.connect()

  artist = models.db.Artist(conn)
  artist_ids = artist.insert_many(data["artists"])
  
  mdata = models.db.Metadata(conn)
  mdata_id = mdata.insert({
    "track": data["track"],
    "album": data["album"],
    "release_date": data["release_date"],
    "disc_number": data["disc_number"],
    "track_number": data["track_number"]
  })

  mdata_artist = models.db.MetadataArtist(conn)
  mdata_artist.insert_many(mdata_id, artist_ids)

  dl = models.db.Download(conn)
  dl.queue({
    "bitrate": data["bitrate"],
    "codec": data["codec"],
    "url": data["download_url"],
    "metadata_id": mdata_id,
  })

  conn.commit()

  if dl.is_in_progress():
    return { "status": "queued" }

  def thread_target():
    progress_hook = get_progress_hook(socket)
    track = YtDlpClient().download_track(
      url=data["download_url"],
      artist=data["artists"][0],
      name=data["track"],
      codec=data["codec"],
      bitrate=data["bitrate"],
      progress_hook=progress_hook
    )
    # fetch details about track from spotify (emit status to socket)
    # extract album id
    # download cover art (emit status to socket)
    # set file metadata here (emit status to socket)
    # download complete (emit status to socket)
  
  try:
    t = threading.Thread(target=thread_target, daemon=True)
    t.start()
  except Exception as e:
    return { "status": "error" }
  
  return { "status": "downloading" }

