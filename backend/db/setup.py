from .connect import connect
from pathlib import Path
import os

def setup():
  conn = connect()
  current_dir = Path(__file__).parent
  schema_path = os.path.join(current_dir, "schema.sql")

  with open(schema_path, "r", encoding="utf-8") as f:
    schema = f.read()

  cur = conn.cursor()
  cur.executescript(schema)
  conn.commit()
  conn.close()