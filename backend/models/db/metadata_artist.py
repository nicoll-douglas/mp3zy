import db
from ..model import Model
from typing import cast

class MetadataArtist(Model):
  """A database model representing the metadata_artists table.
  """

  _TABLE = "metadata_artists"


  def __init__(self, conn = db.connect()):
    super().__init__(conn)
  # END __init__


  def insert_many(self, data: list[dict]) -> list[int]:
    """
    Inserts several rows into the table.

    Args:
      data (list[dict]): A list of dicts (key-value pairs) representing the column names and values to insert for them.

    Returns:
      list[int]: A list of the integer IDs of the rows that were inserted.
    """
    
    ids = []
    
    for d in data:
      id = cast(int, self.insert(d))
      ids.append(id)

    return ids
  # END insert_many

# END class MetadataArtist