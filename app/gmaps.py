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


def get_distance_matrix(origins: str,
                      destinations: str,
                      arrival_time: int,
                      api_key: str) -> dict:
    """
    Retrieves distance matrix from Google Cloud API.

    Google Cloud Distance Matrix Documentation:
    https://developers.google.com/maps/documentation/distance-matrix/intro

    Args:
        origins: Origins of distance matrix.
        destinations: Destinations of distance matrix.
        arrival_time: Time in seconds since midnight January 1st 1970 (UNIX).
        api_key: Google API key.
    Returns:
        Distance matrix result from Google API.
    """
    origins = split_geo_arg(origins)
    destinations = split_geo_arg(destinations)

    gmaps_client = googlemaps.Client(key=api_key)

    distance_matrix = gmaps_client.distance_matrix(origins, destinations,
                                                   arrival_time=arrival_time)

    return distance_matrix
