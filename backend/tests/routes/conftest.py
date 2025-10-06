import pytest
from app import create_app
from flask import Flask
from flask.testing import FlaskClient
from typing import Generator

@pytest.fixture(scope="session")
def flask_app() -> Generator[Flask, None, None]:
  """Fixture that provides the Flask application instance.

  Returns:
    Generator[Flask, None, None]: Yields a configured Flask application instance.
  """

  app, _ = create_app()
  app.config.update({
    "TESTING": True,
    "DEBUG": False,
  })
  
  yield app
# END app_fixture


@pytest.fixture
def flask_app_test_client(flask_app: Flask) -> Generator[FlaskClient, None, None]:
  """Fixture that provides a Flask test client for making HTTP requests.

  Args:
    flask_app (Flask): The Flask application instance provided by the flask_app fixture.

  Returns:
    Generator[FlaskClient, None, None]: Yields a test client for sending requests to the Flask app.
  """
  
  with flask_app.test_client() as client:
    yield client
# END flask_app_test_client