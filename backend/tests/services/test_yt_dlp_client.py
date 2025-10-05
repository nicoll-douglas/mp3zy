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
def query_fixture(request):
  artist, track_name = request.param
  test_value = GetDownloadsSearchRequest()
  test_value.main_artist = artist
  test_value.track_name = track_name
  return test_value
# END query_fixture


@pytest.fixture(params=[
  DownloadError,
  ExtractorError,
  UnsupportedError,
  ValueError,
  Exception
])
def search_error_fixture(request):
  return request.param
# END search_error_fixture


class TestYtDlpClient:

  def test_query_youtube(self, query_fixture):
    query_test_value = query_fixture
    is_success, result = YtDlpClient().query_youtube(query_test_value)

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


  def test_query_youtube_with_error(self, search_error_fixture):
    with patch("yt_dlp.YoutubeDL") as mock_ytdl_class:
      mock_instance = mock_ytdl_class.return_value
      mock_instance.extract_info.side_effect = search_error_fixture("error message")

      query = GetDownloadsSearchRequest()
      query.main_artist = "Queen"
      query.track_name = "Radio Ga Ga"
      is_success, result = YtDlpClient().query_youtube(query)

      assert is_success is False
      assert isinstance(result, str)
  # END test_query_youtube_with_error

# END class TestYtDlpClient