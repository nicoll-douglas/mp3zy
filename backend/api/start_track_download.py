from __future__ import annotations
from utils import format_eta, format_download_speed, get_download_progress, get_track_string
from flask_socketio import SocketIO
from services import YtDlpClient
import threading
import db, models

def get_progress_hook(socket: SocketIO, dl_id, track_data: dict):
  def hook(d: dict):
    conn = db.connect()
    dl = models.db.Download(conn)

    downloaded_bytes = d.get("downloaded_bytes")
    total_bytes = d.get("total_bytes")
    eta = d.get("eta")
    speed = d.get("speed")
    elapsed = d.get("elapsed")
    
    dl.update_progress(dl_id, {
      "downloaded_bytes": downloaded_bytes,
      "total_bytes": total_bytes,
      "eta": eta,
      "speed": speed,
      "elapsed": elapsed,
    })
    conn.commit()
    conn.close()

    socket.emit("progress", {
      "phase": "downloading",
      "progress": get_download_progress(downloaded_bytes, total_bytes),
      "eta": format_eta(eta),
      "speed": format_download_speed(speed),
      "trackStr": get_track_string(track_data["artists"], track_data["track"]),
      "codec": track_data["codec"],
      "bitrate": track_data["bitrate"]
    }, to="download")

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
  conn.commit()
  
  mdata = models.db.Metadata(conn)
  mdata_id = mdata.insert({
    "track": data["track"],
    "album": data["album"],
    "release_date": data["release_date"],
    "disc_number": data["disc_number"],
    "track_number": data["track_number"]
  })
  conn.commit()

  mdata_artist = models.db.MetadataArtist(conn)
  mdata_artist.insert_many(mdata_id, artist_ids)
  conn.commit()

  dl = models.db.Download(conn)
  dl_id = dl.queue({
    "bitrate": data["bitrate"],
    "codec": data["codec"],
    "url": data["download_url"],
    "metadata_id": mdata_id,
  })
  conn.commit()

  if dl.is_in_progress():
    return { "status": "queued" }

  def thread_target():
    progress_hook = get_progress_hook(socket, dl_id, {
      "track": data["track"],
      "artists": data["artists"],
      "codec": data["codec"],
      "bitrate": data["bitrate"]
    })
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
    # set file metadata here (emit updating_metadata to socket)
    
    dl.set_completed(dl_id)
    conn.commit()
    conn.close()

    socket.emit("complete", to="download")
  
  try:
    t = threading.Thread(target=thread_target, daemon=True)
    t.start()
  except Exception as e:
    return { "status": "error" }
  
  return { "status": "downloading" }

