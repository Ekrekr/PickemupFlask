"""
Pickemup Flask - test entry.

Test configuration for pytest.
"""
import pytest
from flask import Flask

from app.main import configure_routes, read_keys


def test_base_route(flask_client):
    url = '/'

    response = flask_client.get(url)
    assert response.get_data() == b"Pickemup Flask Server"
    assert response.status_code == 200
