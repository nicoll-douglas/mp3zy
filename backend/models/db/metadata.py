import db
from ..Model import Model

class Metadata(Model):
  _TABLE = "metadata"
  
  def __init__(self, conn = db.connect()):
    super().__init__(conn)