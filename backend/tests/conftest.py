import pytest
import sqlite3
from typing import Generator
import db

@pytest.fixture
def in_memory_db_conn() -> Generator[sqlite3.Connection, None, None]:
  """Fixture that provides a database connection for an in-memory SQLite database.
  
  Returns:
    Generator[sqlite3.Connection, None, None]: Yields the database connection.
  """

  conn = db.connect(":memory:")

  yield conn

  conn.close()
# END in_memory_db_conn