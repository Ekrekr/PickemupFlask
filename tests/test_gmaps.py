"""
Pickemup Flask - Test Gmaps.

Test gmaps work as expected.
"""
import pytest
from flask import Flask

from app.gmaps import get_distance_matrix

def test_arrival_distance_matrix(solution_request_1, google_key):
    distance_matrix = get_distance_matrix(
        solution_request_1,
        google_key
    )
    assert type(distance_matrix) == dict
    assert "destination_addresses" in distance_matrix
    assert "origin_addresses" in distance_matrix
