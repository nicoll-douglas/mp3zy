import db
from ..model import Model
import sqlite3

class Metadata(Model):
  """A database model representing the metadata table.
  """

  TABLE = "metadata"
  
  
  def __init__(self, conn: sqlite3.Connection = db.connect()):
    super().__init__(conn)
  # END __init__


  def delete_many(self, ids: list[int]) -> int:
    """Deletes several rows in the table

    Args:
      ids (list[int]): The IDs of the metadata/rows to delete.

    Returns:
      int: The number of rows deleted.
    """
    
    placeholders = ", ".join("?" * len(ids))
    sql = f"DELETE FROM {self.TABLE} WHERE id IN ({placeholders})"
    params = tuple(ids)
    
    self._cur.execute(sql, params)
    self._conn.commit()

    return self._cur.rowcount
  # END delete_many

# END class Metadata