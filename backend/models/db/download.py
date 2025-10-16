import db
from ..model import Model
import json
from user_types import DownloadStatus
from datetime import datetime
from .metadata import Metadata
from .metadata_artist import MetadataArtist
from .artist import Artist

class Download(Model):
  """A database model representing the downloads table.
  """
  
  TABLE = "downloads"


  def __init__(self, conn = db.connect()):
    super().__init__(conn)
  # END __init__


  @staticmethod
  def get_current_timestamp() -> str:
    """Gets the current timestamp as a string.

    Useful for setting the terminated_at column.

    Returns:
      str: The timestamp
    """
    
    now = datetime.now()
    
    return now.strftime("%Y-%m-%d %H:%M:%S")
  # END get_current_timestamp


  def get_all_downloads(self) -> list[dict]:
    """Selects all downloads in the database, aggregating metadata.

    Returns:
      list[dict]: The list of rows.
    """
    
    query = f"""
SELECT 
  d.id AS download_id,
  d.url,
  d.codec,
  d.bitrate,
  d.status,
  d.download_dir,
  d.downloaded_bytes,
  d.total_bytes,
  d.speed,
  d.eta,
  d.terminated_at,
  d.error_msg,
  d.created_at,
  m.id AS metadata_id,
  m.track_name,
  m.main_artist,
  m.album_name,
  m.track_number,
  m.disc_number,
  m.release_date,
  m.album_cover_path,
  json_group_array(a.name) AS other_artists
FROM {self.TABLE} d
LEFT JOIN {Metadata.TABLE} m ON d.metadata_id = m.id
LEFT JOIN {MetadataArtist.TABLE} ma ON m.id = ma.metadata_id
LEFT JOIN {Artist.TABLE} a ON ma.artist_id = a.id
GROUP BY d.id
"""
    
    self._cur.execute(query)
    rows = self._cur.fetchall()
    
    if not rows:
      return []
    
    results = []

    for row in rows:
      result = dict(row)
      self._load_other_artists(result)
      results.append(result)

    return results
  # END get_all_downloads


  def get_next_in_queue(self) -> dict | None:
    """Selects the earliest created download where `status` is queued, aggregating all metadata.

    Returns:
      dict | None: A dict with the row's data if a row was found, None otherwise.
    """
    
    query = f"""
SELECT
  d.id AS download_id,
  d.url,
  d.codec,
  d.bitrate,
  d.status,
  d.created_at,
  d.download_dir,
  m.id AS metadata_id,
  m.track_name,
  m.main_artist,
  m.album_name,
  m.track_number,
  m.disc_number,
  m.release_date,
  m.album_cover_path,
  json_group_array(a.name) AS other_artists
FROM {self.TABLE} d
LEFT JOIN {Metadata.TABLE} m ON d.metadata_id = m.id
LEFT JOIN {MetadataArtist.TABLE} ma ON m.id = ma.metadata_id
LEFT JOIN {Artist.TABLE} a ON ma.artist_id = a.id
WHERE d.status = :queued_status
  AND d.created_at = (
    SELECT MIN(created_at) 
    FROM {self.TABLE}
    WHERE status = :queued_status
  ) 
GROUP BY d.id
"""
    self._cur.execute(query, { "queued_status": DownloadStatus.QUEUED.value })
    row = self._cur.fetchone()
    
    if not row:
      return None
    
    result = dict(row)
    self._load_other_artists(result)

    return result
  # END get_next_in_queue


  def get_download(self, download_id: int) -> dict | None:
    """Selects a download/row.

    Args:
      download_id (int): The ID of the download.

    Returns:
      dict | None: A dict with the row's data if a row was found, None otherwise.
    """

    query = f"""
SELECT 
  d.id AS download_id,
  d.url,
  d.codec,
  d.bitrate,
  d.status,
  d.download_dir,
  d.downloaded_bytes,
  d.total_bytes,
  d.speed,
  d.eta,
  d.terminated_at,
  d.error_msg,
  d.created_at,
  m.id AS metadata_id,
  m.track_name,
  m.main_artist,
  m.album_name,
  m.track_number,
  m.disc_number,
  m.release_date,
  m.album_cover_path,
  json_group_array(a.name) AS other_artists
FROM {self.TABLE} d
LEFT JOIN {Metadata.TABLE} m ON d.metadata_id = m.id
LEFT JOIN {MetadataArtist.TABLE} ma ON m.id = ma.metadata_id
LEFT JOIN {Artist.TABLE} a ON ma.artist_id = a.id
WHERE d.id = ?
GROUP BY d.id
"""
    
    self._cur.execute(query, (download_id,))
    row = self._cur.fetchone()
    
    if not row:
      return None
    
    result = dict(row)
    self._load_other_artists(result)

    return result
  # END get_download


  def insert_as_queued(self, data: dict) -> int:
    """Inserts a row into the table with the `status` column set to queued.

    Args:
      data (dict): Key-value pairs representing the column names and values to insert for them.

    Returns:
      int: The integer ID of the row that was inserted.
    """

    return self.insert({ **data, "status": DownloadStatus.QUEUED.value })
  # END insert_as_queued
  

  def set_completed(self, download_id: int, terminated_at: str | None = None):
    """Sets a row/download in the table to a completed state.

    Args:
      download_id (int): The ID of the row/download.
      terminated_at (str | None): The timestamp of when the download completed, gets set to the current timestamp if an empty value passed.
    """
    
    sql = f"UPDATE {self.TABLE} SET status = ?, total_bytes = ?, downloaded_bytes = ?, eta = ?, speed = ?, terminated_at = ? WHERE id = ?"

    terminated_at = terminated_at if terminated_at else self.get_current_timestamp()
    params = (DownloadStatus.COMPLETED.value, None, None, None, None, terminated_at, download_id)

    self._cur.execute(sql, params)
    self._conn.commit()
  # END set_terminated


  def set_failed(self, download_id: int, terminated_at: str | None = None, error_msg: str | None = None):
    """Sets a row/download in the table to a failed state.

    Args:
      download_id (int): The ID of the row/download.
      error_msg (str | None): An error message indicating the error that caused the download to fail.
      terminated_at (str | None): The timestamp of when the download failed, gets set to the current timestamp if an empty value passed.
    """
    
    sql = f"UPDATE {self.TABLE} SET status = ?, terminated_at = ?, error_msg = ?, total_bytes = ?, downloaded_bytes = ?, eta = ?, speed = ? WHERE id = ?"

    terminated_at = terminated_at if terminated_at else self.get_current_timestamp()
    params = (DownloadStatus.FAILED.value, terminated_at, error_msg, None, None, None, None, download_id)

    self._cur.execute(sql, params)
    self._conn.commit()
  # END set_terminated


  def requeue(self, download_id: int) -> bool:
    """Sets a row/download to queued in the table if it is not downloading, essentially requeueing the download.
    
    Args:
      download_it (int): The ID of the row/download.

    Returns
      bool: Whether the download was successfully requeued.
    """
    
    sql = f"UPDATE {self.TABLE} SET status = ?, terminated_at = ?, error_msg = ? WHERE id = ? AND status != ?"

    params = (DownloadStatus.QUEUED.value, None, None, download_id, DownloadStatus.DOWNLOADING.value)

    self._cur.execute(sql, params)
    self._conn.commit()

    return self._cur.rowcount > 0
  # END requeue
    

  def update(self, download_id: int, data: dict):
    """Updates a row in the table based on ID with the given data.

    Args:
      download_id (int): The ID of the row/download.
      data (dict): Key-value pairs representing the column names and values to update for them.
    """
    
    sql = f"UPDATE {self.TABLE} SET "
    set_clauses = ", ".join([f"{k} = ?" for k in data.keys()])

    sql += f"{set_clauses} WHERE id = ?"
    params = (*data.values(), download_id)

    self._cur.execute(sql, params)
    self._conn.commit()
  # END update


  def _load_other_artists(self, row: dict):
    """Parses and sets the other_artists column in a fetched row to the parsed JSON array string.

    Args:
      row (dict): The row.
    """
    
    other_artists = json.loads(row["other_artists"])

    if other_artists == [None]:
      other_artists = []
      
    row["other_artists"] = other_artists
  # END _load_other_artists

# END class Download