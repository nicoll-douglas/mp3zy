import db
from ..model import Model

class Artist(Model):
  """A database model representing the artists table.
  """
  
  TABLE = "artists"


  def __init__(self, conn = db.connect()):
    super().__init__(conn)
  # END __init__


  def insert_many(self, data: list[dict]) -> list[int]:
    """Inserts several rows into the table.

    Args:
      data (list[dict]): A list of dicts (key-value pairs) representing the column names and values to insert for them.

    Returns:
      list[int]: A list of the integer IDs of the rows that were inserted.
    """
    
    ids: list[int] = []
    
    for d in data:
      id = self.insert(d)
      ids.append(id)

    return ids
  # END insert_many


  def delete_many(self, ids: list[int]) -> int:
    """Deletes several rows in the table

    Args:
      ids (list[int]): The IDs of the artists/rows to delete.

    Returns:
      int: The number of artists/rows deleted.
    """
    
    placeholders = ", ".join("?" * len(ids))
    sql = f"DELETE FROM {self.TABLE} WHERE id IN ({placeholders})"
    params = tuple(ids)
    
    self._cur.execute(sql, params)
    self._conn.commit()

    return self._cur.rowcount
  # END delete_many

# END class Artist