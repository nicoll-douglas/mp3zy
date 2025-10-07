import sqlite3, os

PATH = os.path.join(os.getenv("USER_DATA_DIR"), "db.sqlite")

def connect(path: str = PATH) -> sqlite3.Connection:
  """Establishes a connection to the application's SQLite database.

  Args:
    path (str): The path to the databse file.

  Returns:
    sqlite3.Connection: The database connection.
  """
  
  conn = sqlite3.connect(path)
  conn.row_factory = sqlite3.Row
  
  return conn
# END connect