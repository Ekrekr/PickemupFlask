"""
Flask API Relay

App for routing requests to things that requre API keys, preventing me from
having to put them in client side code in unhosted javascript. This is not the
perfect solution as someone could still abuse the access to the server, but
by having this middleware I can prevent call spams, or easily temporarily
disable the service.

Python client for Google Maps Services:
https://github.com/googlemaps/google-maps-services-python
"""
import json
import typing
import datetime
import ortools
from flask import Flask, request

app = Flask(__name__)

def readKeys():
    """
    Reads keys from the '.keys' json file.

    Example .keys file:
    {
        "vrrp_google": "ABCDEFGHI-JKLMNOPQRST-UVWXYZ0123-456789"
    }

    TODO: Add error checking for missing file, etc.

    Returns:
        keys: Dict of keys, in .keys file.
    """
    try:
        with open('.keysa') as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        print("'.keys' file required but not found, exiting.")
        exit(0)
    return data

def getDistanceMatrix(origins: typing.List[typing.Dict[float, float]],
                      destinations: typing.List[typing.Dict[float, float]],
                      arrivalTime: int):
    """
    Retrieves distance matrix from Google Cloud API.

    Google Cloud Distance Matrix Documentation:
    https://developers.google.com/maps/documentation/distance-matrix/intro

    Example request url:
    'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&
    origins=40.6655,-73.8918&destinations=0.7655,-74.8918&key=YOUR_API_KEY'

    Example response:
    {
        "destination_addresses" : [ "New York, NY, USA" ],
        "origin_addresses" : [ "Washington, DC, USA" ],
        "rows" : [
            {
                "elements" : [
                    {
                        "distance" : {
                            "text" : "225 mi",
                            "value" : 361715
                        },
                        "duration" : {
                            "text" : "3 hours 49 mins",
                            "value" : 13725
                        },
                        "status" : "OK"
                    }
                ]
            }
        ],
        "status" : "OK"
    }

    TODO: Add check for OVER_DAILY_LIMIT

    Args:
        origins: Origins of distance matrix.
        destinations: Destinations of distance matrix.
        arrivalTime: Time in seconds since midnight January 1st 1970.
    """
    keys = readKeys()

    url = (f"https://maps.googleapis.com/maps/api/distancematrix/json?"
           f"units=metric&origins=${origins}&destinations=${destinations}"
           f"&mode=driving&arrival_time=  &key=${keys['vrrp_google']}")
    print("Querying", url)

    distanceMatrix = []

    return distanceMatrix



    


@app.route('/gmaps-matrix', methods=['GET'])
def hello():
    print(request.args)

    return "TO BE CONTINUED..."

if __name__ == '__main__':
    app.run()