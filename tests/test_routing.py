"""
Pickemup Flask - Test Routing.

Test routing works as expected.
"""
import pytest
from flask import Flask

from app.route_optimizer import RouteOptimizer


def test_routing_entry(solution_request_1, distance_matrix_response_1):
    route = RouteOptimizer(solution_request_1, distance_matrix_response_1)
    route.print_formulation()
    route.print_solution()
