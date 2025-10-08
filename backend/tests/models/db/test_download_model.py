from models.db import Download
import sqlite3
import pytest
from typing import Callable

@pytest.fixture(params=[
  # (sql file key, precise data that is included in the return from the query)
  (
    "next_in_queue_1", 
    {
      "download_id": 1,
      "url": "https://www.youtube.com/watch?v=8GB9BULxZ8c",
      "codec": "flac",
      "bitrate": 320,
      "status": "queued",
      "metadata_id": 1,
      "track_name": "The Girl Is Mine",
      "main_artist": "Michael Jackson",
      "album_name": "Thriller",
      "track_number": 3,
      "disc_number": 1,
      "release_date": "1982",
      "other_artists": ["Paul McCartney"],
      "download_dir": "/home/user/music"
    }
  ),
  (
    "next_in_queue_2",
    {
      "download_id": 1,
      "url": "https://www.youtube.com/watch?v=azdwsXLmrHE",
      "codec": "mp3",
      "bitrate": 320,
      "status": "queued",
      "metadata_id": 1,
      "track_name": "Radio Ga Ga",
      "main_artist": "Queen",
      "album_name": "The Works",
      "track_number": None,
      "disc_number": None,
      "release_date": "20-02-1984",
      "other_artists": [],
      "download_dir": "/home/user/music"
    }
  ),
  (None, None)
])
def next_in_queue_fixture(request: pytest.FixtureRequest) -> tuple[str | None, dict | None]:
  """Parametrized fixture providing test data for the test_get_next_in_queue method.
  
  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    tuple[str | None, dict | None]: The parameter; is a tuple containing the file key for the .sql seed file and the expected data to be returned from the query. If the file key is None, then the expected data is also None.
  """
  
  return request.param
# END next_in_queue_fixture


class TestDownloadModel:
  """Contains unit/integration tests for the Download model.
  """

  def test_get_next_in_queue(
    self, 
    seeded_app_db: Callable[[str | None], sqlite3.Connection], 
    next_in_queue_fixture: tuple[str | None, dict | None]
  ):
    """Verfies that the get_next_in_queue method queries the database correctly and returns all the correct data.

    Args:
      seeded_app_db (Callable[[str | None], sqlite3.Connection]): The factory function to create the seeded application database and return the connection provided by the fixture.
      next_in_queue_fixture (tuple[str | None, dict, | None]): The parametrized fixture providing the .sql file key for the seed and the expected data from the query. If the file key is None, then the expected data is also None (no queued rows).
    """
    
    sql_seed_file_key, included_data = next_in_queue_fixture
    dl = Download(seeded_app_db(sql_seed_file_key))
    next_in_queue = dl.get_next_in_queue()

    if sql_seed_file_key is None:
      assert next_in_queue is None

    else:
      assert isinstance(next_in_queue, dict)
      assert "created_at" in next_in_queue
      assert included_data.items() <= next_in_queue.items()
  # END test_get_next_in_queue

# END class TestDownloadModel