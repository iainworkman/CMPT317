import math
import sys
import random
import heapq

from problem import ProblemState, City, Vehicle, Package, transition_operator
from errors import ArgumentError

def generate_graph(number_of_nodes):
    """
    Return a graph of cities, organized in a grid, of the provided size
    """
    cities = []
    for position in range(number_of_nodes):
        city = City()
        city.x_position = random.randint(0,1000) + random.random()
        city.y_position = random.randint(0,1000) + random.random()
        cities.append(city)

    for city in cities:
        lefties = [c for c in cities if c.x_position < city.x_position]
        righties = [c for c in cities if c.x_position > city.x_position]
        upies = [c for c in cities if c.y_position > city.y_position]
        downies = [c for c in cities if c.y_position < city.y_position]

        if not (lefties or righties or upies or downies):
            raise Exception("Oops this city has no neighbours.")

        if lefties:
            city.adjacent_cities.append(max(lefties))
        if righties:
            city.adjacent_cities.append(min(righties))
        if upies:
            city.adjacent_cities.append(min(upies))
        if downies:
            city.adjacent_cities.append(max(downies))

    return cities

def assign_packages(vehicles, packages):
    """ len(vehicles) must be > 1, len(packages) must be > 1 """
    num_packages_per_truck = len(packages) / len(vehicles)
    if isinstance(num_packages_per_truck, float) and not num_packages_per_truck.is_integer():
        # give the first vehcile an extra package
        num_packages_per_truck = int(num_packages_per_truck)
        vehicles[0].packages.append(packages[0])
        packages.remove(packages[0])

    for vehicle in vehicles:
        for _ in range(num_packages_per_truck):
            vehicle.packages.append(packages[0])
            packages.remove(packages[0])
    return vehicles



def main():
    """
    Main Function. Just sets up the data, for now.
    """
    # Parse command line arguments
    try:
        number_of_vehicles = int(sys.argv[1])
        number_of_packages = int(sys.argv[2])
        number_of_cities = int(sys.argv[3])
    except IndexError:
        print 'Could not parse arguments, expected:'
        print 'python a1.py <vehicles> <packages> <cities>'
        print 'NOTE: <cities> must be a perfect square'
    else:
        packages = list()
        vehicles = list()

        cities = generate_graph(number_of_cities)

        # initialize the start state
        start_state = ProblemState()

        # # randomly pick a city to be a garage
        start_state.garage_city = random.choice(cities)

        # # Initialize the vehicles
        for i in range(number_of_vehicles):
            new_vehicle = Vehicle()
            new_vehicle.name = i
            new_vehicle.current_city = start_state.garage_city
            vehicles.append(new_vehicle)

        # # Initialize the packages
        for _ in range(number_of_packages):
            new_package = Package()
            # # # Randomly pck a source for the package
            new_package.source = random.choice(cities)
            # # # Randomly pick a DIFFERENT city for the destination
            new_package.destination = random.choice([city for city in cities if city != new_package.source])
            packages.append(new_package)

        # # Assign packages to trucks
        vehicles = assign_packages(vehicles, packages)

        total_distances = []
        total_states = []
        for vehicle in vehicles:
            search_space = [start_state]
            start_state.vehicle = vehicle
            total_states_for_vehicle = 0
            # Goal state represented by truck having no packages, and being
            # at garage
            while vehicle.packages or vehicle.current_city !=  start_state.garage_city:
                total_states_for_vehicle+=1
                current_state = heapq.heappop(search_space)
                if total_states_for_vehicle % 100 == 0:
                    print current_state
                    print "\n"
                successor_states = transition_operator(current_state)

                for state in successor_states:
                    heapq.heappush(search_space, state)
            total_distances.append(current_state.distance_traveled)
            total_states.append(total_states_for_vehicle)
        print "Total distance travelled for all trucks: %s\n " % sum(total_distances)
        # Total number of states needed is the max number of states needed for 1 truck
        print "Total states needed: %s" % max(total_states)





if __name__ == '__main__':
    main()
