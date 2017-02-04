import math
import sys
import random
import heapq
import time

from problem import ProblemState, City, Vehicle, Package, transition_operator, heuristic
from errors import ArgumentError

def generate_graph(number_of_nodes):
    """
    Return a graph of cities, organized in a grid, of the provided size
    """
    cities = []
    size = int(math.sqrt(number_of_nodes))
    if size*size != number_of_nodes:
        raise ArgumentError("At the moment generate_graph() only takes perfect squares (3, 16, 25 etc.). Feel free to improve it.")
    test = 0
    for position in range(0, number_of_nodes):
        city = City()
        city.x_position = (position) % size
        city.y_position = int(position / size)
        cities.append(city)

    for i_city in range(0, len(cities)):
        city = cities[i_city]
        x_pos = city.x_position
        y_pos = city.y_position

        if x_pos != 0:
            city.adjacent_cities.append(cities[i_city - 1])

        if x_pos != size-1:
            city.adjacent_cities.append(cities[i_city + 1])

        if y_pos != size-1:
            city.adjacent_cities.append(cities[i_city - size])

        if y_pos != size-1:
            city.adjacent_cities.append(cities[i_city + size])

    return cities

def assign_packages(vehicles, packages):
    i_vehicle = 0                                                                                                                                                        
    vehicle_count = len(vehicles)                                                                                                                                        
    for package in packages:                                                                                                                                             
        vehicles[i_vehicle].packages.append(package)                                                                                                                     
        i_vehicle = (i_vehicle + 1) % vehicle_count
        
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
        total_time = 0
        for vehicle in vehicles:
            search_space = [start_state]
            start_state.vehicle = vehicle
            total_states_for_vehicle = 0
            # Goal state represented by truck having no packages, and being
            # at garage
            current_state = heapq.heappop(search_space)
            start_time = time.time()
            while not current_state.is_goal_state():
                total_states_for_vehicle+=1
                # if total_states_for_vehicle < 10 or total_states_for_vehicle % 100 == 0:
                print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                print current_state
                print "-------------------"
                successor_states = transition_operator(current_state)
                print "Successors:"
                for state in successor_states:
                    # print state
                    heapq.heappush(search_space, state)
                print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                current_state = heapq.heappop(search_space)
                search_space = []
            search_time = time.time() - start_time
            print "Search complete for a vehicle in {time:.2f}s".format(
                time = search_time
            )
            total_time += search_time
            total_distances.append(current_state.distance_traveled)
            total_states.append(total_states_for_vehicle)
        print "Total distance travelled for all trucks: %s\n " % sum(total_distances)
        # Total number of states needed is the max number of states needed for 1 truck
        print "Total states needed: %s" % max(total_states)
        print "Time taken: {time:.2f}s".format(
            time=total_time
        )

if __name__ == '__main__':
    main()
