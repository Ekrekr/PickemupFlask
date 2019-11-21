"""
PickemupFlask - main.

Entry point and routing for PickemupFlask.
"""
import os
import json
import typing
import datetime
from flask import Flask, request, jsonify

from . import gmaps


def read_keys() -> dict:
    """
    Reads keys from the '.keys' json file.

    Example .keys file:
    {
        "google": "ABCDEFGHI-JKLMNOPQRST-UVWXYZ0123-456789"
    }

    Returns:
        keys: Dict of keys, in .keys file.
    """
    keys_path = os.path.dirname(os.path.abspath(__file__))
    keys_path = os.path.join(keys_path, ".keys")
    try:
        with open(keys_path) as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        print("'.keys' file required but not found, exiting.")
        exit(0)
    return data


def configure_routes(app, keys):
    """
    Configures flask routes.

    Args:
        app: Flask app to configure routes for.
        keys: Secret API keys for various services.
    """

    @staticmethod
    @app.route("/")
    def info():
        return ("Pickemup Flask Server")

    @staticmethod
    @app.route("/solve-routing")
    def solve_routing():
        """
        Solves solution request, responds with a solution response.
        """
        print(f"{datetime.datetime.now()}, /solution-request")
        solution_request = json.loads(request.data)

        solution_response = {}

        return jsonify(solution_response)

    return app

app = Flask(__name__)
keys = read_keys()
app = configure_routes(app, keys)
