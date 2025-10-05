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
    search_results = YtDlpClient().query_youtube(query_test_value)

    assert isinstance(search_results, list)
    assert all(isinstance(s, DownloadSearchResult) for s in search_results)
    assert all(hasattr(s, "title") for s in search_results)
    assert all(s.title is None or isinstance(s.title, str) for s in search_results)
    assert all(hasattr(s, "channel") for s in search_results)
    assert all(s.channel is None or isinstance(s.channel, str) for s in search_results)
    assert all(hasattr(s, "duration") for s in search_results)
    assert all(s.duration is None or isinstance(s.duration, int | float) for s in search_results)
    assert all(hasattr(s, "thumbnail") for s in search_results)
    assert all(s.thumbnail or isinstance(s.thumbnail, str) for s in search_results)
    assert all(hasattr(s, "url") for s in search_results)
    assert all(s.url is None or (isinstance(s.url, str) and s.url != "") for s in search_results)
  # END test_query_youtube

# END class TestYtDlpClient