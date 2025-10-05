import pytest
from app import create_app

@pytest.fixture(scope="session")
def app_fixture():
  app, _ = create_app()
  app.config.update({
      "TESTING": True,
      "DEBUG": False,
  })
  yield app
# END app_fixture


@pytest.fixture()
def test_client_fixture(app_fixture):
  with app_fixture.test_client() as client:
    yield client
# END test_client_fixture