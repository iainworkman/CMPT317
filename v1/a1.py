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
            
        if y_pos != 0:
            city.adjacent_cities.append(cities[i_city - size])
            
        if y_pos != size-1:
            city.adjacent_cities.append(cities[i_city + size])
            
    return cities
    

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
    

    
    cities = generate_graph(number_of_cities)
    
    # initialize the start state
    start_state = ProblemState()
    
    # # randomly pick a city to be a garage
    start_state.garage_city = random.choice(cities)
    
    # # Initialize the vehicles
    for i_vehicle in range(0, number_of_vehicles):
        new_vehicle = Vehicle()
        new_vehicle.current_city = start_state.garage_city
        start_state.vehicles.append(new_vehicle)
    
    # # Initialize the packages    
    for i_package in range(0, number_of_packages):
        new_package = Package()
        # # # Randomly pck a source for the package
        new_package.source = random.choice(cities)
        
        # # # Randomly pick a DIFFERENT city for the destination
        while new_package.source != new_package.destination:
            new_package.destination = random.choice(cities)
            
        start_state.packages.append(new_package)
    
    search_space = [start_state]
    
    while True:
        current_first_state = heapq.heappop(search_space)
        
        successor_states = transition_operator(current_first_state)
        
        for state in successor_states:
            heapq.heappush(search_space, state)
        
    
    

if __name__ == '__main__':
    main()