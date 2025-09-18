import db
from ..Model import Model

class Metadata(Model):
  _TABLE = "metadata"
  
  def __init__(self, conn = db.connect()):
    super().__init__(conn)
  
  def delete(self, id):
    super().delete({ "id": id })

  def select(self, id):
    return super().select(where={ "id": id })