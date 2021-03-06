"""
PickemupFlask - route optimizer

Communication with the gmaps API, which includes distance-matrix.
"""
import typing
import ortools
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


class RouteOptimizer:
    def __init__(self, solution_request, distance_matrix):
        """
        Solves the Pickemup routing problem.

        Args:
            solution_request: Solution request from the client.
            distance matrix: Corresponding distance matrix for the request.
        """
        self.solution_request = solution_request
        self.distance_matrix = distance_matrix

        self._people = self.solution_request["people"]
        self._location_names = self.distance_matrix["destination_addresses"]
        self._dm = self._calculate_matrix()
        self._demands = self._calculate_demands()
        starts, capacities, driver_ids = self._calculate_vehicle_info()
        self._starts = starts
        self._capacities = capacities
        self._driver_ids = driver_ids
        self._num_vehicles = len(capacities)
        self._ends = [self.solution_request["destination"] for i in starts]

        self._manager, self._routing, self._solution = self._solve()
        self._parsed_solution = self._parse()

    def _calculate_matrix(self):
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

    def _calculate_demands(self):
        """
        Calculate demands for each location in the solution request.
        """
        self.demands = [0 for i in self.solution_request["locations"]]
        for person in self.solution_request["people"]:
            self.demands[person["location"]] += 1
        return self.demands

    def _calculate_vehicle_info(self):
        """
        Calculates capacities of vehicles and starting locations.

        Starting locations are where the drivers are driving from, which is
        different to the 'depot'.
        """
        capacities = []
        starts = []
        driver_ids = []
        for p in self.solution_request["people"]:
            if p["capacity"] > 0:
                capacities.append(p["capacity"])
                starts.append(p["location"])
                driver_ids.append(p["id"])
        return starts, capacities, driver_ids

    def _solve(self):
        """
        Calculates optimized routing using predefined data.

        For more explanation see OR-Tools routing example:
        https://developers.google.com/optimization/routing/cvrp.
        """
        # If prior class variables are missing then this function is not
        # viable.
        if not self._starts:
            raise NameError(f"route_optimizer._solve called before class"
                            f"variables initialized.")

        manager = pywrapcp.RoutingIndexManager(
            len(self._dm),
            self._num_vehicles,
            self._starts,
            self._ends
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index: int, to_index: int) -> int:
            """
            Returns distance between nodes in the numeric distance matrix.
            """
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self._dm[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(
            distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(index):
            """
            Returns the demand of a node.
            """
            node = manager.IndexToNode(index)
            return self._demands[node]
        
        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            self._capacities,  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity"
        )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        # "Class 'FirstSolutionStrategy' has no 'PATH_CHEAPEST_ARC' member"
        # error given, though is false; ignore.
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        solution = routing.SolveWithParameters(search_parameters)
        self._manager = manager
        self._routing = routing
        return manager, routing, solution

    def _parse(self):
        """
        Parses the solution into a dict for serialized json transmittance.
        """
        # Parsing is only viable if a solution exists to be parsed.
        if not self._starts:
            raise NameError(f"route_optimizer._parse called before solution"
                            f"found.")

        manager = self._manager
        routing = self._routing
        solution = self._solution
        parsed_solution = {"routes": {}}
        total_distance = 0
        total_load = 0
        for vehicle_id in range(self._num_vehicles):
            route = []
            index = routing.Start(vehicle_id)
            route_distance = 0
            route_load = 0
            
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += self._demands[node_index]
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                distance = routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
                route_distance += distance
                route.append({"node": node_index, "load": route_load, "cum_dist": route_distance})
            route.append({"node": manager.IndexToNode(index), "load": route_load, "cum_dist": route_distance})
            total_distance += route_distance
            total_load += route_load
        parsed_solution["total_distance"] = total_distance
        parsed_solution["total_load"] = total_load
        return parsed_solution

    def print_formulation(self):
        """
        Prints problem presented to optimiser to terminal.
        """
        print("\nDistance matrix:")
        for i in self._dm:
            print(i)

        print("\nLocations and demands:")
        for i_loc, loc in enumerate(self.solution_request["locations"]):
            address = self.distance_matrix['destination_addresses'][i_loc]
            print(f"{i_loc}: "
                  f"Lat: {loc['lat']}, lgn: {loc['lgn']}, "
                  f"name: {address}, "
                  f"demand: {self._demands[i_loc]}")
        print(f"Total demand: {sum(self._demands)}")
        
        print("\nVehicles and drivers:")
        for i, driver_id in enumerate(self._driver_ids):
            name = self.solution_request['people'][driver_id]["name"]
            location = self._location_names[self._starts[i]]
            print(f"{i}: "
                  f"name: {name}, "
                  f"location: {location}, "
                  f"capacity: {self._capacities[i]}")
        print()

    def print_solution(self):
        """
        Prints optimised solution to terminal.
        """
        print("PARSED SOLUTION")
        routes = self._parsed_solution["routes"]
        output = f"There are {len(routes)} vehicles.\n"
        for driver_id, route in routes.items():
            output += f"Route for {self._people[driver_id]['name']}'s vehicle: "
            for stop in route:
                output += f"{stop['node']} load({stop['load']}) -> "
            output = output[:-4] + f", total distance: {stop['cum_dist']}\n"
        print(output)

    @property
    def parsed_solution(self):
        return self._parsed_solution

    @property
    def solution(self):
        return self._solution
