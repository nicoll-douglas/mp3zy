import sqlite3, os

PATH = os.path.join(os.getenv("USER_DATA_DIR"), "db.sqlite")

def connect() -> sqlite3.Connection:
  """Establishes a connection to the application's SQLite database.

  Returns:
    sqlite3.Connection: The database connection.
  """
  
  conn = sqlite3.connect(PATH)
  conn.row_factory = sqlite3.Row
  return conn
# END connect