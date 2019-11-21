"""
Pickemup Flask - Test Routing.

Test routing works as expected.
"""
import pytest
from flask import Flask

from app.routing import Routing


# def test_plan_route(solution_request_1, distance_matrix_response):
#     optimized_

def test_routing_entry(solution_request_1, distance_matrix_response_1):
    route = Routing(solution_request_1, distance_matrix_response_1)
