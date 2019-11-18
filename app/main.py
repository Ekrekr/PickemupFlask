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
        "vrrp_google": "ABCDEFGHI-JKLMNOPQRST-UVWXYZ0123-456789"
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

    @app.route("/")
    def info():
        return ("Pickemup Flask Server")

    @app.route("/gmaps-matrix")
    def gmaps_matrix():
        """
        Gmaps distance matrix from request.
        """
        print(f"{datetime.datetime.now()}, {request.remote_addr}, /gmaps-matrix")
        print(request.form)

        distance_matrix = gmaps.get_distance_matrix(
            origins=request.form["origins"],
            destinations=request.form["destinations"],
            arrival_time=request.form["arrival_time"],
            api_key=keys['vrrp_google']
        )

        return jsonify(distance_matrix)

    return app

app = Flask(__name__)
keys = read_keys()
app = configure_routes(app, keys)
