import db
from ..model import Model
import json
from user_types import DownloadStatus
from datetime import datetime

class Download(Model):
  """A database model representing the downloads table.
  """
  
  _TABLE = "downloads"


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
  json_group_array(a.name) AS other_artists
FROM downloads d
LEFT JOIN metadata m ON d.metadata_id = m.id
LEFT JOIN metadata_artists ma ON m.id = ma.metadata_id
LEFT JOIN artists a ON ma.artist_id = a.id
WHERE d.status = :queued_status
  AND d.created_at = (
    SELECT MIN(created_at) 
    FROM {self._TABLE}
    WHERE status = :queued_status
  ) 
GROUP BY d.id
"""
    self._cur.execute(query, { "queued_status": DownloadStatus.QUEUED.value })
    row = self._cur.fetchone()
    
    if not row:
      return None
    
    result = dict(row)
    other_artists = json.loads(result["other_artists"])

    if other_artists == [None]:
      other_artists = []
      
    result["other_artists"] = other_artists

    return result
  # END get_next_in_queue


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
    
    sql = f"UPDATE {self._TABLE} SET status = ?, total_bytes = ?, downloaded_bytes = ?, eta = ?, speed = ?, terminated_at = ? WHERE id = ?"

    terminated_at = terminated_at if terminated_at else self.get_current_timestamp()
    params = (DownloadStatus.COMPLETED.value, None, None, None, None, terminated_at, download_id)

    self._cur.execute(sql, params)
    self._conn.commit()
  # END set_terminated


  def set_failed(self, download_id: int, terminated_at: str | None = None, error_msg: str | None = None,):
    """Sets a row/download in the table to a failed state.

    Args:
      download_id (int): The ID of the row/download.
      error_msg (str | None): An error message indicating the error that caused the download to fail.
      terminated_at (str | None): The timestamp of when the download failed, gets set to the current timestamp if an empty value passed.
    """
    
    sql = f"UPDATE {self._TABLE} SET status = ?, total_bytes = ?, downloaded_bytes = ?, eta = ?, speed = ?, terminated_at = ?, error_msg = ? WHERE id = ?"

    terminated_at = terminated_at if terminated_at else self.get_current_timestamp()
    params = (DownloadStatus.FAILED.value, None, None, None, None, terminated_at, error_msg, download_id)

    self._cur.execute(sql, params)
    self._conn.commit()
  # END set_terminated


  def update(self, download_id: int, data: dict):
    """Updates a row in the table based on ID with the given data.

    Args:
      download_id (int): The ID of the row/download.
      data (dict): Key-value pairs representing the column names and values to update for them.
    """
    
    sql = f"UPDATE {self._TABLE} SET "
    set_clauses = ", ".join([f"{k} = ?" for k in data.keys()])

    sql += f"{set_clauses} WHERE id = ?"
    params = (*data.values(), download_id)

    self._cur.execute(sql, params)
    self._conn.commit()
  # END update

# END class Download