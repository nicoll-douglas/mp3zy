import db
from ..model import Model
import sqlite3

class Metadata(Model):
  """A database model representing the metadata table.
  """

  _TABLE = "metadata"
  
  
  def __init__(self, conn: sqlite3.Connection = db.connect()):
    super().__init__(conn)
  # END __init__

# END class Metadata