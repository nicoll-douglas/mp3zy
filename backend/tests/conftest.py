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


@pytest.fixture
def app_db(in_memory_db_connn: sqlite3.Connection) -> Generator[sqlite3.Connection, None, None]:
  """Fixture that provides a database connection for an in-memory SQLite database that is set up with the application's schema.
  
  Returns:
    Generator[sqlite3.Connection, None, None]: Yields the database connection.
  """

  db.setup(in_memory_db_connn)

  yield in_memory_db_connn
# END app_db