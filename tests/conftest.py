"""
Pickemup Flask - test entry.

Test configuration for pytest.
"""
import pytest
from flask import Flask

from app.main import configure_routes, read_keys


@pytest.fixture()
def flask_client():
    flask_app = Flask(__name__)
    keys = read_keys()
    configure_routes(flask_app, keys)
    return flask_app.test_client()
