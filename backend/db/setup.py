from .connect import connect
from pathlib import Path
import os
import sqlite3

def setup(conn: sqlite3.Connection = connect()):
  """Sets up the application's database by reading and executing the application's SQL schema.

  Args:
    conn (sqlite3.Connection): A connection to the application's database.
  """
  
  current_dir = Path(__file__).parent
  schema_path = os.path.join(current_dir, "schema.sql")

  with open(schema_path, "r", encoding="utf-8") as f:
    schema = f.read()

  cur = conn.cursor()
  cur.executescript(schema)
  conn.commit()
# END setup