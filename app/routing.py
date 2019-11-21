"""
PickemupFlask - gmaps

Communication with the gmaps API, which includes distance-matrix.
"""
import typing
import ortools


class Routing:
    def __init__(self, solution_request, distance_matrix):
        self.solution_request = solution_request
        self.distance_matrix = distance_matrix

        self.data = {}
        self.data["distance_matrix"] = self.calculate_matrix()
        self.data["demands"] = self.calculate_demands()
        self.data["num_vehicles"] = self.calculate_num_vehicles()
        self.data["depot"] = self.solution_request["destination"]

    def calculate_matrix(self):
        """
        Converts solution request locations to raw time distances.

        Args:
            solution_request: Solution request to convert.

        Returns:
            List of lists of integers.
        """
        # The values in the distance matrix align with the locations. Duration is
        # used as that indicates time, which is a more sensible metric than distance.
        self.matrix = []

        for row in self.distance_matrix["rows"]:
            new_row = []
            for element in row["elements"]:
                if element["status"] != "OK":
                    # If the route isn't OK, then 1,000,000 is used in place of
                    # infinity; the route should not be travelled.
                    new_row.append(1000000)
                else:
                    new_row.append(element["duration"]["value"])
            self.matrix.append(new_row)
        
        return self.matrix

    def calculate_demands(self):
        self.demands = [0 for i in self.solution_request["locations"]]
        for person in self.solution_request["people"]:
            self.demands[person["location"]] += 1
        return self.demands

    def calculate_num_vehicles(self):
        people = self.solution_request["people"]
        return [p["capacity"] for p in people if p["capacity"] > 0]
