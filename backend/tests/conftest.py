import pytest
import sqlite3, os
from typing import Generator, Callable
import db
from pathlib import Path

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
def app_db(in_memory_db_conn: sqlite3.Connection) -> Generator[sqlite3.Connection, None, None]:
  """Fixture that provides a database connection for an in-memory SQLite database that is set up with the application's schema.
  
  Args:
    in_memory_db_conn (sqlite3.Connection): Fixture value that provides a database connection to an in-memory database.
  
  Returns:
    Generator[sqlite3.Connection, None, None]: Yields the database connection.
  """

  db.setup(in_memory_db_conn)

  yield in_memory_db_conn
# END app_db


@pytest.fixture
def seeded_app_db(app_db: sqlite3.Connection) -> Generator[Callable[[str], sqlite3.Connection], None, None]:
  """Fixture that provides a function to create an in-memory SQLite database that is set up with the application's schema and a given seed.
  
  Args:
    app_db (sqlite3.Connection): Fixture value that provides a database connection to an in-memory database set up with application's schema.
  
  Returns:
    Generator[Callable[[str], sqlite3.Connection], None, None]: Yields the function.
  """

  def _make_seeded_db(sql_file_key: str | None = None) -> sqlite3.Connection:
    """Function that seeds the application database depending on the key of the .sql seed file provided. If no key is given then no seeding is performed.

    Args:
      sql_file_key (str | None): The key of the .sql seed file, e.g "next_in_queue" corresponds to next_in_queue_1.seed.sql in the sql directory.

    Returns:
      sqlite3.Connection: The connection to the database.
    """
    
    if sql_file_key:
      current_dir = Path(__file__).parent
      schema_path = os.path.join(current_dir, "sql", f"{sql_file_key}.seed.sql")

      with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()

      cur = app_db.cursor()
      cur.executescript(schema)
      app_db.commit()

    return app_db
  # END _make_seeded_db
  
  yield _make_seeded_db
# END seeded_app_db