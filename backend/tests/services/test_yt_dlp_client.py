import pytest
from user_types.requests import GetDownloadsSearchRequest
from user_types import DownloadSearchResult
from services import YtDlpClient
from yt_dlp.utils import DownloadError, ExtractorError, UnsupportedError
from unittest.mock import patch

@pytest.fixture(params=[
  # (main artist, track name)
  ("Queen", "Radio Ga Ga"),
  ("Daft Punk", "One More Time"),
  ("Led Zeppelin", "Kashmir")
])
def yt_search_query(request: pytest.FixtureRequest) -> GetDownloadsSearchRequest:
  """Parametrized fixture providing search query test cases for the test_query_youtube method.

  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    GetDownloadsSearchRequest: The request query parameters test case.
  """
  
  artist, track_name = request.param
  test_value = GetDownloadsSearchRequest()
  test_value.main_artist = artist
  test_value.track_name = track_name
  return test_value
# END yt_search_query


@pytest.fixture(params=[
  DownloadError,
  ExtractorError,
  UnsupportedError,
  ValueError,
  Exception
])
def yt_search_error(request: pytest.FixtureRequest) -> DownloadError | ExtractorError | UnsupportedError | ValueError | Exception:
  """Parametrized fixture providing error test cases for the test_query_youtube_with_error method.

  Args:
    request (pytest.FixtureRequest): Provides the current parameter.

  Returns:
    DownloadError | ExtractorError | UnsupportedError | ValueError | Exception: The different errors that can be thrown.
  """
  
  return request.param
# END yt_search_error


class TestYtDlpClient:
  """Unit and integration tests for methods of the YtDlpClient class.
  """

  def test_query_youtube(self, yt_search_query: GetDownloadsSearchRequest):
    """Verfies that the query_youtube method aggregates search results of downloadable YouTube videos correctly.

    Args:
      yt_search_query (GetDownloadsSearchRequest): The mock request parameters / search query for the search provided by the fixture.

    Notes:
      - The search may or may not succeed but the test handles all possible return cases of the tested method.
      - The test makes external HTTP requests.
    """
    
    is_success, result = YtDlpClient().query_youtube(yt_search_query)

    assert(isinstance(is_success, bool))

    if is_success:
      assert isinstance(result, list)
      assert all(isinstance(s, DownloadSearchResult) for s in result)
      assert all(hasattr(s, "title") for s in result)
      assert all(s.title is None or isinstance(s.title, str) for s in result)
      assert all(hasattr(s, "channel") for s in result)
      assert all(s.channel is None or isinstance(s.channel, str) for s in result)
      assert all(hasattr(s, "duration") for s in result)
      assert all(s.duration is None or isinstance(s.duration, int | float) for s in result)
      assert all(hasattr(s, "thumbnail") for s in result)
      assert all(s.thumbnail or isinstance(s.thumbnail, str) for s in result)
      assert all(hasattr(s, "url") for s in result)
      assert all(s.url is None or (isinstance(s.url, str) and s.url != "") for s in result)
    else:
      assert isinstance(result, str)
  # END test_query_youtube


  def test_query_youtube_with_error(self, yt_search_error: DownloadError | ExtractorError | UnsupportedError | ValueError | Exception):
    """Verfies that the query_youtube method correctly handles any errors thrown during the search result aggregation process.

    Args:
      yt_search_query (DownloadError | ExtractorError | UnsupportedError | ValueError | Exception): The mock error provided by the fixture.

    Notes:
      - The YoutubeDL class is mocked and the .extract_info method is given a side effect which is a throwing of the error.
      - The test makes external HTTP requests.
    """
    
    with patch("yt_dlp.YoutubeDL") as mock_ytdl_class:
      mock_instance = mock_ytdl_class.return_value
      mock_instance.extract_info.side_effect = yt_search_error("error message")

      query = GetDownloadsSearchRequest()
      query.main_artist = "Queen"
      query.track_name = "Radio Ga Ga"
      is_success, result = YtDlpClient().query_youtube(query)

      assert is_success is False
      assert isinstance(result, str)
  # END test_query_youtube_with_error

# END class TestYtDlpClient