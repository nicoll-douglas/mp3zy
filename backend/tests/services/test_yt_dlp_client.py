import pytest
from user_types.requests import GetDownloadsSearchRequest
from user_types import DownloadSearchResult
from services import YtDlpClient

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

# END class TestYtDlpClient