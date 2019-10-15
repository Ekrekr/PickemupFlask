"""
Flask API Relay

App for relaying anonymous client requests to a cloud service. More info here:
https://eliaskassell.com/2019/10/13/microservice-api-relay.html
"""
import json
import typing
import datetime
import googlemaps
from flask import Flask, request, jsonify

app = Flask(__name__)


def readKeys() -> dict:
    """
    Reads keys from the '.keys' json file.

    Example .keys file:
    {
        "vrrp_google": "ABCDEFGHI-JKLMNOPQRST-UVWXYZ0123-456789"
    }

    Returns:
        keys: Dict of keys, in .keys file.
    """
    try:
        with open('.keys') as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        print("'.keys' file required but not found, exiting.")
        exit(0)
    return data


def splitGeoArg(arg: str) -> typing.List[typing.List[float]]:
    """
    Splits up a geolocation argument.

    0.7655,-74.8918|0.7755,-74.9918
    becomes:
    [[0.7655, -74.8918], [0.7755, -74.9918]]

    Args:
        arg: Geolocation to split.
    Returns:
        Split geolocation.
    """
    arg = arg.split("|")
    arg = [i.split(",") for i in arg]
    return arg


def getDistanceMatrix(origins: str,
                      destinations: str,
                      arrivalTime: int) -> dict:
    """
    Retrieves distance matrix from Google Cloud API.

    Google Cloud Distance Matrix Documentation:
    https://developers.google.com/maps/documentation/distance-matrix/intro

    Args:
        origins: Origins of distance matrix.
        destinations: Destinations of distance matrix.
        arrivalTime: Time in seconds since midnight January 1st 1970 (UNIX).
    Returns:
        Distance matrix result from Google API.
    """
    keys = readKeys()
    origins = splitGeoArg(origins)
    destinations = splitGeoArg(destinations)

    gmaps = googlemaps.Client(key=keys['vrrp_google'])

    distanceMatrix = gmaps.distance_matrix(origins, destinations,
                                           arrival_time=arrivalTime)

    return distanceMatrix


@app.route('/gmaps-matrix')
def gmapsMatrix():
    """
    Gmaps distance matrix from request.
    """
    print(f"{datetime.datetime.now()}, {request.remote_addr}, /gmaps-matrix")
    print(request.form)

    distanceMatrix = getDistanceMatrix(request.form["origins"],
                                       request.form["destinations"],
                                       request.form["arrival_time"])

    return jsonify(distanceMatrix)


if __name__ == '__main__':
    app.run()
