import db
from ..model import Model
from typing import cast

class MetadataArtist(Model):
  """A database model representing the metadata_artists table.
  """

  TABLE = "metadata_artists"


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


  def get_many_artist_ids(self, metadata_ids: list[int]) -> list[int]:
    """Gets several artist IDs from the table based on metadata IDs.

    Args:
      metadata_ids (list[int]): The IDs of the metadata.

    Returns:
      list[int]: The artist IDs.
    """
    
    placeholders = ", ".join("?" * len(metadata_ids))
    sql = f"SELECT artist_id FROM {self.TABLE} WHERE metadata_id IN ({placeholders})"
    params = tuple(metadata_ids)

    self._cur.execute(sql, params)
    rows = self._cur.fetchall()

    return [row["artist_id"] for row in rows]
  # END get_artist_ids

# END class MetadataArtist