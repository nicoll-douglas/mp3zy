import db
from ..model import Model

class Artist(Model):
  """A database model representing the artists table.
  """
  
  _TABLE = "artists"


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
      ids.append()

    return ids
  # END insert_many

# END class Artist