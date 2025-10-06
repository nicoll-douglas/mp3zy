from flask.testing import FlaskClient

def test_get_downloads_search_400(flask_app_test_client: FlaskClient):
  """Integration test that tests that a bad request to the GET /downloads/search endpoint responds correctly.

  Args:
    flask_app_test_client (FlaskClient): The Flask test client provided by the respective fixture.
  """
  
  res = flask_app_test_client.get("/downloads/search?track_name=Radio+Ga+Ga")

  assert res.status_code == 400
  assert "parameter" in res.json
  assert res.json["parameter"] == "main_artist"
  assert "message" in res.json
  assert isinstance(res.json["message"], str)
# END test_get_downloads_search_400


def test_get_downloads_search_200(flask_app_test_client: FlaskClient):
  """Integration test that tests that a good request to the GET /downloads/search endpoint responds correctly.

  Args:
    flask_app_test_client (FlaskClient): The Flask test client provided by the respective fixture.
  """
  
  res = flask_app_test_client.get("/downloads/search?track_name=Radio+Ga+Ga&main_artist=Queen")

  assert res.status_code == 200
  assert "results" in res.json
  assert isinstance(res.json["results"], list)
# END test_get_downloads_search_200
