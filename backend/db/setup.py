from .connect import connect
from pathlib import Path
import os

def setup() -> None:
  """Sets up the database by reading and executing the application's SQL schema.
  """
  current_dir = Path(__file__).parent
  schema_path = os.path.join(current_dir, "schema.sql")

  with open(schema_path, "r", encoding="utf-8") as f:
    schema = f.read()

  with connect() as conn:
    cur = conn.cursor()
    cur.executescript(schema)