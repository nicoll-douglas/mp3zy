from sockets.downloads import DOWNLOADS_NAMESPACE, DownloadsSocket
from flask_socketio import SocketIOTestClient
from typing import cast, Callable
from user_types import DownloadUpdate, DownloadStatus, TrackArtistNames, TrackCodec, TrackBitrate
import pytest

@pytest.fixture
def download_update_fixture():
  update = DownloadUpdate()
  update.download_id = 1
  update.status = DownloadStatus.DOWNLOADING
  update.artist_names = TrackArtistNames(["Queen"])
  update.track_name = "Radio Ga Ga"
  update.codec = TrackCodec.MP3
  update.bitrate = TrackBitrate._192
  update.url = "https://www.youtube.com/watch?v=azdwsXLmrHE"
  update.created_at = "2025-10-06 14:32:15"
  update.total_bytes = 5342234
  update.downloaded_bytes = 234641
  update.speed = 601343.325
  update.terminated_at = None
  update.eta = 12

  return update
# END download_update_fixture


class TestDownloadsSocket:

  def test_send_download_update(
    self,
    socketio_test_client_fixture: Callable[[str], SocketIOTestClient], 
    download_update_fixture: DownloadUpdate
  ):
    client = socketio_test_client_fixture(DOWNLOADS_NAMESPACE)
    
    namespace: DownloadsSocket = client.socketio.server.namespace_handlers[DOWNLOADS_NAMESPACE]
    namespace.send_download_update(download_update_fixture)

    received = client.get_received(DOWNLOADS_NAMESPACE)

    assert any(p["name"] == DownloadsSocket.DOWNLOAD_UPDATE_EVENT for p in received)

    event = next(p for p in received if p["name"] == DownloadsSocket.DOWNLOAD_UPDATE_EVENT)
    data = event["args"][0]

    assert isinstance(data, dict)
    assert data["download_id"] == download_update_fixture.download_id
    assert data["artist_names"] == download_update_fixture.artist_names.data
    assert data["track_name"] == download_update_fixture.track_name
    assert data["codec"] == download_update_fixture.codec.value
    assert data["bitrate"] == download_update_fixture.bitrate.value
    assert data["url"] == download_update_fixture.url
    assert data["created_at"] == download_update_fixture.created_at
    assert data["total_bytes"] == download_update_fixture.total_bytes
    assert data["downloaded_bytes"] == download_update_fixture.downloaded_bytes
    assert data["speed"] == download_update_fixture.speed
    assert data["terminated_at"] == download_update_fixture.terminated_at
    assert data["eta"] == download_update_fixture.eta
  # END test_send_download_update


  def test_send_all_downloads(
    self,
    socketio_test_client_fixture: Callable[[str], SocketIOTestClient],
    download_update_fixture: DownloadUpdate
  ):
    client = socketio_test_client_fixture(DOWNLOADS_NAMESPACE)
    
    namespace: DownloadsSocket = client.socketio.server.namespace_handlers[DOWNLOADS_NAMESPACE]
    namespace.send_all_downloads([download_update_fixture])

    received = client.get_received(DOWNLOADS_NAMESPACE)

    assert any(p["name"] == DownloadsSocket.DOWNLOAD_INIT_EVENT for p in received)

    event = next(p for p in received if p["name"] == DownloadsSocket.DOWNLOAD_INIT_EVENT)
    data = event["args"][0]

    assert isinstance(data, dict)
    assert isinstance(data["downloads"], list)
    assert len(data["downloads"]) == 1

    dl = data["downloads"][0]

    assert dl["download_id"] == download_update_fixture.download_id
    assert dl["artist_names"] == download_update_fixture.artist_names.data
    assert dl["track_name"] == download_update_fixture.track_name
    assert dl["codec"] == download_update_fixture.codec.value
    assert dl["bitrate"] == download_update_fixture.bitrate.value
    assert dl["url"] == download_update_fixture.url
    assert dl["created_at"] == download_update_fixture.created_at
    assert dl["total_bytes"] == download_update_fixture.total_bytes
    assert dl["downloaded_bytes"] == download_update_fixture.downloaded_bytes
    assert dl["speed"] == download_update_fixture.speed
    assert dl["terminated_at"] == download_update_fixture.terminated_at
    assert dl["eta"] == download_update_fixture.eta
  # END test_send_all_downloads

# END class TestDownloadsSocket