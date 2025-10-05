def test_get_downloads_search_400(test_client_fixture):
  res = test_client_fixture.get("/downloads/search?track_name=Radio+Ga+Ga")

  assert res.status_code == 400
  assert "parameter" in res.json
  assert res.json["parameter"] == "main_artist"
  assert "message" in res.json
  assert isinstance(res.json["message"], str)
# END test_get_downloads_search_400


def test_get_downloads_search_200(test_client_fixture):
  res = test_client_fixture.get("/downloads/search?track_name=Radio+Ga+Ga&main_artist=Queen")

  assert res.status_code == 200
  assert "results" in res.json
  assert isinstance(res.json["results"], list)
# END test_get_downloads_search_200
