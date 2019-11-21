"""
PickemupFlask - gmaps

Communication with the gmaps API, which includes distance-matrix.
"""
import typing
import googlemaps


def split_geo_arg(arg: str) -> typing.List[typing.List[float]]:
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


def get_distance_matrix(solution_request: dict,
                        api_key: str,
                        arrival: bool = True) -> dict:
    """
    Retrieves distance matrix from Google Cloud API.

    Google Cloud Distance Matrix Documentation:
    https://developers.google.com/maps/documentation/distance-matrix/intro

    Args:
        solution_request: Raw solution request.
        api_key: Google API key.
        arrival: Uses arrival time if true, otherwise departure as arrival.

    Returns:
        Distance matrix result from Google API.
    """
    gmaps_client = googlemaps.Client(key=api_key)

    locations = [(l["lat"], l["lgn"]) for l in solution_request["locations"]]

    distance_matrix = gmaps_client.distance_matrix(
        origins=locations,
        destinations=locations,
        mode="driving",
        units="metric",
        # arrival_time=solution_request["arrival-time"]
    )

    return distance_matrix
