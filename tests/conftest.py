"""
Pickemup Flask - test entry.

Test configuration for pytest.
"""
import pytest
import json
from flask import Flask

from app.main import configure_routes, read_keys


def read_json(path):
    with open(path) as f:
        ret = json.load(f)
    return ret


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
    return read_json("tests/assets/solution_request_1.json")


@ pytest.fixture()
def distance_matrix_response_1():
    return read_json("tests/assets/distance_matrix_response_1.json")
