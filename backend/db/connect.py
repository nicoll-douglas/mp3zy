import sqlite3, os

PATH = os.path.join(os.getenv("DATA_DIR"), "db.sqlite")

def connect(row_factory = sqlite3.Row):
  conn = sqlite3.connect(PATH, check_same_thread=False)
  conn.row_factory = row_factory
  return conn