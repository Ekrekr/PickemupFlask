"""
Pickemup Flask - test entry.

Test configuration for pytest.
"""
import pytest
import json
from flask import Flask

from app.main import configure_routes, read_keys


@pytest.fixture()
def google_key():
    keys = read_keys()
    return keys["google"]


@pytest.fixture()
def flask_client():
    flask_app = Flask(__name__)
    keys = read_keys()
    configure_routes(flask_app, keys)
    return flask_app.test_client()


@pytest.fixture()
def solution_request_1():
    with open("tests/assets/solution-request-1.json") as f:
        ret = json.load(f)
    return ret
